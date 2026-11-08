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
import base64
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
        txt = _clean_tts_text(_humanize_english_tts_text(f"{s['title']}. {s['highlight']} {s['text']}"))
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
        q_clean = _clean_tts_text(_humanize_english_tts_text(q_txt))
        items[rel_path] = {
            "hash": sha256_text(q_clean),
            "scope": "quotes",
            "part": "0",
            "text": q_clean,
            "part1": q_clean,
            "part2": "",
        }

    for p_idx, p_obj in enumerate(ANONDO_PILLARS):
        rel_path = f"pillars/pillar_{p_idx}.mp3"
        p_txt = _clean_tts_text(_humanize_english_tts_text(f"{p_obj['title']}. {p_obj['detail']}"))
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
        raw_day_txt = d.get("voice_script_bn") or f"Good morning Koushik! Welcome to Day {day_num}: {d['title_bn']}."
        day_txt = _clean_tts_text(_humanize_english_tts_text(raw_day_txt))
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
            part1_en = _clean_tts_text(_humanize_english_tts_text(f"{ag['title_bn']}. {ag['detail_bn']}"))
            follow_en = f" And in Turn 2, ask: {ag['followup_prompt_bn']}" if ag.get("followup_prompt_bn") else ""
            part2_en = _clean_tts_text(_humanize_english_tts_text(f"Open Gemini Live and say: {ag['prompt_bn']}{follow_en}"))
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


_LATEX_GREEK_SPOKEN: dict[str, str] = {
    r"\theta": " theta ",
    r"\omega": " omega ",
    r"\lambda": " lambda ",
    r"\mu": " mu ",
    r"\nu": " nu ",
    r"\pi": " pi ",
    r"\sigma": " sigma ",
    r"\tau": " tau ",
    r"\alpha": " alpha ",
    r"\beta": " beta ",
    r"\gamma": " gamma ",
    r"\delta": " delta ",
    r"\Delta": " delta ",
    r"\epsilon": " epsilon ",
    r"\varepsilon": " epsilon ",
    r"\phi": " phi ",
    r"\varphi": " phi ",
    r"\Phi": " Phi ",
    r"\psi": " psi ",
    r"\Psi": " Psi ",
    r"\rho": " rho ",
    r"\eta": " eta ",
    r"\kappa": " kappa ",
    r"\chi": " chi ",
    r"\xi": " xi ",
    r"\zeta": " zeta ",
    r"\Omega": " Omega ",
    r"\Sigma": " Sigma ",
    r"\Lambda": " Lambda ",
    r"\Theta": " Theta ",
}

_UNIT_SPOKEN: dict[str, str] = {
    "ms": "milliseconds",
    "s": "seconds",
    "Hz": "Hertz",
    "kHz": "kilohertz",
    "MHz": "megahertz",
    "GHz": "gigahertz",
    "dB": "decibels",
    "nm": "nanometres",
    "km": "kilometres",
    "kg": "kilograms",
    "Re": "the real part of",
}


def _expand_escaped_dollar(m: re.Match[str]) -> str:
    raw = m.group(1).replace(",", "")
    if raw.startswith("0.") and len(raw) == 4:
        cents = int(round(float(raw) * 100))
        return f" {cents} cents "
    return f" {m.group(1)} dollars "


