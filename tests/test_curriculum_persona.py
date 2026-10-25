#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Curriculum, Ego-Safety, Zero Number-Bloat, Natural Bengali & YouTube Music Tests for 🌸 কল্যাণী."""

from pathlib import Path
import re
import sys
import unittest

APP_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_ROOT))
sys.path.insert(0, str(APP_ROOT / "scripts"))

from content import DAYS_21, DAYS_PART2_30, GAME_META, MORNING_QUOTES, SLIDES  # noqa: E402
from refresh_voices import collect_expected_audio_items  # noqa: E402


BANNED_PHRASES = (
    "দয়া করে",
    "মস্তিষ্ক",
    "সংকোচ",
    "ভুল থেকে শিক্ষা",
    "পচা ফলটা আগে",
    "ভবঘুরের মতো",
    "Kiptemi",
    "Scarcity",
    "Learned Helplessness",
    "এজেন্ডা",
    "মাথাে",
    "মাথায়র",
    "পার্ট ১",
    "পার্ট ২",
    "পার্ট টু",
    "নিজের গতিতে শান্ত মনে এগিয়ে চলা",
    "১)",
    "২)",
    "1.1",
    "১.১",
)


class TestCurriculumPersona(unittest.TestCase):

    def test_counts_and_six_game_sweet_spot(self) -> None:
        """Verify 8 slides, 7 quotes, 6 number-free game meta slots, and 6 games/day across all 51 days."""
        self.assertEqual(len(SLIDES), 8)
        self.assertEqual(len(MORNING_QUOTES), 7)
        self.assertEqual(len(GAME_META), 6)
        self.assertEqual(len(DAYS_21), 21)
        self.assertEqual(len(DAYS_PART2_30), 30)

        for m in GAME_META:
            self.assertIsNone(re.search(r"[0-9০-৯]\.", m["short_bn"]), f"Number prefix found in short_bn: {m['short_bn']}")
            self.assertIsNone(re.search(r"[0-9০-৯]\.", m["category_bn"]), f"Number prefix found in category_bn: {m['category_bn']}")

        for d in DAYS_21 + DAYS_PART2_30:
            self.assertEqual(len(d["agendas"]), 6, f"Day {d['day']} must have exactly 6 games")
            self.assertTrue(d.get("voice_script_bn", "").strip(), f"Day {d['day']} must have a warm voice_script_bn")

    def test_ego_safety_natural_bangla_zero_bloat_and_youtube_music_prompts(self) -> None:
        """Verify zero banned/nagging words, zero duplicate number readouts, and valid YouTube Music prompts."""
        all_texts: list[str] = list(MORNING_QUOTES)
        for s in SLIDES:
            all_texts.extend([s["badge"], s["title_bn"], s["highlight_bn"], s["text_bn"]])

        for d in DAYS_21 + DAYS_PART2_30:
            all_texts.extend([d["phase"], d["title_bn"], d["summary_bn"], d.get("voice_script_bn", "")])
            for ag in d["agendas"]:
                self.assertIsNone(
                    re.search(r"[0-9০-৯]\.", ag["category"]),
                    f"Duplicate number prefix in category on day {d['day']}: {ag['category']}",
                )
                all_texts.extend([
                    ag["category"],
                    ag["title_bn"],
                    ag["detail_bn"],
                    ag["prompt_bn"],
                    ag.get("followup_prompt_bn", ""),
                ])

            # Game 4 (index 3) must command YouTube Music directly in natural Bengali
            song_game = d["agendas"][3]
            self.assertIn("ইউটিউব মিউজিক", song_game["detail_bn"])
            self.assertTrue(song_game["prompt_bn"].startswith("জেমিনি, ইউটিউব মিউজিকে ‘"))
            self.assertTrue(song_game["prompt_bn"].endswith("’ গানটা চালিয়ে দাও।"))
            self.assertIn("গানটার কথাগুলোর আসল মানে", song_game.get("followup_prompt_bn", ""))

        joined = "\n".join(all_texts)
        for bad in BANNED_PHRASES:
            self.assertNotIn(bad, joined, f"Found banned/nagging/bloated phrase '{bad}' in content/")

        # Verify all 372 voice scripts synthesized by refresh_voices.py contain zero bloated numbering
        voice_items = collect_expected_audio_items()
        self.assertEqual(len(voice_items), 372)
        for rel_path, info in voice_items.items():
            txt = info["text"]
            for bad_voice in ("পার্ট ২", "পার্ট ১", "ধাপ ১", "ধাপ ২", "খেলা ১:", "দিন 1:", "দিন ১: দিন"):
                self.assertNotIn(bad_voice, txt, f"Bloated voice text '{bad_voice}' found in {rel_path}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
