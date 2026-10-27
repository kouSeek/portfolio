#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish `audio/` to the single-commit `ma-audio` orphan branch on GitHub.

Why this exists:
- Keeps `ma-course` ultra-lightweight (<5 MB, zero `.mp3` binaries in code history).
- Publishes all verified Gemini `Aoede` MP3s as a single-commit snapshot on branch `ma-audio`
  (`https://raw.githubusercontent.com/kouSeek/portfolio/ma-audio/audio/...`), preventing old
  replaced MP3 revisions from accumulating in `.git` history while avoiding Git LFS pointer/quota issues.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

APP_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = APP_ROOT / "audio"
AUDIO_BRANCH = "ma-audio"


def get_origin_url() -> str:
    proc = subprocess.run(
        ["git", "-C", str(APP_ROOT), "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()


def sync_ma_audio_orphan_branch(dry_run: bool = False) -> int:
    if not (AUDIO_DIR / "tts_manifest.json").is_file():
        print("[ma-audio] Missing audio/tts_manifest.json", file=sys.stderr)
        return 1

    mp3_files = sorted(AUDIO_DIR.rglob("*.mp3"))
    if not mp3_files:
        print("[ma-audio] No local .mp3 files found in audio/ to publish.", file=sys.stderr)
        return 1

    origin_url = get_origin_url()
    total_mb = sum(p.stat().st_size for p in mp3_files) / (1024 * 1024)
    print(f"[ma-audio] Preparing single-commit orphan snapshot: {len(mp3_files)} MP3s ({total_mb:.1f} MB) -> {origin_url} ({AUDIO_BRANCH})")

    if dry_run:
        return 0

    with tempfile.TemporaryDirectory(prefix="kalyani_ma_audio_") as tmp:
        stage_root = Path(tmp)
        dst_audio = stage_root / "audio"
        shutil.copytree(AUDIO_DIR, dst_audio)
        (stage_root / "README.md").write_text(
            "# 🌸 কল্যাণী (`ma-audio` Single-Commit Voice Asset Branch)\n\n"
            "This orphan branch stores only the latest active Gemini `Aoede` `.mp3` voice assets for `ma-course` "
            "as a single-commit snapshot so replaced audio binaries never bloat Git history.\n",
            encoding="utf-8",
        )

        subprocess.run(["git", "-C", str(stage_root), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(stage_root), "checkout", "-q", "--orphan", AUDIO_BRANCH], check=True)
        subprocess.run(["git", "-C", str(stage_root), "add", "README.md", "audio"], check=True)
        subprocess.run(
            ["git", "-C", str(stage_root), "commit", "-q", "-m", f"Snapshot: {len(mp3_files)} Kalyani Aoede MP3 assets (1-commit orphan branch)"],
            check=True,
        )
        subprocess.run(["git", "-C", str(stage_root), "remote", "add", "origin", origin_url], check=True)
        subprocess.run(["git", "-C", str(stage_root), "push", "--force", "origin", f"{AUDIO_BRANCH}:{AUDIO_BRANCH}"], check=True)

    print(f"[ma-audio] Successfully published {len(mp3_files)} MP3s to single-commit branch '{AUDIO_BRANCH}'.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish audio/ to single-commit ma-audio orphan branch.")
    parser.add_argument("--dry-run", action="store_true", help="Verify local audio files without pushing.")
    args = parser.parse_args()
    return sync_ma_audio_orphan_branch(dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