def _spoken_math_inner(expr: str) -> str:
    s = str(expr or "").strip()
    if not s:
        return ""
    s = re.sub(r"\\(?:left|right)\b", "", s)
    s = re.sub(r"\\mathbb\s*\{([^{}]+)\}", r"\1", s)
    s = re.sub(
        r"\\text\s*\{([^}]*)\}",
        lambda m: " " + _UNIT_SPOKEN.get(m.group(1).strip(), m.group(1).strip()) + " ",
        s,
    )
    s = re.sub(r"\\\$(\d+(?:,\d{3})*(?:\.\d+)?)", _expand_escaped_dollar, s)
    s = re.sub(r"(?:dollars|cents)\s*/\s*(night|day|month|year|hour)\b", lambda m: m.group(0).split("/")[0].strip() + " per " + m.group(1), s)
    s = re.sub(r"\\log_2\b", " log base 2 of ", s)
    s = re.sub(r"\\ln\b", " natural log of ", s)
    for macro, spoken in _LATEX_GREEK_SPOKEN.items():
        s = s.replace(macro, spoken)
    s = re.sub(r"\^\s*\{\\circ\}|\^\s*\\circ|°", " degrees ", s)
    s = re.sub(r"\^\s*\{\(1/2\)\}|\^\s*\(1/2\)", " to the one half ", s)
    s = re.sub(r"\^\s*\{-5/3\}|\^\s*-5/3", " to the minus 5 over 3 ", s)
    s = re.sub(r"\^\s*\{2/3\}|\^\s*2/3", " to the 2 over 3 ", s)
    s = re.sub(r"\^\s*\{2\}|\^\s*2\b", " squared ", s)
    s = re.sub(r"\^\s*\{3\}|\^\s*3\b", " cubed ", s)
    s = re.sub(r"\^\s*\{-1\}|\^\s*-1\b", " inverse ", s)
    s = re.sub(r"\^\s*\{([^{}]+)\}", r" to the \1 ", s)
    s = re.sub(r"\^\s*([A-Za-z0-9+\-]+)", r" to the \1 ", s)
    s = re.sub(r"_\s*\{([^{}]+)\}", r" \1 ", s)
    s = re.sub(r"_\s*([A-Za-z0-9]+)", r" \1 ", s)
    s = re.sub(r"\\frac\s*\{1\}\s*\{2\}", " one half ", s)
    s = re.sub(r"\\frac\s*\{1\}\s*\{3\}", " one third ", s)
    s = re.sub(r"\\frac\s*\{1\}\s*\{4\}", " one quarter ", s)
    for _ in range(2):
        s = re.sub(r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}", r" \1 over \2 ", s)
        s = re.sub(r"\\sqrt\s*\{([^{}]+)\}", r" the square root of \1 ", s)
    s = re.sub(r"\\exp\s*\(([^()]+)\)", r" e to the \1 ", s)
    s = s.replace(r"\infty", " infinity ")
    s = s.replace(r"\times", " times ")
    s = s.replace(r"\cdot", " dot ")
    s = s.replace(r"\leftrightarrow", " corresponds to ")
    s = s.replace(r"\rightarrow", " approaches ")
    s = s.replace(r"\to", " approaches ")
    s = s.replace(r"\geq", " is greater than or equal to ")
    s = s.replace(r"\ge", " is greater than or equal to ")
    s = s.replace(r"\leq", " is less than or equal to ")
    s = s.replace(r"\le", " is less than or equal to ")
    s = s.replace(r"\neg", " not ")
    s = s.replace(r"\lor", " or ")
    s = s.replace(r"\land", " and ")
    s = s.replace(r"\forall", " for all ")
    s = s.replace(r"\exists", " there exists ")
    s = s.replace(r"\neq", " is not equal to ")
    s = s.replace(r"\ne", " is not equal to ")
    s = s.replace(r"\approx", " is approximately ")
    s = s.replace(r"\propto", " is proportional to ")
    s = s.replace(r"\sim", " approximately ")
    s = s.replace(r"\in", " in ")
    s = s.replace(r"\dots", " and so on ")
    s = s.replace(r"\ldots", " and so on ")
    s = s.replace(r"\cdots", " and so on ")
    s = s.replace(r"\pm", " plus or minus ")
    s = s.replace(r"\partial", " partial ")
    s = s.replace(r"\nabla", " del ")
    s = s.replace(r"\int", " the integral of ")
    s = s.replace(r"\sum", " the sum of ")
    s = s.replace(r"\%", " percent ")
    for uni_sym, uni_spoken in (
        ("μ", " mu "),
        ("π", " pi "),
        ("θ", " theta "),
        ("ω", " omega "),
        ("λ", " lambda "),
        ("σ", " sigma "),
        ("Δ", " delta "),
        ("∞", " infinity "),
        ("≈", " is approximately "),
        ("≠", " is not equal to "),
        ("≤", " is less than or equal to "),
        ("≥", " is greater than or equal to "),
        ("×", " times "),
        ("∝", " is proportional to "),
        ("²", " squared "),
        ("³", " cubed "),
        ("⁻¹", " inverse "),
    ):
        s = s.replace(uni_sym, uni_spoken)
    s = re.sub(r"^\s*<\s*(?=\d)", "under ", s)
    s = re.sub(r"^\s*<\s*", "less than ", s)
    s = re.sub(r"^\s*>\s*", "greater than ", s)
    s = re.sub(r"\s*<\s*", " is less than ", s)
    s = re.sub(r"\s*>\s*", " is greater than ", s)
    s = re.sub(r"\s*=\s*", " equals ", s)
    s = re.sub(r"\s*\+\s*", " plus ", s)
    s = re.sub(r"(?:^|(?<=\s))-\s*(?=[A-Za-z0-9])", "minus ", s)
    s = re.sub(r"\s+-\s+", " minus ", s)
    s = re.sub(r"\bd\s+([A-Za-z]+)\s*/\s*d\s*([A-Za-z]+)\b", r"d \1 by d \2", s)
    s = re.sub(r"\b([A-Za-z0-9]+)\s*/\s*([A-Za-z0-9]+)\b", r"\1 over \2", s)
    s = re.sub(r"\b(\d+)\s*:\s*(\d+)\b", r"\1 to \2", s)
    s = re.sub(r"[\\{}]", " ", s)
    return " ".join(s.split())


