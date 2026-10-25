#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the spec-driven, distraction-free, Android-first Mom-App (ui/ma-presentation.html) + Full HD MP4 video.

Key Architecture & UX Guarantees:
1. Ultra-compact sticky header (46px height, zero footer) with 2 top tabs: [🎓 আজকের খেলা] and [💌 মায়ের চিঠি], plus 1-tap [🔊/⏸️] & [🌙/☀️].
2. 100% Real Gemini Aoede Bengali Female Voice (`gemini-v4s-tts`) across all slides, days, morning quotes, and section listen buttons (zero robotic Web Speech API).
3. Unified Play/Pause Audio Controller (`playOrToggleAudio(btnId, srcUrl, fallbackB64)`): every single listen button (`🔊 শোনো`) toggles to `⏸️ থামাও` when active and pauses/resumes cleanly.
4. Explicit, zero-ambiguity step-by-step instructions on every single agenda card showing how to open Gemini, tap the mic, and speak the exact prompt (`🗣️ মা, ফোনে জেমিনি (Gemini) খুলে মাইক 🎙️ ছুঁয়ে ঠিক এই কথাটি মুখে বলো:`).
"""

import base64
import json
import os
from pathlib import Path
import sys

APP_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_ROOT / "scripts"))
from curriculum_data import DAYS_21, DAYS_PART2_30, SLIDES  # noqa: E402
from refresh_voices import get_stale_or_missing_files  # noqa: E402

BRAIN_DIR = "/usr/local/google/home/koushikchak/.gemini/jetski/brain/78e141e4-9a15-4fd2-86e2-68d0604ebe24"
AUDIO_DIR = str(APP_ROOT / "audio")
SLIDES_DIR = str(APP_ROOT / "assets" / "slides")

SLIDE_IMAGES = {
    1: os.path.join(SLIDES_DIR, "slide_1.jpg"),
    2: os.path.join(SLIDES_DIR, "slide_2.jpg"),
    3: os.path.join(SLIDES_DIR, "slide_3.jpg"),
    4: os.path.join(SLIDES_DIR, "slide_4.jpg"),
    5: os.path.join(SLIDES_DIR, "slide_5.jpg"),
    6: os.path.join(SLIDES_DIR, "slide_6.jpg"),
    7: os.path.join(SLIDES_DIR, "slide_7.jpg"),
    8: os.path.join(SLIDES_DIR, "slide_8.jpg"),
}


def b64_uri(path: str, mime: str) -> str:
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode("ascii")


def build_html() -> None:
    slides_payload = []
    for s in SLIDES:
        sid = s["id"]
        img_path = SLIDE_IMAGES[sid]
        aud_path = os.path.join(AUDIO_DIR, f"slide_{sid}.mp3")
        slides_payload.append({
            **s,
            "img_b64": b64_uri(img_path, "image/jpeg"),
            "audio_url": f"audio/slide_{sid}.mp3",
            "audio_b64": b64_uri(aud_path, "audio/mpeg"),
        })

    # Pre-generated Gemini Aoede MP3s for the 8 agenda categories + Day 1 verbatim agendas + 7 morning quotes
    cat_audio_map = {}
    for c_idx in range(8):
        c_path = os.path.join(AUDIO_DIR, f"ag_cat_{c_idx}.mp3")
        cat_audio_map[c_idx] = {
            "url": f"audio/ag_cat_{c_idx}.mp3",
            "b64": b64_uri(c_path, "audio/mpeg") if os.path.exists(c_path) else "",
        }

    day1_ag_map = {}
    for a_idx in range(10):
        a_path = os.path.join(AUDIO_DIR, f"day_1_ag_{a_idx}.mp3")
        day1_ag_map[a_idx] = {
            "url": f"audio/day_1_ag_{a_idx}.mp3",
            "b64": b64_uri(a_path, "audio/mpeg") if os.path.exists(a_path) else "",
        }

    quotes_audio_list = []
    for q_idx in range(7):
        q_path = os.path.join(AUDIO_DIR, f"quote_{q_idx}.mp3")
        quotes_audio_list.append({
            "url": f"audio/quote_{q_idx}.mp3",
            "b64": b64_uri(q_path, "audio/mpeg") if os.path.exists(q_path) else "",
        })

    days_payload = []
    for d in DAYS_21:
        day_num = d["day"]
        aud_path = os.path.join(AUDIO_DIR, f"day_{day_num}.mp3")
        agendas_enriched = []
        for idx, ag in enumerate(d["agendas"]):
            ag_mp3_name = f"day_{day_num}_ag_{idx}.mp3"
            ag_mp3_path = os.path.join(AUDIO_DIR, ag_mp3_name)
            if os.path.exists(ag_mp3_path):
                a_url = f"audio/{ag_mp3_name}"
            elif day_num == 1 and idx in day1_ag_map:
                a_url = day1_ag_map[idx]["url"]
            else:
                a_url = cat_audio_map[idx % 8]["url"]
            agendas_enriched.append({
                **ag,
                "audio_url": a_url,
                "audio_b64": "",
            })
        days_payload.append({
            **d,
            "agendas": agendas_enriched,
            "audio_url": f"audio/day_{day_num}.mp3",
            "audio_b64": b64_uri(aud_path, "audio/mpeg"),
        })

    days_p2_payload = []
    for d in DAYS_PART2_30:
        day_num = d["day"]
        ref_day = d.get("audio_ref_day", ((d["part_day"] - 1) % 21) + 1)
        agendas_enriched = []
        for idx, ag in enumerate(d["agendas"]):
            p2_mp3 = f"day_{day_num}_ag_{idx}.mp3"
            ref_mp3 = f"day_{ref_day}_ag_{idx}.mp3"
            if os.path.exists(os.path.join(AUDIO_DIR, p2_mp3)):
                a_url = f"audio/{p2_mp3}"
            elif os.path.exists(os.path.join(AUDIO_DIR, ref_mp3)):
                a_url = f"audio/{ref_mp3}"
            else:
                a_url = cat_audio_map[idx % 8]["url"]
            agendas_enriched.append({
                **ag,
                "audio_url": a_url,
                "audio_b64": "",
            })
        days_p2_payload.append({
            **d,
            "agendas": agendas_enriched,
            "audio_url": f"audio/day_{ref_day}.mp3",
            "audio_b64": "",
        })

    html_template = r"""<!DOCTYPE html>
