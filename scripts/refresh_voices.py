#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Explicit-only incremental Gemini Aoede (`gemini-v4s-tts`) voice generator for Kalyani App.

CRITICAL RULE (defined in GEMINI.md):
- NEVER run this script automatically during UI changes or data/content edits.
- `scripts/build_app.py` checks `audio/tts_manifest.json` and reports any stale/missing audio files without regenerating them.
- Only run `python3 scripts/refresh_voices.py --confirm` when Koushik explicitly asks to refresh voices.
"""

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

sys.path.insert(0, str(APP_ROOT / "scripts"))
from curriculum_data import DAYS_21, SLIDES  # noqa: E402

MORNING_QUOTES = [
    "সুপ্রভাত মা! যেমনভাবে একটা পাখি ডানা মেলে আকাশে ওড়ে, আজ তোমার মনটাও তেমনই হালকা ও আনন্দে ভরে উঠুক।",
    "সুপ্রভাত মা! মা সারদা বলতেন—‘যখনই ভয় করবে, জানবে আমি তোমার পাশে আছি।’ আজ নতুন কিছু শেখার জন্য দারুণ একটা দিন!",
    "সুপ্রভাত মা! রানাঘাটের সেই মনোযোগী স্কুলছাত্রীটি আজও তোমার ভেতরে বেঁচে আছে। আজ কৌতূহল নিয়ে একটি গানের অর্থ ও নতুন বোতাম শিখবো!",
    "সুপ্রভাত মা! বয়স কেবল সংখ্যামাত্র—প্রতিদিন একটি করে ‘কেন?’ এবং ‘কীভাবে?’ প্রশ্ন করলেই মস্তিষ্ক চিরতরুণ থাকে।",
    "সুপ্রভাত মা! তোমার ছেলে কৌশিক আর দিদি তোমাকে ভীষণ ভালোবাসে। আজ নিজের আনন্দে, কোনো দ্বিধা ছাড়া নতুন কিছু শেখো!",
    "সুপ্রভাত মা! রবীন্দ্রনাথ লিখেছেন—‘আলো আমার, আলো ওগো, আলোয় ভুবন ভরা।’ আজ তোমার মন ও ঘর আনন্দ-আলোয় ভরে থাকুক।",
    "সুপ্রভাত মা! ভুল হওয়া মানেই শেখার শুরু। আজ কোনো লজ্জা ছাড়া রিমোট, ফোন বা ইংরেজি শব্দ নিয়ে নতুন খেলা খেলবো!",
]


def clean_cat(cat_str: str) -> str:
    s = re.sub(r"\([^)]*\)", "", cat_str)
    s = re.sub(r"[^\w\s\u0980-\u09FF।,:-]", "", s)
    return " ".join(s.split())


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def collect_expected_audio_items() -> dict[str, dict[str, str]]:
    """Return mapping of filename -> {hash, text, part1, part2} for all tracked audio files."""
    items: dict[str, dict[str, str]] = {}

    for s in SLIDES:
        sid = s["id"]
        fname = f"slide_{sid}.mp3"
        txt = f"{s['title_bn']}। {s['highlight_bn']}। {s['text_bn']}"
        items[fname] = {"hash": sha256_text(txt), "text": txt, "part1": txt, "part2": ""}

    for q_idx, q_txt in enumerate(MORNING_QUOTES):
        fname = f"quote_{q_idx}.mp3"
        items[fname] = {"hash": sha256_text(q_txt), "text": q_txt, "part1": q_txt, "part2": ""}

    for d in DAYS_21:
        day_num = d["day"]
        day_fname = f"day_{day_num}.mp3"
        day_txt = f"দিন {day_num}: {d['title_bn']}। {d['summary_bn']}"
        items[day_fname] = {"hash": sha256_text(day_txt), "text": day_txt, "part1": day_txt, "part2": ""}

        for idx, ag in enumerate(d["agendas"]):
            ag_fname = f"day_{day_num}_ag_{idx}.mp3"
            cat_bn = clean_cat(ag["category"])
            part1_bn = (
                f"দিন {day_num}, খেলা {idx + 1}: {cat_bn}। "
                f"{ag['title_bn']}। "
                f"ধাপ ১, মা আজ যা করবেন ও শিখবেন: {ag['detail_bn']}"
            )
            part2_bn = (
                f"ধাপ ২, মা, এবার ফোনে জেমিনি অ্যাপ খুলে মাইক বোতাম ছুঁয়ে ঠিক এই কথাটি মুখে বলো: {ag['prompt_bn']}"
            )
            full_txt = f"{part1_bn} {part2_bn}"
            items[ag_fname] = {
                "hash": sha256_text(full_txt),
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


def get_stale_or_missing_files() -> tuple[list[str], dict[str, dict[str, str]], dict[str, str]]:
    expected = collect_expected_audio_items()
    recorded = load_manifest()
    stale: list[str] = []
    for fname, info in expected.items():
        mp3_path = AUDIO_DIR / fname
        if not mp3_path.is_file() or mp3_path.stat().st_size < 4000:
            stale.append(fname)
        elif recorded.get(fname) != info["hash"]:
            stale.append(fname)
    return stale, expected, recorded


def build_one(fname: str, info: dict[str, str]) -> tuple[str, bool]:
    out_mp3 = AUDIO_DIR / fname
    part1_bn = info["part1"]
    part2_bn = info["part2"]
    w1 = Path(f"/tmp/kalyani_p1_{os.getpid()}_{fname}.wav")
    w2 = Path(f"/tmp/kalyani_p2_{os.getpid()}_{fname}.wav")

    for attempt in range(3):
        try:
            if part2_bn:
                p1 = subprocess.run(
                    [GEN_BIN, f"-output={w1}", "tts", "-voice=Aoede", part1_bn],
                    capture_output=True, text=True, timeout=35,
                )
                p2 = subprocess.run(
                    [GEN_BIN, f"-output={w2}", "tts", "-voice=Aoede", part2_bn],
                    capture_output=True, text=True, timeout=35,
                )
                if p1.returncode == 0 and p2.returncode == 0 and w1.is_file() and w2.is_file():
                    subprocess.run(
                        [
                            "ffmpeg", "-y", "-i", str(w1), "-i", str(w2),
                            "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11",
                            "-ar", "24000", "-ac", "1", "-b:a", "32k",
                            str(out_mp3),
                        ],
                        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    )
                    w1.unlink(missing_ok=True)
                    w2.unlink(missing_ok=True)
                    return fname, True
            else:
                p1 = subprocess.run(
                    [GEN_BIN, f"-output={w1}", "tts", "-voice=Aoede", part1_bn],
                    capture_output=True, text=True, timeout=35,
                )
                if p1.returncode == 0 and w1.is_file():
                    subprocess.run(
                        [
                            "ffmpeg", "-y", "-i", str(w1),
                            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                            "-ar", "24000", "-ac", "1", "-b:a", "32k",
                            str(out_mp3),
                        ],
                        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    )
                    w1.unlink(missing_ok=True)
                    return fname, True
        except subprocess.TimeoutExpired:
            pass
        finally:
            w1.unlink(missing_ok=True)
            w2.unlink(missing_ok=True)
        time.sleep(0.4 * (attempt + 1))
    return fname, False


def main() -> int:
    parser = argparse.ArgumentParser(description="Explicit-only incremental Gemini Aoede voice refresher.")
    parser.add_argument("--init-manifest", action="store_true", help="Snapshot current text hashes for existing MP3s into audio/tts_manifest.json.")
    parser.add_argument("--status", action="store_true", help="Check which audio files are stale/out-of-sync without regenerating.")
    parser.add_argument("--confirm", action="store_true", help="Explicit confirmation from Koushik to regenerate stale/missing voices.")
    parser.add_argument("--all", action="store_true", help="Force regenerate all voices (requires --confirm).")
    args = parser.parse_args()

    expected = collect_expected_audio_items()
    if args.init_manifest:
        hashes = {
            fname: info["hash"]
            for fname, info in expected.items()
            if (AUDIO_DIR / fname).is_file() and (AUDIO_DIR / fname).stat().st_size >= 4000
        }
        save_manifest(hashes)
        print(f"[TTS Manifest] Initialized {MANIFEST_PATH} with {len(hashes)}/{len(expected)} verified MP3 hashes.")
        return 0

    stale, expected, recorded = get_stale_or_missing_files()
    if args.status or not args.confirm:
        if not stale:
            print(f"[TTS Status] All {len(expected)} Aoede MP3 files are 100% in sync with curriculum_data.py.")
        else:
            print(f"[TTS Status] {len(stale)}/{len(expected)} audio file(s) have modified text or are missing: {stale[:12]}")
            if not args.confirm:
                print("[TTS Rule] Automatic TTS regeneration is disabled by GEMINI.md. Ask Koushik before running with --confirm.")
        return 0

    targets = list(expected.keys()) if args.all else stale
    if not targets:
        print("[TTS Refresh] Nothing to regenerate — all voices match current text hashes.")
        return 0

    t0 = time.time()
    print(f"[TTS Refresh] Regenerating {len(targets)} Gemini Aoede MP3 file(s)...", flush=True)
    ok_count = 0
    failed = []
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(build_one, fname, expected[fname]): fname for fname in targets}
        for i, fut in enumerate(as_completed(futs), 1):
            fname, ok = fut.result()
            if ok:
                ok_count += 1
                recorded[fname] = expected[fname]["hash"]
            else:
                failed.append(fname)
            if i % 10 == 0 or i == len(targets):
                print(f"Progress: {i}/{len(targets)} (ok={ok_count}, failed={len(failed)}, elapsed={time.time()-t0:.1f}s)", flush=True)

    save_manifest(recorded)
    print(f"[TTS Refresh] Done: {ok_count}/{len(targets)} updated in {time.time()-t0:.1f}s.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