def _humanize_inline_code(m: re.Match[str]) -> str:
    code = m.group(1).strip()
    if code.upper().startswith("# NEXT"):
        return "Next:"
    if code == "personas/*.md":
        return "personas markdown files"
    if code == "wiki/*.md":
        return "wiki markdown files"
    code = re.sub(r"^#+\s*", "", code)
    code = code.replace("_", " ")
    code = re.sub(r"\.py\b", " dot py", code)
    code = re.sub(r"\.json\b", " dot JSON", code)
    code = re.sub(r"\.md\b", " dot M D", code)
    code = re.sub(r"\.js\b", " dot J S", code)
    return code


def _humanize_english_tts_text(s: str) -> str:
    s = str(s or "")
    if not s:
        return ""
    s = re.sub(r"`([^`]+)`", _humanize_inline_code, s)
    s = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), s)
    s = re.sub(r"\\\$(\d+(?:,\d{3})*(?:\.\d+)?)", _expand_escaped_dollar, s)
    s = re.sub(r"\$1,000,000\b", "1 million dollar", s)
    s = re.sub(
        r"\$0\.(\d\d)(?=\s|[.,;!?)]|$)(?![^$\n]*[\\^_{}=<>/:])",
        lambda m: f"{int(m.group(1))} cents",
        s,
    )
    s = re.sub(
        r"\$(\d+(?:,\d{3})*(?:\.\d+)?)(?=\s|[.,;!?)]|$)(?![^$\n]*[\\^_{}=<>/:])",
        r"\1 dollars",
        s,
    )
    s = re.sub(r"\$([^$\n]+)\$", lambda m: " " + _spoken_math_inner(m.group(1)) + " ", s)
    s = re.sub(r"\bAm\s*->\s*G\b", "A minor to G", s)
    s = re.sub(r"\b([A-G])-major\b", r"\1 major", s)
    s = re.sub(r"\b([A-G])-minor\b", r"\1 minor", s)
    s = re.sub(r"\b([A-G])-add9\b", r"\1 add 9", s)
    s = re.sub(r"\b([A-G])-sus4\b", r"\1 sus 4", s)
    s = re.sub(r"\s*(?:<->|↔)\s*", " and ", s)
    s = re.sub(r"\s*(?:->|→|=>|⇒)\s*", ", to ", s)
    s = re.sub(r"\bL2/L3\b", "L 2 and L 3", s)
    s = re.sub(r"\b1/f\b", "1 over f", s)
    s = re.sub(r"\bw/o\b", "without", s)
    s = re.sub(r"\be\.g\.,?\s*", "for example, ", s)
    s = re.sub(r"\bi\.e\.,?\s*", "that is, ", s)
    s = re.sub(r"\bvs\.\s*", "versus ", s)
    return " ".join(s.split())