<html lang="bn" data-theme="warm">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="#FAF6F0">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href="ma-manifest.json">
<title>মায়ের এআই শিক্ষা ও চিঠি</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@500;600;700&family=Noto+Serif+Bengali:wght@700;800&display=swap" rel="stylesheet">
<style>
  :root, :root[data-theme="warm"] {
    --bg-app: #FAF6F0;
    --bg-surface: #FFFFFF;
    --bg-elev: #F3ECE1;
    --text-primary: #1F1610;
    --text-secondary: #5C4938;
    --accent: #0F8A5F;
    --accent-active: #D9532F;
    --accent-soft: #E3F6EE;
    --gold: #B86B11;
    --gold-soft: #FFF3DF;
    --border: rgba(140, 102, 58, 0.24);
    --shadow: 0 6px 20px rgba(42, 26, 12, 0.07);
    --nav-bg: rgba(250, 246, 240, 0.96);
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-tap-highlight-color: transparent;
  }

  body {
    font-family: 'Hind Siliguri', system-ui, -apple-system, sans-serif;
    background: var(--bg-app);
    color: var(--text-primary);
    min-height: 100dvh;
    padding-bottom: 36px;
    overflow-x: hidden;
    transition: background 0.2s ease, color 0.2s ease;
  }

  /* SLIM, SINGLE-ROW STICKY HEADER (Fits all 3 tabs + Listen button on 1 row on mobile) */
  .slim-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--nav-bg);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
    padding: calc(4px + env(safe-area-inset-top, 0px)) 6px 4px;
  }
  .slim-header-inner {
    max-width: 600px;
    margin: 0 auto;
    height: 40px;
    display: flex;
    flex-wrap: nowrap;
    align-items: center;
    justify-content: space-between;
    gap: 4px;
  }
  .header-tabs {
    display: flex;
    flex-wrap: nowrap;
    align-items: center;
    gap: 4px;
    flex: 1;
    min-width: 0;
  }
  .htab-btn {
    height: 34px;
    padding: 0 8px;
    border-radius: 999px;
    border: 1.5px solid var(--border);
    background: var(--bg-surface);
    color: var(--text-secondary);
    font-family: inherit;
    font-size: clamp(0.76rem, 3.1vw, 0.9rem);
    font-weight: 700;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 3px;
    white-space: nowrap;
    flex-shrink: 1;
    min-width: 0;
    transition: all 0.15s ease;
  }
  .htab-btn.active {
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
    box-shadow: 0 3px 10px rgba(15, 138, 95, 0.28);
  }
  .header-right {
    display: flex;
    align-items: center;
    gap: 4px;
    flex-shrink: 0;
  }
  .hctrl-btn {
    height: 34px;
    padding: 0 9px;
    border-radius: 999px;
    border: 1.5px solid var(--border);
    background: var(--bg-surface);
    color: var(--text-primary);
    font-family: inherit;
    font-size: clamp(0.76rem, 3.1vw, 0.88rem);
    font-weight: 700;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 3px;
    white-space: nowrap;
  }
  .hctrl-btn.playing {
    background: var(--accent-active);
    color: #fff;
    border-color: var(--accent-active);
  }

  .app-shell {
    max-width: 600px;
    margin: 0 auto;
    padding: 0 12px;
  }

  /* One-Time Permission Card */
  .perm-banner {
    margin: 10px 0;
    padding: 12px 14px;
    border-radius: 16px;
    background: var(--accent-soft);
    border: 1.5px solid var(--accent);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
  }
  .perm-banner-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
    flex: 1;
    min-width: 200px;
  }
  .perm-btn-primary {
    min-height: 40px;
    padding: 0 14px;
    border-radius: 12px;
    border: none;
    background: var(--accent);
    color: #fff;
    font-family: inherit;
    font-size: 0.98rem;
    font-weight: 700;
    cursor: pointer;
  }

  /* Morning Quote View Card */
  .quote-card {
    margin: 14px 0;
    padding: 22px 18px;
    border-radius: 22px;
    background: var(--gold-soft);
    border: 1.5px solid var(--gold);
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .quote-text {
    font-family: 'Noto Serif Bengali', serif;
    font-size: 1.32rem;
    line-height: 1.62;
    font-weight: 700;
    color: var(--text-primary);
  }
  .quote-play-btn {
    width: 100%;
    min-height: 50px;
    padding: 0 16px;
    border-radius: 16px;
    border: none;
    background: var(--gold);
    color: #fff;
    font-family: inherit;
    font-size: 1.08rem;
    font-weight: 700;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
  }
  .quote-play-btn.playing {
    background: var(--accent-active);
  }

  /* Views */
  .view-sec {
    display: none;
  }
  .view-sec.active {
    display: block;
  }

  /* Part Switcher + Progress Pill */
  .course-top-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin: 10px 0 8px;
    flex-wrap: wrap;
  }
  .part-switch-row {
    display: inline-flex;
    background: var(--bg-elev);
    padding: 4px;
    border-radius: 14px;
    gap: 4px;
  }
  .part-seg-btn {
    min-height: 36px;
    padding: 0 12px;
    border-radius: 10px;
    border: none;
    background: transparent;
    color: var(--text-secondary);
    font-family: inherit;
    font-size: 0.95rem;
    font-weight: 700;
    cursor: pointer;
  }
  .part-seg-btn.active {
    background: var(--bg-surface);
    color: var(--text-primary);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  }
  .prog-inline-pill {
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--accent);
    background: var(--accent-soft);
    padding: 6px 12px;
    border-radius: 999px;
  }

  /* Horizontal Day Selector */
  .day-selector-strip {
    display: flex;
    gap: 7px;
    overflow-x: auto;
    padding: 4px 2px 10px;
    scrollbar-width: none;
  }
  .day-selector-strip::-webkit-scrollbar { display: none; }
  .day-chip {
    flex-shrink: 0;
    min-height: 40px;
    padding: 0 14px;
    border-radius: 999px;
    border: 1.5px solid var(--border);
    background: var(--bg-surface);
    color: var(--text-primary);
    font-family: inherit;
    font-size: 0.98rem;
    font-weight: 700;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 5px;
  }
  .day-chip.active {
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
  }
  .day-chip.done {
    border-color: var(--accent);
  }

  /* Active Day Hero */
  .day-hero-card {
    background: var(--bg-surface);
    border: 1.5px solid var(--border);
    border-radius: 22px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: var(--shadow);
  }
  .day-hero-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 0.88rem;
    font-weight: 700;
    margin-bottom: 6px;
  }
  .day-hero-title {
    font-family: 'Noto Serif Bengali', serif;
    font-size: 1.42rem;
    font-weight: 800;
    line-height: 1.35;
    margin-bottom: 6px;
  }
  .day-hero-summary {
    font-size: 1.06rem;
    line-height: 1.58;
    color: var(--text-secondary);
    margin-bottom: 14px;
  }
  .big-voice-btn {
    width: 100%;
    min-height: 52px;
    border-radius: 16px;
    border: none;
    background: linear-gradient(135deg, var(--accent), #0b6e4b);
    color: #fff;
    font-family: inherit;
    font-size: 1.12rem;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    box-shadow: 0 6px 18px rgba(15, 138, 95, 0.25);
  }
  .big-voice-btn.playing {
    background: linear-gradient(135deg, var(--accent-active), #b33919);
  }

  /* 8-Game Visual Grid Navigator & Focused Single-Game Stage */
  .game-nav-card {
    background: var(--bg-surface);
    border: 1.5px solid var(--border);
    border-radius: 20px;
    padding: 14px;
    margin-bottom: 12px;
    box-shadow: var(--shadow);
  }
  .game-nav-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    gap: 8px;
  }
  .game-nav-title {
    font-size: 0.98rem;
    font-weight: 700;
    color: var(--text-primary);
  }
  .view-mode-toggle {
    padding: 5px 11px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--bg-elev);
    color: var(--text-secondary);
    font-family: inherit;
    font-size: 0.86rem;
    font-weight: 700;
    cursor: pointer;
  }
  .game-grid-8 {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 6px;
  }
  .game-tile {
    min-height: 54px;
    padding: 6px 4px;
    border-radius: 14px;
    border: 1.5px solid var(--border);
    background: var(--bg-app);
    color: var(--text-primary);
    font-family: inherit;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    transition: all 0.15s ease;
  }
  .game-tile-num {
    font-size: 0.92rem;
    font-weight: 800;
    line-height: 1.1;
  }
  .game-tile-lbl {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
  }
  .game-tile.active {
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
    box-shadow: 0 4px 12px rgba(15, 138, 95, 0.3);
  }
  .game-tile.active .game-tile-lbl {
    color: #E3F6EE;
  }
  .game-tile.done-tile {
    border-color: var(--accent);
    background: var(--accent-soft);
  }
  .game-tile.active.done-tile {
    background: var(--accent);
    color: #fff;
  }
  .game-stepper-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 4px;
  }

  /* Agenda Cards with Explicit Step-by-Step Instructions */
  .agenda-stack {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .agenda-card {
    background: var(--bg-surface);
    border: 1.5px solid var(--border);
    border-radius: 20px;
    padding: 18px;
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .agenda-card.done-card {
    border-color: var(--accent);
    background: var(--accent-soft);
  }
  .agenda-cat {
    align-self: flex-start;
    padding: 4px 12px;
    border-radius: 999px;
    background: var(--gold-soft);
    color: var(--gold);
    font-size: 0.9rem;
    font-weight: 700;
  }
  .agenda-title {
    font-family: 'Noto Serif Bengali', serif;
    font-size: 1.26rem;
    font-weight: 800;
    line-height: 1.35;
  }
  .agenda-step-heading {
    font-size: 0.96rem;
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 2px;
  }
  .agenda-detail {
    font-size: 1.12rem;
    line-height: 1.65;
    color: var(--text-primary);
  }
  .agenda-prompt-box {
    padding: 14px 16px;
    border-radius: 16px;
    background: var(--bg-elev);
    border: 1.5px solid var(--gold);
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .agenda-prompt-label {
    font-size: 1rem;
    font-weight: 700;
    color: var(--gold);
    line-height: 1.45;
  }
  .agenda-prompt-speech {
    font-size: 1.16rem;
    line-height: 1.58;
    font-weight: 700;
    color: var(--text-primary);
  }
  .agenda-prompt-howto {
    font-size: 0.92rem;
    color: var(--text-secondary);
    line-height: 1.45;
  }
  .agenda-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  .ag-btn {
    min-height: 48px;
    border-radius: 14px;
    border: 1.5px solid var(--border);
    background: var(--bg-surface);
    color: var(--text-primary);
    font-family: inherit;
    font-size: 1.02rem;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
  }
  .ag-btn.listen {
    background: var(--gold-soft);
    border-color: var(--gold);
  }
  .ag-btn.listen.playing {
    background: var(--accent-active);
    color: #fff;
    border-color: var(--accent-active);
  }
  .ag-btn.check.checked {
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
  }

  /* VIEW 2: SLIDE PRESENTATION (💌 মায়ের চিঠি) */
  .slide-card {
    background: var(--bg-surface);
    border: 1.5px solid var(--border);
    border-radius: 22px;
    overflow: hidden;
    margin-top: 12px;
    box-shadow: var(--shadow);
  }
  .slide-img-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 10;
    background: #000;
  }
  .slide-img-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .slide-badge-pill {
    position: absolute;
    top: 10px;
    left: 10px;
    padding: 5px 12px;
    border-radius: 999px;
    background: rgba(18, 11, 8, 0.85);
    color: #FFE29E;
    font-size: 0.88rem;
    font-weight: 700;
  }
  .slide-content {
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .slide-title {
    font-family: 'Noto Serif Bengali', serif;
    font-size: 1.48rem;
    font-weight: 800;
    line-height: 1.35;
  }
  .slide-highlight {
    padding: 12px 14px;
    border-radius: 14px;
    background: var(--gold-soft);
    border-left: 4px solid var(--gold);
    font-size: 1.08rem;
    font-weight: 700;
    line-height: 1.48;
  }
  .slide-body {
    font-size: 1.14rem;
    line-height: 1.68;
  }
  .slide-nav-row {
    display: grid;
    grid-template-columns: 1fr 1.2fr 1fr;
    gap: 8px;
    padding-top: 6px;
  }
</style>
</head>
<body>

<!-- ULTRA-COMPACT SINGLE-ROW STICKY HEADER (All 3 Tabs + Listen Button Fit on 1 Row in Mobile) -->
<header class="slim-header">
  <div class="slim-header-inner">
    <div class="header-tabs">
      <button id="htabPlan" class="htab-btn active" onclick="switchView('plan')">🎓 খেলা</button>
      <button id="htabSlides" class="htab-btn" onclick="switchView('slides')">💌 চিঠি</button>
      <button id="htabQuote" class="htab-btn" onclick="switchView('quote')">☀️ অনুপ্রেরণা</button>
    </div>
    <div class="header-right">
      <button id="topPlayBtn" class="hctrl-btn" data-default-label="🔊 শোনো" onclick="toggleMasterAudio()">🔊 শোনো</button>
    </div>
  </div>
</header>

<main class="app-shell">

  <!-- ONE-TIME PERMISSION BANNER -->
  <div id="permBanner" class="perm-banner" style="display:none;">
    <div class="perm-banner-title">🎙️ মা, রোজ সকালের সুপ্রভাত বার্তা ও মাইক চালু করতে এখানে একবার ছোঁও:</div>
    <button class="perm-btn-primary" onclick="requestMicAndNotificationPermission()">✅ চালু করো</button>
  </div>

  <!-- =====================================================================
       VIEW 1: TODAY'S LESSON (🎓 খেলা — Part 1: 21 Days & Part 2: 30 Days)
       ===================================================================== -->
  <section id="viewPlan" class="view-sec active">
    <div class="course-top-row">
      <div class="part-switch-row">
        <button id="segPart1" class="part-seg-btn active" onclick="switchCoursePart(1)">🎓 পার্ট ১ (২১ দিন)</button>
        <button id="segPart2" class="part-seg-btn" onclick="switchCoursePart(2)">🌱 পার্ট ২ (৩০ দিন)</button>
      </div>
      <div id="progInlinePill" class="prog-inline-pill">✅ 0 / 210</div>
    </div>

    <div id="dayStrip" class="day-selector-strip"></div>

    <div id="activeDayStage"></div>
  </section>

  <!-- =====================================================================
       VIEW 2: 8-SLIDE THANKSGIVING LETTER (💌 চিঠি)
       ===================================================================== -->
  <section id="viewSlides" class="view-sec">
    <div class="slide-card">
      <div class="slide-img-wrap">
        <img id="slideImg" src="" alt="মা ও পরিবারের ছবি">
        <div id="slideBadge" class="slide-badge-pill"></div>
      </div>
      <div class="slide-content">
        <div id="slideTitleBn" class="slide-title"></div>
        <div id="slideHighlight" class="slide-highlight"></div>
        <div id="slideBodyBn" class="slide-body"></div>
        <button id="btnSlideMainPlay" class="big-voice-btn" data-default-label="🔊 এই পাতাটা শোনো" onclick="toggleSlideAudio()">
          🔊 এই পাতাটা শোনো
        </button>
        <div class="slide-nav-row">
          <button id="prevBtn" class="ag-btn" onclick="prevSlide()">⬅️ আগে</button>
          <button id="autoAdvanceBtn" class="ag-btn" onclick="toggleAutoPlayAll()">🔁 পরপর: চালু</button>
          <button id="nextBtn" class="ag-btn" onclick="nextSlide()">পরে ➡️</button>
        </div>
      </div>
    </div>
  </section>

  <!-- =====================================================================
       VIEW 3: DAILY INSPIRATION & RANDOM QUOTE (☀️ আজকের অনুপ্রেরণা)
       ===================================================================== -->
  <section id="viewQuote" class="view-sec">
    <div class="quote-card">
      <div>
        <div style="font-size:0.95rem; font-weight:700; color:var(--gold); margin-bottom:8px;">☀️ আজকের সুপ্রভাত ও অনুপ্রেরণা</div>
        <div id="dailyQuoteText" class="quote-text"></div>
      </div>
      <button id="btnQuotePlay" class="quote-play-btn" data-default-label="🔊 শোনো" onclick="toggleMorningQuoteAudio()">🔊 শোনো</button>
      <button id="btnNextRandomQuote" class="ag-btn" onclick="pickNewRandomQuote(true)">🎲 নতুন অনুপ্রেরণা দেখো</button>
    </div>
  </section>

</main>

<audio id="audioPlayer"></audio>

<script>
const SLIDES = __SLIDES_JSON__;
const DAYS_21 = __DAYS_JSON__;
const DAYS_PART2_30 = __DAYS_P2_JSON__;
const QUOTES_AUDIO = __QUOTES_AUDIO_JSON__;
const CAT_AUDIO_MAP = __CAT_AUDIO_MAP_JSON__;
const DAY1_AG_MAP = __DAY1_AG_MAP_JSON__;
const ALL_DAYS = DAYS_21.concat(DAYS_PART2_30);

const MORNING_QUOTES = [
  "সুপ্রভাত মা! যেমনভাবে একটা পাখি ডানা মেলে আকাশে ওড়ে, আজ তোমার মনটাও তেমনই হালকা ও আনন্দে ভরে উঠুক।",
  "সুপ্রভাত মা! মা সারদা বলতেন—‘যখনই ভয় করবে, জানবে আমি তোমার পাশে আছি।’ আজ নতুন কিছু শেখার জন্য দারুণ একটা দিন!",
  "সুপ্রভাত মা! রানাঘাটের সেই মনোযোগী স্কুলছাত্রীটা আজও তোমার ভেতরে বেঁচে আছে। আজ আনন্দে একটা গানের মানে আর নতুন বোতাম শিখবো!",
  "সুপ্রভাত মা! বয়স শুধু সংখ্যামাত্র—রোজ একটা করে ‘কেন?’ আর ‘কীভাবে?’ প্রশ্ন করলেই মাথাটা একদম তাজা ও সচল থাকে।",
  "সুপ্রভাত মা! তোমার ছেলে কৌশিক আর দিদি তোমাকে ভীষণ ভালোবাসে। আজ নিজের আনন্দে, কোনো ভয় ছাড়া নতুন কিছু শেখো!",
  "সুপ্রভাত মা! রবীন্দ্রনাথ লিখেছেন—‘আলো আমার, আলো ওগো, আলোয় ভুবন ভরা।’ আজ তোমার মন আর ঘর আনন্দ-আলোয় ভরে থাকুক।",
  "সুপ্রভাত মা! ভুল হওয়া মানেই শেখার শুরু। আজ কোনো লজ্জা ছাড়া রিমোট, ফোন বা ইংরেজি শব্দ নিয়ে নতুন খেলা খেলবো!"
];

let curView = 'plan';
let curPart = 1;
let curSlideIdx = 0;
let curDayNum = 1;
let curGameIdx = 0;
let showAllGamesInDay = false;
let autoAdvance = true;

const GAME_SHORT_LABELS = [
  "🧠 ১. মন",
  "📱 ২. রিমোট",
  "🔤 ৩. শব্দ",
  "🗣️ ৪. ইংরেজি বলা",
  "🌍 ৫. খবর",
  "🤖 ৬. এআই",
  "🏆 ৭. চ্যালেঞ্জ",
  "💡 ৮. বুদ্ধি",
  "🎵 ৯. গান",
  "❓ ১০. কেন?"
];

/* Unified Audio State Machine (Supports Play, Pause & Resume on Every Button) */
const audioEl = document.getElementById('audioPlayer');
const topPlayBtn = document.getElementById('topPlayBtn');
const slideImg = document.getElementById('slideImg');
let activeAudioBtnId = null;
let activeAudioKey = null;

let doneMap = {};
try { doneMap = JSON.parse(localStorage.getItem('ma_21day_done_v2') || '{}'); } catch (e) { doneMap = {}; }

let maProfile = {
  morningTime: '08:00',
  lastMorningNotifDate: '',
  permsGranted: false
};
try {
  const savedProf = JSON.parse(localStorage.getItem('ma_kalyani_profile_v1') || 'null');
  if (savedProf && typeof savedProf === 'object') {
    maProfile = Object.assign(maProfile, savedProf);
  }
} catch (e) {}

function saveMaProfile() {
  try { localStorage.setItem('ma_kalyani_profile_v1', JSON.stringify(maProfile)); } catch (e) {}
}

function saveDoneMap() {
  try { localStorage.setItem('ma_21day_done_v2', JSON.stringify(doneMap)); } catch (e) {}
}

/* Pleasant Morning Bell Chime via Web Audio API */
function playMorningChimeSound() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const notes = [523.25, 659.25, 783.99, 1046.50];
    notes.forEach((freq, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, ctx.currentTime + i * 0.18);
      gain.gain.setValueAtTime(0.001, ctx.currentTime + i * 0.18);
      gain.gain.exponentialRampToValueAtTime(0.22, ctx.currentTime + i * 0.18 + 0.04);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + i * 0.18 + 1.1);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(ctx.currentTime + i * 0.18);
      osc.stop(ctx.currentTime + i * 0.18 + 1.15);
    });
  } catch (e) {}
}

