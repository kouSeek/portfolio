#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build offline audio and text index for Books Library in AI Companion.

Scans `audio/books/` and generates:
1. `assets/books_audio_index.json`: List of all generated audio files, byte sizes, and durations.
2. Updates `assets/books_catalog.json` with has_audio flags and audio file paths.
"""

from __future__ import annotations

import json
from pathlib import Path
import re

APP_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = APP_ROOT / "audio" / "books"
ASSETS_DIR = APP_ROOT / "assets"
WIKI_CATALOG_PATH = Path("/usr/local/google/home/koushikchak/koushik-wiki/assets/books_catalog.json")


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


def build_audio_index() -> dict:
    manifest_files = sorted(AUDIO_DIR.glob("*/manifest.json"))
    catalog_path = ASSETS_DIR / "books_catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8")) if catalog_path.is_file() else []

    audio_files: list[dict] = []
    books_audio_status: dict[str, dict] = {}

    for mf in manifest_files:
        try:
            m = json.loads(mf.read_text(encoding="utf-8"))
            slug = m.get("slug")
            title = m.get("title", slug)
            tracks = m.get("tracks", {})
            slug_audio_files = []

            for track_type, items in tracks.items():
                for item in items:
                    f = item.get("file")
                    if not f:
                        continue
                    p = AUDIO_DIR / slug / f
                    if p.is_file():
                        entry = {
                            "slug": slug,
                            "bookTitle": title,
                            "trackType": track_type,
                            "index": item.get("index"),
                            "label": item.get("label", ""),
                            "url": f"audio/books/{slug}/{f}",
                            "file": f,
                            "sizeBytes": p.stat().st_size,
                            "durationSec": item.get("durationSec", 0),
                            "silences": item.get("silences", []),
                        }
                        audio_files.append(entry)
                        slug_audio_files.append(entry)

            books_audio_status[slug] = {
                "count": len(slug_audio_files),
                "totalBytes": sum(x["sizeBytes"] for x in slug_audio_files),
                "files": [x["file"] for x in slug_audio_files],
            }
        except Exception as e:
            print(f"Error reading {mf}: {e}")

    # Write audio index
    audio_index_path = ASSETS_DIR / "books_audio_index.json"
    audio_index_payload = {
        "generatedAt": "2026-11-14T02:30:00Z",
        "totalFiles": len(audio_files),
        "totalBytes": sum(a["sizeBytes"] for a in audio_files),
        "booksCount": len(books_audio_status),
        "books": books_audio_status,
        "files": audio_files,
    }
    audio_index_path.write_text(json.dumps(audio_index_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote audio index to {audio_index_path} ({len(audio_files)} files, {audio_index_payload['totalBytes'] / (1024 * 1024):.1f} MB)")

    # Update catalog
    for b in catalog:
        slug = b.get("slug")
        clean_slug = get_clean_slug(b)
        st = books_audio_status.get(slug) or books_audio_status.get(clean_slug)
        if st and st["count"] > 0:
            b["has_audio"] = True
            b["audio_count"] = st["count"]
            b["audio_bytes"] = st["totalBytes"]
        else:
            b["has_audio"] = False
            b["audio_count"] = 0
            b["audio_bytes"] = 0

    catalog_json = json.dumps(catalog, indent=2, ensure_ascii=False)
    catalog_path.write_text(catalog_json, encoding="utf-8")
    if WIKI_CATALOG_PATH.parent.is_dir():
        WIKI_CATALOG_PATH.write_text(catalog_json, encoding="utf-8")
    print(f"Updated {len(catalog)} books in {catalog_path} ({sum(1 for b in catalog if b.get('has_audio'))} with audio)")
    return audio_index_payload


if __name__ == "__main__":
    build_audio_index()
