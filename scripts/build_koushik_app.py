#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Modular Jinja2 + Markdown Static Compiler for ⚡ ANANDO (`koushik.html`).

Assembles:
  - Markdown-backed 21-day English curriculum (`content/days/koushik_days.md` via `content/koushik_days.py`)
  - Personalized slide illustrations (`assets/koushik_slides/k_slide_1..8.jpg`)
  - Jinja2 HTML5 shell (`src/templates/koushik.html.j2`)
Into:
  - `koushik.html` (Single canonical CDN-backed mobile/desktop entrypoint)

CRITICAL GOVERNANCE RULE (defined in GEMINI.md):
  - Runs in <0.5s and NEVER invokes TTS voice generation.
  - Verifies the Agentic LLM Curation Gate (`curation_manifest_koushik.json`) and performs a non-blocking
    SHA-256 manifest check (`audio/koushik/tts_manifest.json`).
"""

from __future__ import annotations

import base64
import json
from pathlib import Path
import sys

import jinja2

APP_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_ROOT))
sys.path.insert(0, str(APP_ROOT / "scripts"))

from content import KOUSHIK_DAYS_21, KOUSHIK_PILLARS, KOUSHIK_QUOTES, KOUSHIK_SLIDES  # noqa: E402
from curate_loop import run_quality_gate  # noqa: E402
from refresh_voices import get_stale_or_missing_files  # noqa: E402

SLIDE_IMG_DIR = APP_ROOT / "assets" / "koushik_slides"
TEMPLATES_DIR = APP_ROOT / "src" / "templates"
GH_RAW_BASE = "https://raw.githubusercontent.com/kouSeek/portfolio/ma-audio/audio/koushik/"


def b64_uri(path: Path, mime: str) -> str:
    if not path.is_file():
        return ""
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def assemble_anando_payloads(url_prefix: str = GH_RAW_BASE) -> tuple[dict, list[dict]]:
    slides_payload = []
    for s in KOUSHIK_SLIDES:
        sid = int(s["id"])
        img_path = SLIDE_IMG_DIR / f"k_slide_{sid}.jpg"
        slides_payload.append({
            **s,
            "img_b64": b64_uri(img_path, "image/jpeg"),
            "audio_url": f"{url_prefix}slides/en_slide_{sid}.mp3",
        })

    quotes_payload = [
        {
            "text": q_txt,
            "audio_url": f"{url_prefix}quotes/en_quote_{q_idx}.mp3",
        }
        for q_idx, q_txt in enumerate(KOUSHIK_QUOTES)
    ]

    pillars_payload = [
        {
            **p_obj,
            "audio_url": f"{url_prefix}pillars/en_pillar_{p_idx}.mp3",
        }
        for p_idx, p_obj in enumerate(KOUSHIK_PILLARS)
    ]

    days_payload = []
    for d in KOUSHIK_DAYS_21:
        day_num = int(d["day"])
        games_enriched = []
        for idx, ag in enumerate(d["agendas"]):
            games_enriched.append({
                "pillar": ag.get("pillar", ""),
                "short": ag["short_bn"],
                "category": ag["category"],
                "title": ag["title_bn"],
                "detail": ag["detail_bn"],
                "prompt": ag["prompt_bn"],
                "followup_prompt": ag.get("followup_prompt_bn", ""),
                "audio_url": f"{url_prefix}games/en_day_{day_num}_ag_{idx}.mp3",
            })

        days_payload.append({
            "day": day_num,
            "phase": d.get("phase", "House-Money Era"),
            "title": d["title_bn"],
            "sub": d.get("summary_bn", ""),
            "audio_url": f"{url_prefix}days/en_day_{day_num}.mp3",
            "games": games_enriched,
        })

    anando_data = {
        "slides": slides_payload,
        "quotes": quotes_payload,
        "days": days_payload,
    }
    return anando_data, pillars_payload


def build_koushik_html() -> None:
    passed, issues, dim_scores = run_quality_gate(verbose=False, student_id="koushik")
    if not passed:
        raise RuntimeError(f"Agentic LLM Content Quality Gate failed for koushik: {issues}")
    print(f"[Agentic Quality Gate (koushik)] PASSED all {len(dim_scores)}/12 dimensions.")

    anando_data, pillars_payload = assemble_anando_payloads(url_prefix=GH_RAW_BASE)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
        keep_trailing_newline=True,
    )
    template = env.get_template("koushik.html.j2")
    rendered_html = template.render(
        anando_data_json=json.dumps(anando_data, ensure_ascii=False),
        pillars_data_json=json.dumps(pillars_payload, ensure_ascii=False),
    )

    out_path = APP_ROOT / "koushik.html"
    out_path.write_text(rendered_html, encoding="utf-8")
    print(f"Built {out_path.name} via Jinja2 ({out_path.stat().st_size:,} bytes)")

    stale, expected, _ = get_stale_or_missing_files(scope="all", student_id="koushik")
    if not stale:
        print(f"[TTS Check (koushik)] All {len(expected)} Aoede MP3 files are 100% in sync.")
    else:
        print(f"[TTS Notice (koushik)] {len(stale)}/{len(expected)} audio file(s) pending voice refresh: {stale[:8]}")
        print(
            "[TTS Rule] Skipping automatic TTS regeneration (per GEMINI.md). "
            "Ask Koushik before running: python3 scripts/refresh_voices.py --student koushik --confirm --publish"
        )


if __name__ == "__main__":
    build_koushik_html()
