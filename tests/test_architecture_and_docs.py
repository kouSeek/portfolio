#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Architectural & Governance Invariant Tests for 🌸 কল্যাণী."""

from pathlib import Path
import py_compile
import subprocess
import sys
import unittest

APP_ROOT = Path(__file__).resolve().parent.parent


class TestArchitectureAndDocs(unittest.TestCase):

    def test_modular_directory_topology_and_zero_monoliths(self) -> None:
        """Verify strict modular separation across docs/, content/, src/, assets/, audio/, scripts/, tests/."""
        required_files = [
            "GEMINI.md",
            ".gemini/config/rules/kalyani_app_rules.md",
            "docs/spec.md",
            "docs/content-pipeline.md",
            "docs/student-persona.md",
            "docs/client-side-gemini.md",
            "students/ma_kalyani/persona.md",
            "students/ma_kalyani/curriculum_v2_draft.md",
            "content/__init__.py",
            "content/slides_and_quotes.py",
            "content/part1_days.py",
            "content/part2_days.py",
            "src/template.html",
            "src/styles/tokens.css",
            "src/styles/layout.css",
            "src/styles/components.css",
            "src/js/state.js",
            "src/js/audio.js",
            "src/js/plan-view.py" if False else "src/js/plan-view.js",
            "src/js/letter-view.js",
            "src/js/boot.js",
            "assets/icons/favicon.svg",
            "favicon.svg",
            "ma-manifest.json",
            "ma-sw.js",
            ".gitignore",
            "audio/tts_manifest.json",
            "scripts/build_app.py",
            "scripts/refresh_voices.py",
            "scripts/sync_audio_branch.py",
        ]
        for rel in required_files:
            self.assertTrue((APP_ROOT / rel).is_file(), f"Missing required modular file: {rel}")

        gitignore_txt = (APP_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("audio/**/*.mp3", gitignore_txt)
        self.assertIn("!audio/tts_manifest.json", gitignore_txt)

        # Legacy monolithic curriculum_data.py must not exist in scripts/
        self.assertFalse((APP_ROOT / "scripts" / "curriculum_data.py").exists())

        # build_app.py must remain a lean modular assembler (<220 lines, zero inline JS/CSS strings)
        build_src = (APP_ROOT / "scripts" / "build_app.py").read_text(encoding="utf-8")
        self.assertLess(len(build_src.splitlines()), 220)
        self.assertNotIn("<!DOCTYPE html>", build_src)
        self.assertNotIn("function renderPlanView", build_src)

    def test_no_auto_tts_rule_and_manifest_tracking(self) -> None:
        """Verify build_app.py never calls TTS and refresh_voices.py tracks all expected audio clips."""
        sys.path.insert(0, str(APP_ROOT))
        sys.path.insert(0, str(APP_ROOT / "scripts"))
        from refresh_voices import collect_expected_audio_items  # noqa: PLC0415

        for py_file in [*(APP_ROOT / "scripts").glob("*.py"), *(APP_ROOT / "content").glob("*.py")]:
            py_compile.compile(str(py_file), doraise=True)

        build_src = (APP_ROOT / "scripts" / "build_app.py").read_text(encoding="utf-8")
        self.assertNotIn("gemini-agents-generate/generate", build_src)
        self.assertNotIn("build_one(", build_src)

        gemini_md = (APP_ROOT / "GEMINI.md").read_text(encoding="utf-8")
        self.assertIn("Principal Software Architecture", gemini_md)
        self.assertIn("Genius Artist UX Design", gemini_md)
        self.assertIn("refresh_voices.py --confirm", gemini_md)

        expected_count = len(collect_expected_audio_items())
        proc = subprocess.run(
            [sys.executable, str(APP_ROOT / "scripts" / "refresh_voices.py"), "--status", "--scope", "all"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn(str(expected_count), proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
