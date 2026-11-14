#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate modular, dedicated, standalone HTML pages for every book chapter.

Each chapter gets its own self-contained HTML page:
- 100% full chapter text directly embedded in HTML (zero network fetching for text).
- Embedded audio player with CacheStorage first and Blob fallback for iOS Safari.
- Word-by-word real-time karaoke highlighting.
- Tap/click any word to jump audio playback to that exact word.
- Next / Previous chapter navigation and Back to Library links.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = APP_ROOT / "assets" / "books_catalog.json"
AUDIO_INDEX_PATH = APP_ROOT / "assets" / "books_audio_index.json"
TEXT_VAULT_PATH = APP_ROOT / "assets" / "books_text_vault.json"
CHAPTERS_DIR = APP_ROOT / "chapters"

GH_RAW_AUDIO_BASE = "https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/"


def get_clean_slug(b: dict) -> str:
    title = b.get("title", "")
    slug = b.get("slug", "")
    if "gene" in title.lower():
        return "the-gene"
    if "code book" in title.lower():
        return "the-code-book"
    clean = re.sub(r"^\d+[a-z]?_", "", slug.lower())
    clean = re.sub(r"_+", "-", clean)
    clean = re.sub(r"[^\w\-]", "", clean).strip("-")
    return clean or slug.lower()


def find_audio_track(audio_files: list[dict], book_slug: str, book_title: str, track_type: str, index: int) -> dict | None:
    b_slug = book_slug.lower()
    b_title = book_title.lower()
    for f in audio_files:
        f_slug = (f.get("slug") or "").lower()
        f_title = (f.get("bookTitle") or "").lower()
        slug_match = (
            f_slug == b_slug
            or f_slug.replace("-", "_") in b_slug
            or f_slug in b_slug
            or b_slug in f_slug
        )
        title_match = bool(f_title and (f_title in b_title or b_title in f_title))
        if (slug_match or title_match) and f.get("trackType") == track_type and f.get("index") == index:
            return f
    return None


def render_markdown_to_html(md_text: str) -> tuple[str, list[dict], int]:
    lines = (md_text or "").splitlines()
    body_parts = []
    in_quote = False
    word_index = 0
    words_list = []

    def wrap_words(text: str) -> str:
        nonlocal word_index
        tokens = re.split(r"(\s+)", text)
        res = []
        for tok in tokens:
            if not tok or re.match(r"^\s+$", tok):
                res.append(tok)
                continue
            clean = re.sub(r"[*_#`~\[\]()]", "", tok)
            w_idx = word_index
            word_index += 1
            weight = max(1, len(clean))
            words_list.append({"idx": w_idx, "word": clean, "weight": weight})
            escaped_tok = html.escape(tok)
            res.append(f'<span class="k-word" data-word-idx="{w_idx}" id="w_{w_idx}">{escaped_tok}</span>')
        return "".join(res)

    for line in lines:
        line_s = line.strip()
        if not line_s:
            if in_quote:
                body_parts.append("</blockquote>")
                in_quote = False
            continue

        if line_s.startswith(">"):
            if not in_quote:
                body_parts.append('<blockquote class="chapter-spoken-brief">')
                in_quote = True
            quote_text = re.sub(r"^>\s*", "", line_s)
            body_parts.append(f"<p>{wrap_words(quote_text)}</p>")
        elif line_s.startswith("### "):
            if in_quote:
                body_parts.append("</blockquote>")
                in_quote = False
            body_parts.append(f'<h3 class="section-heading">{wrap_words(line_s[4:])}</h3>')
        elif line_s.startswith("## "):
            if in_quote:
                body_parts.append("</blockquote>")
                in_quote = False
            body_parts.append(f'<h2 class="chapter-prose-title">{wrap_words(line_s[3:])}</h2>')
        elif line_s.startswith("# "):
            if in_quote:
                body_parts.append("</blockquote>")
                in_quote = False
            body_parts.append(f'<h1 class="chapter-prose-title">{wrap_words(line_s[2:])}</h1>')
        else:
            if in_quote:
                body_parts.append("</blockquote>")
                in_quote = False
            body_parts.append(f"<p>{wrap_words(line_s)}</p>")

    if in_quote:
        body_parts.append("</blockquote>")

    cum = 0
    for w in words_list:
        w["cum"] = cum
        cum += w["weight"]
    total_weight = max(1, cum)

    return "\n".join(body_parts), words_list, total_weight