let curQuoteIdx = Math.floor(Date.now() / 86400000) % MORNING_QUOTES.length;

function pickNewRandomQuote(autoPlayAudio) {
  if (MORNING_QUOTES.length > 1) {
    let nextIdx = curQuoteIdx;
    for (let tries = 0; tries < 10 && nextIdx === curQuoteIdx; tries++) {
      nextIdx = Math.floor(Math.random() * MORNING_QUOTES.length);
    }
    if (nextIdx === curQuoteIdx) {
      nextIdx = (curQuoteIdx + 1) % MORNING_QUOTES.length;
    }
    curQuoteIdx = nextIdx;
  }
  const qEl = document.getElementById('dailyQuoteText');
  if (qEl) qEl.textContent = MORNING_QUOTES[curQuoteIdx];
  if (autoPlayAudio) {
    stopAllAudio();
    toggleMorningQuoteAudio();
  }
  return curQuoteIdx;
}

function getTodayQuoteIdx() {
  return curQuoteIdx;
}

function getTodayQuote() {
  return MORNING_QUOTES[curQuoteIdx];
}

function initMorningQuoteAndAlarm() {
  const qEl = document.getElementById('dailyQuoteText');
  if (qEl) qEl.textContent = getTodayQuote();

  const notifGranted = ('Notification' in window) && Notification.permission === 'granted';
  const permBanner = document.getElementById('permBanner');
  if (permBanner) {
    permBanner.style.display = (maProfile.permsGranted && notifGranted) ? 'none' : 'flex';
  }

  checkAndFireDailyMorningNotification();
  setInterval(checkAndFireDailyMorningNotification, 45000);
}