def _clean_tts_text(s: str) -> str:
    s = re.sub(r"[\U00010000-\U0010ffff\u2600-\u27bf\ufe0f]", " ", str(s or ""))
    s = re.sub(r"[•*#_`~↗\[\]]+", " ", s)
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
        title_txt = _clean_tts_text(_humanize_english_tts_text(r.get("title_bn", "")))
        sec_blocks: list[str] = []
        for sec in r.get("sections", []):
            h = _clean_tts_text(_humanize_english_tts_text(sec.get("heading_bn", "")))
            b = _clean_tts_text(_humanize_english_tts_text(sec.get("body_bn", "")))
            if h and b:
                sec_blocks.append(f"{h}. {b}")
            elif b:
                sec_blocks.append(b)
        cur_q = _clean_tts_text(_humanize_english_tts_text(r.get("curiosity_q_bn", "")))
        cur_a = _clean_tts_text(_humanize_english_tts_text(r.get("curiosity_a_bn", "")))
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


def _extract_mp3_acoustic_meta(mp3_path: Path) -> dict:
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp3_path), "-af", "silencedetect=n=-32dB:d=0.12", "-f", "null", "-"],
        capture_output=True, text=True, check=False, timeout=20,
    )
    out = (proc.stderr or "") + "\n" + (proc.stdout or "")
    dur = 0.0
    m_dur = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", out)
    if m_dur:
        dur = round(int(m_dur.group(1)) * 3600 + int(m_dur.group(2)) * 60 + float(m_dur.group(3)), 2)
    silences: list[list[float]] = []
    cur_start: float | None = None
    for line in out.splitlines():
        ms = re.search(r"silence_start:\s*(-?\d+(?:\.\d+)?)", line)
        if ms:
            cur_start = max(0.0, round(float(ms.group(1)), 3))
            continue
        me = re.search(r"silence_end:\s*(\d+(?:\.\d+)?)", line)
        if me and cur_start is not None:
            end_v = round(float(me.group(1)), 3)
            if end_v > cur_start:
                if silences and cur_start - silences[-1][1] <= 0.045:
                    silences[-1][1] = max(silences[-1][1], end_v)
                else:
                    silences.append([cur_start, end_v])
            cur_start = None
    return {"dur": dur, "silences": silences}


