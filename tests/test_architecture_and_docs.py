#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Architectural & Governance Invariant Tests for AI Companion (`kalyani` + `anondo`)."""

from pathlib import Path
import py_compile
import subprocess
import sys
import unittest

APP_ROOT = Path(__file__).resolve().parent.parent


class TestArchitectureAndDocs(unittest.TestCase):

    def test_modular_two_persona_directory_topology_and_zero_monoliths(self) -> None:
        """Verify strict modular separation across personas/{kalyani,anondo}/, content/, src/, assets/, audio/, scripts/."""
        required_files = [
            "GEMINI.md",
            ".gemini/config/rules/ai_companion_rules.md",
            "docs/spec.md",
            "docs/content-pipeline.md",
            "personas/kalyani/persona.md",
            "personas/kalyani/curriculum.md",
            "personas/kalyani/content_curation.md",
            "personas/kalyani/client-side-gemini.md",
            "personas/kalyani/curation_manifest.json",
            "personas/kalyani/days/part1_days.md",
            "personas/anondo/persona.md",
            "personas/anondo/curriculum.md",
            "personas/anondo/content_curation.md",
            "personas/anondo/client-side-gemini.md",
            "personas/anondo/curation_manifest.json",
            "personas/anondo/days/anondo_days.md",
            "content/__init__.py",
            "content/markdown_loader.py",
            "content/kalyani/__init__.py",
            "content/kalyani/slides_and_quotes.py",
            "content/kalyani/part1_days.py",
            "content/anondo/__init__.py",
            "content/anondo/anondo_days.py",
            "src/templates/index.html.j2",
            "src/templates/kalyani.html.j2",
            "src/templates/anondo.html.j2",
            "src/kalyani/styles/tokens.css",
            "src/kalyani/styles/layout.css",
            "src/kalyani/styles/components.css",
            "src/kalyani/js/state.js",
            "src/kalyani/js/audio.js",
            "src/kalyani/js/plan-view.js",
            "src/kalyani/js/letter-view.js",
            "src/kalyani/js/boot.js",
            "src/anondo/styles/tokens.css",
            "src/anondo/styles/components.css",
            "src/anondo/js/audio.js",
            "src/anondo/js/views.js",
            "assets/icons/favicon.svg",
            "favicon.svg",
            "kalyani-manifest.json",
            "kalyani-sw.js",
            ".gitignore",
            "audio/kalyani/tts_manifest.json",
            "audio/anondo/tts_manifest.json",
            "scripts/build_app.py",
            "scripts/curate_loop.py",
            "scripts/refresh_voices.py",
            "scripts/sync_audio_branch.py",
            "index.html",
            "kalyani.html",
            "anondo.html",
        ]
        for rel in required_files:
            self.assertTrue((APP_ROOT / rel).is_file(), f"Missing required modular file: {rel}")

        gitignore_txt = (APP_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("audio/**/*.mp3", gitignore_txt)
        self.assertIn("!audio/kalyani/tts_manifest.json", gitignore_txt)
        self.assertIn("!audio/anondo/tts_manifest.json", gitignore_txt)

        # Obsolete paths must not exist
        for obsolete in (
            "students",
            "scripts/build_koushik_app.py",
            "koushik.html",
            "docs/student-persona.md",
            "personas/kalyani/days/part2_days.md",
            "content/kalyani/part2_days.py",
        ):
            self.assertFalse((APP_ROOT / obsolete).exists(), f"Obsolete path should not exist: {obsolete}")

        # build_app.py must remain a lean Jinja2 modular assembler (<220 lines, zero inline JS/CSS strings)
        build_src = (APP_ROOT / "scripts" / "build_app.py").read_text(encoding="utf-8")
        self.assertLess(len(build_src.splitlines()), 220)
        self.assertIn("jinja2", build_src)
        self.assertNotIn("<!DOCTYPE html>", build_src)
        self.assertNotIn("function renderPlanView", build_src)

        loader_src = (APP_ROOT / "content/kalyani/part1_days.py").read_text(encoding="utf-8")
        self.assertLess(len(loader_src.splitlines()), 25, "content/kalyani/part1_days.py should be a thin Markdown loader")
        self.assertIn("load_days_markdown", loader_src)

    def test_no_auto_tts_rule_and_manifest_tracking(self) -> None:
        """Verify build_app.py never calls TTS and refresh_voices.py tracks all expected audio clips for both personas."""
        sys.path.insert(0, str(APP_ROOT))
        sys.path.insert(0, str(APP_ROOT / "scripts"))
        from refresh_voices import collect_expected_audio_items  # noqa: PLC0415

        for py_file in [*(APP_ROOT / "scripts").glob("*.py"), *(APP_ROOT / "content").rglob("*.py")]:
            py_compile.compile(str(py_file), doraise=True)

        build_src = (APP_ROOT / "scripts" / "build_app.py").read_text(encoding="utf-8")
        self.assertNotIn("gemini-agents-generate/generate", build_src)
        self.assertNotIn("build_one(", build_src)

        gemini_md = (APP_ROOT / "GEMINI.md").read_text(encoding="utf-8")
        self.assertIn("Principal Software Architecture", gemini_md)
        self.assertIn("Genius Artist UX Design", gemini_md)
        self.assertIn("refresh_voices.py --persona", gemini_md)

        for pid in ("kalyani", "anondo", "jhalak"):
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
