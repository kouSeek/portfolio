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

APP_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = APP_ROOT / "audio" / "books"
ASSETS_DIR = APP_ROOT / "assets"


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
        st = books_audio_status.get(slug)
        if st and st["count"] > 0:
            b["has_audio"] = True
            b["audio_count"] = st["count"]
            b["audio_bytes"] = st["totalBytes"]
        else:
            b["has_audio"] = False
            b["audio_count"] = 0
            b["audio_bytes"] = 0

    catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated {len(catalog)} books in {catalog_path}")
    return audio_index_payload


if __name__ == "__main__":
    build_audio_index()
