#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unified Modular Jinja2 Compiler for AI Companion (`jhalak`, `zorba`, and `index.html`).

CRITICAL GOVERNANCE RULE (defined in GEMINI.md):
  - Runs in <0.5s and NEVER invokes TTS voice generation.
  - Checks `audio/<persona>/tts_manifest.json`.
"""

from __future__ import annotations

import argparse
import base64
import json
import shutil
import sys
from pathlib import Path
import jinja2

APP_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_ROOT))
sys.path.insert(0, str(APP_ROOT / "scripts"))

from content import ANONDO_SLIDES, DAYS_21, LETTER_VIDEO_URL, SLIDES  # noqa: E402
from refresh_voices import get_stale_or_missing_files  # noqa: E402

SRC_DIR = APP_ROOT / "src"
TEMPLATES_DIR = SRC_DIR / "templates"
GH_RAW_AUDIO_BASE = "https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/audio/"

JHALAK_CSS = (SRC_DIR / "jhalak" / "styles" / "jhalak.css",)
JHALAK_JS = (
    SRC_DIR / "jhalak" / "js" / "curated-content.js",
    SRC_DIR / "jhalak" / "js" / "feed-engine.js",
    SRC_DIR / "jhalak" / "js" / "player-ui.js",
)
ZORBA_CSS = (SRC_DIR / "jhalak" / "styles" / "jhalak.css", SRC_DIR / "zorba" / "styles" / "zorba.css")
ZORBA_JS = (SRC_DIR / "zorba" / "js" / "curated-content.js", SRC_DIR / "zorba" / "js" / "player-ui.js")


def b64_uri(path: Path, mime: str) -> str:
    return ("data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode("ascii")) if path.is_file() else ""


def build_jhalak(env: jinja2.Environment) -> None:
    url_prefix = GH_RAW_AUDIO_BASE + "jhalak/"
    img_dir = APP_ROOT / "assets" / "jhalak" / "slides"
    jh_mpath = APP_ROOT / "audio" / "jhalak" / "tts_manifest.json"
    jh_manifest = json.loads(jh_mpath.read_text(encoding="utf-8")) if jh_mpath.is_file() else {}
    slide_timings = jh_manifest.get("slide_timings", {})
    jh_timings = jh_manifest.get("audio_timings", {})
    slides_payload = [
        {
            **s,
            "img_b64": b64_uri(img_dir / f"slide_{int(s['id'])}.jpg", "image/jpeg"),
            "audio_url": f"{url_prefix}slides/slide_{int(s['id'])}.mp3",
            "audio_b64": "",
            "audio_meta": slide_timings.get(f"slide_{int(s['id'])}", {}),
        }
        for s in SLIDES
    ]
    data_js = "\n".join([
        f"const LETTER_VIDEO_URL = {json.dumps(LETTER_VIDEO_URL, ensure_ascii=False)};",
        f"const SLIDES = {json.dumps(slides_payload, ensure_ascii=False)};",
        f"const DAYS_21 = {json.dumps(DAYS_21, ensure_ascii=False)};",
        f"const JHALAK_AUDIO_TIMINGS = {json.dumps(jh_timings, ensure_ascii=False)};",
    ])
    out = APP_ROOT / "jhalak.html"
    out.write_text(
        env.get_template("jhalak.html.j2").render(
            css_bundle="\n\n".join(p.read_text(encoding="utf-8").strip() for p in JHALAK_CSS),
            data_js=data_js,
            js_bundle="\n\n".join(p.read_text(encoding="utf-8").strip() for p in JHALAK_JS),
            letter_video_url=LETTER_VIDEO_URL,
            favicon_uri=b64_uri(APP_ROOT / "assets" / "icons" / "favicon-jhalak.png", "image/png"),
        ),
        encoding="utf-8",
    )
    print(f"Built {out.name} via Jinja2 ({out.stat().st_size:,} bytes)")


def build_zorba(env: jinja2.Environment) -> None:
    url_prefix = GH_RAW_AUDIO_BASE + "zorba/"
    img_dir = APP_ROOT / "assets" / "zorba" / "slides"
    zb_mpath = APP_ROOT / "audio" / "zorba" / "tts_manifest.json"
    zb_manifest = json.loads(zb_mpath.read_text(encoding="utf-8")) if zb_mpath.is_file() else {}
    zb_timings = zb_manifest.get("audio_timings", {})
    slides = [
        {
            **s,
            "img_b64": b64_uri(img_dir / f"slide_{int(s['id'])}.jpg", "image/jpeg"),
            "audio_url": f"{url_prefix}slides/slide_{int(s['id'])}.mp3",
            "audio_meta": zb_timings.get(f"slides/slide_{int(s['id'])}.mp3", {}),
        }
        for s in ANONDO_SLIDES
    ]
    data_js = "\n".join([
        f"const ANONDO_DATA = {json.dumps({'slides': slides}, ensure_ascii=False)};",
        f"const JHALAK_AUDIO_TIMINGS = {json.dumps(zb_timings, ensure_ascii=False)};",
    ])
    out = APP_ROOT / "zorba.html"
    out.write_text(
        env.get_template("zorba.html.j2").render(
            css_bundle="\n\n".join(p.read_text(encoding="utf-8").strip() for p in ZORBA_CSS),
            data_js=data_js,
            js_bundle="\n\n".join(p.read_text(encoding="utf-8").strip() for p in ZORBA_JS),
            favicon_uri=b64_uri(APP_ROOT / "assets" / "icons" / "favicon-zorba.png", "image/png"),
        ),
        encoding="utf-8",
    )
    print(f"Built {out.name} via Jinja2 ({out.stat().st_size:,} bytes)")


def build_all(persona: str = "all") -> None:
    src_icon, dst_icon = APP_ROOT / "assets" / "icons" / "favicon.svg", APP_ROOT / "favicon.svg"
    if src_icon.is_file() and src_icon.read_bytes() != (dst_icon.read_bytes() if dst_icon.is_file() else b""):
        shutil.copyfile(src_icon, dst_icon)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False, keep_trailing_newline=True)
    targets = ("jhalak", "zorba") if persona == "all" else (persona,)
    if "jhalak" in targets:
        build_jhalak(env)
    if "zorba" in targets:
        build_zorba(env)

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
    parser = argparse.ArgumentParser(description="Compile AI Companion (`jhalak.html`, `zorba.html`, `index.html`).")
    parser.add_argument("--persona", default="all", choices=("all", "jhalak", "zorba"))
    build_all(parser.parse_args().persona)