def save_manifest(
    hashes: dict[str, str],
    persona_id: str = DEFAULT_PERSONA_ID,
    updated_rels: list[str] | None = None,
    updated_story_cuts: dict[str, float] | None = None,
) -> None:
    pid = normalize_persona_id(persona_id)
    mpath = get_manifest_path(pid)
    aud_root = get_audio_root(pid)
    mpath.parent.mkdir(parents=True, exist_ok=True)
    extra_keys: dict = {}
    if mpath.is_file():
        try:
            old_data = json.loads(mpath.read_text(encoding="utf-8"))
            if isinstance(old_data, dict):
                extra_keys = {k: v for k, v in old_data.items() if k not in ("voice_model", "persona_id", "total_tracked", "hashes")}
        except Exception:
            pass
    if updated_story_cuts and pid == "kalyani":
        story_cuts = dict(extra_keys.get("story_cuts") or {})
        story_cuts.update(updated_story_cuts)
        extra_keys["story_cuts"] = dict(sorted(story_cuts.items()))
    if updated_rels and pid in ("zorba", "jhalak", "anondo"):
        timings = dict(extra_keys.get("audio_timings") or {})
        valid_rels = [rel for rel in updated_rels if (aud_root / rel).is_file()]
        with ThreadPoolExecutor(max_workers=min(16, max(1, len(valid_rels)))) as ex:
            for rel, meta in zip(valid_rels, ex.map(lambda r: _extract_mp3_acoustic_meta(aud_root / r), valid_rels)):
                t_key = rel.replace("reels/", "").replace(".mp3", "") if pid in ("zorba", "jhalak") else rel
                timings[t_key] = meta
        if pid in ("zorba", "jhalak"):
            valid_t_keys = {rel.replace("reels/", "").replace(".mp3", "") for rel in hashes}
            timings = {k: v for k, v in timings.items() if k in valid_t_keys}
        else:
            timings = {k: v for k, v in timings.items() if k in hashes}
        extra_keys["audio_timings"] = timings
    voice_label = "en-gb-gia-server-voicelm-xl#kix08 (Expressive Warm Caring UK Female)" if pid in ("zorba", "anondo") else "gemini-v4s-tts (Aoede)"
    payload = {
        "voice_model": voice_label,
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


_SPEECH_PROTO_PATH = Path("/tmp/aicomp_speech_lucid_prompt.proto")
_SPEECH_PROTO_TEXT = """syntax = "proto2";
package speech;

message VoiceSelection {
  optional string canonical_voice_name = 2;
  optional string voice_alias = 3;
}

message SoundStreamTokens {
  repeated float tokens = 1 [packed = true];
}

message Prompt {
  optional SoundStreamTokens speaker_prompt_tokens = 5;
}

message Annotation {
  optional VoiceSelection voice_selection = 7;
  optional Prompt prompt = 9;
}

message LucidPiece {
  optional int32 own_index = 1;
  optional string input_text = 2;
}

message LucidUtterance {
  repeated LucidPiece pieces = 1;
  optional Annotation annotation = 2;
  optional bool attempt_sentence_splitting = 4;
}

message LucidMarkup {
  message Content {
    optional int32 own_index = 1;
    optional LucidUtterance utterance = 2;
  }
  repeated Content contents = 1;
  optional Annotation annotation = 2;
}

message Text {
  optional LucidMarkup lucid = 2;
  extensions 128 to max;
}

message TtsServiceRequestParams {
  extend Text {
    optional TtsServiceRequestParams tts_service_request_params = 131098250;
  }
  optional string voice_language = 1;
  optional string voice_name = 2;
  optional int32 voice_sample_rate = 3;
  optional string voice_gender = 8;
  optional bool lucid_voice_selection_ran = 14;
}

message PattsRequest {
  optional Text tts_markup = 4;
}

message SynthesisEngineSpecificRequest {
  extensions 1000 to max;
}

extend SynthesisEngineSpecificRequest {
  optional PattsRequest patts_request = 26855169;
}

message Voice {
  required string language = 1;
  optional string gender = 2;
  optional string name = 3;
  optional int32 sample_rate = 4;
}

message AudioEncoding {
  enum Encoding {
    ANY = 0;
    LINEAR_16BIT = 1;
    MP3 = 4;
    MP3_64KBPS = 10;
  }
}

message SpeechSynthesizerRequest {
  required string ssml = 1;
  optional Voice voice = 2;
  optional AudioEncoding.Encoding encoding = 3;
  optional SynthesisEngineSpecificRequest engine_specific = 5;
  optional bool enable_timepoints = 8;
  optional int32 timepoint_level = 12;
}

message SpeechSynthesizerEvent {
  optional int32 type = 1;
  optional bytes audio = 2;
}

message SpeechSynthesizerResponse {
  optional string info = 1;
}

message SpeechSynthesizerSynthesizeMixedResult {
  optional SpeechSynthesizerEvent stream_message = 1;
  optional SpeechSynthesizerResponse result_message = 2;
}

service SpeechSynthesizer {
  rpc Synthesize(SpeechSynthesizerRequest) returns (stream SpeechSynthesizerSynthesizeMixedResult);
}
"""

_UK_FEMALE_VOICES = (
    "en-gb-gia-server-voicelm-xl#kix08",
    "en-gb-gia-server-voicelm-xl#kix04",
)
_UK_WARM_PROMPT_PATH = Path(__file__).resolve().parent / "uk_warm_female_prompt.json"
_CACHED_UK_TOKENS_STR: str | None = None


def _get_uk_warm_tokens_str() -> str:
    global _CACHED_UK_TOKENS_STR
    if _CACHED_UK_TOKENS_STR is None:
        data = json.loads(_UK_WARM_PROMPT_PATH.read_text(encoding="utf-8"))
        _CACHED_UK_TOKENS_STR = ", ".join(f"{float(t):.6f}" for t in data["tokens"])
    return _CACHED_UK_TOKENS_STR


def _prepare_expressive_uk_text(text: str) -> str:
    s = _humanize_english_tts_text(text or "")
    s = re.sub(r"₹\s*(\d+(?:\.\d+)?)\s*Cr\+", r"\1 Crore", s)
    s = re.sub(r"₹\s*(\d+(?:\.\d+)?)\s*Cr\b", r"\1 Crore", s)
    s = re.sub(r"₹\s*(\d+(?:\.\d+)?)\s*L\+", r"\1 Lakh", s)
    s = re.sub(r"₹\s*(\d+(?:\.\d+)?)\s*L\b", r"\1 Lakh", s)
    s = re.sub(r"₹\s*(\d[\d,]*)", r"\1 Rupees", s)
    s = re.sub(r"\b(19\d\d|20\d\d)\s*[–—-]\s*(19\d\d|20\d\d)\b", r"\1 to \2", s)
    s = re.sub(r"\b(\d+)\s*[–—-]\s*(\d+)\b", r"\1 to \2", s)
    s = re.sub(r"\b(\d+)-(Second|Minute|Hour|Day|Slot|Year-Old)\b", lambda m: f"{m.group(1)} {m.group(2).lower().replace('-', ' ')}", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*[—–]\s*", ", ", s)
    s = re.sub(r"\bDidi\b", "Deedee", s)
    s = re.sub(r"\bKORTEX\b", "Kortex", s)
    s = re.sub(r"\bANANDO\b", "Anondo", s)
    s = re.sub(r"\bZORBA\b", "Zorba", s)
    s = re.sub(r"\bSWE\b", "Software Engineer", s)
    s = re.sub(r"&", " and ", s)
    return re.sub(r"\s+", " ", s).strip()


def _split_into_expressive_clauses(text: str, max_chars: int = 300) -> list[str]:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?।])\s+", text) if s.strip()]
    merged: list[str] = []
    i = 0
    while i < len(sentences):
        if len(sentences[i]) < 55 and i + 1 < len(sentences):
            merged.append(sentences[i] + " " + sentences[i + 1])
            i += 2
        else:
            merged.append(sentences[i])
            i += 1
    chunks: list[str] = []
    cur: list[str] = []
    cur_len = 0
    for sent in merged:
        if len(sent) > max_chars:
            parts = re.split(r"(?<=[,:;—–])\s+", sent)
            sub_cur: list[str] = []
            sub_len = 0
            for p in parts:
                if sub_cur and sub_len + 1 + len(p) > max_chars:
                    if cur:
                        chunks.append(" ".join(cur))
                        cur, cur_len = [], 0
                    chunks.append(" ".join(sub_cur))
                    sub_cur = [p]
                    sub_len = len(p)
                else:
                    sub_cur.append(p)
                    sub_len += (1 + len(p) if sub_len else len(p))
            if sub_cur:
                sent = " ".join(sub_cur)
            else:
                continue
        if cur and (cur_len + 1 + len(sent) > max_chars):
            chunks.append(" ".join(cur))
            cur = [sent]
            cur_len = len(sent)
        else:
            cur.append(sent)
            cur_len += (1 + len(sent) if cur_len else len(sent))
    if cur:
        chunks.append(" ".join(cur))
    return chunks


