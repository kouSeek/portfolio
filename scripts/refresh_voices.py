#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Explicit-only incremental Gemini Aoede (`gemini-v4s-tts`) voice refresher for AI Companion (`kalyani` & `anondo`).

CRITICAL GOVERNANCE RULE (defined in GEMINI.md):
- NEVER run this script with `--confirm` automatically during UI tweaks or content/data edits.
- `scripts/build_app.py` inspects `audio/<persona>/tts_manifest.json` in <0.1s without calling TTS.
- Only run `python3 scripts/refresh_voices.py --persona <kalyani|anondo> --confirm` when Koushik explicitly approves.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

APP_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = APP_ROOT / "audio"
GEN_BIN = "/google/bin/releases/gemini-agents-generate/generate"
TTS_MODELS = ("gemini-v4s-tts-no-transcriber", "gemini-v4s-tts")
DEFAULT_PERSONA_ID = "kalyani"
PERSONA_ALIASES = {"ma_kalyani": "kalyani", "ma": "kalyani", "koushik": "anondo", "me": "anondo"}

sys.path.insert(0, str(APP_ROOT))
from content import (  # noqa: E402
    ANONDO_DAYS_21,
    ANONDO_PILLARS,
    ANONDO_QUOTES,
    ANONDO_SLIDES,
    DAYS_21,
    MORNING_QUOTES,
    SLIDES,
)

BN_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")


def normalize_persona_id(persona_id: str = DEFAULT_PERSONA_ID) -> str:
    return PERSONA_ALIASES.get(persona_id, persona_id)


def bn_num(n: int) -> str:
    return str(n).translate(BN_DIGITS)


def clean_cat(cat_str: str) -> str:
    s = re.sub(r"\([^)]*\)", "", cat_str)
    s = re.sub(r"[^\w\s\u0980-\u09FF।,:-]", "", s)
    return " ".join(s.split())


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def get_audio_root(persona_id: str = DEFAULT_PERSONA_ID) -> Path:
    return AUDIO_DIR / normalize_persona_id(persona_id)


def get_manifest_path(persona_id: str = DEFAULT_PERSONA_ID) -> Path:
    return get_audio_root(persona_id) / "tts_manifest.json"


def _collect_anondo_audio_items() -> dict[str, dict[str, str]]:
    """Collect expected English Aoede voice items for `anondo` (`audio/anondo/...`)."""
    items: dict[str, dict[str, str]] = {}

    for s in ANONDO_SLIDES:
        sid = int(s["id"])
        rel_path = f"slides/slide_{sid}.mp3"
        txt = f"{s['title']}. {s['highlight']} {s['text']}"
        items[rel_path] = {
            "hash": sha256_text(txt),
            "scope": "slides",
            "part": "0",
            "text": txt,
            "part1": txt,
            "part2": "",
        }

    for q_idx, q_txt in enumerate(ANONDO_QUOTES):
        rel_path = f"quotes/quote_{q_idx}.mp3"
        items[rel_path] = {
            "hash": sha256_text(q_txt),
            "scope": "quotes",
            "part": "0",
            "text": q_txt,
            "part1": q_txt,
            "part2": "",
        }

    for p_idx, p_obj in enumerate(ANONDO_PILLARS):
        rel_path = f"pillars/pillar_{p_idx}.mp3"
        p_txt = f"{p_obj['title']}. {p_obj['detail']}"
        items[rel_path] = {
            "hash": sha256_text(p_txt),
            "scope": "pillars",
            "part": "0",
            "text": p_txt,
            "part1": p_txt,
            "part2": "",
        }

    for d in ANONDO_DAYS_21:
        day_num = int(d["day"])
        day_rel = f"days/day_{day_num}.mp3"
        day_txt = d.get("voice_script_bn") or f"Good morning Koushik! Welcome to Day {day_num}: {d['title_bn']}."
        items[day_rel] = {
            "hash": sha256_text(day_txt),
            "scope": "days",
            "part": "1",
            "text": day_txt,
            "part1": day_txt,
            "part2": "",
        }

        for idx, ag in enumerate(d["agendas"]):
            ag_rel = f"games/day_{day_num}_ag_{idx}.mp3"
            part1_en = f"{ag['title_bn']}. {ag['detail_bn']}"
            follow_en = f" And in Turn 2, ask: {ag['followup_prompt_bn']}" if ag.get("followup_prompt_bn") else ""
            part2_en = f"Open Gemini Live and say: {ag['prompt_bn']}{follow_en}"
            full_txt = f"{part1_en} {part2_en}"
            items[ag_rel] = {
                "hash": sha256_text(full_txt),
                "scope": "games",
                "part": "1",
                "text": full_txt,
                "part1": part1_en,
                "part2": part2_en,
            }

    return items