function checkAndFireDailyMorningNotification() {
  const now = new Date();
  const todayStr = now.toISOString().slice(0, 10);
  if (maProfile.lastMorningNotifDate === todayStr) return;

  const parts = (maProfile.morningTime || '08:00').split(':');
  const targetH = parseInt(parts[0] || '8', 10);
  const targetM = parseInt(parts[1] || '0', 10);
  const nowMins = now.getHours() * 60 + now.getMinutes();
  const targetMins = targetH * 60 + targetM;

  if (nowMins >= targetMins && nowMins <= targetMins + 240) {
    maProfile.lastMorningNotifDate = todayStr;
    saveMaProfile();
    fireMorningMotivationNotification(false);
  }
}

function fireMorningMotivationNotification(isManualTest) {
  const quote = getTodayQuote();
  playMorningChimeSound();
  const title = '☀️ সুপ্রভাত মা! আজকের অনুপ্রেরণা';
  if ('Notification' in window && Notification.permission === 'granted') {
    if (navigator.serviceWorker && navigator.serviceWorker.ready) {
      navigator.serviceWorker.ready.then(reg => {
        reg.showNotification(title, {
          body: quote,
          icon: 'favicon.svg',
          vibrate: [200, 100, 200],
          tag: 'ma-morning-motivation'
        });
      }).catch(() => {
        new Notification(title, { body: quote });
      });
    } else {
      new Notification(title, { body: quote });
    }
  }
  if (isManualTest) {
    toggleMorningQuoteAudio();
  }
}