def _synthesize_bn_voicelm_aoede(text: str, out_raw: Path, timeout_s: int = 45) -> bool:
    cleaned = _clean_tts_text(text or "")
    if not cleaned:
        return False
    if not _SPEECH_PROTO_PATH.is_file() or _SPEECH_PROTO_PATH.stat().st_size < 200:
        _SPEECH_PROTO_PATH.write_text(_SPEECH_PROTO_TEXT, encoding="utf-8")
    clauses = _split_into_expressive_clauses(cleaned, max_chars=280)
    if not clauses:
        return False
    tokens_str = _get_uk_warm_tokens_str()
    contents_pb = "".join(
        f" contents {{ own_index: {idx} utterance {{ pieces {{ own_index: 0 input_text: {json.dumps(clause, ensure_ascii=False)} }} attempt_sentence_splitting: false }} }}"
        for idx, clause in enumerate(clauses)
    )
    req_file = Path(f"/tmp/aicomp_bn_req_{os.getpid()}_{out_raw.stem}.txtpb")
    try:
        for with_prompt in (True, False):
            annot_pb = f"annotation {{ prompt {{ speaker_prompt_tokens {{ tokens: [{tokens_str}] }} }} }} " if with_prompt else ""
            req_proto = (
                'ssml: "placeholder" '
                'voice { language: "bn-IN" gender: "FEMALE" sample_rate: 24000 } '
                "encoding: MP3_64KBPS "
                "engine_specific { [speech.patts_request] { tts_markup { "
                f"lucid {{ {annot_pb}{contents_pb} }} "
                "[speech.TtsServiceRequestParams.tts_service_request_params] { "
                'voice_language: "bn-IN" voice_gender: "FEMALE" voice_sample_rate: 24000 '
                "} } } }\n"
            )
            req_file.write_text(req_proto, encoding="utf-8")
            proc = subprocess.run(
                [
                    "stubby", "call", "--proto2", "--noremotedb", "--ignore_serverstatus",
                    f"--protofiles={_SPEECH_PROTO_PATH}",
                    f"--infile={req_file}",
                    "--output_json",
                    "blade:speech-tts-synthesizer-speech-synthesizer-prod",
                    "speech.SpeechSynthesizer.Synthesize",
                ],
                capture_output=True, text=True, timeout=timeout_s, check=False,
            )
            if proc.returncode == 0 and proc.stdout:
                mp3_bytes = b"".join(
                    base64.b64decode(m.group(1))
                    for m in re.finditer(r'"audio"\s*:\s*"([^"]+)"', proc.stdout)
                )
                if len(mp3_bytes) > 1000:
                    out_raw.write_bytes(mp3_bytes)
                    return True
    except Exception:
        pass
    finally:
        req_file.unlink(missing_ok=True)
    return False


