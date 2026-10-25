#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Explicit-only incremental Gemini Aoede (`gemini-v4s-tts`) voice refresher for 🌸 কল্যাণী.

CRITICAL GOVERNANCE RULE (defined in GEMINI.md):
- NEVER run this script with `--confirm` automatically during UI tweaks or content/data edits.
- `scripts/build_app.py` inspects `audio/tts_manifest.json` in <0.1s and reports stale/missing voices without calling TTS.
- Only run `python3 scripts/refresh_voices.py --confirm` when Koushik explicitly asks to refresh voices.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

APP_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = APP_ROOT / "audio"
MANIFEST_PATH = AUDIO_DIR / "tts_manifest.json"
GEN_BIN = "/google/bin/releases/gemini-agents-generate/generate"
TTS_MODELS = ("gemini-v4s-tts-no-transcriber", "gemini-v4s-tts")

sys.path.insert(0, str(APP_ROOT))
from content import DAYS_21, DAYS_PART2_30, MORNING_QUOTES, SLIDES  # noqa: E402

BN_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")


def bn_num(n: int) -> str:
    return str(n).translate(BN_DIGITS)


def clean_cat(cat_str: str) -> str:
    s = re.sub(r"\([^)]*\)", "", cat_str)
    s = re.sub(r"[^\w\s\u0980-\u09FF।,:-]", "", s)
    return " ".join(s.split())


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def collect_expected_audio_items() -> dict[str, dict[str, str]]:
    """Return mapping of relative audio path (under `audio/`) -> {hash, scope, part, text, part1, part2}."""
    items: dict[str, dict[str, str]] = {}

    for s in SLIDES:
        sid = s["id"]
        rel_path = f"slides/slide_{sid}.mp3"
        txt = f"{s['title_bn']}। {s['highlight_bn']}। {s['text_bn']}"
        items[rel_path] = {
            "hash": sha256_text(txt),
            "scope": "slides",
            "part": "0",
            "text": txt,
            "part1": txt,
            "part2": "",
        }

    for q_idx, q_txt in enumerate(MORNING_QUOTES):
        rel_path = f"quotes/quote_{q_idx}.mp3"
        items[rel_path] = {
            "hash": sha256_text(q_txt),
            "scope": "quotes",
            "part": "0",
            "text": q_txt,
            "part1": q_txt,
            "part2": "",
        }

    for d in DAYS_21 + DAYS_PART2_30:
        day_num = int(d["day"])
        part_num = int(d.get("part", 1))

        day_rel = f"days/day_{day_num}.mp3"
        day_txt = d.get("voice_script_bn") or f"সুপ্রভাত মা! আজকের বিষয়— {d['title_bn']}। {d['summary_bn']}"
        items[day_rel] = {
            "hash": sha256_text(day_txt),
            "scope": "days",
            "part": str(part_num),
            "text": day_txt,
            "part1": day_txt,
            "part2": "",
        }

        for idx, ag in enumerate(d["agendas"]):
            ag_rel = f"games/day_{day_num}_ag_{idx}.mp3"
            part1_bn = f"{ag['title_bn']}। {ag['detail_bn']}"
            follow_bn = (
                f" আর গানটা শোনা হয়ে গেলে এর মানে জানতে বলো: {ag['followup_prompt_bn']}"
                if ag.get("followup_prompt_bn")
                else ""
            )
            part2_bn = f"এবার ফোনে জেমিনি খুলে মাইক ছুঁয়ে মুখে বলো: {ag['prompt_bn']}{follow_bn}"
            full_txt = f"{part1_bn} {part2_bn}"
            items[ag_rel] = {
                "hash": sha256_text(full_txt),
                "scope": "games",
                "part": str(part_num),
                "text": full_txt,
                "part1": part1_bn,
                "part2": part2_bn,
            }

    return items


def load_manifest() -> dict[str, str]:
    if not MANIFEST_PATH.is_file():
        return {}
    try:
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        return data.get("hashes", {}) if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_manifest(hashes: dict[str, str]) -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "voice_model": "gemini-v4s-tts (Aoede)",
        "total_tracked": len(hashes),
        "hashes": dict(sorted(hashes.items())),
    }
    MANIFEST_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def matches_scope(rel_path: str, info: dict[str, str], scope: str) -> bool:
    if scope == "all":
        return True
    if scope == "days-and-games":
        return info["scope"] in ("days", "games")
    if scope == "days":
        return info["scope"] == "days"
    if scope == "games":
        return info["scope"] == "games"
    if scope == "part1":
        return info["scope"] in ("days", "games") and info["part"] == "1"
    if scope == "part2":
        return info["scope"] in ("days", "games") and info["part"] == "2"
    return info["scope"] == scope


def get_stale_or_missing_files(scope: str = "all") -> tuple[list[str], dict[str, dict[str, str]], dict[str, str]]:
    expected = collect_expected_audio_items()
    recorded = load_manifest()
    stale: list[str] = []
    for rel_path, info in expected.items():
        if not matches_scope(rel_path, info, scope):
            continue
        mp3_path = AUDIO_DIR / rel_path
        if not mp3_path.is_file() or mp3_path.stat().st_size < 4000:
            stale.append(rel_path)
        elif recorded.get(rel_path) != info["hash"]:
            stale.append(rel_path)
    return stale, expected, recorded


def _synthesize_wav(text: str, out_wav: Path, model_name: str, timeout_s: int = 75) -> bool:
    try:
        proc = subprocess.run(
            [GEN_BIN, f"-timeout={timeout_s}s", f"-output={out_wav}", "tts", f"-model={model_name}", "-voice=Aoede", text],
            capture_output=True,
            text=True,
            timeout=timeout_s + 5,
        )
        return proc.returncode == 0 and out_wav.is_file() and out_wav.stat().st_size > 4000
    except subprocess.TimeoutExpired:
        return False