def _find_node_bin() -> str:
    found = shutil.which("node") or shutil.which("nodejs")
    if found:
        return found
    home = Path.home()
    for cand in [
        *sorted(home.glob(".vscode/cli/serve-web/*/node")),
        *sorted(home.glob(".jetski-server/bin/*/node")),
        *sorted(home.glob(".nvm/versions/node/*/bin/node")),
        Path("/usr/local/bin/node"),
        Path("/usr/bin/node"),
    ]:
        if cand.is_file():
            return str(cand)
    return "node"


def _clean_tts_text(s: str) -> str:
    s = re.sub(r"[\U00010000-\U0010ffff\u2600-\u27bf\ufe0f]", " ", str(s or ""))
    s = re.sub(r"[•*#_`~↗]+", " ", s)
    return " ".join(s.split())


def _collect_jhalak_audio_items() -> dict[str, dict[str, str]]:
    """Collect expected full-page Bengali Aoede voice items for `jhalak` (`audio/jhalak/reels/<id>.mp3`)."""
    js_dir = APP_ROOT / "src" / "jhalak" / "js"
    js_code = (
        f"const DAYS_21 = {json.dumps(DAYS_21, ensure_ascii=False)};\n"
        + (js_dir / "curated-content.js").read_text(encoding="utf-8") + "\n"
        + (js_dir / "feed-engine.js").read_text(encoding="utf-8") + "\n"
        + "console.log(JSON.stringify(ALL_JHALAK_REELS));"
    )
    proc = subprocess.run([_find_node_bin(), "-"], input=js_code, capture_output=True, text=True, check=True)
    reels = json.loads(proc.stdout)

    items: dict[str, dict[str, str]] = {}
    for r in reels:
        cid = str(r["id"])
        rel_path = f"reels/{cid}.mp3"
        title_txt = _clean_tts_text(r.get("title_bn", ""))
        sec_blocks: list[str] = []
        for sec in r.get("sections", []):
            h = _clean_tts_text(sec.get("heading_bn", ""))
            b = _clean_tts_text(sec.get("body_bn", ""))
            if h and b:
                sec_blocks.append(f"{h}। {b}")
            elif b:
                sec_blocks.append(b)
        cur_q = _clean_tts_text(r.get("curiosity_q_bn", ""))
        cur_a = _clean_tts_text(r.get("curiosity_a_bn", ""))
        cur_txt = f"{cur_q} {cur_a}".strip()

        mid = max(1, (len(sec_blocks) + 1) // 2)
        p1_list = [title_txt, *sec_blocks[:mid]]
        p2_list = [*sec_blocks[mid:], cur_txt]
        part1 = " ".join(x for x in p1_list if x).strip()
        part2 = " ".join(x for x in p2_list if x).strip()
        full_txt = f"{part1} {part2}".strip()

        items[rel_path] = {
            "hash": sha256_text(full_txt),
            "scope": "reels",
            "part": "0",
            "text": full_txt,
            "part1": part1,
            "part2": part2,
        }
    return items


def _collect_zorba_audio_items() -> dict[str, dict[str, str]]:
    """Collect expected full-page English Aoede voice items for `zorba` (`audio/zorba/reels/<id>.mp3`)."""
    days_payload = [
        {
            "day": int(d["day"]),
            "phase": d.get("phase", "House-Money Era"),
            "title": d["title_bn"],
            "sub": d.get("summary_bn", ""),
            "games": [
                {
                    "pillar": ag.get("pillar", ""),
                    "short": ag["short_bn"],
                    "category": ag["category"],
                    "title": ag["title_bn"],
                    "detail": ag["detail_bn"],
                    "prompt": ag["prompt_bn"],
                    "followup_prompt": ag.get("followup_prompt_bn", ""),
                }
                for ag in d["agendas"]
            ],
        }
        for d in ANONDO_DAYS_21
    ]
    quotes_payload = [{"text": q} for q in ANONDO_QUOTES]
    anondo_data = {"slides": ANONDO_SLIDES, "quotes": quotes_payload, "days": days_payload}
    js_path = APP_ROOT / "src" / "zorba" / "js" / "curated-content.js"
    js_code = (
        f"const ANONDO_DATA = {json.dumps(anondo_data, ensure_ascii=False)};\n"
        f"const PILLARS_DATA = {json.dumps(ANONDO_PILLARS, ensure_ascii=False)};\n"
        + js_path.read_text(encoding="utf-8") + "\n"
        + "console.log(JSON.stringify(ALL_JHALAK_REELS));"
    )
    proc = subprocess.run([_find_node_bin(), "-"], input=js_code, capture_output=True, text=True, check=True)
    reels = json.loads(proc.stdout)

    items: dict[str, dict[str, str]] = {}
    for r in reels:
        cid = str(r["id"])
        rel_path = f"reels/{cid}.mp3"
        title_txt = _clean_tts_text(r.get("title_bn", ""))
        sec_blocks: list[str] = []
        for sec in r.get("sections", []):
            h = _clean_tts_text(sec.get("heading_bn", ""))
            b = _clean_tts_text(sec.get("body_bn", ""))
            if h and b:
                sec_blocks.append(f"{h}. {b}")
            elif b:
                sec_blocks.append(b)
        cur_q = _clean_tts_text(r.get("curiosity_q_bn", ""))
        cur_a = _clean_tts_text(r.get("curiosity_a_bn", ""))
        cur_txt = f"{cur_q} {cur_a}".strip()

        mid = max(1, (len(sec_blocks) + 1) // 2)
        p1_list = [f"{title_txt}." if title_txt else "", *sec_blocks[:mid]]
        p2_list = [*sec_blocks[mid:], cur_txt]
        part1 = " ".join(x for x in p1_list if x).strip()
        part2 = " ".join(x for x in p2_list if x).strip()
        full_txt = f"{part1} {part2}".strip()

        items[rel_path] = {
            "hash": sha256_text(full_txt),
            "scope": "reels",
            "part": "0",
            "text": full_txt,
            "part1": part1,
            "part2": part2,
        }
    return items


def collect_expected_audio_items(persona_id: str = DEFAULT_PERSONA_ID) -> dict[str, dict[str, str]]:
    """Return mapping of relative audio path (under `audio/<persona_id>/`) -> {hash, scope, part, text, part1, part2}."""
    pid = normalize_persona_id(persona_id)
    if pid == "anondo":
        return _collect_anondo_audio_items()
    if pid == "jhalak":
        return _collect_jhalak_audio_items()
    if pid == "zorba":
        return _collect_zorba_audio_items()

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

    for d in DAYS_21:
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
            if ag.get("followup_prompt_bn"):
                if "🎵" in ag.get("category", ""):
                    follow_bn = f" আর গানটা শোনা হয়ে গেলে এর মানে জানতে বলো: {ag['followup_prompt_bn']}"
                else:
                    follow_bn = f" আর উত্তরের পর দ্বিতীয় কথায় বলো: {ag['followup_prompt_bn']}"
            else:
                follow_bn = ""
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


def load_manifest(persona_id: str = DEFAULT_PERSONA_ID) -> dict[str, str]:
    mpath = get_manifest_path(persona_id)
    if not mpath.is_file():
        return {}
    try:
        data = json.loads(mpath.read_text(encoding="utf-8"))
        return data.get("hashes", {}) if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_manifest(hashes: dict[str, str], persona_id: str = DEFAULT_PERSONA_ID) -> None:
    pid = normalize_persona_id(persona_id)
    mpath = get_manifest_path(pid)
    mpath.parent.mkdir(parents=True, exist_ok=True)
    extra_keys: dict = {}
    if mpath.is_file():
        try:
            old_data = json.loads(mpath.read_text(encoding="utf-8"))
            if isinstance(old_data, dict):
                extra_keys = {k: v for k, v in old_data.items() if k not in ("voice_model", "persona_id", "total_tracked", "hashes")}
        except Exception:
            pass
    payload = {
        "voice_model": "gemini-v4s-tts (Aoede)",
        "persona_id": pid,
        "total_tracked": len(hashes),
        "hashes": dict(sorted(hashes.items())),
        **extra_keys,
    }
    mpath.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def matches_scope(rel_path: str, info: dict[str, str], scope: str) -> bool:
    if scope == "all":
        return True
    if scope == "days-and-games":
        return info["scope"] in ("days", "games")
    if scope in ("days", "games", "slides", "quotes", "pillars", "reels"):
        return info["scope"] == scope
    if scope == "part1":
        return info["scope"] in ("days", "games") and info["part"] == "1"
    return info["scope"] == scope


def get_stale_or_missing_files(
    scope: str = "all",
    require_local_mp3: bool | None = None,
    persona_id: str = DEFAULT_PERSONA_ID,
    student_id: str | None = None,
) -> tuple[list[str], dict[str, dict[str, str]], dict[str, str]]:
    pid = normalize_persona_id(student_id or persona_id)
    expected = collect_expected_audio_items(pid)
    recorded = load_manifest(pid)
    aud_root = get_audio_root(pid)
    if require_local_mp3 is None:
        require_local_mp3 = any(aud_root.rglob("*.mp3")) if aud_root.is_dir() else False
    stale: list[str] = []
    for rel_path, info in expected.items():
        if not matches_scope(rel_path, info, scope):
            continue
        mp3_path = aud_root / rel_path
        if require_local_mp3 and (not mp3_path.is_file() or mp3_path.stat().st_size < 4000):
            stale.append(rel_path)
        elif recorded.get(rel_path) != info["hash"]:
            stale.append(rel_path)
    return stale, expected, recorded


_SPEECH_PROTO_PATH = Path("/tmp/aicomp_speech_synth.proto")
_SPEECH_PROTO_TEXT = """syntax = "proto2";
package speech;
message Voice { required string language = 1; optional string gender = 2; optional string name = 3; }
message AudioEncoding { enum Encoding { ANY = 0; LINEAR_16BIT = 1; MP3 = 4; MP3_64KBPS = 10; } }
message SpeechSynthesizerRequest { required string ssml = 1; optional Voice voice = 2; optional AudioEncoding.Encoding encoding = 3; }
message SpeechSynthesizerEvent { optional int32 type = 1; optional bytes audio = 2; }
message SpeechSynthesizerResponse { optional string info = 1; }
message SpeechSynthesizerSynthesizeMixedResult { optional SpeechSynthesizerEvent stream_message = 1; optional SpeechSynthesizerResponse result_message = 2; }
service SpeechSynthesizer { rpc Synthesize(SpeechSynthesizerRequest) returns (stream SpeechSynthesizerSynthesizeMixedResult); }
"""


def _synthesize_voicelm_aoede(text: str, out_raw: Path, timeout_s: int = 25) -> bool:
    cleaned = re.sub(r"\s+", " ", (text or "")).strip()
    if not cleaned:
        return False
    if not _SPEECH_PROTO_PATH.is_file() or _SPEECH_PROTO_PATH.stat().st_size < 100:
        _SPEECH_PROTO_PATH.write_text(_SPEECH_PROTO_TEXT, encoding="utf-8")
    ssml = (
        '<?xml version="1.0"?> '
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.w3.org/TR/speech-synthesis/synthesis.xsd '
        'http://www.w3.org/TR/speech-synthesis/synthesis.xsd" xml:lang="en-US">'
        f"{html.escape(cleaned, quote=False)}</speak>"
    )
    req_proto = (
        f"ssml: {json.dumps(ssml)} "
        'voice { language: "en-US" gender: "female" name: "en-us-gia-server-voicelm#kix02" } '
        "encoding: MP3_64KBPS"
    )
    try:
        proc = subprocess.run(
            [
                "stubby", "call", "--proto2", "--noremotedb", "--ignore_serverstatus",
                f"--protofiles={_SPEECH_PROTO_PATH}",
                "blade:speech-tts-synthesizer-speech-synthesizer-prod",
                "speech.SpeechSynthesizer.Synthesize",
                req_proto,
            ],
            capture_output=True, text=True, timeout=timeout_s, check=False,
        )
        if proc.returncode == 0 and proc.stdout:
            mp3_bytes = b"".join(
                m.group(1).encode("latin1").decode("unicode_escape").encode("latin1")
                for m in re.finditer(r'audio:\s*"((?:[^"\\]|\\.)*)"', proc.stdout)
            )
            if len(mp3_bytes) > 1000:
                out_raw.write_bytes(mp3_bytes)
                return True
    except Exception:
        pass
    return False


def _synthesize_wav(text: str, out_wav: Path, model_name: str, timeout_s: int = 75) -> bool:
    if any(tag in out_wav.name for tag in ("_anondo_", "_zorba_")):
        if _synthesize_voicelm_aoede(text, out_wav, timeout_s=min(30, timeout_s)):
            return True
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


def build_one(rel_path: str, info: dict[str, str], aud_root: Path) -> tuple[str, bool]:
    out_mp3 = aud_root / rel_path
    safe_tag = f"{aud_root.name}_" + rel_path.replace("/", "_").replace(".mp3", "")
    w_full = Path(f"/tmp/aicomp_full_{os.getpid()}_{safe_tag}.wav")
    w1 = Path(f"/tmp/aicomp_p1_{os.getpid()}_{safe_tag}.wav")
    w2 = Path(f"/tmp/aicomp_p2_{os.getpid()}_{safe_tag}.wav")

    for attempt, model_name in enumerate((TTS_MODELS[0], TTS_MODELS[0], TTS_MODELS[1])):
        try:
            if aud_root.name not in ("anondo", "zorba") and len(info["text"]) > 1350 and info["part2"]:
                if _synthesize_wav(info["part1"], w1, model_name, timeout_s=70) and _synthesize_wav(info["part2"], w2, model_name, timeout_s=70):
                    if _wav_to_mp3([w1, w2], out_mp3):
                        return rel_path, True
            if _synthesize_wav(info["text"], w_full, model_name, timeout_s=85):
                if _wav_to_mp3([w_full], out_mp3):
                    return rel_path, True

            if info["part2"]:
                if _synthesize_wav(info["part1"], w1, model_name, timeout_s=70) and _synthesize_wav(info["part2"], w2, model_name, timeout_s=70):
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
    parser.add_argument("--persona", default=DEFAULT_PERSONA_ID, choices=("kalyani", "anondo", "jhalak", "zorba"), help="Target persona voice set.")
    parser.add_argument("--init-manifest", action="store_true", help="Snapshot current text hashes for existing MP3s.")
    parser.add_argument("--status", action="store_true", help="Check which audio files are stale/missing without regenerating.")
    parser.add_argument("--confirm", action="store_true", help="Explicit confirmation from Koushik to regenerate stale/missing voices.")
    parser.add_argument(
        "--scope",
        default="all",
        choices=("all", "days-and-games", "days", "games", "part1", "slides", "quotes", "pillars", "reels"),
        help="Target subset of voices to check or refresh.",
    )
    parser.add_argument("--workers", type=int, default=16, help="Parallel TTS worker count (default: 16).")
    parser.add_argument("--all", action="store_true", help="Force regenerate all items in scope (requires --confirm).")
    parser.add_argument("--publish", action="store_true", help="Also force-push updated audio/ snapshot to `ai-companion-audio` branch.")
    args = parser.parse_args()

    pid = normalize_persona_id(args.persona)
    aud_root = get_audio_root(pid)
    stale, expected, recorded = get_stale_or_missing_files(
        scope=args.scope,
        require_local_mp3=True if args.confirm else None,
        persona_id=pid,
    )
    scoped_keys = [k for k, v in expected.items() if matches_scope(k, v, args.scope)]

    if args.init_manifest:
        hashes = {
            rel_path: info["hash"]
            for rel_path, info in expected.items()
            if (aud_root / rel_path).is_file() and (aud_root / rel_path).stat().st_size >= 4000
        }
        save_manifest(hashes, pid)
        print(f"[TTS Manifest] Initialized {get_manifest_path(pid)} with {len(hashes)}/{len(expected)} verified MP3 hashes.")
        return 0

    if args.status or not args.confirm:
        if not stale:
            print(f"[TTS Status ({pid})] All {len(scoped_keys)} Aoede MP3 files in scope='{args.scope}' are 100% in sync.")
        else:
            print(f"[TTS Status ({pid})] {len(stale)}/{len(scoped_keys)} audio file(s) in scope='{args.scope}' need refresh: {stale[:10]}")
            if not args.confirm:
                print("[TTS Rule] Automatic TTS regeneration is disabled by GEMINI.md. Ask Koushik before running with --confirm.")
        return 0

    targets = scoped_keys if args.all else stale
    if not targets:
        print(f"[TTS Refresh ({pid})] Nothing to regenerate in scope='{args.scope}' — all voices match current text hashes.")
        return 0

    t0 = time.time()
    print(f"[TTS Refresh ({pid})] Regenerating {len(targets)} Gemini Aoede MP3 file(s) (scope={args.scope}, workers={args.workers})...", flush=True)
    ok_count = 0
    failed: list[str] = []

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futs = {ex.submit(build_one, rel_path, expected[rel_path], aud_root): rel_path for rel_path in targets}
        for i, fut in enumerate(as_completed(futs), 1):
            rel_path, ok = fut.result()
            if ok:
                ok_count += 1
                recorded[rel_path] = expected[rel_path]["hash"]
            else:
                failed.append(rel_path)
            if i % 15 == 0 or i == len(targets):
                save_manifest(recorded, pid)
                print(
                    f"Progress: {i}/{len(targets)} (ok={ok_count}, failed={len(failed)}, elapsed={time.time() - t0:.1f}s)",
                    flush=True,
                )

    if args.scope in ("all", "days-and-games"):
        orphan_keys = [k for k in list(recorded.keys()) if k not in expected]
        for ok_key in orphan_keys:
            recorded.pop(ok_key, None)
        pruned_files = 0
        for sub in ("slides", "quotes", "pillars", "days", "games", "reels"):
            sub_dir = aud_root / sub
            if not sub_dir.is_dir():
                continue
            for mp3_file in sub_dir.glob("*.mp3"):
                rel = f"{sub}/{mp3_file.name}"
                if rel not in expected:
                    mp3_file.unlink(missing_ok=True)
                    pruned_files += 1
        if orphan_keys or pruned_files:
            print(f"[TTS Prune] Cleaned {pruned_files} obsolete MP3 file(s) and {len(orphan_keys)} manifest key(s).", flush=True)

    save_manifest(recorded, pid)
    print(f"[TTS Refresh ({pid})] Done: {ok_count}/{len(targets)} updated in {time.time() - t0:.1f}s.")
    if failed:
        print(f"[TTS Refresh ({pid})] Failed ({len(failed)}): {failed[:15]}", flush=True)
        return 1
    if args.publish:
        from sync_audio_branch import sync_audio_orphan_branch  # noqa: PLC0415

        return sync_audio_orphan_branch(dry_run=False)
    print("[TTS Next Step] Run `python3 scripts/sync_audio_branch.py` to publish updated MP3s to `ai-companion-audio`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