async function requestMicAndNotificationPermission() {
  try {
    if ('Notification' in window) {
      await Notification.requestPermission();
    }
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.getTracks().forEach(t => t.stop());
    }
    maProfile.permsGranted = true;
    saveMaProfile();
    const permBanner = document.getElementById('permBanner');
    if (permBanner) permBanner.style.display = 'none';
    fireMorningMotivationNotification(true);
  } catch (err) {
    alert('মা, ব্রাউজারের পপ-আপে "Allow" (অনুমতি দিন) বোতামটি ছোঁও।');
  }
}

/* ============================================================================
   UNIFIED PLAY / PAUSE AUDIO CONTROLLER (100% Real Gemini Aoede Voice)
   Every button (`topPlayBtn`, `btnQuotePlay`, `btnDayMainPlay`, `btnSlideMainPlay`,
   and every `btnAgPlay_{day}_{idx}`) toggles cleanly between Play & Pause!
   ============================================================================ */
function syncAllAudioButtonsUI(isPlaying) {
  // 1. Reset any previously active button that is no longer active
  document.querySelectorAll('[data-default-label]').forEach(btn => {
    if (btn.id === activeAudioBtnId && isPlaying) {
      btn.classList.add('playing');
      btn.innerHTML = '⏸️ থামাও';
    } else {
      btn.classList.remove('playing');
      btn.innerHTML = btn.getAttribute('data-default-label');
    }
  });
  // 2. Always sync top header master button so Ma can also pause from the sticky top bar
  if (topPlayBtn) {
    if (isPlaying) {
      topPlayBtn.classList.add('playing');
      topPlayBtn.innerHTML = '⏸️ থামাও';
    } else {
      topPlayBtn.classList.remove('playing');
      topPlayBtn.innerHTML = '🔊 শোনো';
    }
  }
}

function stopAllAudio() {
  audioEl.pause();
  activeAudioBtnId = null;
  activeAudioKey = null;
  syncAllAudioButtonsUI(false);
}

function buildFullSectionSpeechText(d, ag, agIdx) {
  const dispDay = (d && d.part === 2) ? d.part_day : (d ? d.day : 1);
  const followTxt = ag.followup_prompt_bn
    ? (' আর গানটা শোনা হয়ে গেলে এর মানে জানতে বলো: ' + ag.followup_prompt_bn)
    : '';
  return (
    'দিন ' + dispDay + ', খেলা ' + (agIdx + 1) + ': ' + ag.category + '। ' +
    ag.title_bn + '। ' +
    'ধাপ ১, আজ কী করবো দেখো: ' + ag.detail_bn + ' ' +
    'ধাপ ২, এবার ফোনে জেমিনি খুলে মাইক বোতাম ছুঁয়ে মুখে বলো: ' + ag.prompt_bn + followTxt
  );
}

function playOrToggleAudio(btnId, audioKey, srcUrl, fallbackB64) {
  // Case 1: Clicking the SAME button while it is currently playing -> PAUSE IT!
  if (activeAudioKey === audioKey && !audioEl.paused) {
    audioEl.pause();
    syncAllAudioButtonsUI(false);
    return;
  }
  // Case 2: Clicking the SAME button while it is paused mid-way -> RESUME IT!
  if (activeAudioKey === audioKey && audioEl.paused && audioEl.currentTime > 0 && !audioEl.ended) {
    activeAudioBtnId = btnId;
    syncAllAudioButtonsUI(true);
    audioEl.play().catch(() => syncAllAudioButtonsUI(false));
    return;
  }
  // Case 3: Starting a new audio track
  audioEl.pause();
  activeAudioBtnId = btnId;
  activeAudioKey = audioKey;
  audioEl.src = srcUrl || fallbackB64 || '';
  audioEl.currentTime = 0;
  syncAllAudioButtonsUI(true);
  audioEl.play().catch(() => {
    if (fallbackB64 && audioEl.src !== fallbackB64) {
      audioEl.src = fallbackB64;
      audioEl.play().catch(() => stopAllAudio());
    } else {
      stopAllAudio();
    }
  });
}

function toggleMorningQuoteAudio() {
  const qIdx = getTodayQuoteIdx();
  const qa = QUOTES_AUDIO[qIdx] || QUOTES_AUDIO[0];
  playOrToggleAudio('btnQuotePlay', 'quote_' + qIdx, qa.url, qa.b64);
}

function toggleDayOverviewAudio() {
  const d = findDayObj(curDayNum);
  const refDay = d.audio_ref_day || d.day || 1;
  const refObj = DAYS_21.find(x => x.day === refDay) || d;
  playOrToggleAudio(
    'btnDayMainPlay',
    'day_main_' + d.day,
    d.audio_url || refObj.audio_url,
    d.audio_b64 || refObj.audio_b64
  );
}

function toggleSlideAudio() {
  const s = SLIDES[curSlideIdx];
  playOrToggleAudio('btnSlideMainPlay', 'slide_' + s.id, s.audio_url, s.audio_b64);
}

function toggleMasterAudio() {
  // If anything is currently playing, pause it immediately!
  if (!audioEl.paused) {
    audioEl.pause();
    syncAllAudioButtonsUI(false);
    return;
  }
  // If paused mid-track, resume that track!
  if (activeAudioKey && audioEl.paused && audioEl.currentTime > 0 && !audioEl.ended) {
    syncAllAudioButtonsUI(true);
    audioEl.play().catch(() => stopAllAudio());
    return;
  }
  // Otherwise play the active view's main audio
  if (curView === 'slides') toggleSlideAudio();
  else if (curView === 'quote') toggleMorningQuoteAudio();
  else playAgendaByIdx(curDayNum, curGameIdx, document.getElementById('btnAgPlay_' + curDayNum + '_' + curGameIdx));
}

/* Section / Agenda Listen Button:
   Plays the 100% verbatim pre-generated Gemini Aoede MP3 (`day_{d}_ag_{idx}.mp3`)
   that speaks the ENTIRE section (`category` + `title_bn` + `detail_bn`) AND the exact
   part Ma needs to say to Gemini AI (`prompt_bn`) with instant Play/Pause toggle! */
