#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 100% self-contained mobile-friendly Books Library (`books.html`) for AI Companion.

Inlines `assets/books_catalog.json` and `assets/books_audio_index.json` directly into JavaScript
so the page requires ZERO external JSON fetches on `htmlpreview.github.io` or mobile Chrome.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path
import re

APP_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = APP_ROOT / "assets" / "books_catalog.json"
AUDIO_INDEX_PATH = APP_ROOT / "assets" / "books_audio_index.json"
GENE_TEXT_PATH = APP_ROOT / "assets" / "books_text" / "01_the_gene_an_intimate_history_siddhartha_mukherjee_complete.json"
CODE_TEXT_PATH = APP_ROOT / "assets" / "books_text" / "14_the_code_book_simon_singh.json"
OUTPUT_PATH = APP_ROOT / "books.html"


def b64_uri(path: Path, mime: str) -> str:
    return ("data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode("ascii")) if path.is_file() else ""


def get_clean_book_slug_py(b: dict) -> str:
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


def _normalize_mobile_pillar_category(b: dict) -> str:
    raw = f"{b.get('wing', '')} {b.get('wing_category', '')} {b.get('category', '')}".lower()
    if any(k in raw for k in ("science", "cosmos", "space", "biology", "genetics", "math", "physics", "cryptography", "code", "calculus")):
        return "Science & Cosmos"
    if any(k in raw for k in ("mind", "consciousness", "psychology", "cognition", "tantra", "spiritual", "aghora", "yogi")):
        return "Mind & Consciousness"
    if any(k in raw for k in ("power", "philosophy", "war", "strategy", "history", "political")):
        return "Power & Philosophy"
    if any(k in raw for k in ("imagination", "wonder", "magic", "wizarding", "fantasy", "literature", "classics", "sci-fi", "fiction")):
        return "Imagination & Wonder"
    return "Science & Cosmos"


def generate_books_html() -> None:
    catalog_json = CATALOG_PATH.read_text(encoding="utf-8") if CATALOG_PATH.is_file() else "[]"
    audio_index_json = AUDIO_INDEX_PATH.read_text(encoding="utf-8") if AUDIO_INDEX_PATH.is_file() else "{}"

    catalog_list = json.loads(catalog_json)
    total_books = len(catalog_list)
    cat_counts = {"all": total_books}
    for b in catalog_list:
        cat = _normalize_mobile_pillar_category(b)
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    all_chapter_files = []
    for b in catalog_list:
        slug = get_clean_book_slug_py(b)
        title = b.get("title", "Book")
        for idx, s in enumerate(b.get("adhd_segments") or [], 1):
            all_chapter_files.append({
                "path": f"chapters/{slug}/step_{idx}.html",
                "bookTitle": title,
                "slug": slug,
                "trackType": "adhd",
                "index": idx,
                "label": s.get("label", f"Step {idx}")
            })
        for idx, c in enumerate(b.get("author_chapters") or [], 1):
            all_chapter_files.append({
                "path": f"chapters/{slug}/ch_{idx}.html",
                "bookTitle": title,
                "slug": slug,
                "trackType": "author",
                "index": idx,
                "label": c.get("label", f"Ch {idx}")
            })
    all_chapters_json = json.dumps(all_chapter_files, ensure_ascii=False)

    gene_text = json.loads(GENE_TEXT_PATH.read_text(encoding="utf-8")) if GENE_TEXT_PATH.is_file() else {}
    code_text = json.loads(CODE_TEXT_PATH.read_text(encoding="utf-8")) if CODE_TEXT_PATH.is_file() else {}
    inlined_text_dict = {
        "01_the_gene_an_intimate_history_siddhartha_mukherjee_complete": gene_text,
        "the-gene": gene_text,
        "14_the_code_book_simon_singh": code_text,
        "the-code-book": code_text,
    }
    inlined_text_json = json.dumps(inlined_text_dict, ensure_ascii=False)

    fav_png_path = APP_ROOT / "assets" / "icons" / "favicon-books.png"
    fav_b64 = b64_uri(fav_png_path, "image/png")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <meta name="theme-color" content="#0F172A" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="default" />
  <meta name="description" content="Liberation Books Library — Non-linear core cuts and full audiobooks for offline reading & listening." />
  <title>Books Library 📚</title>
  <link id="pageFavicon" data-emoji="📚" data-png-b64="{fav_b64}" data-https-png="https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/assets/icons/favicon-books.png?v=1" data-https-ico="https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/assets/icons/favicon-books.ico?v=1" rel="icon" type="image/png" sizes="64x64" href="https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/assets/icons/favicon-books.png?v=1" />
  <link rel="shortcut icon" type="image/x-icon" href="https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/assets/icons/favicon-books.ico?v=1" />
  <link rel="apple-touch-icon" sizes="64x64" href="{fav_b64 or 'https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/assets/icons/favicon-books.png?v=1'}" />
  <link rel="manifest" href="books-manifest.json" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,600&family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400;1,6..72,500&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #F8FAFC;
      --surface: #FFFFFF;
      --surface-subtle: #F1F5F9;
      --ink: #0F172A;
      --ink-muted: #475569;
      --border: #E2E8F0;
      --accent: #4F46E5;
      --accent-soft: #EEF2FF;
      --accent-ink: #3730A3;
      --emerald: #059669;
      --emerald-soft: #ECFDF5;
      --amber: #D97706;
      --amber-soft: #FFFBEB;
      --purple: #7C3AED;
      --purple-soft: #F3E8FF;
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --safe-top: env(safe-area-inset-top, 0px);
      --safe-bottom: env(safe-area-inset-bottom, 0px);
    }}

    [data-theme="dark"] {{
      --bg: #0B0F17;
      --surface: #141B26;
      --surface-subtle: #1C2636;
      --ink: #F1F5F9;
      --ink-muted: #94A3B8;
      --border: #233146;
      --accent: #6366F1;
      --accent-soft: rgba(99, 102, 241, 0.16);
      --accent-ink: #A5B4FC;
      --emerald-soft: rgba(5, 150, 105, 0.16);
      --amber-soft: rgba(217, 119, 6, 0.16);
      --purple-soft: rgba(124, 58, 237, 0.16);
    }}

    *, *::before, *::after {{
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
      min-height: 100dvh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      padding-top: var(--safe-top);
      padding-bottom: calc(var(--safe-bottom) + 84px);
    }}

    /* Top Bar */
    .topbar {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }}
    .topbar-left {{
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 0;
    }}
    .back-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 999px;
      font-size: 0.85rem;
      font-weight: 700;
      text-decoration: none;
      background: var(--surface-subtle);
      color: var(--ink);
      border: 1px solid var(--border);
      flex-shrink: 0;
    }}
    .topbar-title {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 1.15rem;
      font-weight: 700;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .topbar-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }}
    .icon-btn {{
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      color: var(--ink);
      padding: 6px 10px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      font-size: 0.95rem;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: background 0.15s ease;
    }}
    .icon-btn:hover {{
      background: var(--border);
    }}

    /* Container */
    .container {{
      max-width: 960px;
      width: 100%;
      margin: 0 auto;
      padding: 16px;
      flex: 1;
    }}

    /* Search & Wing Filters */
    .search-section {{
      margin-bottom: 18px;
    }}
    .search-box-wrap {{
      position: relative;
      margin-bottom: 12px;
    }}
    .search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 1rem;
      color: var(--ink-muted);
      pointer-events: none;
    }}
    .search-input {{
      width: 100%;
      padding: 12px 14px 12px 40px;
      border-radius: var(--radius-md);
      border: 1.5px solid var(--border);
      background: var(--surface);
      color: var(--ink);
      font-size: 0.95rem;
      outline: none;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }}
    .search-input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-soft);
    }}
    .category-collapsible {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      overflow: hidden;
      margin-top: 10px;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
      transition: border-color 0.2s ease;
    }}
    .category-collapsible-header {{
      padding: 10px 14px;
      background: var(--surface-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      font-size: 0.88rem;
      font-weight: 700;
      user-select: none;
      transition: background 0.15s ease;
    }}
    .category-collapsible-header:hover {{
      background: var(--border);
    }}
    .category-chevron {{
      font-size: 0.85rem;
      transition: transform 0.2s ease;
    }}
    .category-collapsible.collapsed .category-chevron {{
      transform: rotate(-90deg);
    }}
    .category-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      padding: 12px 14px;
      transition: all 0.2s ease;
    }}
    .category-collapsible.collapsed .category-pills,
    .category-collapsible.collapsed .in-progress-bar {{
      display: none;
    }}
    .in-progress-bar {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      padding: 10px 14px;
      border-top: 1px solid var(--border);
      background: var(--surface-subtle);
    }}
    .in-progress-list {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
      flex: 1;
      min-width: 0;
    }}
    .in-progress-chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 11px;
      border-radius: 999px;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--ink);
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: border-color 0.15s ease, transform 0.12s ease;
      max-width: 100%;
    }}
    .in-progress-chip:hover {{
      border-color: var(--accent);
    }}
    .in-progress-chip-title {{
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 160px;
    }}
    .in-progress-chip-step {{
      color: var(--ink-muted);
      font-size: 0.72rem;
      white-space: nowrap;
    }}
    .in-progress-empty {{
      color: var(--ink-muted);
      font-size: 0.78rem;
    }}
    .filter-chip {{
      white-space: nowrap;
      padding: 7px 13px;
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 600;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--ink-muted);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s ease;
    }}
    .filter-chip:hover {{
      border-color: var(--accent);
      color: var(--ink);
    }}
    .filter-chip.active {{
      background: var(--accent);
      color: #FFFFFF;
      border-color: var(--accent);
      box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25);
    }}
    .filter-chip-count {{
      font-size: 0.72rem;
      font-weight: 700;
      opacity: 0.75;
      padding: 1px 5px;
      border-radius: 999px;
      background: rgba(0, 0, 0, 0.08);
    }}
    .filter-chip.active .filter-chip-count {{
      background: rgba(255, 255, 255, 0.25);
    }}

    /* Books Grid */
    .books-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
    }}
    .book-card {{
      background: var(--surface);
      border: 1.5px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 16px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
      position: relative;
    }}
    .book-card:hover, .book-card:active {{
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
      border-color: var(--accent);
    }}
    .book-card-header {{
      display: flex;
      gap: 12px;
      margin-bottom: 12px;
    }}
    .book-card-emoji {{
      font-size: 2.2rem;
      line-height: 1;
      padding: 8px;
      background: var(--surface-subtle);
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}
    .book-card-titles {{
      flex: 1;
      min-width: 0;
    }}
    .book-card-title {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 1.05rem;
      font-weight: 700;
      line-height: 1.35;
      margin-bottom: 4px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .book-card-author {{
      font-size: 0.82rem;
      color: var(--ink-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .book-card-stats {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 10px;
    }}
    .badge-chip {{
      font-size: 0.74rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}
    .badge-chip.adhd {{
      background: #FEF3C7;
      color: #92400E;
    }}
    .badge-chip.full {{
      background: #E0E7FF;
      color: #3730A3;
    }}
    .badge-chip.voice {{
      background: var(--emerald-soft);
      color: var(--emerald);
    }}

    /* Detail View */
    .book-detail-view {{
      display: none;
    }}
    .book-detail-view.active {{
      display: block;
    }}
    .detail-hero {{
      background: var(--surface);
      border: 1.5px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 20px;
      margin-bottom: 18px;
      position: relative;
    }}
    .detail-hero-top {{
      display: flex;
      gap: 16px;
      align-items: flex-start;
      margin-bottom: 14px;
    }}
    .detail-hero-emoji {{
      font-size: 3.2rem;
      line-height: 1;
      padding: 12px;
      background: var(--surface-subtle);
      border-radius: var(--radius-md);
      flex-shrink: 0;
    }}
    .detail-hero-text h1 {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 1.45rem;
      line-height: 1.3;
      margin-bottom: 6px;
    }}
    .detail-hero-author {{
      font-size: 0.92rem;
      color: var(--ink-muted);
      margin-bottom: 10px;
    }}
    .detail-hero-desc {{
      font-size: 0.88rem;
      color: var(--ink-muted);
      line-height: 1.5;
      margin-bottom: 14px;
    }}
    .detail-action-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .btn-action {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      border-radius: var(--radius-md);
      font-size: 0.85rem;
      font-weight: 700;
      border: 1px solid var(--border);
      background: var(--surface-subtle);
      color: var(--ink);
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .btn-action.primary {{
      background: var(--accent);
      color: #FFFFFF;
      border-color: var(--accent);
    }}
    .btn-action:hover {{
      opacity: 0.92;
      transform: translateY(-1px);
    }}

    /* Track Sections */
    .track-section {{
      background: var(--surface);
      border: 1.5px solid var(--border);
      border-radius: var(--radius-lg);
      margin-bottom: 16px;
      overflow: hidden;
    }}
    .track-header {{
      padding: 14px 18px;
      background: var(--surface-subtle);
      border-bottom: 1px solid var(--border);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      user-select: none;
    }}
    .track-title {{
      font-weight: 700;
      font-size: 1rem;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .track-badge {{
      font-size: 0.75rem;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 999px;
      background: var(--surface);
      border: 1px solid var(--border);
    }}
    .track-chevron {{
      font-size: 0.9rem;
      transition: transform 0.2s ease;
    }}
    .track-section.collapsed .track-chevron {{
      transform: rotate(-90deg);
    }}
    .track-section.collapsed .track-body {{
      display: none;
    }}
    .track-body {{
      padding: 8px 0;
    }}

    /* Chapter Row — Stacked Full-Width Row Layout (Zero 3-Column Squeeze) */
    .track-book-desc {{
      margin: 6px 16px 10px;
      padding: 10px 12px;
      background: var(--surface-subtle);
      border-left: 3px solid var(--accent);
      border-radius: 0 8px 8px 0;
      font-size: 0.85rem;
      color: var(--ink-muted);
      line-height: 1.5;
    }}
    .book-card-desc {{
      font-size: 0.84rem;
      color: var(--ink-muted);
      line-height: 1.48;
      margin: 8px 0 12px;
      padding: 7px 10px;
      background: var(--surface-subtle);
      border-left: 3px solid var(--accent);
      border-radius: 0 8px 8px 0;
    }}
    .chapter-row {{
      padding: 14px 18px;
      border-bottom: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      align-items: stretch;
      gap: 7px;
      transition: background 0.12s ease;
    }}
    .chapter-row:last-child {{
      border-bottom: none;
    }}
    .chapter-row:hover {{
      background: var(--surface-subtle);
    }}
    .chapter-info {{
      width: 100%;
      min-width: 0;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .chapter-title-row {{
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 4px;
      width: 100%;
    }}
    .chapter-label {{
      font-weight: 700;
      font-size: 0.95rem;
      line-height: 1.4;
      width: 100%;
    }}
    .chapter-brief {{
      font-size: 0.84rem;
      color: var(--ink-muted);
      line-height: 1.48;
      width: 100%;
    }}
    .chapter-bottom-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
      width: 100%;
      margin-top: 2px;
    }}
    .chapter-metrics {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}
    .chapter-chip {{
      font-size: 0.74rem;
      padding: 2px 7px;
      border-radius: 5px;
      background: var(--surface-subtle);
      color: var(--ink-muted);
      border: 1px solid var(--border);
      white-space: nowrap;
    }}
    .chapter-chip.count {{
      color: var(--accent);
      background: var(--accent-light);
      border-color: rgba(99, 102, 241, 0.25);
      font-weight: 600;
    }}
    .chapter-chip.effort {{
      color: #D97706;
      background: rgba(245, 158, 11, 0.12);
      border-color: rgba(245, 158, 11, 0.25);
      font-weight: 600;
    }}
    .book-toc-vol-bar-track {{
      width: 100%;
      height: 4px;
      background: rgba(148, 163, 184, 0.18);
      border-radius: 2px;
      margin: 2px 0;
      overflow: hidden;
    }}
    .book-toc-vol-bar-fill {{
      height: 100%;
      border-radius: 2px;
      transition: width 0.3s ease;
    }}
    .book-toc-vol-bar-fill.adhd {{
      background: #10B981;
    }}
    .book-toc-vol-bar-fill.author {{
      background: #6366F1;
    }}
    .chapter-actions {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      flex-shrink: 0;
      margin-left: auto;
    }}
    .btn-ch {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--ink);
      transition: all 0.12s ease;
      white-space: nowrap;
    }}
    .btn-ch.play-btn {{
      background: var(--accent-soft);
      color: var(--accent-ink);
      border-color: rgba(99, 102, 241, 0.3);
    }}
    .btn-ch.play-btn:hover {{
      background: var(--accent);
      color: #FFFFFF;
    }}

    /* Bottom Sticky Player — Hidden by default, shown ONLY when a book/chapter is played */
    .player-bar {{
      position: fixed;
      bottom: var(--safe-bottom);
      left: 0;
      right: 0;
      background: var(--surface);
      border-top: 1.5px solid var(--border);
      padding: 10px 16px;
      z-index: 60;
      box-shadow: 0 -4px 20px rgba(15, 23, 42, 0.08);
      display: none; /* Hidden by default */
      flex-direction: column;
      gap: 8px;
    }}
    .player-progress-wrap {{
      display: flex;
      align-items: center;
      gap: 8px;
      width: 100%;
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
    .player-controls-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}
    .player-track-info {{
      flex: 1;
      min-width: 0;
    }}
    .player-book-title {{
      font-size: 0.78rem;
      color: var(--ink-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .player-chapter-title {{
      font-size: 0.88rem;
      font-weight: 700;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .player-buttons {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .player-btn {{
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      color: var(--ink);
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 0.95rem;
      cursor: pointer;
      transition: background 0.15s ease;
    }}
    .player-btn.play-main {{
      width: 42px;
      height: 42px;
      background: var(--accent);
      color: #FFFFFF;
      border-color: var(--accent);
      font-size: 1.15rem;
    }}

    /* Settings & Offline Modal */
    .offline-modal {{
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      z-index: 120;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 16px;
    }}
    .offline-modal.active {{
      display: flex;
    }}
    .offline-modal-card {{
      background: var(--surface);
      border: 1.5px solid var(--border);
      border-radius: var(--radius-lg);
      max-width: 480px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      padding: 22px;
      box-shadow: 0 16px 40px rgba(15, 23, 42, 0.2);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .modal-header-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .modal-title {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 1.25rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .modal-close-btn {{
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      color: var(--ink);
      width: 32px;
      height: 32px;
      border-radius: 50%;
      cursor: pointer;
      font-weight: bold;
    }}
    .progress-box {{
      background: var(--surface-subtle);
      border-radius: var(--radius-md);
      padding: 14px;
      border: 1px solid var(--border);
      display: none;
      flex-direction: column;
      gap: 8px;
    }}
    .progress-box.active {{
      display: flex;
    }}
    .progress-bar-track {{
      width: 100%;
      height: 8px;
      background: var(--border);
      border-radius: 999px;
      overflow: hidden;
    }}
    .progress-bar-fill {{
      height: 100%;
      background: var(--accent);
      width: 0%;
      transition: width 0.15s ease;
    }}
    .progress-status-text {{
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--ink-muted);
    }}
    .storage-detail-box {{
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 14px;
      background: var(--surface-subtle);
    }}
    .storage-stat-line {{
      display: flex;
      justify-content: space-between;
      font-size: 0.85rem;
      padding: 4px 0;
      border-bottom: 1px solid rgba(15, 23, 42, 0.06);
    }}
    .storage-stat-line:last-child {{
      border-bottom: none;
      font-weight: 700;
    }}
    .btn-sync-all {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 12px 18px;
      border-radius: var(--radius-md);
      font-size: 0.92rem;
      font-weight: 700;
      background: var(--accent);
      color: #FFFFFF;
      border: none;
      cursor: pointer;
      width: 100%;
      box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
      transition: all 0.15s ease;
    }}
    .btn-sync-all:hover {{
      opacity: 0.95;
      transform: translateY(-1px);
    }}

    /* Reader Modal */
    .reader-modal {{
      position: fixed;
      inset: 0;
      background: var(--bg);
      z-index: 100;
      display: none;
      flex-direction: column;
      padding-top: var(--safe-top);
      padding-bottom: var(--safe-bottom);
    }}
    .reader-modal.active {{
      display: flex;
    }}
    .reader-topbar {{
      padding: 12px 16px;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }}
    .reader-chapter-drawer {{
      background: var(--surface);
      border-bottom: 2px solid var(--accent);
      max-height: 280px;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
      z-index: 100;
    }}
    .reader-drawer-item {{
      padding: 10px 16px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      font-size: 0.88rem;
      transition: background 0.12s ease;
    }}
    .reader-drawer-item:hover {{
      background: var(--surface-subtle);
    }}
    .reader-drawer-item.active {{
      background: var(--accent-soft);
      color: var(--accent);
      font-weight: 700;
      border-left: 3.5px solid var(--accent);
    }}
    .reader-drawer-item-title {{
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      flex: 1;
      padding-right: 8px;
    }}
    .reader-drawer-item-meta {{
      font-size: 0.75rem;
      color: var(--ink-muted);
      flex-shrink: 0;
    }}
    .reader-content-body {{
      flex: 1;
      overflow-y: auto;
      padding: 24px 20px;
      max-width: 760px;
      width: 100%;
      margin: 0 auto;
      line-height: 1.75;
      font-size: 1.05rem;
      font-family: 'Newsreader', Georgia, serif;
    }}
    .reader-content-body h1, .reader-content-body h2, .reader-content-body h3 {{
      font-family: 'Playfair Display', Georgia, serif;
      margin-top: 24px;
      margin-bottom: 12px;
      line-height: 1.35;
    }}
    .reader-content-body p {{
      margin-bottom: 16px;
    }}
    .reader-meta-banner {{
      background: var(--surface-subtle);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 20px;
      margin-bottom: 24px;
    }}
    .reader-meta-pill-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px 12px;
      font-size: 0.82rem;
      color: var(--ink-muted);
      margin-bottom: 10px;
    }}
    .reader-overview-box {{
      font-size: 0.95rem;
      line-height: 1.55;
      color: var(--ink);
      border-top: 1px solid var(--border);
      padding-top: 10px;
      margin-top: 10px;
    }}
    .reader-prose {{
      font-size: 1.08rem;
      line-height: 1.85;
      color: var(--ink);
    }}
    .reader-prose blockquote {{
      border-left: 3px solid var(--accent);
      margin: 16px 0;
      padding: 8px 16px;
      color: var(--ink-muted);
      background: rgba(99, 102, 241, 0.05);
      border-radius: 0 8px 8px 0;
    }}
    .k-word {{
      display: inline;
      border-radius: 4px;
      padding: 0 2px;
      transition: background-color 0.12s ease, color 0.12s ease, box-shadow 0.12s ease;
      cursor: pointer;
    }}
    .k-word:hover {{
      background-color: rgba(99, 102, 241, 0.12);
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
    .reader-bottom-nav {{
      padding: 12px 16px;
      background: var(--surface);
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}

    /* Simple Toast Notification */
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
      z-index: 200;
      display: none;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }}
    .toast-msg.active {{
      display: block;
      animation: fadeInOut 2.8s ease forwards;
    }}
    @keyframes fadeInOut {{
      0% {{ opacity: 0; transform: translate(-50%, -8px); }}
      15% {{ opacity: 1; transform: translate(-50%, 0); }}
      85% {{ opacity: 1; transform: translate(-50%, 0); }}
      100% {{ opacity: 0; transform: translate(-50%, -8px); }}
    }}
  </style>
</head>
<body>
  <!-- Toast -->
  <div class="toast-msg" id="toastMsg"></div>

  <!-- Top Navigation Bar -->
  <header class="topbar">
    <div class="topbar-left">
      <a class="back-btn" id="navBackBtn" href="index.html">← AI Hub</a>
      <div class="topbar-title">📚 <span id="headerTitle">Liberation Library</span></div>
    </div>
    <div class="topbar-actions">
      <button class="icon-btn" id="btnOpenSettings" aria-label="Settings & Offline Sync" title="Settings & Offline Sync">⚙️</button>
      <button class="icon-btn" id="themeToggleBtn" aria-label="Toggle Theme">🌓</button>
    </div>
  </header>

  <!-- Main Container -->
  <main class="container">
    <!-- Library View -->
    <div id="libraryView">
      <!-- Search Section -->
      <div class="search-section">
        <div class="search-box-wrap">
          <span class="search-icon">🔍</span>
          <input type="search" class="search-input" id="bookSearchInput" placeholder="Search books, authors, topics..." autocomplete="off" />
        </div>
        <div class="category-collapsible" id="categoryCollapsible">
          <div class="category-collapsible-header" onclick="toggleCategoryCollapsible()">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span>📂 Browse by Pillar</span>
              <span class="track-badge" id="activeCategoryBadge">🌐 All Pillars ({total_books})</span>
            </div>
            <span class="category-chevron" id="categoryChevron">▼</span>
          </div>
          <div class="category-pills" id="categoryPills" role="group" aria-label="Multi-select book pillars">
            <button class="filter-chip active" data-cat="all">🌐 All Books <span class="filter-chip-count">{total_books}</span></button>
            <button class="filter-chip" data-cat="Science & Cosmos">🧬 Science & Cosmos <span class="filter-chip-count">{cat_counts.get('Science & Cosmos', 0)}</span></button>
            <button class="filter-chip" data-cat="Mind & Consciousness">🧠 Mind & Consciousness <span class="filter-chip-count">{cat_counts.get('Mind & Consciousness', 0)}</span></button>
            <button class="filter-chip" data-cat="Power & Philosophy">⚔️ Power & Philosophy <span class="filter-chip-count">{cat_counts.get('Power & Philosophy', 0)}</span></button>
            <button class="filter-chip" data-cat="Imagination & Wonder">🪄 Imagination & Wonder <span class="filter-chip-count">{cat_counts.get('Imagination & Wonder', 0)}</span></button>
          </div>
          <div class="in-progress-bar in-progress-card" id="inProgressBar">
            <div style="display: inline-flex; align-items: center; gap: 8px; flex-shrink: 0;">
              <button class="filter-chip" id="inProgressFilterChip" data-cat="in-progress">🔖 In-Progress <span class="filter-chip-count" id="inProgressCountBadge">0</span></button>
              <span style="font-size: 0.78rem; font-weight: 600; color: var(--ink-muted);">Saved / In-Progress Books</span>
            </div>
            <div class="in-progress-list" id="inProgressList">
              <span class="in-progress-empty">Open any chapter to keep active reads here</span>
            </div>
          </div>
        </div>
      </div>

      <div class="books-grid" id="booksGrid">
        <!-- Rendered dynamically from inlined BOOKS_DATA -->
      </div>
    </div>

    <!-- Detail View -->
    <div class="book-detail-view" id="bookDetailView">
      <div class="detail-hero">
        <div class="detail-hero-top">
          <div class="detail-hero-emoji" id="detailEmoji">📖</div>
          <div class="detail-hero-text">
            <h1 id="detailTitle">Book Title</h1>
            <div class="detail-hero-author" id="detailAuthor">Author Name</div>
            <div class="book-card-stats" id="detailBadges"></div>
          </div>
        </div>
        <p class="detail-hero-desc" id="detailDesc"></p>
        <div class="detail-action-bar">
          <button class="btn-action primary" id="btnPlayAllAdhd">⚡ Play Core Steps</button>
          <button class="btn-action" id="btnPlayAllFull">📖 Play Full Book</button>
          <button class="btn-action" id="btnDownloadBookOffline">💾 Download Offline</button>
          <button class="btn-action" id="btnBackToLibrary">← All Books</button>
        </div>
      </div>

      <!-- Core Steps Section -->
      <section class="track-section" id="adhdTrackSection">
        <div class="track-header" onclick="toggleTrackSection('adhdTrackSection')">
          <div class="track-title">
            <span>⚡ Non-Linear Core Steps</span>
            <span class="track-badge" id="adhdTrackBadge">0 steps</span>
          </div>
          <span class="track-chevron">▼</span>
        </div>
        <div class="track-body" id="adhdTrackBody">
          <!-- Rendered dynamically -->
        </div>
      </section>

      <!-- Full Book Section -->
      <section class="track-section" id="fullTrackSection">
        <div class="track-header" onclick="toggleTrackSection('fullTrackSection')">
          <div class="track-title">
            <span>📖 Full Book Chapters</span>
            <span class="track-badge" id="fullTrackBadge">0 chapters</span>
          </div>
          <span class="track-chevron">▼</span>
        </div>
        <div class="track-body" id="fullTrackBody">
          <!-- Rendered dynamically -->
        </div>
      </section>
    </div>
  </main>

  <!-- Sticky Audio Player Bar (Hidden by default, shown ONLY when a book/chapter is played) -->
  <div class="player-bar" id="playerBar">
    <div class="player-progress-wrap">
      <span class="player-time" id="playerCurrentTime">0:00</span>
      <input type="range" class="player-slider" id="playerScrubber" min="0" max="100" value="0" />
      <span class="player-time right" id="playerTotalTime">0:00</span>
    </div>
    <div class="player-controls-row">
      <div class="player-track-info">
        <div class="player-book-title" id="playerBookTitle">Book Title</div>
        <div class="player-chapter-title" id="playerChapterTitle">Chapter Title</div>
      </div>
      <div class="player-buttons">
        <button class="player-btn" id="btnRewind15" aria-label="Rewind 15s">↺15</button>
        <button class="player-btn play-main" id="btnPlayPause" aria-label="Play or Pause">▶</button>
        <button class="player-btn" id="btnForward15" aria-label="Forward 15s">15↻</button>
      </div>
    </div>
  </div>

  <!-- Settings & Offline Modal -->
  <div class="offline-modal" id="settingsModal">
    <div class="offline-modal-card">
      <div class="modal-header-row">
        <div class="modal-title">⚙️ Settings & Offline Mode</div>
        <button class="modal-close-btn" id="btnCloseSettingsModal">✕</button>
      </div>

      <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.88rem;">
        <span style="font-weight: 600;">Connection Status:</span>
        <span class="badge-chip" id="modalStatusBadge">🟢 Online</span>
      </div>

      <p style="font-size: 0.85rem; color: var(--ink-muted); line-height: 1.5;">
        Save all {total_books} books, chapter summaries, and neural voice files to your phone's browser cache for 100% offline reading and listening during flights.
      </p>

      <!-- Progress Box -->
      <div class="progress-box" id="offlineProgressBox">
        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 0.85rem;">
          <span id="progressStepTitle">Syncing...</span>
          <span id="progressPercentage">0%</span>
        </div>
        <div class="progress-bar-track">
          <div class="progress-bar-fill" id="progressBarFill"></div>
        </div>
        <div class="progress-status-text" id="progressStatusSub">Starting sync...</div>
      </div>

      <button class="btn-sync-all" id="btnModalStartSync">
        ⚡ Download All for Offline (Flights)
      </button>

      <!-- Storage Breakdown -->
      <div class="storage-detail-box">
        <div style="font-weight: 700; font-size: 0.88rem; margin-bottom: 8px;">📊 Offline Storage Status</div>
        <div class="storage-stat-line">
          <span>📚 Total Books</span>
          <span id="statModalVolumesCount">{total_books} volumes (Inlined)</span>
        </div>
        <div class="storage-stat-line">
          <span>📄 Chapter HTML Pages</span>
          <span id="statModalChaptersCount">{len(all_chapter_files)} chapters</span>
        </div>
        <div class="storage-stat-line">
          <span>🎙️ Available Voice Tracks</span>
          <span id="statModalAudioFiles">7 chapters (99.3 MB)</span>
        </div>
        <div class="storage-stat-line">
          <span>📥 Downloaded to Phone</span>
          <span id="statModalDownloadedCount" style="font-weight: 700; color: #10B981;">Checking...</span>
        </div>
        <div class="storage-stat-line">
          <span>⚠️ Not Downloaded (Remaining)</span>
          <span id="statModalMissingCount" style="font-weight: 700; color: #F59E0B;">Checking...</span>
        </div>
        <div class="storage-stat-line">
          <span>💾 Storage Space in Cache</span>
          <span id="statModalCacheSize">Calculating...</span>
        </div>
      </div>

      <div style="display: flex; gap: 10px; justify-content: space-between; margin-top: 4px;">
        <button class="btn-action" id="btnClearCacheBtn" style="color: #DC2626; border-color: rgba(220, 38, 38, 0.3);">
          🗑️ Clear Offline Cache
        </button>
        <button class="btn-action" id="btnRefreshManifestBtn">
          🔄 Refresh
        </button>
      </div>
    </div>
  </div>

  <!-- In-App Chapter Reader Modal -->
  <div class="reader-modal" id="readerModal">
    <header class="reader-topbar">
      <button class="back-btn" id="btnCloseReader">✕ Close</button>
      <button class="btn-action" id="btnToggleReaderChapters" onclick="toggleReaderChapterDrawer()" style="display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px;">
        <span>📑 Chapters</span>
        <span id="readerChaptersChevron" style="font-size: 0.75rem;">▼</span>
      </button>
      <div style="font-weight: 700; font-size: 0.92rem; text-align: center; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" id="readerHeaderTitle">Chapter Title</div>
      <div style="display: flex; gap: 6px;">
        <button class="btn-action" style="padding: 4px 8px;" id="btnFontSmaller">A-</button>
        <button class="btn-action" style="padding: 4px 8px;" id="btnFontLarger">A+</button>
      </div>
    </header>

    <!-- Collapsible Chapter Selection Drawer inside Reader -->
    <div class="reader-chapter-drawer" id="readerChapterDrawer" style="display: none;">
      <div class="reader-chapter-drawer-inner" id="readerChapterDrawerList">
        <!-- Rendered list of chapters for direct 1-tap jump -->
      </div>
    </div>
    <div class="reader-content-body" id="readerContentBody">
      <!-- Chapter text rendered here -->
    </div>
    <div class="reader-bottom-nav">
      <button class="btn-action" id="btnReaderPrev">← Previous</button>
      <button class="btn-action primary" id="btnReaderListenCurrent">▶️ Listen</button>
      <button class="btn-action" id="btnReaderNext">Next →</button>
    </div>
  </div>

  <audio id="audioElement" preload="metadata"></audio>

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

    /* ==========================================================================
       INLINED CATALOG & AUDIO INDEX (100% SELF-CONTAINED, ZERO EXTERNAL JSON FETCHES)
       ========================================================================== */
    const BOOKS_DATA = {catalog_json};
    const AUDIO_INDEX = {audio_index_json};
    const CHAPTER_FILES = {all_chapters_json};
    const INLINED_BOOKS_TEXT = {inlined_text_json};
    const GH_RAW_AUDIO_BASE = "https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/";
    const CACHE_NAME = "kortex-books-v1";

    let currentBook = null;
    let currentTrackType = "adhd";
    let currentItemIndex = 1;
    let activeCategory = "all";
    const selectedCategories = new Set();
    let inProgressOnly = false;
    let activeSearchQuery = "";
    let readerFontSize = 1.05;
    let isDownloading = false;
    let activeBlobUrl = null;
    let currentChapterWords = [];
    let currentChapterTotalWeight = 0;
    let activeWordIdx = -1;
    let karaokeActive = false;
    const PROGRESS_STORAGE_KEY = "kortex_mobile_books_progress_v1";

    function loadMobileProgressMap() {{
      try {{
        if (typeof localStorage === "undefined") return {{}};
        const raw = localStorage.getItem(PROGRESS_STORAGE_KEY);
        const parsed = raw ? JSON.parse(raw) : {{}};
        return (parsed && typeof parsed === "object") ? parsed : {{}};
      }} catch (_e) {{
        return {{}};
      }}
    }}

    function saveMobileBookProgress(book, stepLabel, chapterHref) {{
      try {{
        if (!book || typeof localStorage === "undefined") return;
        const key = book.slug || book.filename || book.title;
        if (!key) return;
        const pMap = loadMobileProgressMap();
        pMap[key] = {{
          slug: book.slug || book.filename,
          title: book.title,
          emoji: book.cover_emoji || "📖",
          stepLabel: stepLabel || "Step 1",
          href: chapterHref || "",
          updatedAt: Date.now()
        }};
        localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(pMap));
        renderInProgressBar();
      }} catch (_e) {{}}
    }}

    function renderInProgressBar() {{
      const pMap = loadMobileProgressMap();
      const entries = Object.values(pMap).sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0));
      const countEl = document.getElementById("inProgressCountBadge");
      if (countEl) countEl.textContent = String(entries.length);
      const chipBtn = document.getElementById("inProgressFilterChip");
      if (chipBtn) {{
        if (inProgressOnly) chipBtn.classList.add("active");
        else chipBtn.classList.remove("active");
      }}
      const listEl = document.getElementById("inProgressList");
      if (!listEl) return;
      if (entries.length === 0) {{
        listEl.innerHTML = `<span class="in-progress-empty">Open any chapter to keep active reads here</span>`;
        return;
      }}
      listEl.innerHTML = entries.map(item => {{
        const shortStep = String(item.stepLabel || "Resume").slice(0, 28);
        return `
          <button type="button" class="in-progress-chip" data-resume-slug="${{escapeHtml(item.slug || "")}}" data-resume-href="${{escapeHtml(item.href || "")}}">
            <span>${{escapeHtml(item.emoji || "📖")}}</span>
            <span class="in-progress-chip-title">${{escapeHtml(item.title || "")}}</span>
            <span class="in-progress-chip-step">${{escapeHtml(shortStep)}} ▸</span>
          </button>
        `;
      }}).join("");
      listEl.querySelectorAll(".in-progress-chip").forEach(btn => {{
        btn.addEventListener("click", () => {{
          const href = btn.getAttribute("data-resume-href");
          const slug = btn.getAttribute("data-resume-slug");
          if (href) {{
            window.location.href = href;
          }} else if (slug) {{
            openBookDetail(slug);
          }}
        }});
      }});
    }}

    const audioEl = document.getElementById("audioElement");

    function showToast(msg) {{
      const t = document.getElementById("toastMsg");
      t.textContent = msg;
      t.classList.remove("active");
      void t.offsetWidth;
      t.classList.add("active");
    }}

    function cleanEffortStr(raw) {{
      return String(raw || "").replace(/^~+/, "").trim();
    }}

    // Wake Lock
    let _screenWakeLock = null;
    async function requestScreenWakeLock() {{
      try {{
        if ("wakeLock" in navigator && !(_screenWakeLock && !_screenWakeLock.released)) {{
          _screenWakeLock = await navigator.wakeLock.request("screen");
        }}
      }} catch (e) {{}}
    }}

    // Audio Element Event Handlers — Sync buttons cleanly
    function updateReaderPlayButton(isPlaying) {{
      const btn = document.getElementById("btnReaderListenCurrent");
      if (btn) {{
        btn.textContent = isPlaying ? "⏸ Pause" : "▶️ Listen";
      }}
    }}

    audioEl.addEventListener("play", () => {{
      document.getElementById("btnPlayPause").textContent = "⏸";
      updateReaderPlayButton(true);
      karaokeActive = true;
    }});

    audioEl.addEventListener("pause", () => {{
      document.getElementById("btnPlayPause").textContent = "▶";
      updateReaderPlayButton(false);
    }});

    audioEl.addEventListener("ended", () => {{
      document.getElementById("btnPlayPause").textContent = "▶";
      updateReaderPlayButton(false);
      karaokeActive = false;
      if (activeWordIdx >= 0) {{
        const prev = document.getElementById(`kword_${{activeWordIdx}}`);
        if (prev) prev.classList.remove("active-word");
      }}
      if (!currentBook) return;
      const items = currentTrackType === "adhd" ? (currentBook.adhd_segments || []) : (currentBook.author_chapters || []);
      if (currentItemIndex < items.length) {{
        playChapter(currentTrackType, currentItemIndex + 1);
      }}
    }});

    audioEl.addEventListener("error", (e) => {{
      console.warn("Audio error event:", audioEl.error);
      document.getElementById("btnPlayPause").textContent = "▶";
      updateReaderPlayButton(false);
      showToast("Audio not available offline. Tap ⚙️ to download.");
    }});

    // Scrubber & Karaoke updates
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

    document.getElementById("btnPlayPause").addEventListener("click", async () => {{
      if (!audioEl.src) {{
        if (currentBook) playChapter(currentTrackType, currentItemIndex);
        return;
      }}
      if (audioEl.paused) {{
        try {{
          await audioEl.play();
          document.getElementById("btnPlayPause").textContent = "⏸";
        }} catch (err) {{
          document.getElementById("btnPlayPause").textContent = "▶";
        }}
      }} else {{
        audioEl.pause();
        document.getElementById("btnPlayPause").textContent = "▶";
      }}
    }});

    function formatSeconds(sec) {{
      if (!sec || isNaN(sec)) return "0:00";
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return `${{m}}:${{s < 10 ? "0" : ""}}${{s}}`;
    }}

    function findAudioTrack(book, trackType, index) {{
      if (!AUDIO_INDEX || !AUDIO_INDEX.files || !book) return null;
      const bSlug = (book.slug || book.filename || "").toLowerCase();
      const bTitle = (book.title || "").toLowerCase();

      return AUDIO_INDEX.files.find(f => {{
        const fSlug = (f.slug || "").toLowerCase();
        const fTitle = (f.bookTitle || "").toLowerCase();
        const matchesBook =
          fSlug === bSlug ||
          bSlug.includes(fSlug.replace(/-/g, "_")) ||
          bSlug.includes(fSlug) ||
          fSlug.includes(bSlug) ||
          (fTitle && bTitle.includes(fTitle)) ||
          (fTitle && fTitle.includes(bTitle));
        return matchesBook && f.trackType === trackType && f.index === index;
      }});
    }}

    async function getChapterText(book, trackType, index) {{
      if (!book) return null;
      const bSlug = (book.slug || book.filename.replace(/\\.pdf$/i, "")).toLowerCase();

      // 1. Check inlined text dictionary (The Gene, The Code Book, etc.)
      if (typeof INLINED_BOOKS_TEXT !== "undefined" && INLINED_BOOKS_TEXT) {{
        const bookData = INLINED_BOOKS_TEXT[bSlug] || INLINED_BOOKS_TEXT[book.slug] || INLINED_BOOKS_TEXT[(book.slug || "").toLowerCase()];
        if (bookData) {{
          const group = bookData[trackType] || {{}};
          const item = group[String(index)];
          if (item && item.content) return item;
        }}
      }}

      // 2. Check CacheStorage for assets/books_text/<slug>.json
      const textUrl = `https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/assets/books_text/${{bSlug}}.json`;
      if ("caches" in window) {{
        try {{
          const cache = await caches.open(CACHE_NAME);
          const cachedResp = await cache.match(textUrl);
          if (cachedResp) {{
            const bData = await cachedResp.json();
            const group = bData[trackType] || {{}};
            const item = group[String(index)];
            if (item && item.content) return item;
          }}
        }} catch (ce) {{}}
      }}

      // 3. Fetch from remote
      try {{
        const resp = await fetch(textUrl);
        if (resp.ok) {{
          const bData = await resp.json();
          if ("caches" in window) {{
            try {{
              const cache = await caches.open(CACHE_NAME);
              cache.put(textUrl, new Response(JSON.stringify(bData)));
            }} catch (pe) {{}}
          }}
          const group = bData[trackType] || {{}};
          const item = group[String(index)];
          if (item && item.content) return item;
        }}
      }} catch (fe) {{}}

      // Fallback to brief
      const items = trackType === "adhd" ? (book.adhd_segments || []) : (book.author_chapters || []);
      return items[index - 1] || null;
    }}

    function escapeHtml(str) {{
      return String(str || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }}

    function renderMarkdownWithKaraoke(content, brief, label, pages, durMin) {{
      let wordIndex = 0;
      const wordsList = [];

      function wrapWords(text, lineType, isBlockEnd) {{
        const rawTokens = text.split(/(\\s+)/);
        const nonWsTokens = rawTokens.filter(t => t && !/^\\s+$/.test(t));
        let tokenPos = 0;
        return rawTokens.map(tok => {{
          if (/^\\s+$/.test(tok) || !tok) return tok;
          const clean = tok.replace(/[*_#`~[\\]()]/g, "");
          const isLast = (tokenPos === nonWsTokens.length - 1);
          tokenPos++;

          const wIdx = wordIndex++;
          let weight = Math.max(3, clean.length);
          const isSentEnd = /[.?!]$/.test(clean) || /[.?!]["')\\]]*$/.test(tok) || isLast;
          if (isSentEnd) {{
            weight += 4;
          }} else if (/[,;:—–·]$/.test(clean) || /[,;:—–·]["')\\]]*$/.test(tok) || tok === "—" || tok === "–" || tok === "·") {{
            weight += 2;
          }}
          wordsList.push({{
            index: wIdx,
            word: clean,
            weight: weight,
            s: isSentEnd ? 1 : 0
          }});
          return `<span class="k-word" data-word-idx="${{wIdx}}" id="kword_${{wIdx}}">${{escapeHtml(tok)}}</span>`;
        }}).join("");
      }}

      const bookDesc = currentBook ? (currentBook.description || currentBook.skipped_note || "") : "";
      let headerHtml = `
        <div class="reader-meta-banner">
          <h2 style="font-size: 1.4rem; margin-top: 0; margin-bottom: 8px;">${{escapeHtml(label)}}</h2>
          <div class="reader-meta-pill-row">
            <span>📚 ${{escapeHtml(currentBook.title)}}</span>
            <span>📄 Pages: ${{escapeHtml(pages || "N/A")}}</span>
            <span>⏱️ Duration: ~${{escapeHtml(durMin || 15)}} mins</span>
          </div>
          ${{bookDesc ? `<div style="font-size: 0.88rem; color: var(--ink-muted); line-height: 1.5; margin-bottom: 8px; padding-left: 10px; border-left: 3px solid var(--accent);">${{escapeHtml(bookDesc)}}</div>` : ""}}
          ${{brief ? `<div class="reader-overview-box"><strong>Core Takeaway:</strong> ${{escapeHtml(brief)}}</div>` : ""}}
        </div>
      `;

      const lines = (content || "").split(/\\r?\\n/);
      let bodyHtml = "";
      let inQuote = false;

      for (let i = 0; i < lines.length; i++) {{
        let line = lines[i].trim();
        if (!line) {{
          if (inQuote) {{ bodyHtml += "</blockquote>"; inQuote = false; }}
          continue;
        }}

        const isQuoteLine = line.startsWith(">");
        let isBlockEnd = false;
        if (i + 1 >= lines.length) {{
          isBlockEnd = true;
        }} else {{
          const nxt = lines[i + 1].trim();
          if (!nxt) isBlockEnd = true;
          else if (nxt.startsWith("#") || (nxt.startsWith(">") !== isQuoteLine)) isBlockEnd = true;
        }}

        if (line.startsWith(">")) {{
          if (!inQuote) {{ bodyHtml += "<blockquote>"; inQuote = true; }}
          line = line.replace(/^>\\s*/, "");
          bodyHtml += `<p>${{wrapWords(line, "quote", isBlockEnd)}}</p>`;
        }} else if (line.startsWith("### ")) {{
          if (inQuote) {{ bodyHtml += "</blockquote>"; inQuote = false; }}
          bodyHtml += `<h3>${{wrapWords(line.slice(4), "h3", true)}}</h3>`;
        }} else if (line.startsWith("## ")) {{
          if (inQuote) {{ bodyHtml += "</blockquote>"; inQuote = false; }}
          bodyHtml += `<h2>${{wrapWords(line.slice(3), "h2", true)}}</h2>`;
        }} else if (line.startsWith("# ")) {{
          if (inQuote) {{ bodyHtml += "</blockquote>"; inQuote = false; }}
          bodyHtml += `<h1>${{wrapWords(line.slice(2), "h1", true)}}</h1>`;
        }} else {{
          if (inQuote) {{ bodyHtml += "</blockquote>"; inQuote = false; }}
          bodyHtml += `<p>${{wrapWords(line, "body", isBlockEnd)}}</p>`;
        }}
      }}
      if (inQuote) {{ bodyHtml += "</blockquote>"; }}

      let cum = 0;
      for (let w of wordsList) {{
        w.cumWeight = cum;
        cum += w.weight;
      }}
      const totalWeight = Math.max(1, cum);

      return {{
        html: headerHtml + `<div class="reader-prose">${{bodyHtml}}</div>`,
        wordsList,
        totalWeight
      }};
    }}

    function buildAcousticWordTimeline(words, totalWeight, audioMeta) {{
      if (!words || !words.length || totalWeight <= 0) return;
      const totalDur = (audioMeta && Number(audioMeta.durationSec || audioMeta.dur) > 0.5)
        ? Number(audioMeta.durationSec || audioMeta.dur)
        : (audioEl && audioEl.duration > 0 ? audioEl.duration : 0);
      if (totalDur <= 0) return;

      const rawSilences = (audioMeta && Array.isArray(audioMeta.silences)) ? audioMeta.silences : [];
      if (!rawSilences.length) {{
        for (let i = 0; i < words.length; i++) {{
          words[i].startSec = (words[i].cumWeight / totalWeight) * totalDur;
          words[i].endSec = ((words[i].cumWeight + words[i].weight) / totalWeight) * totalDur;
        }}
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
        for (let iter = 0; iter < 26; iter++) {{
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
        const cumW = w.cumWeight + w.weight;
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
        const baseC = words[startWIdx].cumWeight;
        const spanW = Math.max(1, (words[endWIdx].cumWeight + words[endWIdx].weight) - baseC);
        const spanT = Math.max(0.05, tEnd - tStart);

        for (let i = startWIdx; i <= endWIdx; i++) {{
          const fracS = (words[i].cumWeight - baseC) / spanW;
          const fracE = ((words[i].cumWeight + words[i].weight) - baseC) / spanW;
          words[i].startSec = tStart + fracS * spanT;
          words[i].endSec = tStart + fracE * spanT;
        }}
      }}

      words[0].startSec = 0.0;
      words[words.length - 1].endSec = totalDur;
    }}

    function syncKaraokeWord() {{
      if (!karaokeActive || !currentChapterWords.length || currentChapterTotalWeight <= 0) return;
      const dur = audioEl.duration;
      if (!Number.isFinite(dur) || dur <= 0) return;
      const curTime = audioEl.currentTime;

      let foundIdx = 0;
      if (currentChapterWords[0] && currentChapterWords[0].startSec !== undefined) {{
        let low = 0;
        let high = currentChapterWords.length - 1;
        while (low <= high) {{
          const mid = (low + high) >> 1;
          if (currentChapterWords[mid].startSec <= curTime) {{
            foundIdx = mid;
            low = mid + 1;
          }} else {{
            high = mid - 1;
          }}
        }}
      }} else {{
        const progress = Math.min(1.0, Math.max(0, curTime / dur));
        const targetWeight = progress * currentChapterTotalWeight;
        let low = 0;
        let high = currentChapterWords.length - 1;
        while (low <= high) {{
          const mid = (low + high) >> 1;
          if (currentChapterWords[mid].cumWeight <= targetWeight) {{
            foundIdx = mid;
            low = mid + 1;
          }} else {{
            high = mid - 1;
          }}
        }}
      }}

      if (foundIdx !== activeWordIdx) {{
        if (activeWordIdx >= 0) {{
          const prevEl = document.getElementById(`kword_${{activeWordIdx}}`);
          if (prevEl) prevEl.classList.remove("active-word");
        }}
        activeWordIdx = foundIdx;
        const curEl = document.getElementById(`kword_${{activeWordIdx}}`);
        if (curEl) {{
          curEl.classList.add("active-word");
          const container = document.getElementById("readerContentBody");
          if (container) {{
            const cRect = container.getBoundingClientRect();
            const elRect = curEl.getBoundingClientRect();
            const relTop = elRect.top - cRect.top;
            const targetCenter = cRect.height * 0.40;
            if (relTop < 50 || relTop > cRect.height * 0.70) {{
              container.scrollBy({{
                top: relTop - targetCenter,
                behavior: "smooth"
              }});
            }}
          }}
        }}
      }}
    }}

    function bookMatchesCategoryLabel(b, aCatRaw) {{
      const cat = (b.wing_category || b.category || "").toLowerCase();
      const aCat = String(aCatRaw || "").toLowerCase();
      if (!aCat || aCat === "all") return true;
      if (aCat.includes("science")) {{
        return cat.includes("science") || cat.includes("space") || cat.includes("frontier") || cat.includes("cosmos");
      }}
      if (aCat.includes("mind")) {{
        return cat.includes("mind") || cat.includes("psychology") || cat.includes("consciousness");
      }}
      if (aCat.includes("power") || aCat.includes("philosophy")) {{
        return cat.includes("power") || cat.includes("philosophy") || cat.includes("warfare");
      }}
      if (aCat.includes("imagination") || aCat.includes("wonder")) {{
        return cat.includes("imagination") || cat.includes("wonder") || cat.includes("wizarding") || cat.includes("fantasy") || cat.includes("classics") || cat.includes("literature");
      }}
      return cat.includes(aCat);
    }}

    function renderBooksGrid() {{
      const grid = document.getElementById("booksGrid");
      grid.innerHTML = "";
      const pMap = loadMobileProgressMap();

      const filtered = BOOKS_DATA.filter(b => {{
        if (inProgressOnly) {{
          const key = b.slug || b.filename || b.title;
          if (!pMap[key]) return false;
        }}
        let matchesCat = true;
        if (selectedCategories.size > 0) {{
          matchesCat = Array.from(selectedCategories).some(selCat => bookMatchesCategoryLabel(b, selCat));
        }} else if (activeCategory !== "all" && activeCategory !== "in-progress") {{
          matchesCat = bookMatchesCategoryLabel(b, activeCategory);
        }}
        const q = activeSearchQuery.toLowerCase().trim();
        const matchesSearch = !q || b.title.toLowerCase().includes(q) || b.author.toLowerCase().includes(q) || (b.description || "").toLowerCase().includes(q);
        return matchesCat && matchesSearch;
      }});

      const badge = document.getElementById("activeCategoryBadge");
      if (badge) {{
        if (selectedCategories.size === 0 && !inProgressOnly) {{
          badge.textContent = `All Books (${{BOOKS_DATA.length}})`;
        }} else if (inProgressOnly && selectedCategories.size === 0) {{
          badge.textContent = `🔖 In-Progress (${{filtered.length}})`;
        }} else if (selectedCategories.size === 1) {{
          const onlyCat = Array.from(selectedCategories)[0];
          badge.textContent = `${{onlyCat}}${{inProgressOnly ? " · 🔖" : ""}} (${{filtered.length}})`;
        }} else {{
          badge.textContent = `${{selectedCategories.size}} Pillars${{inProgressOnly ? " · 🔖" : ""}} (${{filtered.length}})`;
        }}
      }}

      if (filtered.length === 0) {{
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--ink-muted);">No books found matching "${{activeSearchQuery}}".</div>`;
        return;
      }}

      filtered.forEach(b => {{
        const card = document.createElement("div");
        card.className = "book-card";
        card.onclick = () => openBookDetail(b.slug || b.filename);

        const adhdCount = (b.adhd_segments || []).length;
        const fullCount = (b.author_chapters || []).length;
        const cleanAdhdTime = cleanEffortStr(b.adhd_time_label);
        const cleanFullTime = cleanEffortStr(b.full_time_label);
        const adhdPages = b.adhd_total_pages ? `${{b.adhd_total_pages}}p` : "";
        const adhdVol = b.adhd_volume_pct ? `${{b.adhd_volume_pct}}%` : "";
        const fullPages = b.full_book_pages || b.pages ? `${{b.full_book_pages || b.pages}}p` : "";

        const hasAudio = b.has_audio || (AUDIO_INDEX.books && AUDIO_INDEX.books[b.slug]);
        const bookDesc = b.description || b.skipped_note || "";
        const pillarBadge = b.wing || b.category || "";

        card.innerHTML = `
          <div>
            <div class="book-card-header">
              <div class="book-card-emoji">${{b.cover_emoji || "📖"}}</div>
              <div class="book-card-titles">
                <div class="book-card-title">${{escapeHtml(b.title)}}</div>
                <div class="book-card-author">${{escapeHtml(b.author || "Liberation Library")}}${{pillarBadge ? ` · <span style="color:var(--accent);font-weight:600;">${{escapeHtml(pillarBadge)}}</span>` : ""}}</div>
              </div>
            </div>
            ${{bookDesc ? `<div class="book-card-desc">${{escapeHtml(bookDesc)}}</div>` : ""}}
          </div>
          <div>
            <div class="book-card-stats">
              <span class="badge-chip adhd">⚡ ${{adhdCount}} Steps ${{adhdPages ? `· ${{adhdPages}}` : ""}} ${{adhdVol ? `(${{adhdVol}})` : ""}} ${{cleanAdhdTime ? `· ⏱️ ${{cleanAdhdTime}}` : ""}}</span>
              <span class="badge-chip full">📖 ${{fullCount}} Ch ${{fullPages ? `· ${{fullPages}}` : ""}} ${{cleanFullTime ? `· ⏱️ ${{cleanFullTime}}` : ""}}</span>
              ${{hasAudio ? `<span class="badge-chip voice">🎙️ Audio Ready</span>` : ""}}
            </div>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    let lastLibraryScrollY = 0;

    function openBookDetail(slugOrFilename, pushToHistory = true) {{
      const book = BOOKS_DATA.find(b => b.slug === slugOrFilename || b.filename === slugOrFilename);
      if (!book) return;
      currentBook = book;
      lastLibraryScrollY = window.scrollY || window.pageYOffset || 0;

      document.getElementById("libraryView").style.display = "none";
      const dv = document.getElementById("bookDetailView");
      dv.classList.add("active");

      // Adapt topbar back button for detail view
      const navBackBtn = document.getElementById("navBackBtn");
      if (navBackBtn) {{
        navBackBtn.textContent = "← Books";
        navBackBtn.onclick = (e) => {{
          e.preventDefault();
          backToLibrary();
        }};
      }}

      const cleanSlug = getCleanBookSlug(book);
      if (pushToHistory && typeof history !== "undefined" && history.pushState) {{
        history.pushState({{ view: "detail", slug: cleanSlug }}, "", "#book=" + encodeURIComponent(cleanSlug));
      }}

      const bookDesc = book.description || book.skipped_note || "";
      document.getElementById("detailEmoji").textContent = book.cover_emoji || "📖";
      document.getElementById("detailTitle").textContent = book.title;
      document.getElementById("detailAuthor").textContent = book.author || "Liberation Library";
      document.getElementById("detailDesc").textContent = bookDesc;
      document.getElementById("headerTitle").textContent = book.title;

      const adhdTime = cleanEffortStr(book.adhd_time_label);
      const fullTime = cleanEffortStr(book.full_time_label);
      const adhdPages = book.adhd_total_pages ? `${{book.adhd_total_pages}} pages` : "";
      const adhdVol = book.adhd_volume_pct ? `${{book.adhd_volume_pct}}% of book` : "";
      const prunedInfo = book.pruned_pct ? `${{book.pruned_pct}}% pruned` : "";
      const fullPages = book.full_book_pages || book.pages ? `${{book.full_book_pages || book.pages}} pages` : "";
      const pillarBadge = book.wing || book.category || "";

      document.getElementById("detailBadges").innerHTML = `
        ${{pillarBadge ? `<span class="badge-chip" style="background:var(--surface-subtle);color:var(--ink);border:1px solid var(--border);">${{escapeHtml(pillarBadge)}}</span>` : ""}}
        <span class="badge-chip adhd">⚡ ${{(book.adhd_segments || []).length}} Steps ${{adhdPages ? `· ${{adhdPages}}` : ""}} ${{adhdVol ? `· ${{adhdVol}}` : ""}} ${{prunedInfo ? `(${{prunedInfo}})` : ""}} ${{adhdTime ? `· ⏱️ ${{adhdTime}}` : ""}}</span>
        <span class="badge-chip full">📖 ${{(book.author_chapters || []).length}} Chapters ${{fullPages ? `· ${{fullPages}}` : ""}} ${{fullTime ? `· ⏱️ ${{fullTime}}` : ""}}</span>
      `;

      // Render ADHD track
      const adhdSec = document.getElementById("adhdTrackSection");
      if (adhdSec) adhdSec.classList.remove("collapsed");
      const adhdBody = document.getElementById("adhdTrackBody");
      adhdBody.innerHTML = bookDesc
        ? `<div class="track-book-desc"><strong>📖 About ${{escapeHtml(book.title)}}:</strong> ${{escapeHtml(bookDesc)}}</div>`
        : "";
      const adhdItems = book.adhd_segments || [];
      document.getElementById("adhdTrackBadge").textContent = `${{adhdItems.length}} steps`;

      adhdItems.forEach((item, idx) => {{
        const stepNum = idx + 1;
        const row = document.createElement("div");
        row.className = "chapter-row";
        row.style.cursor = "pointer";
        const stepHref = `chapters/${{cleanSlug}}/step_${{stepNum}}.html`;
        row.onclick = (e) => {{
          saveMobileBookProgress(currentBook, `Step ${{stepNum}} · ${{item.label}}`, stepHref);
          if (!e.target.closest("a")) {{
            window.location.href = stepHref;
          }}
        }};
        const pageRange = item.pages ? `p. ${{item.pages}}` : "";
        const pageCnt = item.pageCount ? `${{item.pageCount}}p` : "";
        const volPct = item.volumePct ? `${{item.volumePct}}%` : "";
        const effStr = item.effortLabel || (item.estMinutes ? `⏱️ ${{item.estMinutes}}m` : (item.duration_min ? `⏱️ ${{item.duration_min}}m` : ""));
        const volWidth = Math.min(100, Math.max(4, Math.round((Number(item.volumePct) || 2) * 2.2)));

        row.innerHTML = `
          <div class="chapter-info">
            <div class="chapter-title-row">
              <span class="chapter-label">Step ${{stepNum}} · ${{escapeHtml(item.label)}}</span>
            </div>
            ${{item.brief ? `<div class="chapter-brief">${{escapeHtml(item.brief)}}</div>` : ""}}
            <div class="book-toc-vol-bar-track">
              <div class="book-toc-vol-bar-fill adhd" style="width: ${{volWidth}}%;"></div>
            </div>
            <div class="chapter-bottom-bar">
              <div class="chapter-metrics">
                ${{pageRange ? `<span class="chapter-chip">${{pageRange}}</span>` : ""}}
                ${{pageCnt ? `<span class="chapter-chip count">${{pageCnt}} (${{volPct}})</span>` : ""}}
                ${{effStr ? `<span class="chapter-chip effort">${{effStr}}</span>` : ""}}
              </div>
              <div class="chapter-actions">
                <a class="btn-ch play-btn" href="${{stepHref}}" style="text-decoration:none;">Absorb</a>
              </div>
            </div>
          </div>
        `;
        adhdBody.appendChild(row);
      }});

      // Render Full Book track
      const fullSec = document.getElementById("fullTrackSection");
      if (fullSec) fullSec.classList.add("collapsed");
      const fullBody = document.getElementById("fullTrackBody");
      fullBody.innerHTML = bookDesc
        ? `<div class="track-book-desc"><strong>📖 About ${{escapeHtml(book.title)}}:</strong> ${{escapeHtml(bookDesc)}}</div>`
        : "";
      const fullItems = book.author_chapters || [];
      document.getElementById("fullTrackBadge").textContent = `${{fullItems.length}} chapters · Tap to expand`;

      fullItems.forEach((item, idx) => {{
        const chNum = idx + 1;
        const row = document.createElement("div");
        row.className = "chapter-row";
        row.style.cursor = "pointer";
        const chHref = `chapters/${{cleanSlug}}/ch_${{chNum}}.html`;
        row.onclick = (e) => {{
          saveMobileBookProgress(currentBook, `Ch ${{chNum}} · ${{item.label}}`, chHref);
          if (!e.target.closest("a")) {{
            window.location.href = chHref;
          }}
        }};
        const pageRange = item.pages ? `p. ${{item.pages}}` : "";
        const pageCnt = item.pageCount ? `${{item.pageCount}}p` : "";
        const volPct = item.volumePct ? `${{item.volumePct}}%` : "";
        const effStr = item.effortLabel || (item.estMinutes ? `⏱️ ${{item.estMinutes}}m` : (item.duration_min ? `⏱️ ${{item.duration_min}}m` : ""));
        const volWidth = Math.min(100, Math.max(4, Math.round((Number(item.volumePct) || 2) * 2.2)));

        row.innerHTML = `
          <div class="chapter-info">
            <div class="chapter-title-row">
              <span class="chapter-label">Ch ${{chNum}} · ${{escapeHtml(item.label)}}</span>
            </div>
            ${{item.brief ? `<div class="chapter-brief">${{escapeHtml(item.brief)}}</div>` : ""}}
            <div class="book-toc-vol-bar-track">
              <div class="book-toc-vol-bar-fill author" style="width: ${{volWidth}}%;"></div>
            </div>
            <div class="chapter-bottom-bar">
              <div class="chapter-metrics">
                ${{pageRange ? `<span class="chapter-chip">${{pageRange}}</span>` : ""}}
                ${{pageCnt ? `<span class="chapter-chip count">${{pageCnt}} (${{volPct}})</span>` : ""}}
                ${{effStr ? `<span class="chapter-chip effort">${{effStr}}</span>` : ""}}
              </div>
              <div class="chapter-actions">
                <a class="btn-ch play-btn" href="${{chHref}}" style="text-decoration:none;">Absorb</a>
              </div>
            </div>
          </div>
        `;
        fullBody.appendChild(row);
      }});

      window.scrollTo({{ top: 0, behavior: "smooth" }});
      hydrateAppLinks();
    }}

    function backToLibrary(triggerHistory = true) {{
      document.getElementById("bookDetailView").classList.remove("active");
      document.getElementById("libraryView").style.display = "block";
      document.getElementById("headerTitle").textContent = "Liberation Library";
      const navBackBtn = document.getElementById("navBackBtn");
      if (navBackBtn) {{
        navBackBtn.textContent = "← AI Hub";
        navBackBtn.onclick = null;
        hydrateAppLinks();
      }}
      if (triggerHistory && typeof history !== "undefined" && history.pushState && (location.hash || location.search)) {{
        history.pushState({{ view: "library" }}, "", location.pathname + (location.search ? location.search.replace(/[?&]book=[^&]+/g, "") : ""));
      }}
      currentBook = null;
      if (lastLibraryScrollY > 0) {{
        window.scrollTo({{ top: lastLibraryScrollY, behavior: "instant" }});
      }}
    }}

    function toggleTrackSection(id) {{
      const sec = document.getElementById(id);
      if (sec) sec.classList.toggle("collapsed");
    }}

    function toggleCategoryCollapsible() {{
      const pane = document.getElementById("categoryCollapsible");
      if (pane) {{
        pane.classList.toggle("collapsed");
      }}
    }}

    function toggleReaderChapterDrawer() {{
      const drawer = document.getElementById("readerChapterDrawer");
      const chevron = document.getElementById("readerChaptersChevron");
      if (!drawer) return;
      const isHidden = (drawer.style.display === "none" || !drawer.style.display);
      if (isHidden) {{
        populateReaderChapterDrawer();
        drawer.style.display = "block";
        if (chevron) chevron.textContent = "▲";
      }} else {{
        drawer.style.display = "none";
        if (chevron) chevron.textContent = "▼";
      }}
    }}

    function populateReaderChapterDrawer() {{
      const list = document.getElementById("readerChapterDrawerList");
      if (!list || !currentBook) return;
      const bookDesc = currentBook.description || currentBook.skipped_note || "";
      list.innerHTML = bookDesc
        ? `<div class="track-book-desc" style="margin:6px 8px 10px;"><strong>📖 About ${{escapeHtml(currentBook.title)}}:</strong> ${{escapeHtml(bookDesc)}}</div>`
        : "";
      const items = currentTrackType === "adhd" ? (currentBook.adhd_segments || []) : (currentBook.author_chapters || []);
      items.forEach((item, idx) => {{
        const num = idx + 1;
        const el = document.createElement("div");
        const isActive = (currentItemIndex === num);
        el.className = "reader-drawer-item" + (isActive ? " active" : "");
        el.style.flexDirection = "column";
        el.style.alignItems = "stretch";
        el.style.gap = "5px";
        const pCount = item.pageCount ? `${{item.pageCount}}p` : (item.pages ? `p. ${{item.pages}}` : "");
        const effStr = item.effortLabel || (item.estMinutes ? `⏱️ ${{item.estMinutes}}m` : "");
        const prefix = currentTrackType === "adhd" ? `Step ${{num}}` : `Ch ${{num}}`;
        el.innerHTML = `
          <div class="reader-drawer-item-title" style="white-space:normal;overflow:visible;">${{isActive ? "▶ " : ""}}${{prefix}} · ${{escapeHtml(item.label)}}</div>
          ${{item.brief ? `<div style="font-size:0.78rem;color:var(--ink-muted);line-height:1.4;">${{escapeHtml(item.brief)}}</div>` : ""}}
          <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;">
            <div class="reader-drawer-item-meta">${{pCount}}${{effStr ? ` · ${{effStr}}` : ""}}</div>
            <span class="btn-ch play-btn" style="padding:3px 10px;font-size:0.74rem;">Absorb</span>
          </div>
        `;
        el.onclick = () => {{
          selectChapterFromDrawer(num);
        }};
        list.appendChild(el);
      }});
      const activeEl = list.querySelector(".reader-drawer-item.active");
      if (activeEl) {{
        activeEl.scrollIntoView({{ block: "nearest" }});
      }}
    }}

    function selectChapterFromDrawer(newIdx) {{
      const drawer = document.getElementById("readerChapterDrawer");
      const chevron = document.getElementById("readerChaptersChevron");
      if (drawer) drawer.style.display = "none";
      if (chevron) chevron.textContent = "▼";
      readChapter(currentTrackType, newIdx);
    }}

    /* ==========================================================================
       ROBUST AUDIO PLAYBACK (OFFLINE CACHE FIRST -> BLOB URL -> GITHUB RAW STREAM)
       ========================================================================== */
    async function playChapter(trackType, index) {{
      if (!currentBook) return;
      currentTrackType = trackType;
      currentItemIndex = index;

      const trackInfo = findAudioTrack(currentBook, trackType, index);
      if (!trackInfo) {{
        showToast("Audio track not yet generated for this chapter.");
        return;
      }}

      const trackTitle = (trackType === "adhd" ? `Step ${{index}}` : `Chapter ${{index}}`) + ` · ${{trackInfo.label || "Chapter"}}`;
      document.getElementById("playerBookTitle").textContent = currentBook.title;
      document.getElementById("playerChapterTitle").textContent = trackTitle;

      // SHOW the player bar only when user explicitly chooses to play!
      document.getElementById("playerBar").style.display = "flex";

      const remoteUrl = `${{GH_RAW_AUDIO_BASE}}${{trackInfo.url}}`;
      const relPath = trackInfo.url;

      if (activeBlobUrl) {{
        URL.revokeObjectURL(activeBlobUrl);
        activeBlobUrl = null;
      }}

      // 1. Try CacheStorage first (guarantees 100% offline playback even on airplane mode)
      let resolvedSrc = null;
      try {{
        if ("caches" in window) {{
          const cache = await caches.open(CACHE_NAME);
          const cachedResp = (await cache.match(remoteUrl)) || (await cache.match(relPath));
          if (cachedResp) {{
            const blob = await cachedResp.blob();
            activeBlobUrl = URL.createObjectURL(blob);
            resolvedSrc = activeBlobUrl;
          }}
        }}
      }} catch (e) {{
        console.warn("Cache lookup error:", e);
      }}

      // 2. If not in cache, use remote raw URL directly
      if (!resolvedSrc) {{
        resolvedSrc = remoteUrl;
      }}

      audioEl.src = resolvedSrc;
      audioEl.load();

      try {{
        if (currentChapterWords && currentChapterWords.length && trackInfo) {{
          buildAcousticWordTimeline(currentChapterWords, currentChapterTotalWeight, trackInfo);
        }}
        await audioEl.play();
        requestScreenWakeLock();
        karaokeActive = true;
        updateReaderPlayButton(true);

        if ("mediaSession" in navigator) {{
          navigator.mediaSession.metadata = new MediaMetadata({{
            title: trackTitle,
            artist: currentBook.author || "Liberation Library",
            album: currentBook.title,
            artwork: [{{ src: "assets/icons/favicon-hub.png", sizes: "96x96", type: "image/png" }}]
          }});
        }}
      }} catch (err) {{
        console.warn("Playback play() rejected:", err);
        document.getElementById("btnPlayPause").textContent = "▶";
        updateReaderPlayButton(false);
        showToast("Audio unavailable offline. Tap ⚙️ to download.");
      }}
    }}

    /* ==========================================================================
       SETTINGS & OFFLINE CACHE MANAGER (CHAPTERS + AUDIO FLIGHT MODE SYNC)
       ========================================================================== */
    async function checkOfflineFilesStatus() {{
      const audioFiles = AUDIO_INDEX.files || [];
      const chapterFiles = CHAPTER_FILES || [];
      const total = audioFiles.length + chapterFiles.length;

      if (!("caches" in window)) {{
        return {{
          total,
          cached: 0,
          missing: total,
          audioTotal: audioFiles.length,
          audioCached: 0,
          chaptersTotal: chapterFiles.length,
          chaptersCached: 0,
          missingAudio: audioFiles.map(f => ({{ file: f, url: `${{GH_RAW_AUDIO_BASE}}${{f.url}}`, type: "audio" }})),
          missingChapters: chapterFiles.map(c => ({{ chapter: c, path: c.path, type: "chapter" }})),
        }};
      }}

      try {{
        const cache = await caches.open(CACHE_NAME);
        let audioCachedCount = 0;
        const missingAudio = [];
        for (const f of audioFiles) {{
          const remoteUrl = `${{GH_RAW_AUDIO_BASE}}${{f.url}}`;
          const relPath = `audio/${{f.url}}`;
          const hasRemote = await cache.match(remoteUrl);
          const hasRel = await cache.match(relPath);
          if (hasRemote || hasRel) {{
            audioCachedCount++;
          }} else {{
            missingAudio.push({{ file: f, url: remoteUrl, relPath, type: "audio" }});
          }}
        }}

        let chaptersCachedCount = 0;
        const missingChapters = [];
        for (const c of chapterFiles) {{
          const relPath = c.path;
          const remoteUrl = `https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/${{c.path}}`;
          const previewUrl = `https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/kalyani-reels/${{c.path}}`;
          const hasRel = await cache.match(relPath);
          const hasRemote = await cache.match(remoteUrl);
          const hasPrev = await cache.match(previewUrl);
          if (hasRel || hasRemote || hasPrev) {{
            chaptersCachedCount++;
          }} else {{
            missingChapters.push({{ chapter: c, path: relPath, remoteUrl, previewUrl, type: "chapter" }});
          }}
        }}

        return {{
          total,
          cached: audioCachedCount + chaptersCachedCount,
          missing: missingAudio.length + missingChapters.length,
          audioTotal: audioFiles.length,
          audioCached: audioCachedCount,
          chaptersTotal: chapterFiles.length,
          chaptersCached: chaptersCachedCount,
          missingAudio,
          missingChapters,
        }};
      }} catch (err) {{
        console.warn("Error checking offline files status:", err);
        return {{
          total,
          cached: 0,
          missing: total,
          audioTotal: audioFiles.length,
          audioCached: 0,
          chaptersTotal: chapterFiles.length,
          chaptersCached: 0,
          missingAudio: audioFiles.map(f => ({{ file: f, url: `${{GH_RAW_AUDIO_BASE}}${{f.url}}`, type: "audio" }})),
          missingChapters: chapterFiles.map(c => ({{ chapter: c, path: c.path, type: "chapter" }})),
        }};
      }}
    }}

    async function updateStorageMetrics() {{
      try {{
        const audioFiles = AUDIO_INDEX.files || [];
        const statAudio = document.getElementById("statModalAudioFiles");
        const statChapters = document.getElementById("statModalChaptersCount");
        const statDownloaded = document.getElementById("statModalDownloadedCount");
        const statMissing = document.getElementById("statModalMissingCount");
        const btnSync = document.getElementById("btnModalStartSync");

        // Check how many files are downloaded vs not downloaded
        const status = await checkOfflineFilesStatus();

        if (statAudio) {{
          statAudio.textContent = `${{status.audioCached}} / ${{status.audioTotal}} audio tracks downloaded`;
        }}
        if (statChapters) {{
          statChapters.textContent = `${{status.chaptersCached}} / ${{status.chaptersTotal}} chapter HTML pages`;
        }}
        if (statDownloaded) {{
          statDownloaded.textContent = `${{status.cached}} / ${{status.total}} files cached`;
        }}
        if (statMissing) {{
          if (status.missing === 0) {{
            statMissing.textContent = "0 files (100% offline ready ✓)";
            statMissing.style.color = "#10B981";
          }} else {{
            statMissing.textContent = `${{status.missing}} files remaining (${{status.missingChapters.length}} chapters, ${{status.missingAudio.length}} audio)`;
            statMissing.style.color = "#F59E0B";
          }}
        }}

        // Check cache storage size
        const statCacheSize = document.getElementById("statModalCacheSize");
        if (statCacheSize) {{
          if ("storage" in navigator && "estimate" in navigator.storage) {{
            const est = await navigator.storage.estimate();
            const usedMb = ((est.usage || 0) / (1024 * 1024)).toFixed(1);
            statCacheSize.textContent = `${{usedMb}} MB in Cache`;
          }} else if ("caches" in window) {{
            const cache = await caches.open(CACHE_NAME);
            const keys = await cache.keys();
            statCacheSize.textContent = `${{keys.length}} files in Cache`;
          }} else {{
            statCacheSize.textContent = "Available";
          }}
        }}

        if (btnSync && !isDownloading) {{
          if (status.missing === 0) {{
            btnSync.textContent = "✓ All Files Downloaded (100% Offline Ready)";
            btnSync.style.background = "#059669";
          }} else if (status.cached > 0) {{
            btnSync.textContent = `⚡ Download Remaining ${{status.missing}} Files for Offline`;
            btnSync.style.background = "";
          }} else {{
            btnSync.textContent = `⚡ Download All for Offline (${{status.total}} files)`;
            btnSync.style.background = "";
          }}
        }}
      }} catch (e) {{
        console.warn("Storage metric error:", e);
      }}
    }}

    async function downloadEntireLibraryOffline() {{
      if (isDownloading) return;
      isDownloading = true;

      const pBox = document.getElementById("offlineProgressBox");
      const pFill = document.getElementById("progressBarFill");
      const pPct = document.getElementById("progressPercentage");
      const pTitle = document.getElementById("progressStepTitle");
      const pSub = document.getElementById("progressStatusSub");
      const btnSync = document.getElementById("btnModalStartSync");

      pBox.classList.add("active");
      btnSync.disabled = true;

      try {{
        const cache = await caches.open(CACHE_NAME);
        const status = await checkOfflineFilesStatus();
        const total = status.total;
        const missingChapters = status.missingChapters;
        const missingAudio = status.missingAudio;
        const totalMissing = missingChapters.length + missingAudio.length;

        // If no files are missing, everything is already downloaded!
        if (totalMissing === 0) {{
          pFill.style.width = "100%";
          pPct.textContent = "100%";
          pTitle.textContent = "✓ Already Up to Date";
          pSub.textContent = `All ${{total}} files (${{CHAPTER_FILES.length}} chapters + audio) are already saved in offline cache.`;
          showToast(`✓ All ${{total}} files are already cached.`);
          setTimeout(() => {{
            btnSync.disabled = false;
            isDownloading = false;
            updateStorageMetrics();
          }}, 1200);
          return;
        }}

        let newlyDownloaded = 0;
        let processedCount = status.cached;

        // 1. Download Chapter HTML files (All ${{CHAPTER_FILES.length}} chapters across all ${{BOOKS_DATA.length}} books)
        for (let i = 0; i < missingChapters.length; i++) {{
          const item = missingChapters[i];
          const ch = item.chapter;
          processedCount++;
          const pct = Math.round((processedCount / total) * 100);
          pFill.style.width = `${{pct}}%`;
          pPct.textContent = `${{pct}}%`;
          pTitle.textContent = `Downloading Chapters [${{i + 1}}/${{missingChapters.length}}]`;
          pSub.textContent = `${{ch.bookTitle}} — ${{ch.label}}`;

          try {{
            let resp = null;
            try {{
              resp = await fetch(item.path);
            }} catch (_e) {{}}
            if (!resp || !resp.ok) {{
              resp = await fetch(item.remoteUrl, {{ mode: "cors" }});
            }}
            if (resp && resp.ok) {{
              const htmlText = await resp.text();
              const responseObj = () => new Response(htmlText, {{
                headers: {{ "Content-Type": "text/html; charset=utf-8" }}
              }});
              await cache.put(item.path, responseObj());
              await cache.put(item.remoteUrl, responseObj());
              if (item.previewUrl) {{
                await cache.put(item.previewUrl, responseObj());
              }}
              newlyDownloaded++;
            }}
          }} catch (err) {{
            console.warn("Could not cache chapter:", item.path, err);
          }}
        }}

        // 2. Download Voice Audio files
        for (let j = 0; j < missingAudio.length; j++) {{
          const item = missingAudio[j];
          const f = item.file;
          processedCount++;
          const pct = Math.round((processedCount / total) * 100);
          pFill.style.width = `${{pct}}%`;
          pPct.textContent = `${{pct}}%`;
          pTitle.textContent = `Downloading Audio Tracks [${{j + 1}}/${{missingAudio.length}}]`;
          pSub.textContent = `${{f.bookTitle || "Audiobook"}} — ${{f.label || f.file}}`;

          try {{
            const resp = await fetch(item.url, {{ mode: "cors" }});
            if (resp.ok) {{
              const buf = await resp.arrayBuffer();
              const blobResponse = () => new Response(new Blob([buf], {{ type: "audio/mpeg" }}), {{
                headers: {{ "Content-Type": "audio/mpeg" }}
              }});
              await cache.put(item.url, blobResponse());
              if (item.relPath) {{
                await cache.put(item.relPath, blobResponse());
              }}
              newlyDownloaded++;
            }} else {{
              console.warn("Fetch failed for audio:", item.url, resp.status);
            }}
          }} catch (err) {{
            console.warn("Could not cache audio:", item.url, err);
          }}
        }}

        // 3. Cache books.html itself for offline access
        try {{
          const bResp = await fetch("books.html");
          if (bResp && bResp.ok) {{
            await cache.put("books.html", bResp.clone());
            await cache.put("./books.html", bResp.clone());
            await cache.put(location.href, bResp.clone());
          }}
        }} catch (_be) {{}}

        pFill.style.width = "100%";
        pPct.textContent = "100%";
        pTitle.textContent = "✓ 100% Offline Ready!";
        pSub.textContent = `Downloaded ${{newlyDownloaded}} files. All ${{CHAPTER_FILES.length}} chapters & audio are saved for flights.`;
        showToast(`✓ All chapters and voices downloaded for offline flights!`);

        setTimeout(() => {{
          btnSync.disabled = false;
          isDownloading = false;
          updateStorageMetrics();
        }}, 1500);

      }} catch (err) {{
        console.error("Offline download error:", err);
        pTitle.textContent = "Sync incomplete";
        pSub.textContent = "Some files could not be downloaded.";
        btnSync.disabled = false;
        isDownloading = false;
        updateStorageMetrics();
      }}
    }}

    async function clearOfflineCache() {{
      if (confirm("Clear offline library cache? You can re-download anytime before a flight.")) {{
        try {{
          await caches.delete(CACHE_NAME);
          showToast("Offline cache cleared.");
          updateStorageMetrics();
        }} catch (e) {{
          showToast("Error clearing cache.");
        }}
      }}
    }}

    function updateOfflineStatus() {{
      const badge = document.getElementById("modalStatusBadge");
      if (badge) {{
        if (navigator.onLine) {{
          badge.textContent = "🟢 Online";
          badge.style.color = "var(--emerald)";
        }} else {{
          badge.textContent = "📴 Offline";
          badge.style.color = "var(--amber)";
        }}
      }}
    }}
    window.addEventListener("online", updateOfflineStatus);
    window.addEventListener("offline", updateOfflineStatus);

    /* ==========================================================================
       CHAPTER READER (FULL PAGE RANGE TEXT + KARAOKE-STYLE HIGHLIGHTING)
       ========================================================================== */
    async function readChapter(trackType, index) {{
      if (!currentBook) return;
      currentTrackType = trackType;
      currentItemIndex = index;

      // Reset reader chapters drawer state
      const drawer = document.getElementById("readerChapterDrawer");
      const chevron = document.getElementById("readerChaptersChevron");
      if (drawer) drawer.style.display = "none";
      if (chevron) chevron.textContent = "▼";

      const items = trackType === "adhd" ? (currentBook.adhd_segments || []) : (currentBook.author_chapters || []);
      const fallbackItem = items[index - 1] || {{}};

      const title = (trackType === "adhd" ? `Step ${{index}}` : `Ch ${{index}}`) + ` · ${{fallbackItem.label || "Chapter"}}`;
      document.getElementById("readerHeaderTitle").textContent = title;

      const modal = document.getElementById("readerModal");
      const body = document.getElementById("readerContentBody");
      modal.classList.add("active");

      // Show friendly loading skeleton while full text loads
      body.innerHTML = `
        <div style="padding: 40px 20px; text-align: center; color: var(--ink-muted);">
          <div style="font-size: 1.6rem; margin-bottom: 8px;">📖 Loading complete chapter text...</div>
          <div style="font-size: 0.9rem;">Retrieving full page range for ${{currentBook.title}}</div>
        </div>
      `;

      const itemData = await getChapterText(currentBook, trackType, index);
      const content = itemData && itemData.content ? itemData.content : (fallbackItem.brief || "");
      const label = itemData && itemData.label ? itemData.label : fallbackItem.label;
      const pages = itemData && itemData.pages ? itemData.pages : fallbackItem.pages;
      const durMin = itemData && itemData.duration_min ? itemData.duration_min : fallbackItem.duration_min;
      const brief = itemData && itemData.brief ? itemData.brief : fallbackItem.brief;

      const {{ html, wordsList, totalWeight }} = renderMarkdownWithKaraoke(content, brief, label, pages, durMin);
      body.innerHTML = html;

      currentChapterWords = wordsList;
      currentChapterTotalWeight = totalWeight;
      activeWordIdx = -1;

      // Calibrate acoustic timeline if audio track metadata / silences exist
      const trackInfo = findAudioTrack(currentBook, trackType, index);
      if (trackInfo) {{
        buildAcousticWordTimeline(currentChapterWords, currentChapterTotalWeight, trackInfo);
      }}

      // Sync reader listen button state
      const isCurrentlyPlayingThis = (!audioEl.paused && currentTrackType === trackType && currentItemIndex === index);
      updateReaderPlayButton(isCurrentlyPlayingThis);

      if (isCurrentlyPlayingThis) {{
        karaokeActive = true;
        syncKaraokeWord();
      }}
    }}

    // Tap/Click anywhere on a word in the text to jump audio playback to that exact word
    document.getElementById("readerContentBody").addEventListener("click", (e) => {{
      const span = e.target.closest(".k-word");
      if (!span) return;
      const wIdx = parseInt(span.getAttribute("data-word-idx"), 10);
      if (Number.isFinite(wIdx) && currentChapterWords[wIdx]) {{
        if (currentChapterWords[wIdx].startSec !== undefined) {{
          audioEl.currentTime = currentChapterWords[wIdx].startSec;
        }} else {{
          const dur = audioEl.duration;
          if (Number.isFinite(dur) && dur > 0 && currentChapterTotalWeight > 0) {{
            const targetTime = (currentChapterWords[wIdx].cumWeight / currentChapterTotalWeight) * dur;
            audioEl.currentTime = targetTime;
          }}
        }}
        if (audioEl.paused) {{
          audioEl.play();
        }}
      }}
    }});

    document.getElementById("btnCloseReader").addEventListener("click", () => {{
      document.getElementById("readerModal").classList.remove("active");
    }});
    document.getElementById("btnReaderListenCurrent").addEventListener("click", () => {{
      if (currentBook && currentTrackType && currentItemIndex) {{
        if (!audioEl.paused && audioEl.src) {{
          audioEl.pause();
        }} else if (audioEl.paused && audioEl.src && currentTrackType && currentItemIndex) {{
          audioEl.play();
        }} else {{
          playChapter(currentTrackType, currentItemIndex);
        }}
      }}
    }});
    document.getElementById("btnReaderPrev").addEventListener("click", () => {{
      if (currentItemIndex > 1) {{
        readChapter(currentTrackType, currentItemIndex - 1);
      }}
    }});
    document.getElementById("btnReaderNext").addEventListener("click", () => {{
      const items = currentTrackType === "adhd" ? (currentBook.adhd_segments || []) : (currentBook.author_chapters || []);
      if (currentItemIndex < items.length) {{
        readChapter(currentTrackType, currentItemIndex + 1);
      }}
    }});
    document.getElementById("btnFontSmaller").addEventListener("click", () => {{
      readerFontSize = Math.max(0.85, readerFontSize - 0.1);
      document.getElementById("readerContentBody").style.fontSize = `${{readerFontSize}}rem`;
    }});
    document.getElementById("btnFontLarger").addEventListener("click", () => {{
      readerFontSize = Math.min(1.45, readerFontSize + 0.1);
      document.getElementById("readerContentBody").style.fontSize = `${{readerFontSize}}rem`;
    }});

    /* ==========================================================================
       SETTINGS & GENERAL EVENT LISTENERS
       ========================================================================== */
    const settingsModal = document.getElementById("settingsModal");
    document.getElementById("btnOpenSettings").addEventListener("click", () => {{
      settingsModal.classList.add("active");
      updateStorageMetrics();
    }});
    document.getElementById("btnCloseSettingsModal").addEventListener("click", () => {{
      settingsModal.classList.remove("active");
    }});
    document.getElementById("btnModalStartSync").addEventListener("click", downloadEntireLibraryOffline);
    document.getElementById("btnClearCacheBtn").addEventListener("click", clearOfflineCache);
    document.getElementById("btnRefreshManifestBtn").addEventListener("click", () => {{
      updateStorageMetrics();
      showToast("Refreshed storage status.");
    }});

    document.getElementById("btnBackToLibrary").addEventListener("click", backToLibrary);
    document.getElementById("btnDownloadBookOffline").addEventListener("click", () => {{
      settingsModal.classList.add("active");
      downloadEntireLibraryOffline();
    }});
    document.getElementById("btnPlayAllAdhd").addEventListener("click", () => playChapter("adhd", 1));
    document.getElementById("btnPlayAllFull").addEventListener("click", () => playChapter("author", 1));

    document.getElementById("bookSearchInput").addEventListener("input", (e) => {{
      activeSearchQuery = e.target.value;
      renderBooksGrid();
    }});

    function syncPillarChipsUI() {{
      const allChip = document.querySelector('.filter-chip[data-cat="all"]');
      if (allChip) {{
        if (selectedCategories.size === 0 && !inProgressOnly) allChip.classList.add("active");
        else allChip.classList.remove("active");
      }}
      document.querySelectorAll('.category-pills .filter-chip:not([data-cat="all"])').forEach(c => {{
        const cName = c.getAttribute("data-cat");
        if (selectedCategories.has(cName)) c.classList.add("active");
        else c.classList.remove("active");
      }});
      const ipChip = document.getElementById("inProgressFilterChip");
      if (ipChip) {{
        if (inProgressOnly) ipChip.classList.add("active");
        else ipChip.classList.remove("active");
      }}
    }}

    document.querySelectorAll(".filter-chip").forEach(chip => {{
      chip.addEventListener("click", () => {{
        const cat = chip.getAttribute("data-cat") || "all";
        if (cat === "all") {{
          selectedCategories.clear();
          inProgressOnly = false;
          activeCategory = "all";
        }} else if (cat === "in-progress") {{
          inProgressOnly = !inProgressOnly;
          activeCategory = inProgressOnly ? "in-progress" : (Array.from(selectedCategories)[0] || "all");
        }} else {{
          if (selectedCategories.has(cat)) {{
            selectedCategories.delete(cat);
          }} else {{
            selectedCategories.add(cat);
          }}
          if (selectedCategories.size >= 4) {{
            selectedCategories.clear();
          }}
          activeCategory = Array.from(selectedCategories)[0] || (inProgressOnly ? "in-progress" : "all");
        }}
        syncPillarChipsUI();
        renderBooksGrid();
      }});
    }});

    // Theme Toggle
    document.getElementById("themeToggleBtn").addEventListener("click", () => {{
      const isDark = document.documentElement.getAttribute("data-theme") === "dark";
      if (isDark) {{
        document.documentElement.removeAttribute("data-theme");
      }} else {{
        document.documentElement.setAttribute("data-theme", "dark");
      }}
    }});

    function getCleanBookSlug(b) {{
      if (!b) return "";
      const title = (b.title || "").toLowerCase();
      const slug = (b.slug || "").toLowerCase();
      if (title.includes("gene") || slug.includes("gene")) return "the-gene";
      if (title.includes("code book") || slug.includes("code_book")) return "the-code-book";
      let clean = slug.replace(/^\\d+[a-z]?_/, "");
      clean = clean.replace(/_+/g, "-");
      clean = clean.replace(/[^\\w\\-]/g, "").replace(/^-+|-+$/g, "");
      return clean || slug;
    }}

    function hydrateAppLinks() {{
      try {{
        if (typeof location === "undefined" || typeof document === "undefined") return;
        const isHtmlPreview = /htmlpreview\\.github\\.io/i.test(location.hostname || "") || /github\\.com[\\/]kouSeek[\\/]portfolio[\\/]blob[\\/]/i.test(location.search || "");
        if (!isHtmlPreview) return;
        const m = (location.search || "").match(/https:[\\/][\\/]github\\.com[\\/]kouSeek[\\/]portfolio[\\/]blob[\\/]([^/]+)[\\/]/i);
        const branch = (m && m[1]) ? m[1] : "kalyani-reels";

        document.querySelectorAll("a[href^='chapters/']").forEach(a => {{
          const href = a.getAttribute("href");
          a.href = "https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/" + branch + "/" + href;
        }});
      }} catch (e) {{}}
    }}

    // Support GitHub Preview rewriting
    (function hydrateHubAppLinks() {{
      try {{
        if (typeof location === "undefined" || typeof document === "undefined") return;
        const isHtmlPreview = /htmlpreview\\.github\\.io/i.test(location.hostname || "") || /github\\.com[\\/]kouSeek[\\/]portfolio[\\/]blob[\\/]/i.test(location.search || "");
        if (!isHtmlPreview) return;
        const m = (location.search || "").match(/https:[\\/][\\/]github\\.com[\\/]kouSeek[\\/]portfolio[\\/]blob[\\/]([^/]+)[\\/]/i);
        const branch = (m && m[1]) ? m[1] : "kalyani-reels";
        const backBtn = document.getElementById("navBackBtn");
        if (backBtn) {{
          backBtn.href = "https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/" + branch + "/index.html";
        }}
        hydrateAppLinks();
      }} catch (e) {{}}
    }})();

    // Offline Navigation Interceptor: When offline in flight mode, intercept clicks to chapter pages
    // and render them directly from CacheStorage (0ms, zero network requests).
    document.addEventListener("click", async (e) => {{
      const a = e.target.closest("a[href*='chapters/']");
      if (!a) return;
      const href = a.getAttribute("href");
      if (!href) return;
      if (currentBook) {{
        const rowEl = a.closest(".chapter-row");
        const lblEl = rowEl && rowEl.querySelector ? rowEl.querySelector(".chapter-label") : null;
        const stepLabel = lblEl ? lblEl.textContent.trim() : "Step 1";
        saveMobileBookProgress(currentBook, stepLabel, href);
      }}

      const isOffline = (!navigator.onLine || window.__FORCE_OFFLINE__);
      if (isOffline) {{
        e.preventDefault();
        const cleanPath = href.replace(/^.*[\\/]chapters[\\/]/, "chapters/");
        if ("caches" in window) {{
          try {{
            const cache = await caches.open(CACHE_NAME);
            let cachedResp = await cache.match(cleanPath);
            if (!cachedResp) cachedResp = await cache.match(href);
            if (!cachedResp) {{
              const remoteUrl = `https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/${{cleanPath}}`;
              cachedResp = await cache.match(remoteUrl);
            }}
            if (cachedResp) {{
              const htmlText = await cachedResp.text();
              document.open();
              document.write(htmlText);
              document.close();
              try {{ window.history.pushState({{ path: cleanPath }}, "", cleanPath); }} catch (_e) {{}}
              return;
            }}
          }} catch (ce) {{
            console.warn("Offline cache read error:", ce);
          }}
        }}
      }}
    }});

    // Register Service Worker for offline flight mode
    if (typeof navigator !== "undefined" && "serviceWorker" in navigator) {{
      navigator.serviceWorker.register("kalyani-sw.js").catch(() => {{}});
    }}

    function updateDynamicCounts() {{
      let totalCh = 0;
      BOOKS_DATA.forEach(b => {{
        totalCh += (b.adhd_segments || []).length + (b.author_chapters || []).length;
      }});
      document.querySelectorAll(".category-pills .filter-chip").forEach(chip => {{
        const cat = chip.getAttribute("data-cat") || "all";
        const countEl = chip.querySelector(".filter-chip-count");
        if (!countEl) return;
        if (cat === "all") {{
          countEl.textContent = String(BOOKS_DATA.length);
        }} else {{
          const cnt = BOOKS_DATA.filter(b => bookMatchesCategoryLabel(b, cat)).length;
          countEl.textContent = String(cnt);
        }}
      }});
      const badge = document.getElementById("activeCategoryBadge");
      if (badge && selectedCategories.size === 0 && !inProgressOnly) {{
        badge.textContent = `🌐 All Pillars (${{BOOKS_DATA.length}})`;
      }}
      const statVols = document.getElementById("statModalVolumesCount");
      if (statVols) statVols.textContent = `${{BOOKS_DATA.length}} volumes (Inlined)`;
      const statChaps = document.getElementById("statModalChaptersCount");
      if (statChaps) statChaps.textContent = `${{totalCh}} chapters`;
    }}

    async function refreshLiveCatalogCountsIfUpdated() {{
      try {{
        if (typeof fetch !== "function" || (typeof navigator !== "undefined" && navigator.onLine === false) || window.__FORCE_OFFLINE__) return;
        const resp = await fetch("assets/books_catalog.json", {{ cache: "no-store" }});
        if (!resp || !resp.ok) return;
        const liveList = await resp.json();
        if (Array.isArray(liveList) && liveList.length !== BOOKS_DATA.length) {{
          BOOKS_DATA.length = 0;
          liveList.forEach(item => BOOKS_DATA.push(item));
          updateDynamicCounts();
          renderBooksGrid();
        }}
      }} catch (_e) {{}}
    }}

    // Render immediately from inlined data and sync any newly added books dynamically
    updateDynamicCounts();
    renderInProgressBar();
    renderBooksGrid();
    refreshLiveCatalogCountsIfUpdated();
    updateOfflineStatus();
    updateStorageMetrics();

    function checkInitialUrlBook() {{
      try {{
        if (typeof location === "undefined") return;
        const hashMatch = (location.hash || "").match(/#book=([^&]+)/i);
        const searchMatch = (location.search || "").match(/[?&]book=([^&]+)/i);
        const slug = hashMatch ? decodeURIComponent(hashMatch[1]) : (searchMatch ? decodeURIComponent(searchMatch[1]) : null);
        if (slug) {{
          openBookDetail(slug, false);
        }}
      }} catch (_e) {{}}
    }}

    window.addEventListener("popstate", (e) => {{
      if (e.state && e.state.view === "detail" && e.state.slug) {{
        openBookDetail(e.state.slug, false);
      }} else {{
        const dv = document.getElementById("bookDetailView");
        if (dv && dv.classList.contains("active")) {{
          backToLibrary(false);
        }}
      }}
    }});

    checkInitialUrlBook();
  </script>
</body>
</html>
"""

    OUTPUT_PATH.write_text(html_content, encoding="utf-8")
    print(f"Generated self-contained {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size:,} bytes)")


main = generate_books_html

if __name__ == "__main__":
    generate_books_html()
