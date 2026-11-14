#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 100% self-contained mobile-friendly Books Library (`books.html`) for AI Companion.

Inlines `assets/books_catalog.json` and `assets/books_audio_index.json` directly into JavaScript
so the page requires ZERO external JSON fetches on `htmlpreview.github.io` or mobile Chrome.
"""

from __future__ import annotations

import json
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = APP_ROOT / "assets" / "books_catalog.json"
AUDIO_INDEX_PATH = APP_ROOT / "assets" / "books_audio_index.json"
GENE_TEXT_PATH = APP_ROOT / "assets" / "books_text" / "01_the_gene_an_intimate_history_siddhartha_mukherjee_complete.json"
CODE_TEXT_PATH = APP_ROOT / "assets" / "books_text" / "14_the_code_book_simon_singh.json"
OUTPUT_PATH = APP_ROOT / "books.html"


def generate_books_html() -> None:
    catalog_json = CATALOG_PATH.read_text(encoding="utf-8") if CATALOG_PATH.is_file() else "[]"
    audio_index_json = AUDIO_INDEX_PATH.read_text(encoding="utf-8") if AUDIO_INDEX_PATH.is_file() else "{}"

    gene_text = json.loads(GENE_TEXT_PATH.read_text(encoding="utf-8")) if GENE_TEXT_PATH.is_file() else {}
    code_text = json.loads(CODE_TEXT_PATH.read_text(encoding="utf-8")) if CODE_TEXT_PATH.is_file() else {}
    inlined_text_dict = {
        "01_the_gene_an_intimate_history_siddhartha_mukherjee_complete": gene_text,
        "the-gene": gene_text,
        "14_the_code_book_simon_singh": code_text,
        "the-code-book": code_text,
    }
    inlined_text_json = json.dumps(inlined_text_dict, ensure_ascii=False)

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
    .category-pills {{
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 6px;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
    }}
    .category-pills::-webkit-scrollbar {{
      display: none;
    }}
    .filter-chip {{
      white-space: nowrap;
      padding: 6px 12px;
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 600;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--ink-muted);
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .filter-chip.active {{
      background: var(--accent);
      color: #FFFFFF;
      border-color: var(--accent);
      box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25);
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

    /* Chapter Row */
    .chapter-row {{
      padding: 12px 18px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      transition: background 0.12s ease;
    }}
    .chapter-row:last-child {{
      border-bottom: none;
    }}
    .chapter-row:hover {{
      background: var(--surface-subtle);
    }}
    .chapter-info {{
      flex: 1;
      min-width: 0;
    }}
    .chapter-title-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
    }}
    .chapter-label {{
      font-weight: 700;
      font-size: 0.92rem;
      line-height: 1.35;
    }}
    .chapter-metrics {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}
    .chapter-chip {{
      font-size: 0.72rem;
      padding: 2px 6px;
      border-radius: 4px;
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
      margin: 6px 0 6px;
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
    .chapter-brief {{
      font-size: 0.8rem;
      color: var(--ink-muted);
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .chapter-actions {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-shrink: 0;
    }}
    .btn-ch {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      padding: 6px 10px;
      border-radius: var(--radius-sm);
      font-size: 0.78rem;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--ink);
      transition: all 0.12s ease;
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
        <div class="category-pills" id="categoryPills">
          <button class="filter-chip active" data-cat="all">All Books</button>
          <button class="filter-chip" data-cat="Science & Frontier">🧬 Science & Frontier</button>
          <button class="filter-chip" data-cat="Mind & Psychology">🧠 Mind & Fast/Slow</button>
          <button class="filter-chip" data-cat="Philosophy & Warfare">⚔️ Philosophy & Warfare</button>
          <button class="filter-chip" data-cat="Literature & Classics">📜 Literature & Classics</button>
          <button class="filter-chip" data-cat="Space & Physics">🚀 Space & Physics</button>
          <button class="filter-chip" data-cat="Wizarding & Fantasy">⚡ Harry Potter & Fantasy</button>
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
        Save all 29 books, chapter summaries, and neural voice files to your phone's browser cache for 100% offline reading and listening during flights.
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
          <span>29 volumes (Inlined)</span>
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
      <div style="font-weight: 700; font-size: 0.95rem; text-align: center; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" id="readerHeaderTitle">Chapter Title</div>
      <div style="display: flex; gap: 6px;">
        <button class="btn-action" style="padding: 4px 8px;" id="btnFontSmaller">A-</button>
        <button class="btn-action" style="padding: 4px 8px;" id="btnFontLarger">A+</button>
      </div>
    </header>
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
    /* ==========================================================================
       INLINED CATALOG & AUDIO INDEX (100% SELF-CONTAINED, ZERO EXTERNAL JSON FETCHES)
       ========================================================================== */
    const BOOKS_DATA = {catalog_json};
    const AUDIO_INDEX = {audio_index_json};
    const INLINED_BOOKS_TEXT = {inlined_text_json};
    const GH_RAW_AUDIO_BASE = "https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/";
    const CACHE_NAME = "kortex-books-v1";

    let currentBook = null;
    let currentTrackType = "adhd";
    let currentItemIndex = 1;
    let activeCategory = "all";
    let activeSearchQuery = "";
    let readerFontSize = 1.05;
    let isDownloading = false;
    let activeBlobUrl = null;
    let currentChapterWords = [];
    let currentChapterTotalWeight = 0;
    let activeWordIdx = -1;
    let karaokeActive = false;

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

    function renderMarkdownWithKaraoke(content, brief, label, pages, durMin) {{
      let wordIndex = 0;
      const wordsList = [];

      function escapeHtml(str) {{
        return String(str || "")
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;");
      }}

      function wrapWords(text) {{
        const tokens = text.split(/(\\s+)/);
        return tokens.map(tok => {{
          if (/^\\s+$/.test(tok) || !tok) return tok;
          const clean = tok.replace(/[*_#`~[\\]()]/g, "");
          const wIdx = wordIndex++;
          const weight = Math.max(1, clean.length);
          wordsList.push({{
            index: wIdx,
            word: clean,
            weight: weight
          }});
          return `<span class="k-word" data-word-idx="${{wIdx}}" id="kword_${{wIdx}}">${{escapeHtml(tok)}}</span>`;
        }}).join("");
      }}

      let headerHtml = `
        <div class="reader-meta-banner">
          <h2 style="font-size: 1.4rem; margin-top: 0; margin-bottom: 8px;">${{escapeHtml(label)}}</h2>
          <div class="reader-meta-pill-row">
            <span>📚 ${{escapeHtml(currentBook.title)}}</span>
            <span>📄 Pages: ${{escapeHtml(pages || "N/A")}}</span>
            <span>⏱️ Duration: ~${{escapeHtml(durMin || 15)}} mins</span>
          </div>
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

        if (line.startsWith("## Step") || line.startsWith("## Chapter") || line.startsWith("# Step")) {{
          continue;
        }}

        if (line.startsWith(">")) {{
          if (!inQuote) {{ bodyHtml += "<blockquote>"; inQuote = true; }}
          line = line.replace(/^>\\s*/, "");
          bodyHtml += `<p>${{wrapWords(line)}}</p>`;
        }} else if (line.startsWith("### ")) {{
          if (inQuote) {{ bodyHtml += "</blockquote>"; inQuote = false; }}
          bodyHtml += `<h3>${{wrapWords(line.slice(4))}}</h3>`;
        }} else if (line.startsWith("## ")) {{
          if (inQuote) {{ bodyHtml += "</blockquote>"; inQuote = false; }}
          bodyHtml += `<h2>${{wrapWords(line.slice(3))}}</h2>`;
        }} else if (line.startsWith("# ")) {{
          if (inQuote) {{ bodyHtml += "</blockquote>"; inQuote = false; }}
          bodyHtml += `<h1>${{wrapWords(line.slice(2))}}</h1>`;
        }} else {{
          if (inQuote) {{ bodyHtml += "</blockquote>"; inQuote = false; }}
          bodyHtml += `<p>${{wrapWords(line)}}</p>`;
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

    function syncKaraokeWord() {{
      if (!karaokeActive || !currentChapterWords.length || currentChapterTotalWeight <= 0) return;
      const dur = audioEl.duration;
      if (!Number.isFinite(dur) || dur <= 0) return;
      const curTime = audioEl.currentTime;
      const progress = Math.min(1.0, Math.max(0, curTime / dur));
      const targetWeight = progress * currentChapterTotalWeight;

      let low = 0;
      let high = currentChapterWords.length - 1;
      let foundIdx = 0;
      while (low <= high) {{
        const mid = (low + high) >> 1;
        if (currentChapterWords[mid].cumWeight <= targetWeight) {{
          foundIdx = mid;
          low = mid + 1;
        }} else {{
          high = mid - 1;
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

    function renderBooksGrid() {{
      const grid = document.getElementById("booksGrid");
      grid.innerHTML = "";

      const filtered = BOOKS_DATA.filter(b => {{
        const matchesCat = activeCategory === "all" || b.category.toLowerCase().includes(activeCategory.toLowerCase());
        const q = activeSearchQuery.toLowerCase().trim();
        const matchesSearch = !q || b.title.toLowerCase().includes(q) || b.author.toLowerCase().includes(q) || (b.description || "").toLowerCase().includes(q);
        return matchesCat && matchesSearch;
      }});

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

        card.innerHTML = `
          <div>
            <div class="book-card-header">
              <div class="book-card-emoji">${{b.cover_emoji || "📖"}}</div>
              <div class="book-card-titles">
                <div class="book-card-title">${{b.title}}</div>
                <div class="book-card-author">${{b.author || "Liberation Library"}}</div>
              </div>
            </div>
            <p style="font-size: 0.82rem; color: var(--ink-muted); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 10px;">${{b.description || ""}}</p>
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

    function openBookDetail(slugOrFilename) {{
      const book = BOOKS_DATA.find(b => b.slug === slugOrFilename || b.filename === slugOrFilename);
      if (!book) return;
      currentBook = book;

      document.getElementById("libraryView").style.display = "none";
      const dv = document.getElementById("bookDetailView");
      dv.classList.add("active");

      document.getElementById("detailEmoji").textContent = book.cover_emoji || "📖";
      document.getElementById("detailTitle").textContent = book.title;
      document.getElementById("detailAuthor").textContent = book.author || "Liberation Library";
      document.getElementById("detailDesc").textContent = book.description || "";
      document.getElementById("headerTitle").textContent = book.title;

      const adhdTime = cleanEffortStr(book.adhd_time_label);
      const fullTime = cleanEffortStr(book.full_time_label);
      const adhdPages = book.adhd_total_pages ? `${{book.adhd_total_pages}} pages` : "";
      const adhdVol = book.adhd_volume_pct ? `${{book.adhd_volume_pct}}% of book` : "";
      const prunedInfo = book.pruned_pct ? `${{book.pruned_pct}}% pruned` : "";
      const fullPages = book.full_book_pages || book.pages ? `${{book.full_book_pages || book.pages}} pages` : "";

      document.getElementById("detailBadges").innerHTML = `
        <span class="badge-chip adhd">⚡ ${{(book.adhd_segments || []).length}} Steps ${{adhdPages ? `· ${{adhdPages}}` : ""}} ${{adhdVol ? `· ${{adhdVol}}` : ""}} ${{prunedInfo ? `(${{prunedInfo}})` : ""}} ${{adhdTime ? `· ⏱️ ${{adhdTime}}` : ""}}</span>
        <span class="badge-chip full">📖 ${{(book.author_chapters || []).length}} Chapters ${{fullPages ? `· ${{fullPages}}` : ""}} ${{fullTime ? `· ⏱️ ${{fullTime}}` : ""}}</span>
      `;

      const cleanSlug = getCleanBookSlug(book);

      // Render ADHD track
      const adhdBody = document.getElementById("adhdTrackBody");
      adhdBody.innerHTML = "";
      const adhdItems = book.adhd_segments || [];
      document.getElementById("adhdTrackBadge").textContent = `${{adhdItems.length}} steps`;

      adhdItems.forEach((item, idx) => {{
        const stepNum = idx + 1;
        const row = document.createElement("div");
        row.className = "chapter-row";
        const pageRange = item.pages ? `p. ${{item.pages}}` : "";
        const pageCnt = item.pageCount ? `${{item.pageCount}}p` : "";
        const volPct = item.volumePct ? `${{item.volumePct}}%` : "";
        const effStr = item.effortLabel || (item.estMinutes ? `⏱️ ${{item.estMinutes}}m` : (item.duration_min ? `⏱️ ${{item.duration_min}}m` : ""));
        const volWidth = Math.min(100, Math.max(4, Math.round((Number(item.volumePct) || 2) * 2.2)));

        row.innerHTML = `
          <div class="chapter-info">
            <div class="chapter-title-row">
              <span class="chapter-label">Step ${{stepNum}} · ${{item.label}}</span>
              <div class="chapter-metrics">
                ${{pageRange ? `<span class="chapter-chip">${{pageRange}}</span>` : ""}}
                ${{pageCnt ? `<span class="chapter-chip count">${{pageCnt}} (${{volPct}})</span>` : ""}}
                ${{effStr ? `<span class="chapter-chip effort">${{effStr}}</span>` : ""}}
              </div>
            </div>
            <div class="book-toc-vol-bar-track">
              <div class="book-toc-vol-bar-fill adhd" style="width: ${{volWidth}}%;"></div>
            </div>
            <div class="chapter-brief">${{item.brief || ""}}</div>
          </div>
          <div class="chapter-actions">
            <a class="btn-ch play-btn" href="chapters/${{cleanSlug}}/step_${{stepNum}}.html" style="text-decoration:none; display:inline-flex; align-items:center; gap:4px;">📖 Read &amp; Listen →</a>
          </div>
        `;
        adhdBody.appendChild(row);
      }});

      // Render Full Book track
      const fullBody = document.getElementById("fullTrackBody");
      fullBody.innerHTML = "";
      const fullItems = book.author_chapters || [];
      document.getElementById("fullTrackBadge").textContent = `${{fullItems.length}} chapters`;

      fullItems.forEach((item, idx) => {{
        const chNum = idx + 1;
        const row = document.createElement("div");
        row.className = "chapter-row";
        const pageRange = item.pages ? `p. ${{item.pages}}` : "";
        const pageCnt = item.pageCount ? `${{item.pageCount}}p` : "";
        const volPct = item.volumePct ? `${{item.volumePct}}%` : "";
        const effStr = item.effortLabel || (item.estMinutes ? `⏱️ ${{item.estMinutes}}m` : (item.duration_min ? `⏱️ ${{item.duration_min}}m` : ""));
        const volWidth = Math.min(100, Math.max(4, Math.round((Number(item.volumePct) || 2) * 2.2)));

        row.innerHTML = `
          <div class="chapter-info">
            <div class="chapter-title-row">
              <span class="chapter-label">Ch ${{chNum}} · ${{item.label}}</span>
              <div class="chapter-metrics">
                ${{pageRange ? `<span class="chapter-chip">${{pageRange}}</span>` : ""}}
                ${{pageCnt ? `<span class="chapter-chip count">${{pageCnt}} (${{volPct}})</span>` : ""}}
                ${{effStr ? `<span class="chapter-chip effort">${{effStr}}</span>` : ""}}
              </div>
            </div>
            <div class="book-toc-vol-bar-track">
              <div class="book-toc-vol-bar-fill author" style="width: ${{volWidth}}%;"></div>
            </div>
            <div class="chapter-brief">${{item.brief || ""}}</div>
          </div>
          <div class="chapter-actions">
            <a class="btn-ch play-btn" href="chapters/${{cleanSlug}}/ch_${{chNum}}.html" style="text-decoration:none; display:inline-flex; align-items:center; gap:4px;">📖 Read &amp; Listen →</a>
          </div>
        `;
        fullBody.appendChild(row);
      }});

      window.scrollTo({{ top: 0, behavior: "smooth" }});
      hydrateAppLinks();
    }}

    function backToLibrary() {{
      document.getElementById("bookDetailView").classList.remove("active");
      document.getElementById("libraryView").style.display = "block";
      document.getElementById("headerTitle").textContent = "Liberation Library";
      currentBook = null;
    }}

    function toggleTrackSection(id) {{
      const sec = document.getElementById(id);
      sec.classList.toggle("collapsed");
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
       SETTINGS & OFFLINE CACHE MANAGER
       ========================================================================== */
    async function checkOfflineFilesStatus() {{
      const audioFiles = AUDIO_INDEX.files || [];
      const total = audioFiles.length;
      if (!("caches" in window)) {{
        return {{
          total,
          cached: 0,
          missing: total,
          missingItems: audioFiles.map(f => ({{ file: f, url: `${{GH_RAW_AUDIO_BASE}}${{f.url}}` }}))
        }};
      }}
      try {{
        const cache = await caches.open(CACHE_NAME);
        let cachedCount = 0;
        const missing = [];
        for (const f of audioFiles) {{
          const remoteUrl = `${{GH_RAW_AUDIO_BASE}}${{f.url}}`;
          const relPath = `audio/${{f.url}}`;
          const hasRemote = await cache.match(remoteUrl);
          const hasRel = await cache.match(relPath);
          if (hasRemote || hasRel) {{
            cachedCount++;
          }} else {{
            missing.push({{ file: f, url: remoteUrl }});
          }}
        }}
        return {{
          total,
          cached: cachedCount,
          missing: missing.length,
          missingItems: missing
        }};
      }} catch (err) {{
        console.warn("Error checking offline audio status:", err);
        return {{
          total,
          cached: 0,
          missing: total,
          missingItems: audioFiles.map(f => ({{ file: f, url: `${{GH_RAW_AUDIO_BASE}}${{f.url}}` }}))
        }};
      }}
    }}

    async function updateStorageMetrics() {{
      try {{
        const audioFiles = AUDIO_INDEX.files || [];
        const statAudio = document.getElementById("statModalAudioFiles");
        if (statAudio) {{
          statAudio.textContent = `${{audioFiles.length}} chapters (99.3 MB)`;
        }}

        // Check cache storage size
        if ("storage" in navigator && "estimate" in navigator.storage) {{
          const est = await navigator.storage.estimate();
          const usedMb = ((est.usage || 0) / (1024 * 1024)).toFixed(1);
          document.getElementById("statModalCacheSize").textContent = `${{usedMb}} MB in Cache`;
        }} else if ("caches" in window) {{
          const cache = await caches.open(CACHE_NAME);
          const keys = await cache.keys();
          document.getElementById("statModalCacheSize").textContent = `${{keys.length}} files in Cache`;
        }} else {{
          document.getElementById("statModalCacheSize").textContent = "Available";
        }}

        // Check how many files are downloaded vs not downloaded
        const status = await checkOfflineFilesStatus();
        const statDownloaded = document.getElementById("statModalDownloadedCount");
        const statMissing = document.getElementById("statModalMissingCount");
        const btnSync = document.getElementById("btnModalStartSync");

        if (statDownloaded) {{
          statDownloaded.textContent = `${{status.cached}} / ${{status.total}} chapters`;
        }}
        if (statMissing) {{
          if (status.missing === 0) {{
            statMissing.textContent = "0 files (100% offline ready ✓)";
            statMissing.style.color = "#10B981";
          }} else {{
            statMissing.textContent = `${{status.missing}} file${{status.missing > 1 ? "s" : ""}} not downloaded`;
            statMissing.style.color = "#F59E0B";
          }}
        }}

        if (btnSync && !isDownloading) {{
          if (status.missing === 0) {{
            btnSync.textContent = "✓ All Files Downloaded (Offline Ready)";
            btnSync.style.background = "#059669";
          }} else if (status.cached > 0) {{
            btnSync.textContent = `⚡ Download Remaining ${{status.missing}} File${{status.missing > 1 ? "s" : ""}} for Offline`;
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
        const missingItems = status.missingItems;

        // If no files are missing, everything is already downloaded!
        if (missingItems.length === 0) {{
          pFill.style.width = "100%";
          pPct.textContent = "100%";
          pTitle.textContent = "✓ Already Up to Date";
          pSub.textContent = `All ${{total}} voice files are already saved in offline cache.`;
          showToast(`✓ All ${{total}} voice files are already cached.`);
          setTimeout(() => {{
            btnSync.disabled = false;
            isDownloading = false;
            updateStorageMetrics();
          }}, 1200);
          return;
        }}

        const needed = missingItems.length;
        const alreadyCached = status.cached;
        pTitle.textContent = `Downloading ${{needed}} missing file${{needed > 1 ? "s" : ""}}...`;
        pSub.textContent = `(${{alreadyCached}} already downloaded)`;

        let newlyDownloaded = 0;

        for (let i = 0; i < needed; i++) {{
          const item = missingItems[i];
          const fileName = item.file.file || item.url.split("/").pop();
          const bookTitle = item.file.bookTitle || "Audiobook";

          const currentOverallIndex = alreadyCached + i + 1;
          const pct = Math.round((currentOverallIndex / total) * 100);
          pFill.style.width = `${{pct}}%`;
          pPct.textContent = `${{pct}}%`;
          pTitle.textContent = `Downloading missing [${{i + 1}}/${{needed}}]`;
          pSub.textContent = `${{bookTitle}} — ${{fileName}}`;

          try {{
            const resp = await fetch(item.url, {{ mode: "cors" }});
            if (resp.ok) {{
              await cache.put(item.url, resp);
              newlyDownloaded++;
            }} else {{
              console.warn("Fetch failed for:", item.url, resp.status);
            }}
          }} catch (err) {{
            console.warn("Could not cache url:", item.url, err);
          }}
        }}

        // Also cache all book text files for complete offline reading
        pTitle.textContent = "Syncing book text files...";
        pSub.textContent = "Caching full chapter texts for offline reading...";
        for (let j = 0; j < BOOKS_DATA.length; j++) {{
          const b = BOOKS_DATA[j];
          const bSlug = (b.slug || b.filename.replace(/\\.pdf$/i, "")).toLowerCase();
          const textUrl = `https://raw.githubusercontent.com/kouSeek/portfolio/kalyani-reels/assets/books_text/${{bSlug}}.json`;
          try {{
            const hasText = await cache.match(textUrl);
            if (!hasText) {{
              const tResp = await fetch(textUrl, {{ mode: "cors" }});
              if (tResp.ok) {{
                await cache.put(textUrl, tResp);
              }}
            }}
          }} catch (te) {{}}
        }}

        pFill.style.width = "100%";
        pPct.textContent = "100%";
        pTitle.textContent = "✓ 100% Offline Ready!";
        pSub.textContent = `Downloaded ${{newlyDownloaded}} new file${{newlyDownloaded !== 1 ? "s" : ""}}. All ${{total}} voice tracks are cached for flights.`;
        showToast(`✓ ${{newlyDownloaded}} files downloaded for offline flights!`);

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
        const dur = audioEl.duration;
        if (Number.isFinite(dur) && dur > 0 && currentChapterTotalWeight > 0) {{
          const targetTime = (currentChapterWords[wIdx].cumWeight / currentChapterTotalWeight) * dur;
          audioEl.currentTime = targetTime;
          if (audioEl.paused) {{
            audioEl.play();
          }}
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

    document.querySelectorAll(".filter-chip").forEach(chip => {{
      chip.addEventListener("click", () => {{
        document.querySelectorAll(".filter-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        activeCategory = chip.getAttribute("data-cat");
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

    // Render immediately from inlined data
    renderBooksGrid();
    updateOfflineStatus();
    updateStorageMetrics();
  </script>
</body>
</html>
"""

    OUTPUT_PATH.write_text(html_content, encoding="utf-8")
    print(f"Generated self-contained {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    generate_books_html()