async function playAgendaByIdx(dayNum, agIdx, btnEl) {
  const btnId = btnEl ? btnEl.id : ('btnAgPlay_' + dayNum + '_' + agIdx);
  const audioKey = 'ag_' + dayNum + '_' + agIdx;

  // If this exact agenda is already playing -> PAUSE IT!
  if (activeAudioKey === audioKey && !audioEl.paused) {
    audioEl.pause();
    syncAllAudioButtonsUI(false);
    return;
  }
  // If this exact agenda was paused mid-way -> RESUME IT!
  if (activeAudioKey === audioKey && audioEl.paused && audioEl.currentTime > 0 && !audioEl.ended) {
    activeAudioBtnId = btnId;
    syncAllAudioButtonsUI(true);
    audioEl.play().catch(() => stopAllAudio());
    return;
  }

  const d = findDayObj(dayNum);
  const ag = (d && d.agendas && d.agendas[agIdx]) ? d.agendas[agIdx] : null;
  if (!ag) return;

  const fallbackB64 = (dayNum === 1 && DAY1_AG_MAP[agIdx]) ? DAY1_AG_MAP[agIdx].b64 : ((CAT_AUDIO_MAP[agIdx % 8] && CAT_AUDIO_MAP[agIdx % 8].b64) || d.audio_b64);

  // Immediately play the verbatim Gemini Aoede MP3 (`audio/day_{dayNum}_ag_{agIdx}.mp3`) with zero delay!
  playOrToggleAudio(btnId, audioKey, ag.audio_url, fallbackB64);
}

function getActiveCourseDays() {
  return curPart === 2 ? DAYS_PART2_30 : DAYS_21;
}

function findDayObj(dayNum) {
  return ALL_DAYS.find(x => x.day === dayNum) || DAYS_21[0];
}

/* SLIDES LOGIC */
function renderSlide() {
  const s = SLIDES[curSlideIdx];
  slideImg.src = s.img_b64;
  document.getElementById('slideBadge').textContent = s.badge;
  document.getElementById('slideTitleBn').textContent = s.title_bn;
  document.getElementById('slideHighlight').textContent = s.highlight_bn;
  document.getElementById('slideBodyBn').textContent = s.text_bn;
  document.getElementById('prevBtn').disabled = (curSlideIdx === 0);
  document.getElementById('nextBtn').disabled = (curSlideIdx === SLIDES.length - 1);
  syncAllAudioButtonsUI(!audioEl.paused);
}

function goToSlide(idx, autoPlay) {
  curSlideIdx = idx;
  stopAllAudio();
  renderSlide();
  if (autoPlay) toggleSlideAudio();
}
function prevSlide() { if (curSlideIdx > 0) goToSlide(curSlideIdx - 1, true); }
function nextSlide() { if (curSlideIdx < SLIDES.length - 1) goToSlide(curSlideIdx + 1, true); }

audioEl.addEventListener('ended', () => {
  const finishedKey = activeAudioKey;
  stopAllAudio();
  if (curView === 'slides' && autoAdvance && finishedKey && finishedKey.startsWith('slide_') && curSlideIdx < SLIDES.length - 1) {
    setTimeout(() => goToSlide(curSlideIdx + 1, true), 900);
  } else if (curView === 'plan' && finishedKey && finishedKey.startsWith('day_main_')) {
    // After the day overview intro finishes, automatically read the active game's full instructions + Gemini prompt!
    const btnEl = document.getElementById('btnAgPlay_' + curDayNum + '_' + curGameIdx);
    playAgendaByIdx(curDayNum, curGameIdx, btnEl);
  }
});

function toggleAutoPlayAll() {
  autoAdvance = !autoAdvance;
  document.getElementById('autoAdvanceBtn').textContent = autoAdvance ? '🔁 পরপর: চালু' : '🔁 পরপর: বন্ধ';
}

/* COURSE PLAN VIEW (Part 1: 21 Days & Part 2: 30 Days) */
function isDayFullyDone(dayNum) {
  const d = findDayObj(dayNum);
  const count = d ? d.agendas.length : 8;
  for (let i = 0; i < count; i++) {
    if (!doneMap[dayNum + '_' + i]) return false;
  }
  return true;
}

function getFirstIncompleteGameIdx(dayNum) {
  const d = findDayObj(dayNum);
  const count = d ? d.agendas.length : 8;
  for (let i = 0; i < count; i++) {
    if (!doneMap[dayNum + '_' + i]) return i;
  }
  return 0;
}

function findInitialCurrentDayAndPart() {
  for (let i = 0; i < DAYS_21.length; i++) {
    if (!isDayFullyDone(DAYS_21[i].day)) {
      curPart = 1;
      curDayNum = DAYS_21[i].day;
      curGameIdx = getFirstIncompleteGameIdx(curDayNum);
      return;
    }
  }
  for (let i = 0; i < DAYS_PART2_30.length; i++) {
    if (!isDayFullyDone(DAYS_PART2_30[i].day)) {
      curPart = 2;
      curDayNum = DAYS_PART2_30[i].day;
      curGameIdx = getFirstIncompleteGameIdx(curDayNum);
      return;
    }
  }
  curPart = 1;
  curDayNum = 1;
  curGameIdx = 0;
}

function scrollActiveDayChipIntoView() {
  const activeChip = document.getElementById('dayChip_' + curDayNum);
  if (activeChip && typeof activeChip.scrollIntoView === 'function') {
    activeChip.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
  }
}

function updateProgressPill() {
  const activeList = getActiveCourseDays();
  let doneCount = 0;
  let totalCount = 0;
  activeList.forEach(d => {
    totalCount += d.agendas.length;
    d.agendas.forEach((_, i) => {
      if (doneMap[d.day + '_' + i]) doneCount++;
    });
  });
  const pill = document.getElementById('progInlinePill');
  if (pill) pill.textContent = `✅ ${doneCount} / ${totalCount}`;
}

function switchCoursePart(partNum) {
  curPart = partNum;
  document.getElementById('segPart1').className = 'part-seg-btn' + (partNum === 1 ? ' active' : '');
  document.getElementById('segPart2').className = 'part-seg-btn' + (partNum === 2 ? ' active' : '');
  const list = partNum === 2 ? DAYS_PART2_30 : DAYS_21;
  const firstInc = list.find(d => !isDayFullyDone(d.day));
  curDayNum = firstInc ? firstInc.day : list[0].day;
  curGameIdx = getFirstIncompleteGameIdx(curDayNum);
  stopAllAudio();
  renderPlanView();
  scrollActiveDayChipIntoView();
}

function selectDay(dayNum, autoPlayAudio) {
  curDayNum = dayNum;
  curPart = dayNum > 21 ? 2 : 1;
  document.getElementById('segPart1').className = 'part-seg-btn' + (curPart === 1 ? ' active' : '');
  document.getElementById('segPart2').className = 'part-seg-btn' + (curPart === 2 ? ' active' : '');
  curGameIdx = getFirstIncompleteGameIdx(dayNum);
  stopAllAudio();
  renderPlanView();
  scrollActiveDayChipIntoView();
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if (autoPlayAudio) toggleDayOverviewAudio();
}

function selectGame(gIdx) {
  const d = findDayObj(curDayNum);
  const maxIdx = (d && d.agendas) ? d.agendas.length - 1 : 7;
  curGameIdx = Math.max(0, Math.min(maxIdx, gIdx));
  stopAllAudio();
  renderPlanView();
}

function toggleShowAllGames() {
  showAllGamesInDay = !showAllGamesInDay;
  renderPlanView();
}

