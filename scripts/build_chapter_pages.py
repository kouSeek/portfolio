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

import base64
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


def b64_uri(path: Path, mime: str) -> str:
    return ("data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode("ascii")) if path.is_file() else ""


FAV_BOOKS_B64 = b64_uri(APP_ROOT / "assets" / "icons" / "favicon-books.png", "image/png")


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

    def wrap_words(text: str, line_type: str = "body", is_block_end: bool = False) -> str:
        nonlocal word_index
        tokens = re.split(r"(\s+)", text)
        non_ws = [t for t in tokens if t and not re.match(r"^\s+$", t)]
        token_pos = 0
        res = []
        for tok in tokens:
            if not tok or re.match(r"^\s+$", tok):
                res.append(tok)
                continue
            clean = re.sub(r"[*_#`~\[\]()]", "", tok)
            is_last = (token_pos == len(non_ws) - 1)
            token_pos += 1

            w_idx = word_index
            word_index += 1
            weight = max(3, len(clean))
            is_sent_end = bool(re.search(r'[.?!]["\'\)\]]*$', tok)) or is_last
            if is_sent_end:
                weight += 4
            elif re.search(r'[,;:—–·]["\'\)\]]*$', tok) or tok in ("—", "–", "·"):
                weight += 2

            words_list.append({"idx": w_idx, "word": clean, "weight": weight, "s": 1 if is_sent_end else 0})
            escaped_tok = html.escape(tok)
            res.append(f'<span class="k-word" data-word-idx="{w_idx}" id="w_{w_idx}">{escaped_tok}</span>')
        return "".join(res)

    for i, line in enumerate(lines):
        line_s = line.strip()
        if not line_s:
            if in_quote:
                body_parts.append("</blockquote>")
                in_quote = False
            continue

        is_quote = line_s.startswith(">")
        is_block_end = (i + 1 >= len(lines)) or not lines[i + 1].strip() or lines[i + 1].strip().startswith("#") or (lines[i + 1].strip().startswith(">") != is_quote)

        if line_s.startswith(">"):
            if not in_quote:
                body_parts.append('<blockquote class="chapter-spoken-brief">')
                in_quote = True
            quote_text = re.sub(r"^>\s*", "", line_s)
            body_parts.append(f"<p>{wrap_words(quote_text, 'quote', is_block_end=is_block_end)}</p>")
        elif line_s.startswith("### "):
            if in_quote:
                body_parts.append("</blockquote>")
                in_quote = False
            body_parts.append(f'<h3 class="section-heading">{wrap_words(line_s[4:], "h3", is_block_end=True)}</h3>')
        elif line_s.startswith("## "):
            if in_quote:
                body_parts.append("</blockquote>")
                in_quote = False
            body_parts.append(f'<h2 class="chapter-prose-title">{wrap_words(line_s[3:], "h2", is_block_end=True)}</h2>')
        elif line_s.startswith("# "):
            if in_quote:
                body_parts.append("</blockquote>")
                in_quote = False
            body_parts.append(f'<h1 class="chapter-prose-title">{wrap_words(line_s[2:], "h1", is_block_end=True)}</h1>')
        else:
            if in_quote:
                body_parts.append("</blockquote>")
                in_quote = False
            body_parts.append(f"<p>{wrap_words(line_s, 'body', is_block_end=is_block_end)}</p>")

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
    book_desc = book.get("description") or book.get("skipped_note") or ""
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
    words_json = json.dumps([{"c": w["cum"], "w": w["weight"], "s": w["s"]} for w in words_list])

    audio_url = f"{GH_RAW_AUDIO_BASE}{audio_track['url']}" if audio_track else ""
    audio_dur = float(audio_track.get("durationSec") or 0.0) if audio_track else 0.0
    audio_silences_json = json.dumps(audio_track.get("silences", [])) if audio_track else "[]"
    has_audio = bool(audio_url)

    step_title_short = f"Step {index}" if track_type == "adhd" else f"Ch {index}"
    track_type_name = "⚡ Non-Linear Core Cut" if track_type == "adhd" else "📖 Full Book Chapter"

    track_items = (book.get("adhd_segments") or []) if track_type == "adhd" else (book.get("author_chapters") or [])
    toc_rows_list = []
    if book_desc:
        toc_rows_list.append(
            f'<div style="padding:8px 10px;margin-bottom:8px;background:var(--surface-subtle);border-left:3px solid var(--accent);border-radius:0 6px 6px 0;font-size:0.82rem;color:var(--ink-muted);line-height:1.45;"><strong>📖 About {html.escape(book_title)}:</strong> {html.escape(book_desc)}</div>'
        )
    for t_idx, t_item in enumerate(track_items, 1):
        t_is_cur = (t_idx == index)
        t_lbl = t_item.get("label", f"Chapter {t_idx}")
        t_pgs = t_item.get("pages", "")
        t_pcnt = t_item.get("pageCount") or 1
        t_vol = t_item.get("volumePct", 0.0)
        t_eff = t_item.get("effortLabel") or f"{t_item.get('estMinutes', t_item.get('duration_min', 15))}m"
        t_brief = t_item.get("brief", "")
        t_href = f"step_{t_idx}.html" if track_type == "adhd" else f"ch_{t_idx}.html"
        t_prefix = f"Step {t_idx}" if track_type == "adhd" else f"Ch {t_idx}"
        t_bar_w = min(100, max(4, round(float(t_vol) * 2.2))) if t_vol else 8
        toc_rows_list.append(
            f'<div style="padding:10px 12px;border-bottom:1px solid var(--border);display:flex;flex-direction:column;gap:5px;background:{"var(--accent-light)" if t_is_cur else "transparent"};border-radius:6px;">'
            f'<div style="font-weight:700;font-size:0.88rem;line-height:1.35;">{"▶ " if t_is_cur else ""}{html.escape(t_prefix)} · {html.escape(t_lbl)}</div>'
            + (f'<div style="font-size:0.8rem;color:var(--ink-muted);line-height:1.42;">{html.escape(t_brief)}</div>' if t_brief else '')
            + f'<div class="book-toc-vol-bar-track" style="height:4px;"><div class="book-toc-vol-bar-fill {track_type}" style="width:{t_bar_w}%;"></div></div>'
            f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;margin-top:2px;">'
            f'<div style="display:inline-flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:0.74rem;color:var(--ink-muted);">'
            + (f'<span class="meta-chip" style="padding:2px 7px;font-size:0.72rem;">p. {html.escape(str(t_pgs))}</span>' if t_pgs else '')
            + f'<span class="meta-chip primary" style="padding:2px 7px;font-size:0.72rem;">{t_pcnt}p ({t_vol}%)</span>'
            f'<span class="meta-chip effort" style="padding:2px 7px;font-size:0.72rem;">⏱️ {html.escape(str(t_eff))}</span>'
            f'</div>'
            f'<a href="{t_href}" style="text-decoration:none;padding:4px 11px;border-radius:999px;font-size:0.75rem;font-weight:700;background:var(--accent);color:#FFFFFF;">Absorb</a>'
            f'</div></div>'
        )
    chapter_toc_drawer_html = "".join(toc_rows_list)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <meta name="theme-color" content="#0F172A" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <title>{html.escape(step_title_short)} • {html.escape(book_title)} 📚</title>
  <link id="pageFavicon" data-emoji="📚" data-png-b64="{FAV_BOOKS_B64}" data-https-png="https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/assets/icons/favicon-books.png?v=1" data-https-ico="https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/assets/icons/favicon-books.ico?v=1" rel="icon" type="image/png" sizes="64x64" href="https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/assets/icons/favicon-books.png?v=1" />
  <link rel="shortcut icon" type="image/x-icon" href="https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/assets/icons/favicon-books.ico?v=1" />
  <link rel="apple-touch-icon" sizes="64x64" href="{FAV_BOOKS_B64 or 'https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/assets/icons/favicon-books.png?v=1'}" />
  <link rel="manifest" href="../../books-manifest.json" />
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
      padding-bottom: calc(var(--safe-bottom) + 36px);
      transition: background 0.2s ease, color 0.2s ease;
    }}
    body.has-active-player {{
      padding-bottom: calc(var(--safe-bottom) + 110px);
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

    /* Sticky Bottom Player Bar (only shown when audio is playing/active) */
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
      display: none;
      flex-direction: column;
      gap: 8px;
    }}
    body.has-active-player .sticky-player {{
      display: flex;
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
    <a class="back-btn" id="navBackBtn" href="../../books.html#book={clean_slug}">← Library</a>
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
      {f'<div class="hero-book-desc" style="font-size: 0.86rem; color: var(--ink-muted); line-height: 1.5; margin: 6px 0 10px; padding-left: 10px; border-left: 3px solid var(--accent);">{html.escape(book_desc)}</div>' if book_desc else ""}
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

      <details style="margin-top: 12px; border: 1px solid var(--border); border-radius: 10px; background: var(--surface-subtle); overflow: hidden;">
        <summary style="padding: 10px 14px; font-size: 0.85rem; font-weight: 700; cursor: pointer; user-select: none; display: flex; align-items: center; justify-content: space-between;">
          <span>📑 Chapters List &amp; Book Details ({total_items})</span>
          <span style="font-size: 0.78rem; color: var(--ink-muted);">Tap to expand ▼</span>
        </summary>
        <div style="padding: 10px 12px; background: var(--surface); border-top: 1px solid var(--border); max-height: 360px; overflow-y: auto; display: flex; flex-direction: column; gap: 4px;">
          {chapter_toc_drawer_html}
        </div>
      </details>

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
      <a class="primary" href="../../books.html#book={clean_slug}">📚 All Books</a>
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
    (function hydratePageFavicon() {{
      function apply() {{
        try {{
          if (!document.head || typeof document.createElement !== "function") return;
          const el = document.getElementById("pageFavicon");
          if (!el || !el.getAttribute) return;
          const emoji = el.getAttribute("data-emoji") || "";
          const b64 = el.getAttribute("data-png-b64") || "";
          const httpsPng = el.getAttribute("data-https-png") || b64;
          const httpsIco = el.getAttribute("data-https-ico") || httpsPng;
          const useHttps = (typeof location !== "undefined" && /^https?:$/i.test(location.protocol) && (typeof navigator === "undefined" || navigator.onLine !== false));
          const pngHref = useHttps ? httpsPng : (b64 || httpsPng);
          const icoHref = useHttps ? httpsIco : (b64 || httpsIco);
          document.querySelectorAll('link[rel*="icon"]').forEach(n => {{ if (n.parentNode) n.parentNode.removeChild(n); }});
          const l1 = document.createElement("link");
          l1.id = "pageFavicon";
          l1.setAttribute("data-emoji", emoji);
          l1.setAttribute("data-png-b64", b64);
          l1.setAttribute("data-https-png", httpsPng);
          l1.setAttribute("data-https-ico", httpsIco);
          l1.rel = "icon"; l1.type = "image/png"; l1.sizes = "64x64"; l1.href = pngHref;
          document.head.appendChild(l1);
          const l2 = document.createElement("link");
          l2.rel = "shortcut icon"; l2.type = useHttps ? "image/x-icon" : "image/png"; l2.href = icoHref;
          document.head.appendChild(l2);
          const l3 = document.createElement("link");
          l3.rel = "apple-touch-icon"; l3.sizes = "64x64"; l3.href = b64 || pngHref;
          document.head.appendChild(l3);
        }} catch (e) {{}}
      }}
      apply();
      if (typeof setTimeout === "function") setTimeout(apply, 90);
    }})();

    const AUDIO_URL = "{audio_url}";
    const AUDIO_DURATION = {audio_dur};
    const AUDIO_SILENCES = {audio_silences_json};
    const CACHE_NAME = "kortex-books-v1";
    const WORDS_DATA = {words_json};
    const TOTAL_WEIGHT = {total_weight};
    let timelineCalibrated = false;

    function buildAcousticWordTimeline(words, totalWeight, audioMeta) {{
      if (!words || !words.length || totalWeight <= 0) return;
      const totalDur = (audioMeta && Number(audioMeta.dur) > 0.5)
        ? Number(audioMeta.dur)
        : (audioEl && audioEl.duration > 0 ? audioEl.duration : AUDIO_DURATION);
      if (totalDur <= 0) return;

      const rawSilences = (audioMeta && Array.isArray(audioMeta.silences)) ? audioMeta.silences : (AUDIO_SILENCES || []);
      if (!rawSilences.length) {{
        for (let i = 0; i < words.length; i++) {{
          words[i].startSec = (words[i].c / totalWeight) * totalDur;
          words[i].endSec = ((words[i].c + words[i].w) / totalWeight) * totalDur;
        }}
        timelineCalibrated = true;
        return;
      }}

      function voicedTimeAt(t) {{
        const clamped = Math.max(0, Math.min(totalDur, t));
        let v = clamped;
        for (let i = 0; i < rawSilences.length; i++) {{
          const s = rawSilences[i][0];
          const e = rawSilences[i][1];
          if (clamped <= s) break;
          v -= (Math.min(clamped, e) - s);
        }}
        return Math.max(0, v);
      }}

      function invVoicedTime(targetV) {{
        let lo = 0;
        let hi = totalDur;
        for (let iter = 0; iter < 28; iter++) {{
          const mid = (lo + hi) * 0.5;
          if (voicedTimeAt(mid) < targetV) lo = mid;
          else hi = mid;
        }}
        return (lo + hi) * 0.5;
      }}

      const totalVoiced = voicedTimeAt(totalDur);
      if (totalVoiced <= 0) return;

      // 1. Sentence boundary word indices
      const sentEndIndices = [];
      for (let i = 0; i < words.length; i++) {{
        if (words[i].s) sentEndIndices.push(i);
      }}
      if (!sentEndIndices.length || sentEndIndices[sentEndIndices.length - 1] !== words.length - 1) {{
        sentEndIndices.push(words.length - 1);
      }}

      // 2. Anchor every K sentences (K=2 sentences per anchor)
      const K = 2;
      const anchorIndices = [];
      for (let i = K - 1; i < sentEndIndices.length; i += K) {{
        anchorIndices.push(sentEndIndices[i]);
      }}
      if (!anchorIndices.length || anchorIndices[anchorIndices.length - 1] !== words.length - 1) {{
        anchorIndices.push(words.length - 1);
      }}

      // 3. Compute anchor timestamps snapped to acoustic silences
      const anchors = [{{ wordIdx: -1, timeSec: 0.0 }}];
      for (let a = 0; a < anchorIndices.length; a++) {{
        const idx = anchorIndices[a];
        const w = words[idx];
        const cumW = w.c + w.w;
        const frac = cumW / totalWeight;
        const targetV = frac * totalVoiced;
        const tEst = invVoicedTime(targetV);

        let bestSilStart = null;
        let minDist = 1.6;
        for (let s = 0; s < rawSilences.length; s++) {{
          const dist = Math.abs(rawSilences[s][0] - tEst);
          if (dist < minDist) {{
            minDist = dist;
            bestSilStart = rawSilences[s][0];
          }}
        }}
        const aTime = bestSilStart !== null ? bestSilStart : tEst;
        anchors.push({{
          wordIdx: idx,
          timeSec: Math.max(0.1, aTime)
        }});
      }}

      for (let a = 1; a < anchors.length; a++) {{
        if (anchors[a].timeSec <= anchors[a - 1].timeSec) {{
          anchors[a].timeSec = anchors[a - 1].timeSec + 0.3;
        }}
      }}
      anchors[anchors.length - 1].timeSec = totalDur;

      // 4. Interpolate words strictly within each 2-sentence anchor interval
      for (let a = 0; a < anchors.length - 1; a++) {{
        const startWIdx = anchors[a].wordIdx + 1;
        const endWIdx = anchors[a + 1].wordIdx;
        if (startWIdx > endWIdx) continue;

        const tStart = anchors[a].timeSec;
        const tEnd = anchors[a + 1].timeSec;
        const baseC = words[startWIdx].c;
        const spanW = Math.max(1, (words[endWIdx].c + words[endWIdx].w) - baseC);
        const spanT = Math.max(0.05, tEnd - tStart);

        for (let i = startWIdx; i <= endWIdx; i++) {{
          const fracS = (words[i].c - baseC) / spanW;
          const fracE = ((words[i].c + words[i].w) - baseC) / spanW;
          words[i].startSec = tStart + fracS * spanT;
          words[i].endSec = tStart + fracE * spanT;
        }}
      }}

      words[0].startSec = 0.0;
      words[words.length - 1].endSec = totalDur;
      timelineCalibrated = true;
    }}

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
      if (isPlaying) {{
        document.body.classList.add("has-active-player");
        const sp = document.getElementById("stickyPlayer");
        if (sp) sp.style.display = "flex";
      }}
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
      const dur = (audioEl && audioEl.duration > 0) ? audioEl.duration : AUDIO_DURATION;
      if (!Number.isFinite(dur) || dur <= 0) return;
      const cur = audioEl.currentTime;

      let foundIdx = 0;
      if (WORDS_DATA[0].startSec !== undefined) {{
        let low = 0;
        let high = WORDS_DATA.length - 1;
        while (low <= high) {{
          const mid = (low + high) >> 1;
          if (WORDS_DATA[mid].startSec <= cur) {{
            foundIdx = mid;
            low = mid + 1;
          }} else {{
            high = mid - 1;
          }}
        }}
      }} else {{
        const progress = Math.min(1.0, Math.max(0, cur / dur));
        const targetWeight = progress * TOTAL_WEIGHT;
        let low = 0;
        let high = WORDS_DATA.length - 1;
        while (low <= high) {{
          const mid = (low + high) >> 1;
          if (WORDS_DATA[mid].c <= targetWeight) {{
            foundIdx = mid;
            low = mid + 1;
          }} else {{
            high = mid - 1;
          }}
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
      if (!timelineCalibrated) {{
        buildAcousticWordTimeline(WORDS_DATA, TOTAL_WEIGHT, {{ dur: audioEl.duration || AUDIO_DURATION, silences: AUDIO_SILENCES }});
      }}
    }});
    audioEl.addEventListener("loadedmetadata", () => {{
      buildAcousticWordTimeline(WORDS_DATA, TOTAL_WEIGHT, {{ dur: audioEl.duration || AUDIO_DURATION, silences: AUDIO_SILENCES }});
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
        if (WORDS_DATA[wIdx].startSec !== undefined) {{
          audioEl.currentTime = WORDS_DATA[wIdx].startSec;
        }} else {{
          const dur = audioEl.duration || AUDIO_DURATION;
          if (Number.isFinite(dur) && dur > 0 && TOTAL_WEIGHT > 0) {{
            audioEl.currentTime = (WORDS_DATA[wIdx].c / TOTAL_WEIGHT) * dur;
          }}
        }}
        if (audioEl.paused) {{
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