def build_chapter_html(
    book: dict,
    clean_slug: str,
    track_type: str,
    index: int,
    total_items: int,
    chapter_data: dict,
    audio_track: dict | None,
    prev_link: str,
    next_link: str,
) -> str:
    book_title = book.get("title", "Book")
    label = chapter_data.get("label", f"Chapter {index}")
    pages = chapter_data.get("pages", "")
    page_count = chapter_data.get("pageCount")
    if not page_count and pages and "-" in str(pages):
        try:
            parts = str(pages).split("-")
            page_count = max(1, int(parts[1]) - int(parts[0]) + 1)
        except Exception:
            page_count = 1
    page_count = page_count or 1

    volume_pct = chapter_data.get("volumePct", 0.0)
    est_minutes = chapter_data.get("estMinutes", chapter_data.get("duration_min", 15))
    effort_label = chapter_data.get("effortLabel", f"{est_minutes} min")

    full_book_pages = book.get("full_book_pages") or book.get("pages", 0)
    full_book_effort = book.get("full_book_effort_label") or book.get("full_time_label", "")
    adhd_pages = book.get("adhd_total_pages", 0)
    adhd_effort = book.get("adhd_effort_label") or book.get("adhd_time_label", "")
    adhd_vol_pct = book.get("adhd_volume_pct", 0.0)
    pruned_pct = book.get("pruned_pct", 0.0)

    bar_width = min(100, max(4, round(float(volume_pct) * 2.2))) if volume_pct else 8

    duration_min = est_minutes
    brief = chapter_data.get("brief", "")
    content = chapter_data.get("content", brief)

    body_html, words_list, total_weight = render_markdown_to_html(content)
    words_json = json.dumps([{"c": w["cum"], "w": w["weight"]} for w in words_list])

    audio_url = f"{GH_RAW_AUDIO_BASE}{audio_track['url']}" if audio_track else ""
    has_audio = bool(audio_url)

    step_title_short = f"Step {index}" if track_type == "adhd" else f"Ch {index}"
    track_type_name = "⚡ Non-Linear Core Cut" if track_type == "adhd" else "📖 Full Book Chapter"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <meta name="theme-color" content="#0F172A" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <title>{html.escape(step_title_short)} • {html.escape(book_title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,600&family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400;1,6..72,500&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #F8FAFC;
      --surface: #FFFFFF;
      --surface-subtle: #F1F5F9;
      --border: #E2E8F0;
      --ink: #0F172A;
      --ink-muted: #64748B;
      --accent: #4F46E5;
      --accent-light: #EEF2FF;
      --emerald: #10B981;
      --safe-top: env(safe-area-inset-top, 0px);
      --safe-bottom: env(safe-area-inset-bottom, 0px);
    }}
    body.dark-mode {{
      --bg: #0F172A;
      --surface: #1E293B;
      --surface-subtle: #334155;
      --border: #334155;
      --ink: #F8FAFC;
      --ink-muted: #94A3B8;
      --accent: #818CF8;
      --accent-light: rgba(99, 102, 241, 0.15);
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg);
      color: var(--ink);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      padding-top: calc(var(--safe-top) + 56px);
      padding-bottom: calc(var(--safe-bottom) + 110px);
      transition: background 0.2s ease, color 0.2s ease;
    }}
    /* Topbar */
    .topbar {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: calc(var(--safe-top) + 56px);
      padding-top: var(--safe-top);
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-left: 12px;
      padding-right: 12px;
      z-index: 50;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }}
    .back-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--ink);
      text-decoration: none;
      padding: 6px 10px;
      border-radius: 8px;
      background: var(--surface-subtle);
    }}
    .top-title {{
      font-size: 0.88rem;
      font-weight: 700;
      text-align: center;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      max-width: 55%;
    }}
    .top-actions {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .btn-icon {{
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      color: var(--ink);
      font-size: 0.82rem;
      font-weight: 600;
      padding: 5px 8px;
      border-radius: 6px;
      cursor: pointer;
    }}

    /* Main Container */
    .reader-container {{
      max-width: 760px;
      width: 100%;
      margin: 0 auto;
      padding: 20px 18px;
    }}

    /* Chapter Header Banner */
    .chapter-hero {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 20px;
      margin-bottom: 24px;
      box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }}
    .hero-book-title {{
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
    }}
    .hero-chapter-title {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 1.45rem;
      font-weight: 700;
      line-height: 1.35;
      margin-bottom: 12px;
    }}
    .hero-meta-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 12px;
    }}
    .meta-chip {{
      font-size: 0.76rem;
      font-weight: 600;
      padding: 3px 9px;
      border-radius: 999px;
      background: var(--surface-subtle);
      color: var(--ink-muted);
      border: 1px solid var(--border);
    }}
    .meta-chip.primary {{
      background: var(--accent-light);
      color: var(--accent);
      border-color: rgba(99, 102, 241, 0.25);
    }}
    .meta-chip.effort {{
      color: #D97706;
      background: rgba(245, 158, 11, 0.1);
      border-color: rgba(245, 158, 11, 0.25);
    }}
    .meta-chip.voice {{
      background: #ECFDF5;
      color: #059669;
      border-color: rgba(16, 185, 129, 0.25);
    }}
    .hero-distribution-bar {{
      margin: 10px 0 12px;
      padding: 10px 12px;
      background: var(--surface-subtle);
      border-radius: 8px;
      border: 1px solid var(--border);
    }}
    .hero-dist-info {{
      display: flex;
      justify-content: space-between;
      font-size: 0.78rem;
      color: var(--ink-muted);
      margin-bottom: 6px;
    }}
    .hero-dist-info strong {{
      color: var(--ink);
    }}
    .book-toc-vol-bar-track {{
      width: 100%;
      height: 6px;
      background: rgba(148, 163, 184, 0.2);
      border-radius: 3px;
      overflow: hidden;
    }}
    .book-toc-vol-bar-fill {{
      height: 100%;
      border-radius: 3px;
      transition: width 0.3s ease;
    }}
    .book-toc-vol-bar-fill.adhd {{
      background: #10B981;
    }}
    .book-toc-vol-bar-fill.author {{
      background: #6366F1;
    }}
    .hero-curation-pill {{
      font-size: 0.78rem;
      color: #059669;
      background: #ECFDF5;
      padding: 4px 10px;
      border-radius: 6px;
      margin-bottom: 12px;
      display: inline-block;
      font-weight: 500;
      border: 1px solid rgba(16, 185, 129, 0.2);
    }}
    .hero-brief {{
      font-size: 0.95rem;
      line-height: 1.6;
      color: var(--ink);
      border-top: 1px solid var(--border);
      padding-top: 12px;
    }}

    /* Top Play Button Card */
    .hero-listen-card {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      background: var(--accent-light);
      border: 1px solid rgba(79, 70, 229, 0.2);
      border-radius: 12px;
      padding: 12px 16px;
      margin-top: 14px;
    }}
    .btn-top-listen {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 0.95rem;
      font-weight: 700;
      background: var(--accent);
      color: #FFFFFF;
      border: none;
      padding: 10px 18px;
      border-radius: 999px;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(79, 70, 229, 0.35);
      transition: all 0.15s ease;
    }}
    .btn-top-listen:hover {{
      transform: translateY(-1px);
    }}

    /* Reading Typography */
    .prose-body {{
      font-family: 'Newsreader', Georgia, serif;
      font-size: 1.12rem;
      line-height: 1.85;
      color: var(--ink);
    }}
    .prose-body h1, .prose-body h2, .prose-body h3 {{
      font-family: 'Playfair Display', Georgia, serif;
      margin-top: 28px;
      margin-bottom: 12px;
      line-height: 1.35;
    }}
    .prose-body p {{
      margin-bottom: 18px;
    }}
    .prose-body blockquote {{
      border-left: 3.5px solid var(--accent);
      margin: 18px 0;
      padding: 10px 18px;
      color: var(--ink-muted);
      background: var(--surface-subtle);
      border-radius: 0 8px 8px 0;
      font-style: italic;
    }}

    /* Karaoke Highlighting */
    .k-word {{
      display: inline;
      border-radius: 4px;
      padding: 0 2px;
      transition: background-color 0.12s ease, color 0.12s ease, box-shadow 0.12s ease;
      cursor: pointer;
    }}
    .k-word:hover {{
      background-color: rgba(99, 102, 241, 0.15);
    }}
    .k-word.active-word {{
      background-color: #FEF08A !important;
      color: #0F172A !important;
      font-weight: 700;
      border-radius: 4px;
      box-shadow: 0 0 0 2px #FEF08A, 0 2px 6px rgba(0, 0, 0, 0.15);
    }}
    body.dark-mode .k-word.active-word {{
      background-color: #6366F1 !important;
      color: #FFFFFF !important;
      box-shadow: 0 0 0 2px #6366F1, 0 2px 6px rgba(0, 0, 0, 0.35);
    }}

    /* Chapter Footer Navigation */
    .nav-footer {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-top: 36px;
      padding-top: 20px;
      border-top: 1px solid var(--border);
    }}
    .nav-footer a {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--ink);
      text-decoration: none;
      padding: 10px 16px;
      border-radius: 10px;
      background: var(--surface);
      border: 1px solid var(--border);
    }}
    .nav-footer a.primary {{
      background: var(--accent);
      color: #FFFFFF;
      border-color: var(--accent);
    }}

    /* Sticky Bottom Player Bar */
    .sticky-player {{
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--surface);
      border-top: 1.5px solid var(--border);
      padding: 10px 16px calc(var(--safe-bottom) + 10px);
      z-index: 60;
      box-shadow: 0 -4px 20px rgba(15, 23, 42, 0.08);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .player-progress-wrap {{
      display: flex;
      align-items: center;
      gap: 8px;
      width: 100%;
      max-width: 760px;
      margin: 0 auto;
    }}
    .player-time {{
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--ink-muted);
      min-width: 38px;
      font-variant-numeric: tabular-nums;
    }}
    .player-time.right {{
      text-align: right;
    }}
    .player-slider {{
      flex: 1;
      height: 4px;
      -webkit-appearance: none;
      appearance: none;
      background: var(--border);
      border-radius: 999px;
      outline: none;
    }}
    .player-slider::-webkit-slider-thumb {{
      -webkit-appearance: none;
      appearance: none;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: var(--accent);
      cursor: pointer;
    }}
    .player-controls {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      max-width: 760px;
      margin: 0 auto;
    }}
    .player-info {{
      flex: 1;
      min-width: 0;
      margin-right: 12px;
    }}
    .player-info-title {{
      font-size: 0.88rem;
      font-weight: 700;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .player-info-sub {{
      font-size: 0.75rem;
      color: var(--ink-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .player-btns {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .btn-play-circle {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: var(--accent);
      color: #FFFFFF;
      border: none;
      font-size: 1.15rem;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(79, 70, 229, 0.35);
    }}
    .btn-skip {{
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      color: var(--ink);
      font-size: 0.82rem;
      font-weight: 600;
      padding: 6px 10px;
      border-radius: 8px;
      cursor: pointer;
    }}

    /* Toast */
    .toast-msg {{
      position: fixed;
      top: calc(var(--safe-top) + 60px);
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.92);
      color: #FFFFFF;
      padding: 8px 16px;
      border-radius: 999px;
      font-size: 0.85rem;
      font-weight: 600;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
      z-index: 100;
    }}
    .toast-msg.active {{
      opacity: 1;
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <a class="back-btn" id="navBackBtn" href="../../books.html">← Library</a>
    <div class="top-title">{html.escape(book_title)}</div>
    <div class="top-actions">
      <button class="btn-icon" id="btnFontSmaller">A-</button>
      <button class="btn-icon" id="btnFontLarger">A+</button>
      <button class="btn-icon" id="btnToggleTheme">🎨</button>
    </div>
  </header>

  <main class="reader-container">
    <article class="chapter-hero">
      <div class="hero-book-title">{html.escape(book_title)}</div>
      <h1 class="hero-chapter-title">{html.escape(label)}</h1>
      <div class="hero-meta-row">
        <span class="meta-chip primary">{html.escape(track_type_name)} ({html.escape(step_title_short)} of {total_items})</span>
        <span class="meta-chip">📄 Pages {html.escape(str(pages) or "N/A")} ({page_count}p · {volume_pct}% vol)</span>
        <span class="meta-chip effort">⏱️ ~{est_minutes}m effort ({effort_label})</span>
        {"<span class='meta-chip voice'>🎙️ Voice Track Ready</span>" if has_audio else ""}
      </div>

      <div class="hero-distribution-bar">
        <div class="hero-dist-info">
          <span>Volume Share: <strong>{page_count} pages ({volume_pct}% of book)</strong></span>
          <span>Full Book: <strong>{full_book_pages} pages ({full_book_effort})</strong></span>
        </div>
        <div class="book-toc-vol-bar-track">
          <div class="book-toc-vol-bar-fill {track_type}" style="width: {bar_width}%;"></div>
        </div>
      </div>
      {f'<div class="hero-curation-pill">⚡ ADHD Core Cut: {adhd_pages} pages total ({adhd_effort}) · {pruned_pct}% filler pruned for maximum flow</div>' if (track_type == 'adhd' and pruned_pct > 0) else ''}

      {f'<div class="hero-brief"><strong>Core Takeaway:</strong> {html.escape(brief)}</div>' if brief else ""}

      {f'''
      <div class="hero-listen-card">
        <div>
          <div style="font-weight: 700; font-size: 0.9rem;">🎙️ Expressive Voice Audiobook</div>
          <div style="font-size: 0.78rem; color: var(--ink-muted);">Aoede UK Female · Real-time karaoke text sync</div>
        </div>
        <button class="btn-top-listen" id="btnTopListen" onclick="toggleAudioPlay()">
          ▶️ Listen
        </button>
      </div>
      ''' if has_audio else '''
      <div style="margin-top: 14px; font-size: 0.85rem; color: var(--ink-muted); background: var(--surface-subtle); padding: 10px 14px; border-radius: 8px;">
        📖 Distraction-free reading mode. Voice track is in generation queue.
      </div>
      '''}
    </article>

    <section class="prose-body" id="proseBody">
      {body_html}
    </section>

    <nav class="nav-footer">
      {f'<a href="{prev_link}">← Previous Chapter</a>' if prev_link else '<span style="flex:1;"></span>'}
      <a class="primary" href="../../books.html">📚 All Books</a>
      {f'<a href="{next_link}">Next Chapter →</a>' if next_link else '<span style="flex:1;"></span>'}
    </nav>
  </main>

  <!-- Sticky Player Bar -->
  <div class="sticky-player" id="stickyPlayer">
    <div class="player-progress-wrap">
      <span class="player-time" id="playerCurrentTime">0:00</span>
      <input type="range" class="player-slider" id="playerScrubber" min="0" max="100" value="0" />
      <span class="player-time right" id="playerTotalTime">0:00</span>
    </div>
    <div class="player-controls">
      <div class="player-info">
        <div class="player-info-title">{html.escape(label)}</div>
        <div class="player-info-sub">{html.escape(book_title)} · {html.escape(step_title_short)}</div>
      </div>
      <div class="player-btns">
        <button class="btn-skip" id="btnRewind15" title="Rewind 15s">⏪ 15s</button>
        <button class="btn-play-circle" id="btnBottomPlay" onclick="toggleAudioPlay()">▶</button>
        <button class="btn-skip" id="btnForward15" title="Forward 15s">⏩ 15s</button>
      </div>
    </div>
  </div>

  <div class="toast-msg" id="toastMsg"></div>
  <audio id="playerAudio" preload="auto" playsinline webkit-playsinline></audio>

  <script>
    const AUDIO_URL = "{audio_url}";
    const CACHE_NAME = "kortex-books-v1";
    const WORDS_DATA = {words_json};
    const TOTAL_WEIGHT = {total_weight};

    let audioEl = document.getElementById("playerAudio");
    let activeBlobUrl = null;
    let audioLoaded = false;
    let karaokeActive = false;
    let activeWordIdx = -1;
    let readerFontSize = 1.12;

    function showToast(msg) {{
      const t = document.getElementById("toastMsg");
      t.textContent = msg;
      t.classList.remove("active");
      void t.offsetWidth;
      t.classList.add("active");
      setTimeout(() => t.classList.remove("active"), 2500);
    }}

    function formatSeconds(sec) {{
      if (!sec || isNaN(sec)) return "0:00";
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return `${{m}}:${{s < 10 ? "0" : ""}}${{s}}`;
    }}

    let _screenWakeLock = null;
    async function requestScreenWakeLock() {{
      try {{
        if ("wakeLock" in navigator && !(_screenWakeLock && !_screenWakeLock.released)) {{
          _screenWakeLock = await navigator.wakeLock.request("screen");
        }}
      }} catch (e) {{}}
    }}

    function syncPlayButtonUi(isPlaying) {{
      const bBtn = document.getElementById("btnBottomPlay");
      const tBtn = document.getElementById("btnTopListen");
      if (bBtn) bBtn.textContent = isPlaying ? "⏸" : "▶";
      if (tBtn) tBtn.textContent = isPlaying ? "⏸ Pause" : "▶️ Listen";
    }}

    async function toggleAudioPlay() {{
      if (!AUDIO_URL) {{
        showToast("Voice track not yet available for this chapter.");
        return;
      }}

      if (!audioEl.paused && audioLoaded) {{
        audioEl.pause();
        return;
      }}

      if (audioLoaded && audioEl.paused && audioEl.src) {{
        try {{
          await audioEl.play();
          return;
        }} catch (e) {{
          console.warn("Resume failed, reloading src...", e);
        }}
      }}

      showToast("Loading voice track...");
      let resolvedSrc = null;

      // 1. Try CacheStorage
      if ("caches" in window) {{
        try {{
          const cache = await caches.open(CACHE_NAME);
          const cached = await cache.match(AUDIO_URL);
          if (cached) {{
            const blob = await cached.blob();
            activeBlobUrl = URL.createObjectURL(blob);
            resolvedSrc = activeBlobUrl;
          }}
        }} catch (ce) {{}}
      }}

      // 2. If not in cache, try direct URL
      if (!resolvedSrc) {{
        resolvedSrc = AUDIO_URL;
      }}

      audioEl.src = resolvedSrc;
      audioEl.load();

      try {{
        await audioEl.play();
        audioLoaded = true;
        karaokeActive = true;
        requestScreenWakeLock();
      }} catch (err) {{
        console.warn("Direct play failed, trying Blob fetch fallback (iOS Safari / octet-stream workaround)...", err);
        try {{
          const resp = await fetch(AUDIO_URL, {{ mode: "cors" }});
          if (resp.ok) {{
            const buf = await resp.arrayBuffer();
            const audioBlob = new Blob([buf], {{ type: "audio/mpeg" }});
            activeBlobUrl = URL.createObjectURL(audioBlob);
            audioEl.src = activeBlobUrl;
            audioEl.load();
            await audioEl.play();
            audioLoaded = true;
            karaokeActive = true;
            requestScreenWakeLock();

            // Save to CacheStorage for offline flights
            if ("caches" in window) {{
              caches.open(CACHE_NAME).then(c => c.put(AUDIO_URL, new Response(audioBlob)));
            }}
          }} else {{
            throw new Error("HTTP " + resp.status);
          }}
        }} catch (blobErr) {{
          console.error("Audio playback error:", blobErr);
          showToast("⚠️ Could not load audio. Check internet or tap ⚙️ in Library.");
        }}
      }}
    }}

    // Sync Karaoke Word
    function syncKaraokeWord() {{
      if (!karaokeActive || !WORDS_DATA.length || TOTAL_WEIGHT <= 0) return;
      const dur = audioEl.duration;
      if (!Number.isFinite(dur) || dur <= 0) return;
      const cur = audioEl.currentTime;
      const progress = Math.min(1.0, Math.max(0, cur / dur));
      const targetWeight = progress * TOTAL_WEIGHT;

      let low = 0;
      let high = WORDS_DATA.length - 1;
      let foundIdx = 0;
      while (low <= high) {{
        const mid = (low + high) >> 1;
        if (WORDS_DATA[mid].c <= targetWeight) {{
          foundIdx = mid;
          low = mid + 1;
        }} else {{
          high = mid - 1;
        }}
      }}

      if (foundIdx !== activeWordIdx) {{
        if (activeWordIdx >= 0) {{
          const prev = document.getElementById(`w_${{activeWordIdx}}`);
          if (prev) prev.classList.remove("active-word");
        }}
        activeWordIdx = foundIdx;
        const curEl = document.getElementById(`w_${{activeWordIdx}}`);
        if (curEl) {{
          curEl.classList.add("active-word");
          const r = curEl.getBoundingClientRect();
          const targetY = window.innerHeight * 0.40;
          if (r.top < 80 || r.top > window.innerHeight * 0.65) {{
            window.scrollBy({{
              top: r.top - targetY,
              behavior: "smooth"
            }});
          }}
        }}
      }}
    }}

    // Audio Listeners
    audioEl.addEventListener("play", () => {{
      syncPlayButtonUi(true);
      karaokeActive = true;
    }});
    audioEl.addEventListener("pause", () => {{
      syncPlayButtonUi(false);
    }});
    audioEl.addEventListener("ended", () => {{
      syncPlayButtonUi(false);
      karaokeActive = false;
      if (activeWordIdx >= 0) {{
        const prev = document.getElementById(`w_${{activeWordIdx}}`);
        if (prev) prev.classList.remove("active-word");
      }}
      showToast("Chapter complete.");
    }});
    audioEl.addEventListener("timeupdate", () => {{
      const cur = audioEl.currentTime || 0;
      const dur = audioEl.duration || 0;
      document.getElementById("playerCurrentTime").textContent = formatSeconds(cur);
      document.getElementById("playerTotalTime").textContent = formatSeconds(dur);
      if (dur > 0) {{
        document.getElementById("playerScrubber").value = (cur / dur) * 100;
      }}
      if (karaokeActive) {{
        syncKaraokeWord();
      }}
    }});

    // Scrubber
    document.getElementById("playerScrubber").addEventListener("input", (e) => {{
      const dur = audioEl.duration || 0;
      if (dur > 0) {{
        audioEl.currentTime = (e.target.value / 100) * dur;
      }}
    }});
    document.getElementById("btnRewind15").addEventListener("click", () => {{
      audioEl.currentTime = Math.max(0, audioEl.currentTime - 15);
    }});
    document.getElementById("btnForward15").addEventListener("click", () => {{
      audioEl.currentTime = Math.min(audioEl.duration || 0, audioEl.currentTime + 15);
    }});

    // Tap/Click any word to seek audio
    document.getElementById("proseBody").addEventListener("click", (e) => {{
      const span = e.target.closest(".k-word");
      if (!span) return;
      const wIdx = parseInt(span.getAttribute("data-word-idx"), 10);
      if (Number.isFinite(wIdx) && WORDS_DATA[wIdx]) {{
        const dur = audioEl.duration;
        if (Number.isFinite(dur) && dur > 0 && TOTAL_WEIGHT > 0) {{
          const targetTime = (WORDS_DATA[wIdx].c / TOTAL_WEIGHT) * dur;
          audioEl.currentTime = targetTime;
          if (audioEl.paused) {{
            toggleAudioPlay();
          }}
        }} else if (!audioLoaded) {{
          toggleAudioPlay();
        }}
      }}
    }});

    // Font Controls
    document.getElementById("btnFontSmaller").addEventListener("click", () => {{
      readerFontSize = Math.max(0.9, readerFontSize - 0.1);
      document.getElementById("proseBody").style.fontSize = `${{readerFontSize}}rem`;
    }});
    document.getElementById("btnFontLarger").addEventListener("click", () => {{
      readerFontSize = Math.min(1.5, readerFontSize + 0.1);
      document.getElementById("proseBody").style.fontSize = `${{readerFontSize}}rem`;
    }});

    // Theme Toggle
    document.getElementById("btnToggleTheme").addEventListener("click", () => {{
      document.body.classList.toggle("dark-mode");
      const isDark = document.body.classList.contains("dark-mode");
      localStorage.setItem("kortex_theme", isDark ? "dark" : "light");
    }});
    if (localStorage.getItem("kortex_theme") === "dark") {{
      document.body.classList.add("dark-mode");
    }}

    // GitHub Preview Link Hydration
    (function hydratePageLinks() {{
      try {{
        if (typeof location === "undefined" || typeof document === "undefined") return;
        const isHtmlPreview = /htmlpreview\\.github\\.io/i.test(location.hostname || "") || /github\\.com[\\/]kouSeek[\\/]portfolio[\\/]blob[\\/]/i.test(location.search || "");
        if (!isHtmlPreview) return;
        const m = (location.search || "").match(/https:[\\/][\\/]github\\.com[\\/]kouSeek[\\/]portfolio[\\/]blob[\\/]([^/]+)[\\/]/i);
        const branch = (m && m[1]) ? m[1] : "kalyani-reels";
        
        document.querySelectorAll("a[href]").forEach(a => {{
          const href = a.getAttribute("href");
          if (!href || href.startsWith("http") || href.startsWith("#")) return;
          // Resolve relative path against current directory: chapters/<clean_slug>/
          let targetPath = "";
          if (href.startsWith("../../")) {{
            targetPath = href.replace("../../", "");
          }} else {{
            targetPath = "chapters/{clean_slug}/" + href;
          }}
          a.href = "https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/" + branch + "/" + targetPath;
        }});
      }} catch (e) {{}}
    }})();

    // Offline Navigation Interceptor: When in offline flight mode, intercept Back to Library and Chapter links
    document.addEventListener("click", async (e) => {{
      const a = e.target.closest("a[href*='books.html'], a[href*='step_'], a[href*='ch_']");
      if (!a) return;
      const href = a.getAttribute("href");
      if (!href) return;

      const isOffline = (!navigator.onLine || window.__FORCE_OFFLINE__);
      if (isOffline) {{
        e.preventDefault();
        let targetKey = href;
        if (href.includes("books.html")) {{
          targetKey = "books.html";
        }} else if (href.includes("step_") || href.includes("ch_")) {{
          const fname = href.split("/").pop();
          targetKey = `chapters/{clean_slug}/${{fname}}`;
        }}
        if ("caches" in window) {{
          try {{
            const cache = await caches.open(CACHE_NAME);
            let cachedResp = await cache.match(targetKey) || await cache.match(href);
            if (!cachedResp && href.includes("books.html")) {{
              cachedResp = await cache.match("./books.html") || await cache.match("books.html");
            }}
            if (cachedResp) {{
              const htmlText = await cachedResp.text();
              document.open();
              document.write(htmlText);
              document.close();
              try {{ window.history.pushState({{ path: targetKey }}, "", targetKey); }} catch (_e) {{}}
              return;
            }}
          }} catch (ce) {{}}
        }}
      }}
    }});

    // Register Service Worker for offline flight mode
    if (typeof navigator !== "undefined" && "serviceWorker" in navigator) {{
      navigator.serviceWorker.register("../../kalyani-sw.js", {{ scope: "../../" }}).catch(() => {{}});
    }}
  </script>
</body>
</html>
"""


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8")) if CATALOG_PATH.is_file() else []
    audio_index = json.loads(AUDIO_INDEX_PATH.read_text(encoding="utf-8")) if AUDIO_INDEX_PATH.is_file() else {}
    vault = json.loads(TEXT_VAULT_PATH.read_text(encoding="utf-8")) if TEXT_VAULT_PATH.is_file() else {}
    audio_files = audio_index.get("files", [])

    CHAPTERS_DIR.mkdir(exist_ok=True)
    total_generated = 0

    for book in catalog:
        clean_slug = get_clean_slug(book)
        book_dir = CHAPTERS_DIR / clean_slug
        book_dir.mkdir(exist_ok=True)

        # Lookup in text vault
        vault_key = (book.get("slug") or book.get("filename", "")).replace(".pdf", "").replace(".PDF", "").lower()
        book_text_data = vault.get(vault_key, {})
        if not book_text_data:
            # Fallback by matching clean_slug
            for vk, vd in vault.items():
                if clean_slug in vk or vk in clean_slug:
                    book_text_data = vd
                    break

        adhd_vault = book_text_data.get("adhd", {})
        author_vault = book_text_data.get("author", {})

        # 1. Generate ADHD Steps
        adhd_items = book.get("adhd_segments") or []
        for idx, item in enumerate(adhd_items, start=1):
            v_item = adhd_vault.get(str(idx), {})
            combined_item = {**item, **v_item}
            audio_track = find_audio_track(audio_files, clean_slug, book.get("title", ""), "adhd", idx)

            prev_link = f"step_{idx - 1}.html" if idx > 1 else ""
            next_link = f"step_{idx + 1}.html" if idx < len(adhd_items) else ""

            html_str = build_chapter_html(
                book=book,
                clean_slug=clean_slug,
                track_type="adhd",
                index=idx,
                total_items=len(adhd_items),
                chapter_data=combined_item,
                audio_track=audio_track,
                prev_link=prev_link,
                next_link=next_link,
            )
            out_file = book_dir / f"step_{idx}.html"
            out_file.write_text(html_str, encoding="utf-8")
            total_generated += 1

        # 2. Generate Author Chapters
        author_items = book.get("author_chapters") or []
        for idx, item in enumerate(author_items, start=1):
            v_item = author_vault.get(str(idx), {})
            combined_item = {**item, **v_item}
            audio_track = find_audio_track(audio_files, clean_slug, book.get("title", ""), "author", idx)

            prev_link = f"ch_{idx - 1}.html" if idx > 1 else ""
            next_link = f"ch_{idx + 1}.html" if idx < len(author_items) else ""

            html_str = build_chapter_html(
                book=book,
                clean_slug=clean_slug,
                track_type="author",
                index=idx,
                total_items=len(author_items),
                chapter_data=combined_item,
                audio_track=audio_track,
                prev_link=prev_link,
                next_link=next_link,
            )
            out_file = book_dir / f"ch_{idx}.html"
            out_file.write_text(html_str, encoding="utf-8")
            total_generated += 1

    print(f"Generated {total_generated} dedicated chapter pages across {len(catalog)} books in {CHAPTERS_DIR}")


if __name__ == "__main__":
    main()