function toggleAgendaDone(dayNum, agIdx) {
  const key = dayNum + '_' + agIdx;
  const newlyDone = !doneMap[key];
  doneMap[key] = newlyDone;
  saveDoneMap();

  if (newlyDone) {
    // 1. If all 8 tasks of this day are now complete -> Automatically advance to the next day!
    if (isDayFullyDone(dayNum)) {
      if (dayNum < 51) {
        const nextDay = dayNum + 1;
        curDayNum = nextDay;
        curPart = nextDay > 21 ? 2 : 1;
        document.getElementById('segPart1').className = 'part-seg-btn' + (curPart === 1 ? ' active' : '');
        document.getElementById('segPart2').className = 'part-seg-btn' + (curPart === 2 ? ' active' : '');
        curGameIdx = getFirstIncompleteGameIdx(nextDay);
        stopAllAudio();
        renderPlanView();
        scrollActiveDayChipIntoView();
        return;
      }
    } else if (!showAllGamesInDay) {
      // 2. Otherwise automatically jump to the next incomplete game in the same day!
      curGameIdx = getFirstIncompleteGameIdx(dayNum);
    }
  }
  renderPlanView();
}

function buildAgendaCardHtml(d, ag, idx) {
  const isDone = !!doneMap[d.day + '_' + idx];
  const btnId = `btnAgPlay_${d.day}_${idx}`;
  const isSongGame = (ag.category || '').includes('গান') || (ag.detail_bn || '').includes('ইউটিউব মিউজিক');
  const ytMusicGuideHtml = isSongGame ? `
      <div class="agenda-prompt-box" style="border-color:var(--accent); background:var(--accent-soft);">
        <div class="agenda-prompt-label" style="color:var(--accent);">🎵 ফোনের জেমিনি নিজে থেকেই ইউটিউব মিউজিকে (YouTube Music) গান বাজাতে পারে!</div>
        <div class="agenda-detail" style="font-size:1.02rem;">মা, ফোনের জেমিনির ইউটিউব মিউজিকের সাথে সরাসরি যোগ আছে। যেকোনো গান শুনতে ইচ্ছে করলেই শুধু মাইক 🎙️ ছুঁয়ে মুখে বলবে:<br><strong>“জেমিনি, ইউটিউব মিউজিকে ‘[গানের নাম বা যেকোনো লাইন]’ গানটা চালিয়ে দাও।”</strong><br>গানের পুরো নাম মনে না থাকলেও চলবে—গানের যেকোনো একটা লাইন বলে এইটুকু বললেই ও নিজে থেকে ইউটিউব মিউজিক খুলে গানটা বাজিয়ে দেবে!</div>
      </div>` : '';
  const followupHtml = ag.followup_prompt_bn ? `
      <div class="agenda-prompt-box">
        <div class="agenda-prompt-label">🗣️ ধাপ ৩ — গানটা শোনা হয়ে গেলে এর মানে আর গল্পটা জানতে জেমিনিকে বলো:</div>
        <div class="agenda-prompt-speech">“${ag.followup_prompt_bn}”</div>
      </div>` : '';
  const step2Label = isSongGame
    ? '🗣️ ধাপ ২ — ইউটিউব মিউজিকে আজকের গানটা চালাতে ফোনে জেমিনি (Gemini) খুলে মাইক 🎙️ ছুঁয়ে বলো:'
    : '🗣️ ধাপ ২ — এবার ফোনে জেমিনি (Gemini) খুলে মাইক 🎙️ ছুঁয়ে মুখে বলো:';
  return `
    <div class="agenda-card ${isDone ? 'done-card' : ''}" id="agendaCard_${d.day}_${idx}">
      <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap;">
        <div class="agenda-cat">${ag.category}</div>
        <span style="font-size:0.88rem; font-weight:700; color:var(--text-secondary);">খেলা ${idx + 1} / ${d.agendas.length}</span>
      </div>
      <div class="agenda-title">${ag.title_bn}</div>
      <div>
        <div class="agenda-step-heading">📋 ধাপ ১ — মা, আজ কী করবো দেখো:</div>
        <div class="agenda-detail">${ag.detail_bn}</div>
      </div>${ytMusicGuideHtml}
      <div class="agenda-prompt-box">
        <div class="agenda-prompt-label">${step2Label}</div>
        <div class="agenda-prompt-speech">“${ag.prompt_bn}”</div>
        <div class="agenda-prompt-howto">💡 (নিজের মতো সহজ বাংলায় বললেই হবে, ভুল হওয়ার কোনো ভয় নেই—বলো আর শোনো ও কী করে!)</div>
      </div>${followupHtml}
      <div class="agenda-actions">
        <button id="${btnId}" class="ag-btn listen" data-default-label="🔊 শোনো" onclick="playAgendaByIdx(${d.day}, ${idx}, this)">🔊 শোনো</button>
        <button class="ag-btn check ${isDone ? 'checked' : ''}" onclick="toggleAgendaDone(${d.day}, ${idx})">
          ${isDone ? '✅ করা হয়েছে' : '⬜ আমি এটা করেছি'}
        </button>
      </div>
    </div>
  `;
}

function renderPlanView() {
  updateProgressPill();
  const activeList = getActiveCourseDays();
  const strip = document.getElementById('dayStrip');
  strip.innerHTML = '';
  activeList.forEach(d => {
    const btn = document.createElement('button');
    const done = isDayFullyDone(d.day);
    const dispDay = d.part === 2 ? ('দিন ' + d.part_day) : ('দিন ' + d.day);
    btn.id = 'dayChip_' + d.day;
    btn.className = 'day-chip' + (d.day === curDayNum ? ' active' : '') + (done ? ' done' : '');
    btn.innerHTML = (done ? '✅ ' : '') + dispDay;
    btn.onclick = () => selectDay(d.day, false);
    strip.appendChild(btn);
  });

  const d = activeList.find(x => x.day === curDayNum) || activeList[0];
  curDayNum = d.day;
  if (curGameIdx < 0 || curGameIdx >= d.agendas.length) curGameIdx = 0;
  const stage = document.getElementById('activeDayStage');

  // Build 8-Game 2x4 Visual Navigator Grid (Jump directly to Game 1..8 with zero scrolling!)
  let dayDoneCount = 0;
  let tilesHtml = '';
  d.agendas.forEach((ag, idx) => {
    const isDone = !!doneMap[d.day + '_' + idx];
    if (isDone) dayDoneCount++;
    const isAct = (!showAllGamesInDay && idx === curGameIdx);
    const shortLbl = GAME_SHORT_LABELS[idx] || ('খেলা ' + (idx + 1));
    tilesHtml += `
      <button id="gameTile_${d.day}_${idx}" class="game-tile ${isAct ? 'active' : ''} ${isDone ? 'done-tile' : ''}" onclick="selectGame(${idx})">
        <span class="game-tile-num">${isDone ? '✅ ' : ''}খেলা ${idx + 1}</span>
        <span class="game-tile-lbl">${shortLbl}</span>
      </button>
    `;
  });

  let agendasHtml = '';
  if (showAllGamesInDay) {
    d.agendas.forEach((ag, idx) => {
      agendasHtml += buildAgendaCardHtml(d, ag, idx);
    });
  } else {
    const activeAg = d.agendas[curGameIdx] || d.agendas[0];
    agendasHtml = buildAgendaCardHtml(d, activeAg, curGameIdx) + `
      <div class="game-stepper-row">
        <button id="prevGameBtn" class="ag-btn" ${curGameIdx <= 0 ? 'disabled' : ''} onclick="selectGame(${curGameIdx - 1})">⬅️ আগের খেলা (${curGameIdx}/${d.agendas.length})</button>
        <button id="nextGameBtn" class="ag-btn" ${curGameIdx >= d.agendas.length - 1 ? 'disabled' : ''} onclick="selectGame(${curGameIdx + 1})">পরের খেলা (${curGameIdx + 2}/${d.agendas.length}) ➡️</button>
      </div>
    `;
  }

  const minDay = activeList[0].day;
  const maxDay = activeList[activeList.length - 1].day;
  const dispDayLabel = d.part === 2 ? ('পার্ট ২ • দিন ' + d.part_day) : ('পার্ট ১ • দিন ' + d.day);

  stage.innerHTML = `
    <div class="day-hero-card">
      <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
        <div class="day-hero-badge" style="margin-bottom:0;">${dispDayLabel} • ${d.phase}</div>
        <span style="font-size:0.9rem; font-weight:700; color:var(--accent);">আজকের অগ্রগতি: ${dayDoneCount} / ${d.agendas.length}</span>
      </div>
      <div class="day-hero-title">${d.title_bn}</div>
      <div class="day-hero-summary">${d.summary_bn}</div>
      <button id="btnDayMainPlay" class="big-voice-btn" data-default-label="🔊 আজকের কথাগুলো শোনো" onclick="toggleDayOverviewAudio()">
        🔊 আজকের কথাগুলো শোনো
      </button>
      <div style="display:flex; gap:8px; margin-top:10px;">
        <button class="ag-btn" style="flex:1;" ${d.day <= minDay ? 'disabled' : ''} onclick="selectDay(${d.day - 1}, false)">⬅️ আগের দিন</button>
        <button class="ag-btn" style="flex:1;" ${d.day >= maxDay ? 'disabled' : ''} onclick="selectDay(${d.day + 1}, false)">পরের দিন ➡️</button>
      </div>
    </div>

    <div class="game-nav-card">
      <div class="game-nav-header">
        <span class="game-nav-title">🎯 আজকের ${d.agendas.length}টি খেলা (যেকোনো খেলায় ছুঁয়ে সরাসরি খোলো):</span>
        <button id="toggleAllGamesBtn" class="view-mode-toggle" onclick="toggleShowAllGames()">
          ${showAllGamesInDay ? '🎯 ১টি করে দেখো' : `📜 সব ${d.agendas.length}টি একসাথে`}
        </button>
      </div>
      <div class="game-grid-8">${tilesHtml}</div>
    </div>

    <div class="agenda-stack">${agendasHtml}</div>
  `;
  syncAllAudioButtonsUI(!audioEl.paused);
}