def _synthesize_voicelm_aoede(text: str, out_raw: Path, timeout_s: int = 45) -> bool:
    cleaned = _prepare_expressive_uk_text(text)
    if not cleaned:
        return False
    if not _SPEECH_PROTO_PATH.is_file() or _SPEECH_PROTO_PATH.stat().st_size < 200:
        _SPEECH_PROTO_PATH.write_text(_SPEECH_PROTO_TEXT, encoding="utf-8")
    clauses = _split_into_expressive_clauses(cleaned, max_chars=300)
    if not clauses:
        return False
    tokens_str = _get_uk_warm_tokens_str()
    contents_pb = "".join(
        f" contents {{ own_index: {idx} utterance {{ pieces {{ own_index: 0 input_text: {json.dumps(clause)} }} attempt_sentence_splitting: false }} }}"
        for idx, clause in enumerate(clauses)
    )
    req_file = Path(f"/tmp/aicomp_req_{os.getpid()}_{out_raw.stem}.txtpb")
    try:
        for voice_name in _UK_FEMALE_VOICES:
            req_proto = (
                'ssml: "placeholder" '
                f'voice {{ language: "en-GB" name: "{voice_name}" sample_rate: 24000 }} '
                "encoding: MP3_64KBPS "
                "engine_specific { [speech.patts_request] { tts_markup { "
                "lucid { annotation { "
                f'voice_selection {{ canonical_voice_name: "{voice_name}" }} '
                f"prompt {{ speaker_prompt_tokens {{ tokens: [{tokens_str}] }} }} "
                f"}} {contents_pb} }} "
                "[speech.TtsServiceRequestParams.tts_service_request_params] { "
                f'voice_language: "en-GB" voice_name: "{voice_name}" voice_sample_rate: 24000 lucid_voice_selection_ran: true '
                "} } } }\n"
            )
            req_file.write_text(req_proto, encoding="utf-8")
            proc = subprocess.run(
                [
                    "stubby", "call", "--proto2", "--noremotedb", "--ignore_serverstatus",
                    f"--protofiles={_SPEECH_PROTO_PATH}",
                    f"--infile={req_file}",
                    "--output_json",
                    "blade:speech-tts-synthesizer-speech-synthesizer-prod",
                    "speech.SpeechSynthesizer.Synthesize",
                ],
                capture_output=True, text=True, timeout=timeout_s, check=False,
            )
            if proc.returncode == 0 and proc.stdout:
                mp3_bytes = b"".join(
                    base64.b64decode(m.group(1))
                    for m in re.finditer(r'"audio"\s*:\s*"([^"]+)"', proc.stdout)
                )
                if len(mp3_bytes) > 1000:
                    out_raw.write_bytes(mp3_bytes)
                    return True
    except Exception:
        pass
    finally:
        req_file.unlink(missing_ok=True)
    return False


