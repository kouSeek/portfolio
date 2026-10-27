#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Modular Static Compiler for 🌸 কল্যাণী (Kalyani App).

Assembles:
  - Declarative curriculum & content (`content/`)
  - Artisanal CSS design-token layers (`src/styles/{tokens,layout,components}.css`)
  - Modular JS application controllers (`src/js/{state,audio,plan-view,letter-view,boot}.js`)
  - Semantic HTML5 shell (`src/template.html`)
Into:
  1. `ma-presentation.html` & `index.html` (CDN-backed lightweight mobile PWA entrypoints)
  2. Standalone Google Drive / Artifact HTML bundle (with embedded offline fallback audio)

CRITICAL GOVERNANCE RULE (defined in GEMINI.md):
- Runs in <0.5s and NEVER invokes TTS voice generation.
- Performs a non-blocking SHA-256 manifest check (`audio/tts_manifest.json`) and reports any stale audio clips.
"""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path
import shutil
import sys

APP_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_ROOT))
sys.path.insert(0, str(APP_ROOT / "scripts"))

from content import DAYS_21, DAYS_PART2_30, GAME_META, LETTER_VIDEO_URL, MORNING_QUOTES, SLIDES  # noqa: E402
from refresh_voices import get_stale_or_missing_files  # noqa: E402

AUDIO_DIR = APP_ROOT / "audio"
SLIDES_IMG_DIR = APP_ROOT / "assets" / "slides"
SRC_DIR = APP_ROOT / "src"
GH_RAW_BASE = "https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-app-v0/"

CSS_MODULES = (
    SRC_DIR / "styles" / "tokens.css",
    SRC_DIR / "styles" / "layout.css",
    SRC_DIR / "styles" / "components.css",
)

JS_MODULES = (
    SRC_DIR / "js" / "state.js",
    SRC_DIR / "js" / "audio.js",
    SRC_DIR / "js" / "plan-view.js",
    SRC_DIR / "js" / "letter-view.js",
    SRC_DIR / "js" / "boot.js",
)


def b64_uri(path: Path, mime: str) -> str:
    if not path.is_file():
        return ""
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def enrich_days(days_list: list[dict], embed_part1_audio: bool, url_prefix: str) -> list[dict]:
    enriched_days: list[dict] = []
    for d in days_list:
        day_num = int(d["day"])
        ref_day = int(d.get("audio_ref_day", day_num))

        day_rel = f"audio/days/day_{day_num}.mp3"
        ref_day_rel = f"audio/days/day_{ref_day}.mp3"
        resolved_day_rel = day_rel if (APP_ROOT / day_rel).is_file() else ref_day_rel

        ags_enriched = []
        for idx, ag in enumerate(d["agendas"]):
            ag_rel = f"audio/games/day_{day_num}_ag_{idx}.mp3"
            ref_ag_rel = f"audio/games/day_{ref_day}_ag_{idx}.mp3"
            resolved_ag_rel = ag_rel if (APP_ROOT / ag_rel).is_file() else ref_ag_rel
            ags_enriched.append({
                **ag,
                "audio_url": url_prefix + resolved_ag_rel,
                "audio_b64": "",
            })

        enriched_days.append({
            **d,
            "agendas": ags_enriched,
            "audio_url": url_prefix + resolved_day_rel,
            "audio_b64": b64_uri(APP_ROOT / resolved_day_rel, "audio/mpeg") if (embed_part1_audio and day_num <= 21) else "",
        })
    return enriched_days


def assemble_data_js(embed_offline_b64: bool, url_prefix: str) -> str:
    slides_payload = []
    for s in SLIDES:
        sid = int(s["id"])
        img_path = SLIDES_IMG_DIR / f"slide_{sid}.jpg"
        aud_rel = f"audio/slides/slide_{sid}.mp3"
        slides_payload.append({
            **s,
            "img_b64": b64_uri(img_path, "image/jpeg"),
            "audio_url": url_prefix + aud_rel,
            "audio_b64": b64_uri(APP_ROOT / aud_rel, "audio/mpeg") if embed_offline_b64 else "",
        })

    quotes_audio = []
    for q_idx in range(len(MORNING_QUOTES)):
        q_rel = f"audio/quotes/quote_{q_idx}.mp3"
        quotes_audio.append({
            "url": url_prefix + q_rel,
            "b64": b64_uri(APP_ROOT / q_rel, "audio/mpeg") if embed_offline_b64 else "",
        })

    day1_ag_map = {}
    if embed_offline_b64:
        for a_idx in range(6):
            ag_rel = f"audio/games/day_1_ag_{a_idx}.mp3"
            day1_ag_map[a_idx] = {
                "url": url_prefix + ag_rel,
                "b64": b64_uri(APP_ROOT / ag_rel, "audio/mpeg"),
            }

    days_p1 = enrich_days(DAYS_21, embed_part1_audio=embed_offline_b64, url_prefix=url_prefix)
    days_p2 = enrich_days(DAYS_PART2_30, embed_part1_audio=False, url_prefix=url_prefix)

    return "\n".join([
        f"const LETTER_VIDEO_URL = {json.dumps(LETTER_VIDEO_URL, ensure_ascii=False)};",
        f"const SLIDES = {json.dumps(slides_payload, ensure_ascii=False)};",
        f"const MORNING_QUOTES = {json.dumps(MORNING_QUOTES, ensure_ascii=False)};",
        f"const GAME_META = {json.dumps(GAME_META, ensure_ascii=False)};",
        f"const DAYS_21 = {json.dumps(days_p1, ensure_ascii=False)};",
        f"const DAYS_PART2_30 = {json.dumps(days_p2, ensure_ascii=False)};",
        f"const QUOTES_AUDIO = {json.dumps(quotes_audio, ensure_ascii=False)};",
        f"const DAY1_AG_MAP = {json.dumps(day1_ag_map, ensure_ascii=False)};",
    ])


def render_bundle(template_html: str, css_bundle: str, js_bundle: str, data_js: str) -> str:
    return (
        template_html
        .replace("/*__INJECT_CSS__*/", css_bundle)
        .replace("/*__INJECT_DATA__*/", data_js)
        .replace("/*__INJECT_JS__*/", js_bundle)
    )


def build_html() -> None:
    # Sync root favicon.svg from canonical assets/icons/favicon.svg
    src_icon = APP_ROOT / "assets" / "icons" / "favicon.svg"
    dst_icon = APP_ROOT / "favicon.svg"
    if src_icon.is_file() and src_icon.read_bytes() != (dst_icon.read_bytes() if dst_icon.is_file() else b""):
        shutil.copyfile(src_icon, dst_icon)

    template_html = (SRC_DIR / "template.html").read_text(encoding="utf-8")
    css_bundle = "\n\n".join(p.read_text(encoding="utf-8").strip() for p in CSS_MODULES)
    js_bundle = "\n\n".join(p.read_text(encoding="utf-8").strip() for p in JS_MODULES)

    # 1. Public CDN-backed Mobile PWA HTML (ma-presentation.html & index.html)
    cdn_data_js = assemble_data_js(embed_offline_b64=False, url_prefix=GH_RAW_BASE)
    cdn_html = render_bundle(template_html, css_bundle, js_bundle, cdn_data_js)

    out_ma = APP_ROOT / "ma-presentation.html"
    out_idx = APP_ROOT / "index.html"
    out_ma.write_text(cdn_html, encoding="utf-8")
    out_idx.write_text(cdn_html, encoding="utf-8")
    print(f"Built {out_ma.name} & {out_idx.name} ({out_ma.stat().st_size:,} bytes)")

    # 2. Non-blocking TTS hash check (NEVER auto-regenerates voices!)
    stale, expected, _ = get_stale_or_missing_files(scope="all")
    if not stale:
        print(f"[TTS Check] All {len(expected)} Aoede MP3 files are 100% in sync with content/.")
    else:
        print(f"[TTS Notice] {len(stale)}/{len(expected)} audio file(s) pending voice refresh: {stale[:8]}")
        print("[TTS Rule] Skipping automatic TTS regeneration (per GEMINI.md). Ask Koushik before running: python3 scripts/refresh_voices.py --confirm")


if __name__ == "__main__":
    build_html()