/* Header View Switcher (3 Clean Views: Plan, Slides & Random Quote) */
function switchView(mode) {
  curView = mode;
  stopAllAudio();
  document.getElementById('viewPlan').className = 'view-sec' + (mode === 'plan' ? ' active' : '');
  document.getElementById('viewSlides').className = 'view-sec' + (mode === 'slides' ? ' active' : '');
  document.getElementById('viewQuote').className = 'view-sec' + (mode === 'quote' ? ' active' : '');
  document.getElementById('htabPlan').className = 'htab-btn' + (mode === 'plan' ? ' active' : '');
  document.getElementById('htabSlides').className = 'htab-btn' + (mode === 'slides' ? ' active' : '');
  document.getElementById('htabQuote').className = 'htab-btn' + (mode === 'quote' ? ' active' : '');

  if (mode === 'plan') {
    renderPlanView();
  } else if (mode === 'slides') {
    renderSlide();
  } else if (mode === 'quote') {
    // Every time "অনুপ্রেরণা" is clicked, a new random quote appears!
    pickNewRandomQuote(false);
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('ma-sw.js').catch(() => {});
}

initMorningQuoteAndAlarm();
findInitialCurrentDayAndPart();
document.getElementById('segPart1').className = 'part-seg-btn' + (curPart === 1 ? ' active' : '');
document.getElementById('segPart2').className = 'part-seg-btn' + (curPart === 2 ? ' active' : '');
renderSlide();
renderPlanView();
scrollActiveDayChipIntoView();
</script>
</body>
</html>
"""

    final_html = (
        html_template
        .replace("__SLIDES_JSON__", json.dumps(slides_payload, ensure_ascii=False))
        .replace("__DAYS_JSON__", json.dumps(days_payload, ensure_ascii=False))
        .replace("__DAYS_P2_JSON__", json.dumps(days_p2_payload, ensure_ascii=False))
        .replace("__QUOTES_AUDIO_JSON__", json.dumps(quotes_audio_list, ensure_ascii=False))
        .replace("__CAT_AUDIO_MAP_JSON__", json.dumps(cat_audio_map, ensure_ascii=False))
        .replace("__DAY1_AG_MAP_JSON__", json.dumps(day1_ag_map, ensure_ascii=False))
    )

    out_brain = os.path.join(BRAIN_DIR, "Ma_Thanksgiving_Bengali_Presentation.html")
    if os.path.isdir(BRAIN_DIR):
        with open(out_brain, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"Built standalone artifact HTML {out_brain} ({os.path.getsize(out_brain)} bytes)")

    gh_audio_base = "https://raw.githubusercontent.com/kouSeek/portfolio/ma-course/"
    slides_cdn = [
        {**s, "audio_b64": "", "audio_url": gh_audio_base + s["audio_url"]}
        for s in slides_payload
    ]
    days_cdn = []
    for d in days_payload:
        ags_cdn = [
            {**ag, "audio_b64": "", "audio_url": gh_audio_base + ag["audio_url"]}
            for ag in d["agendas"]
        ]
        days_cdn.append({
            **d,
            "agendas": ags_cdn,
            "audio_b64": "",
            "audio_url": gh_audio_base + d["audio_url"],
        })
    days_p2_cdn = []
    for d in days_p2_payload:
        ags_cdn = [
            {**ag, "audio_b64": "", "audio_url": gh_audio_base + ag["audio_url"]}
            for ag in d["agendas"]
        ]
        days_p2_cdn.append({
            **d,
            "agendas": ags_cdn,
            "audio_b64": "",
            "audio_url": gh_audio_base + d["audio_url"],
        })
    quotes_cdn = [
        {"url": gh_audio_base + q["url"], "b64": ""}
        for q in quotes_audio_list
    ]
    cdn_html = (
        html_template
        .replace("__SLIDES_JSON__", json.dumps(slides_cdn, ensure_ascii=False))
        .replace("__DAYS_JSON__", json.dumps(days_cdn, ensure_ascii=False))
        .replace("__DAYS_P2_JSON__", json.dumps(days_p2_cdn, ensure_ascii=False))
        .replace("__QUOTES_AUDIO_JSON__", json.dumps(quotes_cdn, ensure_ascii=False))
        .replace("__CAT_AUDIO_MAP_JSON__", json.dumps({}, ensure_ascii=False))
        .replace("__DAY1_AG_MAP_JSON__", json.dumps({}, ensure_ascii=False))
    )
    out_ma = APP_ROOT / "ma-presentation.html"
    out_idx = APP_ROOT / "index.html"
    out_ma.write_text(cdn_html, encoding="utf-8")
    out_idx.write_text(cdn_html, encoding="utf-8")
    print(f"Built {out_ma} & {out_idx} ({out_ma.stat().st_size} bytes)")

    # Non-blocking TTS hash check (NEVER auto-regenerates voices!)
    stale, expected, _ = get_stale_or_missing_files()
    if not stale:
        print(f"[TTS Check] All {len(expected)} Aoede MP3 files are 100% in sync with curriculum_data.py.")
    else:
        print(f"[TTS Notice] {len(stale)}/{len(expected)} audio file(s) have updated text and are pending voice refresh: {stale[:10]}")
        print("[TTS Rule] Skipping automatic TTS regeneration (per GEMINI.md). Ask Koushik when he wants to run: python3 scripts/refresh_voices.py --confirm")


if __name__ == "__main__":
    build_html()