def _wav_to_mp3(wav_paths: list[Path], out_mp3: Path) -> bool:
    out_mp3.parent.mkdir(parents=True, exist_ok=True)
    if len(wav_paths) == 1:
        cmd = [
            "ffmpeg", "-y", "-i", str(wav_paths[0]),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ar", "24000", "-ac", "1", "-b:a", "32k",
            str(out_mp3),
        ]
    else:
        cmd = [
            "ffmpeg", "-y", "-i", str(wav_paths[0]), "-i", str(wav_paths[1]),
            "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ar", "24000", "-ac", "1", "-b:a", "32k",
            str(out_mp3),
        ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    return res.returncode == 0 and out_mp3.is_file() and out_mp3.stat().st_size >= 4000


def build_one(rel_path: str, info: dict[str, str]) -> tuple[str, bool]:
    out_mp3 = AUDIO_DIR / rel_path
    safe_tag = rel_path.replace("/", "_").replace(".mp3", "")
    w_full = Path(f"/tmp/kalyani_full_{os.getpid()}_{safe_tag}.wav")
    w1 = Path(f"/tmp/kalyani_p1_{os.getpid()}_{safe_tag}.wav")
    w2 = Path(f"/tmp/kalyani_p2_{os.getpid()}_{safe_tag}.wav")

    for attempt, model_name in enumerate((TTS_MODELS[0], TTS_MODELS[0], TTS_MODELS[1])):
        try:
            # Strategy 1: Seamless single-shot synthesis for continuous prosody
            if _synthesize_wav(info["text"], w_full, model_name, timeout_s=75):
                if _wav_to_mp3([w_full], out_mp3):
                    return rel_path, True

            # Strategy 2: Two-part synthesis fallback if full text hit window limits
            if info["part2"]:
                if _synthesize_wav(info["part1"], w1, model_name, timeout_s=55) and _synthesize_wav(info["part2"], w2, model_name, timeout_s=45):
                    if _wav_to_mp3([w1, w2], out_mp3):
                        return rel_path, True
        finally:
            w_full.unlink(missing_ok=True)
            w1.unlink(missing_ok=True)
            w2.unlink(missing_ok=True)
        time.sleep(0.5 * (attempt + 1))

    return rel_path, False


def main() -> int:
    parser = argparse.ArgumentParser(description="Explicit-only incremental Gemini Aoede voice refresher.")
    parser.add_argument("--init-manifest", action="store_true", help="Snapshot current text hashes for existing MP3s.")
    parser.add_argument("--status", action="store_true", help="Check which audio files are stale/missing without regenerating.")
    parser.add_argument("--confirm", action="store_true", help="Explicit confirmation from Koushik to regenerate stale/missing voices.")
    parser.add_argument(
        "--scope",
        default="all",
        choices=("all", "days-and-games", "days", "games", "part1", "part2", "slides", "quotes"),
        help="Target subset of voices to check or refresh.",
    )
    parser.add_argument("--workers", type=int, default=16, help="Parallel TTS worker count (default: 16).")
    parser.add_argument("--all", action="store_true", help="Force regenerate all items in scope (requires --confirm).")
    args = parser.parse_args()

    stale, expected, recorded = get_stale_or_missing_files(scope=args.scope)
    scoped_keys = [k for k, v in expected.items() if matches_scope(k, v, args.scope)]

    if args.init_manifest:
        hashes = {
            rel_path: info["hash"]
            for rel_path, info in expected.items()
            if (AUDIO_DIR / rel_path).is_file() and (AUDIO_DIR / rel_path).stat().st_size >= 4000
        }
        save_manifest(hashes)
        print(f"[TTS Manifest] Initialized {MANIFEST_PATH} with {len(hashes)}/{len(expected)} verified MP3 hashes.")
        return 0

    if args.status or not args.confirm:
        if not stale:
            print(f"[TTS Status] All {len(scoped_keys)} Aoede MP3 files in scope='{args.scope}' are 100% in sync.")
        else:
            print(f"[TTS Status] {len(stale)}/{len(scoped_keys)} audio file(s) in scope='{args.scope}' need refresh: {stale[:10]}")
            if not args.confirm:
                print("[TTS Rule] Automatic TTS regeneration is disabled by GEMINI.md. Ask Koushik before running with --confirm.")
        return 0

    targets = scoped_keys if args.all else stale
    if not targets:
        print(f"[TTS Refresh] Nothing to regenerate in scope='{args.scope}' — all voices match current text hashes.")
        return 0

    t0 = time.time()
    print(f"[TTS Refresh] Regenerating {len(targets)} Gemini Aoede MP3 file(s) (scope={args.scope}, workers={args.workers})...", flush=True)
    ok_count = 0
    failed: list[str] = []

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futs = {ex.submit(build_one, rel_path, expected[rel_path]): rel_path for rel_path in targets}
        for i, fut in enumerate(as_completed(futs), 1):
            rel_path, ok = fut.result()
            if ok:
                ok_count += 1
                recorded[rel_path] = expected[rel_path]["hash"]
            else:
                failed.append(rel_path)
            if i % 15 == 0 or i == len(targets):
                save_manifest(recorded)
                print(
                    f"Progress: {i}/{len(targets)} (ok={ok_count}, failed={len(failed)}, elapsed={time.time() - t0:.1f}s)",
                    flush=True,
                )

    save_manifest(recorded)
    print(f"[TTS Refresh] Done: {ok_count}/{len(targets)} updated in {time.time() - t0:.1f}s.")
    if failed:
        print(f"[TTS Refresh] Failed ({len(failed)}): {failed[:15]}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
