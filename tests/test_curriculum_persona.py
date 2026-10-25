#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Curriculum, Ego-Safety, Natural Bengali & YouTube Music Prompt Tests for 🌸 কল্যাণী."""

from pathlib import Path
import sys
import unittest

APP_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_ROOT))

from content import DAYS_21, DAYS_PART2_30, GAME_META, MORNING_QUOTES, SLIDES  # noqa: E402


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
)


class TestCurriculumPersona(unittest.TestCase):

    def test_counts_and_six_game_sweet_spot(self) -> None:
        """Verify 8 slides, 7 quotes, 6 game meta slots, and 6 games/day across all 51 days."""
        self.assertEqual(len(SLIDES), 8)
        self.assertEqual(len(MORNING_QUOTES), 7)
        self.assertEqual(len(GAME_META), 6)
        self.assertEqual(len(DAYS_21), 21)
        self.assertEqual(len(DAYS_PART2_30), 30)

        for d in DAYS_21 + DAYS_PART2_30:
            self.assertEqual(len(d["agendas"]), 6, f"Day {d['day']} must have exactly 6 games")

    def test_ego_safety_natural_bangla_and_youtube_music_prompts(self) -> None:
        """Verify zero banned/blaming words and valid YouTube Music prompts on every day."""
        all_texts: list[str] = list(MORNING_QUOTES)
        for s in SLIDES:
            all_texts.extend([s["title_bn"], s["highlight_bn"], s["text_bn"]])

        for d in DAYS_21 + DAYS_PART2_30:
            all_texts.extend([d["title_bn"], d["summary_bn"], d.get("voice_script_bn", "")])
            for ag in d["agendas"]:
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
            self.assertNotIn(bad, joined, f"Found banned/unnatural phrase '{bad}' in content/")


if __name__ == "__main__":
    unittest.main(verbosity=2)
