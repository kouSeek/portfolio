#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish `audio/` (`audio/kalyani/` + `audio/anondo/`) to the single-commit `ai-companion-audio` orphan branch.

Why this exists:
- Keeps `ai-companion` ultra-lightweight (<5 MB, zero `.mp3` binaries in code history).
- Publishes all verified Gemini `Aoede` MP3s as a single-commit snapshot on branch `ai-companion-audio`
  (`https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/audio/<persona>/...`),
  preventing replaced MP3 revisions from accumulating in `.git` history while avoiding Git LFS quota issues.
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
AUDIO_BRANCH = "ai-companion-audio"


def get_origin_url() -> str:
    proc = subprocess.run(
        ["git", "-C", str(APP_ROOT), "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()


def sync_audio_orphan_branch(dry_run: bool = False) -> int:
    if not (AUDIO_DIR / "kalyani" / "tts_manifest.json").is_file():
        print("[ai-companion-audio] Missing audio/kalyani/tts_manifest.json", file=sys.stderr)
        return 1

    mp3_files = sorted(AUDIO_DIR.rglob("*.mp3"))
    if not mp3_files:
        print("[ai-companion-audio] No local .mp3 files found in audio/ to publish.", file=sys.stderr)
        return 1

    origin_url = get_origin_url()
    total_mb = sum(p.stat().st_size for p in mp3_files) / (1024 * 1024)
    print(f"[ai-companion-audio] Preparing 1-commit orphan snapshot: {len(mp3_files)} MP3s ({total_mb:.1f} MB) -> {origin_url} ({AUDIO_BRANCH})")

    if dry_run:
        return 0

    with tempfile.TemporaryDirectory(prefix="ai_companion_audio_") as tmp:
        stage_root = Path(tmp)
        shutil.copytree(AUDIO_DIR, stage_root / "audio")
        (stage_root / "README.md").write_text(
            "# ✨ AI Companion (`ai-companion-audio` Single-Commit Voice Asset Branch)\n\n"
            "Stores active Gemini `Aoede` `.mp3` voice assets for `ai-companion` (`audio/kalyani/`, `audio/anondo/` & `audio/jhalak/`) "
            "as a single-commit snapshot so replaced audio binaries never bloat Git history.\n",
            encoding="utf-8",
        )

        subprocess.run(["git", "-C", str(stage_root), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(stage_root), "checkout", "-q", "--orphan", AUDIO_BRANCH], check=True)
        subprocess.run(["git", "-C", str(stage_root), "add", "README.md", "audio"], check=True)
        subprocess.run(
            ["git", "-C", str(stage_root), "commit", "-q", "-m", f"Snapshot: {len(mp3_files)} AI Companion Aoede MP3 assets (1-commit orphan branch)"],
            check=True,
        )
        subprocess.run(["git", "-C", str(stage_root), "remote", "add", "origin", origin_url], check=True)
        subprocess.run(["git", "-C", str(stage_root), "push", "--force", "origin", f"{AUDIO_BRANCH}:{AUDIO_BRANCH}"], check=True)

    print(f"[ai-companion-audio] Successfully published {len(mp3_files)} MP3s to single-commit branch '{AUDIO_BRANCH}'.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish audio/ to single-commit ai-companion-audio orphan branch.")
    parser.add_argument("--dry-run", action="store_true", help="Verify local audio files without pushing.")
    args = parser.parse_args()
    raise SystemExit(sync_audio_orphan_branch(dry_run=args.dry_run))