def _synthesize_wav(text: str, out_wav: Path, model_name: str, timeout_s: int = 75) -> bool:
    if any(tag in out_wav.name for tag in ("_anondo_", "_zorba_")):
        return _synthesize_voicelm_aoede(text, out_wav, timeout_s=min(60, timeout_s))
    if any(tag in out_wav.name for tag in ("_kalyani_", "_jhalak_")):
        if _synthesize_bn_voicelm_aoede(text, out_wav, timeout_s=min(60, timeout_s)):
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
    is_voicelm_mp3 = bool(wav_paths) and any(tag in wav_paths[0].name for tag in ("_anondo_", "_zorba_", "_jhalak_"))
    if len(wav_paths) == 1 and is_voicelm_mp3:
        cmd = [
            "ffmpeg", "-y", "-i", str(wav_paths[0]),
            "-ar", "24000", "-ac", "1", "-b:a", "64k",
            str(out_mp3),
        ]
    elif len(wav_paths) == 1:
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


def build_one(rel_path: str, info: dict[str, str], aud_root: Path) -> tuple[str, bool, float | None]:
    out_mp3 = aud_root / rel_path
    safe_tag = f"{aud_root.name}_" + rel_path.replace("/", "_").replace(".mp3", "")
    w_full = Path(f"/tmp/aicomp_full_{os.getpid()}_{safe_tag}.wav")
    w1 = Path(f"/tmp/aicomp_p1_{os.getpid()}_{safe_tag}.wav")
    w2 = Path(f"/tmp/aicomp_p2_{os.getpid()}_{safe_tag}.wav")

    for attempt, model_name in enumerate((TTS_MODELS[0], TTS_MODELS[0], TTS_MODELS[1])):
        try:
            if aud_root.name == "kalyani" and info.get("scope") == "games" and info.get("part2"):
                if _synthesize_wav(info["part1"], w1, model_name, timeout_s=70) and _synthesize_wav(info["part2"], w2, model_name, timeout_s=70):
                    w1_dur = _extract_mp3_acoustic_meta(w1).get("dur", 0.0)
                    if _wav_to_mp3([w1, w2], out_mp3):
                        return rel_path, True, round(w1_dur, 2) if w1_dur > 4.0 else None
            if aud_root.name not in ("anondo", "zorba", "jhalak") and len(info["text"]) > 1350 and info["part2"]:
                if _synthesize_wav(info["part1"], w1, model_name, timeout_s=70) and _synthesize_wav(info["part2"], w2, model_name, timeout_s=70):
                    if _wav_to_mp3([w1, w2], out_mp3):
                        return rel_path, True, None
            if _synthesize_wav(info["text"], w_full, model_name, timeout_s=85):
                if _wav_to_mp3([w_full], out_mp3):
                    return rel_path, True, None

            if info["part2"]:
                if _synthesize_wav(info["part1"], w1, model_name, timeout_s=70) and _synthesize_wav(info["part2"], w2, model_name, timeout_s=70):
                    w1_dur = _extract_mp3_acoustic_meta(w1).get("dur", 0.0) if aud_root.name == "kalyani" else 0.0
                    if _wav_to_mp3([w1, w2], out_mp3):
                        return rel_path, True, round(w1_dur, 2) if w1_dur > 4.0 else None
        finally:
            w_full.unlink(missing_ok=True)
            w1.unlink(missing_ok=True)
            w2.unlink(missing_ok=True)
        time.sleep(0.5 * (attempt + 1))

    return rel_path, False, None


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
    updated_ok: list[str] = []
    updated_cuts: dict[str, float] = {}
    failed: list[str] = []

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futs = {ex.submit(build_one, rel_path, expected[rel_path], aud_root): rel_path for rel_path in targets}
        for i, fut in enumerate(as_completed(futs), 1):
            rel_path, ok, cut_sec = fut.result()
            if ok:
                ok_count += 1
                updated_ok.append(rel_path)
                recorded[rel_path] = expected[rel_path]["hash"]
                if cut_sec is not None:
                    updated_cuts[rel_path] = cut_sec
            else:
                failed.append(rel_path)
            if i % 15 == 0 or i == len(targets):
                save_manifest(recorded, pid, updated_story_cuts=updated_cuts)
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

    save_manifest(recorded, pid, updated_rels=updated_ok, updated_story_cuts=updated_cuts)
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
