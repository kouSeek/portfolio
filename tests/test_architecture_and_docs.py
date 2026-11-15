#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Architectural & Governance Invariant Tests for AI Companion (`jhalak`, `zorba`, `books`, and `index.html`)."""

from pathlib import Path
import py_compile
import subprocess
import sys
import unittest

APP_ROOT = Path(__file__).resolve().parent.parent


class TestArchitectureAndDocs(unittest.TestCase):

    def test_modular_directory_topology_and_removed_21day_apps(self) -> None:
        """Verify strict modular separation across content/, src/{jhalak,zorba}/, assets/, audio/, scripts/ and complete removal of Kalyani & Anondo 21-day apps."""
        required_files = [
            "GEMINI.md",
            ".gemini/config/rules/ai_companion_rules.md",
            "docs/spec.md",
            "docs/content-pipeline.md",
            "content/__init__.py",
            "content/reels_seed.json",
            "src/templates/index.html.j2",
            "src/templates/jhalak.html.j2",
            "src/templates/zorba.html.j2",
            "src/jhalak/styles/jhalak.css",
            "src/jhalak/js/curated-content.js",
            "src/jhalak/js/feed-engine.js",
            "src/jhalak/js/player-ui.js",
            "src/zorba/styles/zorba.css",
            "src/zorba/js/curated-content.js",
            "src/zorba/js/player-ui.js",
            "assets/icons/favicon.svg",
            "favicon.svg",
            "kalyani-sw.js",
            ".gitignore",
            "audio/jhalak/tts_manifest.json",
            "audio/zorba/tts_manifest.json",
            "scripts/build_app.py",
            "scripts/refresh_voices.py",
            "scripts/sync_audio_branch.py",
            "index.html",
            "jhalak.html",
            "zorba.html",
            "jhalak-manifest.json",
            "zorba-manifest.json",
        ]
        for rel in required_files:
            self.assertTrue((APP_ROOT / rel).is_file(), f"Missing required modular file: {rel}")

        gitignore_txt = (APP_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("audio/**/*.mp3", gitignore_txt)
        self.assertIn("!audio/jhalak/tts_manifest.json", gitignore_txt)
        self.assertIn("!audio/zorba/tts_manifest.json", gitignore_txt)

        # Removed Kalyani & Anondo 21-Day apps and obsolete paths must not exist
        for obsolete in (
            "kalyani.html",
            "kalyani-manifest.json",
            "anondo.html",
            "personas",
            "src/kalyani",
            "src/anondo",
            "src/templates/kalyani.html.j2",
            "src/templates/anondo.html.j2",
            "content/kalyani",
            "content/anondo",
            "content/markdown_loader.py",
            "assets/kalyani",
            "assets/anondo",
            "assets/icons/favicon-kalyani.png",
            "assets/icons/favicon-anondo.png",
            "audio/kalyani",
            "audio/anondo",
            "scripts/curate_loop.py",
            "students",
            "scripts/build_koushik_app.py",
            "koushik.html",
            "docs/student-persona.md",
        ):
            self.assertFalse((APP_ROOT / obsolete).exists(), f"Removed/obsolete path should not exist: {obsolete}")

        # build_app.py must remain a lean Jinja2 modular assembler (<220 lines, zero inline JS/CSS strings)
        build_src = (APP_ROOT / "scripts" / "build_app.py").read_text(encoding="utf-8")
        self.assertLess(len(build_src.splitlines()), 220)
        self.assertIn("jinja2", build_src)
        self.assertNotIn("<!DOCTYPE html>", build_src)

    def test_no_auto_tts_rule_and_manifest_tracking(self) -> None:
        """Verify build_app.py never calls TTS and refresh_voices.py tracks all expected audio clips for jhalak and zorba."""
        sys.path.insert(0, str(APP_ROOT))
        sys.path.insert(0, str(APP_ROOT / "scripts"))
        from refresh_voices import collect_expected_audio_items  # noqa: PLC0415

        for py_file in [*(APP_ROOT / "scripts").glob("*.py"), *(APP_ROOT / "content").rglob("*.py")]:
            py_compile.compile(str(py_file), doraise=True)

        build_src = (APP_ROOT / "scripts" / "build_app.py").read_text(encoding="utf-8")
        self.assertNotIn("gemini-agents-generate/generate", build_src)
        self.assertNotIn("build_one(", build_src)

        for pid in ("jhalak", "zorba"):
            expected_count = len(collect_expected_audio_items(pid))
            proc = subprocess.run(
                [sys.executable, str(APP_ROOT / "scripts" / "refresh_voices.py"), "--persona", pid, "--status", "--scope", "all"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn(str(expected_count), proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
