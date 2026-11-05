#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unified Modular Jinja2 + Markdown Compiler for AI Companion (`kalyani` + `anondo`).

Compiles:
  1. `kalyani.html` — Ma's 21-day Bengali companion (`personas/kalyani/` + `src/kalyani/`)
  2. `anondo.html`  — Koushik's 21-day English companion (`personas/anondo/` + `src/anondo/`)
  3. `index.html`   — Two-persona AI Companion Hub (`src/templates/index.html.j2`)

CRITICAL GOVERNANCE RULE (defined in GEMINI.md):
  - Runs in <0.5s and NEVER invokes TTS voice generation.
  - Verifies the 12-dimension Agentic LLM Curation Gate and checks `audio/<persona>/tts_manifest.json`.
"""

from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
import shutil
import sys

import jinja2

APP_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_ROOT))
sys.path.insert(0, str(APP_ROOT / "scripts"))

from content import (  # noqa: E402
    ANONDO_DAYS_21, ANONDO_PILLARS, ANONDO_QUOTES, ANONDO_SLIDES,
    DAYS_21, GAME_META, LETTER_VIDEO_URL, MORNING_QUOTES, SLIDES,
)
from curate_loop import run_quality_gate  # noqa: E402
from refresh_voices import get_stale_or_missing_files, load_manifest  # noqa: E402

SRC_DIR = APP_ROOT / "src"
TEMPLATES_DIR = SRC_DIR / "templates"
GH_RAW_AUDIO_BASE = "https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/audio/"

KALYANI_CSS = (
    SRC_DIR / "kalyani" / "styles" / "tokens.css",
    SRC_DIR / "kalyani" / "styles" / "layout.css",
    SRC_DIR / "kalyani" / "styles" / "components.css",
)
KALYANI_JS = (
    SRC_DIR / "kalyani" / "js" / "state.js",
    SRC_DIR / "kalyani" / "js" / "audio.js",
    SRC_DIR / "kalyani" / "js" / "plan-view.js",
    SRC_DIR / "kalyani" / "js" / "letter-view.js",
    SRC_DIR / "kalyani" / "js" / "boot.js",
)
ANONDO_CSS = (SRC_DIR / "anondo" / "styles" / "tokens.css", SRC_DIR / "anondo" / "styles" / "components.css")
ANONDO_JS = (SRC_DIR / "anondo" / "js" / "audio.js", SRC_DIR / "anondo" / "js" / "views.js")
JHALAK_CSS = (SRC_DIR / "jhalak" / "styles" / "jhalak.css",)
JHALAK_JS = (SRC_DIR / "jhalak" / "js" / "feed-engine.js", SRC_DIR / "jhalak" / "js" / "player-ui.js")


def b64_uri(path: Path, mime: str) -> str:
    return ("data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode("ascii")) if path.is_file() else ""


def _enrich_kalyani_days(days_list: list[dict], url_prefix: str) -> list[dict]:
    manifest_hashes = load_manifest("kalyani")
    aud_root = APP_ROOT / "audio" / "kalyani"
    mpath = aud_root / "tts_manifest.json"
    story_cuts = json.loads(mpath.read_text(encoding="utf-8")).get("story_cuts", {}) if mpath.is_file() else {}
    enriched: list[dict] = []
    for d in days_list:
        day_num = int(d["day"])
        ref_day = int(d.get("audio_ref_day", day_num))
        day_rel = f"days/day_{day_num}.mp3"
        has_day = (aud_root / day_rel).is_file() or (day_rel in manifest_hashes)
        resolved_day_rel = day_rel if has_day else f"days/day_{ref_day}.mp3"

        ags_enriched = []
        for idx, ag in enumerate(d["agendas"]):
            ag_rel = f"games/day_{day_num}_ag_{idx}.mp3"
            has_ag = (aud_root / ag_rel).is_file() or (ag_rel in manifest_hashes)
            resolved_ag = ag_rel if has_ag else f"games/day_{ref_day}_ag_{idx}.mp3"
            cut_sec = story_cuts.get(resolved_ag, 0)
            ags_enriched.append({**ag, "audio_url": url_prefix + resolved_ag, "audio_b64": "", "story_end": cut_sec})

        enriched.append({**d, "agendas": ags_enriched, "audio_url": url_prefix + resolved_day_rel, "audio_b64": ""})
    return enriched


def build_kalyani(env: jinja2.Environment) -> None:
    passed, issues, dim_scores = run_quality_gate(verbose=False, persona_id="kalyani")
    if not passed:
        raise RuntimeError(f"Quality Gate failed for kalyani: {issues}")
    print(f"[Agentic Quality Gate (kalyani)] PASSED all {len(dim_scores)}/12 dimensions.")

    url_prefix = GH_RAW_AUDIO_BASE + "kalyani/"
    img_dir = APP_ROOT / "assets" / "kalyani" / "slides"
    sys_md = (APP_ROOT / "personas" / "kalyani" / "client-side-gemini.md").read_text(encoding="utf-8")
    sys_prompt = sys_md.split("```text", 1)[-1].rsplit("```", 1)[0].strip()
    slides_payload = [
        {**s, "img_b64": b64_uri(img_dir / f"slide_{int(s['id'])}.jpg", "image/jpeg"), "audio_url": f"{url_prefix}slides/slide_{int(s['id'])}.mp3", "audio_b64": ""}
        for s in SLIDES
    ]
    quotes_audio = [{"url": f"{url_prefix}quotes/quote_{i}.mp3", "b64": ""} for i in range(len(MORNING_QUOTES))]
    data_js = "\n".join([
        f"const LETTER_VIDEO_URL = {json.dumps(LETTER_VIDEO_URL, ensure_ascii=False)};",
        f"const KALYANI_SYSTEM_PROMPT = {json.dumps(sys_prompt, ensure_ascii=False)};",
        f"const SLIDES = {json.dumps(slides_payload, ensure_ascii=False)};",
        f"const MORNING_QUOTES = {json.dumps(MORNING_QUOTES, ensure_ascii=False)};",
        f"const GAME_META = {json.dumps(GAME_META, ensure_ascii=False)};",
        f"const DAYS_21 = {json.dumps(_enrich_kalyani_days(DAYS_21, url_prefix), ensure_ascii=False)};",
        f"const QUOTES_AUDIO = {json.dumps(quotes_audio, ensure_ascii=False)};",
        "const DAY1_AG_MAP = {};",
    ])
    for fname, tpl, css_list, js_list in (
        ("kalyani.html", "kalyani.html.j2", KALYANI_CSS, KALYANI_JS),
        ("jhalak.html", "jhalak.html.j2", JHALAK_CSS, JHALAK_JS),
    ):
        out = APP_ROOT / fname
        out.write_text(env.get_template(tpl).render(
            css_bundle="\n\n".join(p.read_text(encoding="utf-8").strip() for p in css_list),
            data_js=data_js,
            js_bundle="\n\n".join(p.read_text(encoding="utf-8").strip() for p in js_list),
            letter_video_url=LETTER_VIDEO_URL,
            favicon_uri=b64_uri(APP_ROOT / "assets" / "icons" / "favicon-kalyani.png", "image/png"),
        ), encoding="utf-8")
        print(f"Built {out.name} via Jinja2 ({out.stat().st_size:,} bytes)")


def build_anondo(env: jinja2.Environment) -> None:
    passed, issues, dim_scores = run_quality_gate(verbose=False, persona_id="anondo")
    if not passed:
        raise RuntimeError(f"Quality Gate failed for anondo: {issues}")
    print(f"[Agentic Quality Gate (anondo)] PASSED all {len(dim_scores)}/12 dimensions.")

    url_prefix = GH_RAW_AUDIO_BASE + "anondo/"
    img_dir = APP_ROOT / "assets" / "anondo" / "slides"
    slides = [
        {**s, "img_b64": b64_uri(img_dir / f"slide_{int(s['id'])}.jpg", "image/jpeg"), "audio_url": f"{url_prefix}slides/slide_{int(s['id'])}.mp3"}
        for s in ANONDO_SLIDES
    ]
    quotes = [{"text": q, "audio_url": f"{url_prefix}quotes/quote_{i}.mp3"} for i, q in enumerate(ANONDO_QUOTES)]
    pillars = [{**p, "audio_url": f"{url_prefix}pillars/pillar_{i}.mp3"} for i, p in enumerate(ANONDO_PILLARS)]
    days = [
        {
            "day": int(d["day"]),
            "phase": d.get("phase", "House-Money Era"),
            "title": d["title_bn"],
            "sub": d.get("summary_bn", ""),
            "audio_url": f"{url_prefix}days/day_{int(d['day'])}.mp3",
            "games": [
                {
                    "pillar": ag.get("pillar", ""),
                    "short": ag["short_bn"],
                    "category": ag["category"],
                    "title": ag["title_bn"],
                    "detail": ag["detail_bn"],
                    "prompt": ag["prompt_bn"],
                    "followup_prompt": ag.get("followup_prompt_bn", ""),
                    "audio_url": f"{url_prefix}games/day_{int(d['day'])}_ag_{idx}.mp3",
                }
                for idx, ag in enumerate(d["agendas"])
            ],
        }
        for d in ANONDO_DAYS_21
    ]
    data_js = "\n".join([
        f"const ANONDO_DATA = {json.dumps({'slides': slides, 'quotes': quotes, 'days': days}, ensure_ascii=False)};",
        f"const PILLARS_DATA = {json.dumps(pillars, ensure_ascii=False)};",
    ])
    html = env.get_template("anondo.html.j2").render(
        css_bundle="\n\n".join(p.read_text(encoding="utf-8").strip() for p in ANONDO_CSS),
        data_js=data_js,
        js_bundle="\n\n".join(p.read_text(encoding="utf-8").strip() for p in ANONDO_JS),
        favicon_uri=b64_uri(APP_ROOT / "assets" / "icons" / "favicon-anondo.png", "image/png"),
    )
    out = APP_ROOT / "anondo.html"
    out.write_text(html, encoding="utf-8")
    print(f"Built {out.name} via Jinja2 ({out.stat().st_size:,} bytes)")


def build_all(persona: str = "all") -> None:
    src_icon, dst_icon = APP_ROOT / "assets" / "icons" / "favicon.svg", APP_ROOT / "favicon.svg"
    if src_icon.is_file() and src_icon.read_bytes() != (dst_icon.read_bytes() if dst_icon.is_file() else b""):
        shutil.copyfile(src_icon, dst_icon)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False, keep_trailing_newline=True)
    targets = ("kalyani", "anondo") if persona == "all" else (persona,)
    if "kalyani" in targets:
        build_kalyani(env)
    if "anondo" in targets:
        build_anondo(env)

    hub = APP_ROOT / "index.html"
    hub.write_text(
        env.get_template("index.html.j2").render(favicon_uri=b64_uri(APP_ROOT / "assets" / "icons" / "favicon-hub.png", "image/png")),
        encoding="utf-8",
    )
    print(f"Built {hub.name} Persona Hub via Jinja2 ({hub.stat().st_size:,} bytes)")

    for pid in targets:
        stale, expected, _ = get_stale_or_missing_files(scope="all", persona_id=pid)
        if not stale:
            print(f"[TTS Check ({pid})] All {len(expected)} Aoede MP3 files are 100% in sync.")
        else:
            print(f"[TTS Notice ({pid})] {len(stale)}/{len(expected)} audio file(s) pending voice refresh: {stale[:6]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile AI Companion (`kalyani.html`, `anondo.html`, `index.html`).")
    parser.add_argument("--persona", default="all", choices=("all", "kalyani", "anondo"))
    build_all(parser.parse_args().persona)
