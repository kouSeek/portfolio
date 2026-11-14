#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate offline VoiceLM-XL Aoede UK Female audio for Liberation Library books in AI Companion.

Produces clean, high-quality chapter MP3s for phone offline reading & listening.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

APP_ROOT = Path(__file__).resolve().parent.parent
WIKI_ROOT = Path("/usr/local/google/home/koushikchak/koushik-wiki")
LIBERATION_LIB_DIR = Path.home() / "Downloads" / "Liberation_Library"
AUDIO_BOOKS_DIR = APP_ROOT / "audio" / "books"

sys.path.insert(0, str(WIKI_ROOT / "scripts"))
sys.path.insert(0, str(APP_ROOT / "scripts"))

from transcript_cards import (
    LIBERATION_LIBRARY_CATALOG,
    extract_readable_book_markdown,
)
from server import (
    split_tts_text_chunks,
    synthesize_gemini_neural_tts,
)
from calibrate_books_audio_sync import (
    extract_mp3_silences,
    calibrate_all_audio_timings,
)


def clean_markdown_for_speech(raw_text: str) -> str:
    """Strip markdown headers, links, backticks, and clean formatting for VoiceLM speech."""
    s = str(raw_text or "")
    # Remove link cards or listen links
    s = re.sub(r"\[[^\]]*Listen[^\]]*\]\(sidecar://[^\)]+\)", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", s)
    s = re.sub(r"\[\[([^|\]]+)(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), s)
    # Strip markdown headers, blockquotes, bullets
    s = re.sub(r"^[#>-]+\s*", "", s, flags=re.MULTILINE)
    # Convert ~ before numbers to 'about'
    s = re.sub(r"(?:^|(?<=\s|[(\[]))~\s*(?=[₹$€£]?\d)", "about ", s)
    # Clean code blocks and inline code
    s = re.sub(r"```[^\n]*\n([\s\S]*?)```", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    # Clean bold / italics / strikethrough
    s = re.sub(r"[*_~]+", "", s)
    # Clean multiple spaces and blank lines
    lines = [ln.strip() for ln in s.splitlines() if ln.strip()]
    cleaned = " ".join(lines)
    return " ".join(cleaned.split())


def synthesize_text_to_mp3(text: str, voice_name: str = "Aoede", max_workers: int = 6) -> bytes:
    """Chunk and synthesize text using parallel VoiceLM-XL Aoede calls, returning concatenated MP3 bytes."""
    chunks = split_tts_text_chunks(text, max_chars=360)
    if not chunks:
        return b""

    results: list[bytes | None] = [None] * len(chunks)

    def worker(idx: int, chunk: str) -> tuple[int, bytes]:
        for attempt in range(3):
            try:
                mp3 = synthesize_gemini_neural_tts(chunk, voice_name=voice_name, timeout_sec=20.0)
                if mp3 and len(mp3) > 100:
                    return idx, mp3
            except Exception as e:
                time.sleep(0.5 * (attempt + 1))
        return idx, b""

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(worker, i, ch) for i, ch in enumerate(chunks)]
        for fut in as_completed(futures):
            i, data = fut.result()
            results[i] = data

    valid_chunks = [c for c in results if c]
    return b"".join(valid_chunks)


def get_mp3_duration_sec(mp3_path: Path) -> float:
    """Use ffprobe to determine duration of an MP3 file."""
    try:
        proc = subprocess.run(
            ["ffprobe", "-i", str(mp3_path), "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"],
            capture_output=True,
            text=True,
            check=False,
        )
        return float(proc.stdout.strip())
    except Exception:
        return 0.0


def generate_book_audio(
    book_filename: str,
    slug: str,
    track_types: list[str] = ("adhd", "author"),
    max_steps_per_track: int | None = None,
    overwrite: bool = False,
) -> dict[str, object]:
    """Generate audio files for all steps and chapters of a book."""
    pdf_path = LIBERATION_LIB_DIR / book_filename
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Book PDF not found: {pdf_path}")

    meta = LIBERATION_LIBRARY_CATALOG.get(book_filename, {})
    title = meta.get("title", pdf_path.stem)
    author = meta.get("author", "")

    book_out_dir = AUDIO_BOOKS_DIR / slug
    book_out_dir.mkdir(parents=True, exist_ok=True)

    manifest_file = book_out_dir / "manifest.json"
    manifest: dict[str, object] = {
        "title": title,
        "author": author,
        "filename": book_filename,
        "slug": slug,
        "voice": "Aoede",
        "tracks": {},
    }

    print(f"\n==================================================")
    print(f"🎙️ Generating Voices for: {title} by {author}")
    print(f"📂 Output Directory: {book_out_dir}")
    print(f"==================================================")

    tracks_data: dict[str, list[dict[str, object]]] = {}

    for t_type in track_types:
        raw_items = meta.get("adhd_segments" if t_type == "adhd" else "author_chapters", [])
        if max_steps_per_track:
            raw_items = raw_items[:max_steps_per_track]

        track_entries: list[dict[str, object]] = []
        track_label = "⚡ Core Steps" if t_type == "adhd" else "📖 Full Book Chapters"
        print(f"\n--- Track: {track_label} ({len(raw_items)} items) ---")

        for idx, item in enumerate(raw_items, 1):
            fname = f"{t_type}_{idx}.mp3"
            mp3_path = book_out_dir / fname
            label = item.get("label", f"Chapter {idx}")
            pages = item.get("pages", "")
            brief = item.get("brief", "")

            if mp3_path.is_file() and mp3_path.stat().st_size > 1000 and not overwrite:
                dur = get_mp3_duration_sec(mp3_path)
                sils = extract_mp3_silences(mp3_path)
                print(f"  [{idx}/{len(raw_items)}] ✓ Cached: {fname} ({dur:.1f}s, {len(sils)} silences) - {label[:45]}")
                track_entries.append({
                    "index": idx,
                    "label": label,
                    "pages": pages,
                    "brief": brief,
                    "file": fname,
                    "durationSec": dur,
                    "sizeBytes": mp3_path.stat().st_size,
                    "silences": sils,
                })
                continue

            print(f"  [{idx}/{len(raw_items)}] 🎙️ Synthesizing {fname}: {label[:45]} (pages {pages})...")
            # Extract text
            res = extract_readable_book_markdown(pdf_path, pages_spec=pages, track=t_type, step_index=idx)
            raw_content = res.get("content", "")
            clean_speech = clean_markdown_for_speech(raw_content)

            # Synthesize MP3
            t0 = time.time()
            mp3_bytes = synthesize_text_to_mp3(clean_speech, voice_name="Aoede", max_workers=6)
            elapsed = time.time() - t0

            if mp3_bytes:
                mp3_path.write_bytes(mp3_bytes)
                dur = get_mp3_duration_sec(mp3_path)
                sils = extract_mp3_silences(mp3_path)
                print(f"     ✓ Done in {elapsed:.1f}s -> {len(mp3_bytes):,} bytes ({dur:.1f}s audio, {len(sils)} silences)")
                track_entries.append({
                    "index": idx,
                    "label": label,
                    "pages": pages,
                    "brief": brief,
                    "file": fname,
                    "durationSec": dur,
                    "sizeBytes": len(mp3_bytes),
                    "silences": sils,
                })
            else:
                print(f"     ❌ Failed to synthesize audio for {label}")

        tracks_data[t_type] = track_entries

    manifest["tracks"] = tracks_data
    manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✅ Manifest saved to {manifest_file}")
    return manifest


def main():
    parser = argparse.ArgumentParser(description="Generate Aoede UK Female audio for Liberation Library books.")
    parser.add_argument("--book", choices=("gene", "code-book", "both"), default="both", help="Which book to generate voices for")
    parser.add_argument("--track", choices=("adhd", "author", "all"), default="all", help="Tracks to generate")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing audio files")
    args = parser.parse_args()

    AUDIO_BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    tracks = ("adhd", "author") if args.track == "all" else (args.track,)

    if args.book in ("gene", "both"):
        generate_book_audio(
            book_filename="01_The_Gene_An_Intimate_History_Siddhartha_Mukherjee_COMPLETE.pdf",
            slug="the-gene",
            track_types=list(tracks),
            overwrite=args.overwrite,
        )

    if args.book in ("code-book", "both"):
        generate_book_audio(
            book_filename="14_The_Code_Book_Simon_Singh.pdf",
            slug="the-code-book",
            track_types=list(tracks),
            overwrite=args.overwrite,
        )

    # Automatically calibrate acoustic silence maps and update books_audio_index.json
    calibrate_all_audio_timings()


if __name__ == "__main__":
    main()
