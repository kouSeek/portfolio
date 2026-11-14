#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract and calibrate acoustic silence maps for Liberation Library book audio files.

Automatically runs ffmpeg silencedetect to map voiced intervals for every chapter audio file.
Stores calibrated silence intervals in assets/books_audio_index.json and audio/books/<slug>/manifest.json.
This ensures word-by-word karaoke highlighting stays in exact 1:1 acoustic sync across text blocks,
headings, blockquotes, and paragraph pairings without drift.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import time

APP_ROOT = Path(__file__).resolve().parent.parent
AUDIO_INDEX_PATH = APP_ROOT / "assets" / "books_audio_index.json"
AUDIO_BOOKS_DIR = APP_ROOT / "audio" / "books"


def extract_mp3_silences(mp3_path: Path, min_silence_sec: float = 0.35, noise_db: float = -30.0) -> list[list[float]]:
    """Use ffmpeg silencedetect to find all silence intervals [start, end] in seconds."""
    if not mp3_path.is_file():
        return []
    try:
        proc = subprocess.run(
            ["ffmpeg", "-i", str(mp3_path), "-af", f"silencedetect=noise={noise_db}dB:d={min_silence_sec}", "-f", "null", "-"],
            capture_output=True,
            text=True,
            check=False,
        )
        silences: list[list[float]] = []
        for line in proc.stderr.splitlines():
            if "silence_end:" in line and "silence_duration:" in line:
                m_e = re.search(r"silence_end:\s*([\d.]+)", line)
                m_d = re.search(r"silence_duration:\s*([\d.]+)", line)
                if m_e and m_d:
                    s = round(float(m_e.group(1)) - float(m_d.group(1)), 3)
                    e = round(float(m_e.group(1)), 3)
                    if e > s:
                        silences.append([s, e])
        return silences
    except Exception as e:
        print(f"Warning: could not extract silences from {mp3_path}: {e}")
        return []


def calibrate_all_audio_timings() -> dict:
    """Extract silence maps for all audio tracks in books_audio_index.json."""
    if not AUDIO_INDEX_PATH.is_file():
        raise FileNotFoundError(f"Audio index not found: {AUDIO_INDEX_PATH}")

    data = json.load(open(AUDIO_INDEX_PATH, encoding="utf-8"))
    files = data.get("files", [])
    print(f"🎙️ Calibrating acoustic silence maps for {len(files)} audio files...")

    timings_by_path: dict[str, dict] = {}

    for idx, item in enumerate(files, 1):
        rel_url = item.get("url", "")
        mp3_path = APP_ROOT / rel_url
        if not mp3_path.is_file():
            print(f"  [{idx}/{len(files)}] ⚠️ Missing file: {rel_url}")
            continue

        t0 = time.time()
        existing_sils = item.get("silences")
        if isinstance(existing_sils, list) and len(existing_sils) > 0:
            sils = existing_sils
            dur = item.get("durationSec") or 0.0
            elapsed = time.time() - t0
            timings_by_path[rel_url] = {"dur": dur, "silences": sils}
            print(f"  [{idx}/{len(files)}] ✓ Cached {item.get('slug')} / {item.get('file')}: {len(sils)} silences ({dur:.1f}s)")
            continue

        sils = extract_mp3_silences(mp3_path)
        dur = item.get("durationSec") or 0.0
        elapsed = time.time() - t0

        item["silences"] = sils
        timings_by_path[rel_url] = {
            "dur": dur,
            "silences": sils,
        }
        print(f"  [{idx}/{len(files)}] ✓ {item.get('slug')} / {item.get('file')}: {len(sils)} silences ({dur:.1f}s) in {elapsed:.2f}s")

    # Update books_audio_index.json
    AUDIO_INDEX_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Updated {AUDIO_INDEX_PATH}")

    # Also update per-book manifest.json
    for book_dir in AUDIO_BOOKS_DIR.iterdir():
        if not book_dir.is_dir():
            continue
        man_path = book_dir / "manifest.json"
        if not man_path.is_file():
            continue
        try:
            m_data = json.load(open(man_path, encoding="utf-8"))
            tracks = m_data.get("tracks", {})
            for t_type, t_list in tracks.items():
                if not isinstance(t_list, list):
                    continue
                for t_entry in t_list:
                    f_name = t_entry.get("file", "")
                    f_rel = f"audio/books/{book_dir.name}/{f_name}"
                    if f_rel in timings_by_path:
                        t_entry["silences"] = timings_by_path[f_rel]["silences"]
            man_path.write_text(json.dumps(m_data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"  ✓ Updated manifest: {man_path}")
        except Exception as err:
            print(f"  ⚠️ Error updating {man_path}: {err}")

    return data


if __name__ == "__main__":
    calibrate_all_audio_timings()
