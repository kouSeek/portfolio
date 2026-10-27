#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Curriculum v2, Variable Wave, Spaced Reinforcement, Ego-Safety & YouTube Music Tests for 🌸 কল্যাণী."""

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

CORE_ENGLISH_WORDS = (
    "comfortable",
    "peaceful",
    "actually",
    "prefer",
    "choice",
    "definitely",
    "relax",
    "manage",
)


class TestCurriculumPersona(unittest.TestCase):

    def test_variable_waves_alternate_day_stories_and_spaced_reinforcement(self) -> None:
        """Verify Day 1 starts small (3), variable waves (3..5), 10 alternate-day stories, and >=3x English reinforcement."""
        self.assertEqual(len(SLIDES), 8)
        self.assertEqual(len(MORNING_QUOTES), 7)
        self.assertEqual(len(GAME_META), 6)
        self.assertEqual(len(DAYS_21), 21)
        self.assertEqual(len(DAYS_PART2_30), 30)

        for m in GAME_META:
            self.assertIsNone(re.search(r"[0-9০-৯]\.", m["short_bn"]))
            self.assertIsNone(re.search(r"[0-9০-৯]\.", m["category_bn"]))

        # Day 1 starts gently with 3 light games, and Days 1..21 vary across 3, 4, and 5 games
        self.assertEqual(len(DAYS_21[0]["agendas"]), 3)
        wave_counts = {len(d["agendas"]) for d in DAYS_21}
        self.assertEqual(wave_counts, {3, 4, 5}, f"Expected variable wave sizes {{3, 4, 5}}, got {wave_counts}")

        # Alternate-day stories on Days 2, 4, 6, 8, 10, 12, 14, 16, 18, 20
        story_days = [
            d["day"]
            for d in DAYS_21
            if any("📖" in ag.get("short_bn", "") or "গল্প" in ag.get("short_bn", "") for ag in d["agendas"])
        ]
        self.assertEqual(story_days, [2, 4, 6, 8, 10, 12, 14, 16, 18, 20])

        # Spaced reinforcement: each of the 8 core English words appears across >= 3 distinct days in DAYS_21
        for word in CORE_ENGLISH_WORDS:
            days_with_word = [
                d["day"]
                for d in DAYS_21
                if word in " ".join(ag["title_bn"] + " " + ag["detail_bn"] + " " + ag["prompt_bn"] for ag in d["agendas"]).lower()
            ]
            self.assertGreaterEqual(
                len(days_with_word),
                3,
                f"Core English word '{word}' must be reinforced on >=3 days, found on {days_with_word}",
            )

        for d in DAYS_21 + DAYS_PART2_30:
            self.assertGreaterEqual(len(d["agendas"]), 3)
            self.assertLessEqual(len(d["agendas"]), 6)
            self.assertTrue(d.get("voice_script_bn", "").strip(), f"Day {d['day']} must have a warm voice_script_bn")

    def test_ego_safety_natural_bangla_zero_bloat_and_youtube_music_prompts(self) -> None:
        """Verify zero banned/nagging words, zero duplicate number readouts, and valid YouTube Music prompts."""
        all_texts: list[str] = list(MORNING_QUOTES)
        for s in SLIDES:
            all_texts.extend([s["badge"], s["title_bn"], s["highlight_bn"], s["text_bn"]])

        song_game_count = 0
        for d in DAYS_21 + DAYS_PART2_30:
            all_texts.extend([d["phase"], d["title_bn"], d["summary_bn"], d.get("voice_script_bn", "")])
            for ag in d["agendas"]:
                self.assertIsNone(
                    re.search(r"[0-9০-৯]\.", ag["category"]),
                    f"Duplicate number prefix in category on day {d['day']}: {ag['category']}",
                )
                if "short_bn" in ag:
                    self.assertIsNone(re.search(r"[0-9০-৯]\.", ag["short_bn"]))
                all_texts.extend([
                    ag["category"],
                    ag["title_bn"],
                    ag["detail_bn"],
                    ag["prompt_bn"],
                    ag.get("followup_prompt_bn", ""),
                ])
                if "🎵" in ag["category"]:
                    song_game_count += 1
                    self.assertIn("ইউটিউব মিউজিক", ag["detail_bn"], f"Day {d['day']} song game missing ইউটিউব মিউজিক")
                    self.assertTrue(ag["prompt_bn"].startswith("জেমিনি, ইউটিউব মিউজিকে ‘"), f"Day {d['day']}: {ag['prompt_bn']}")
                    self.assertTrue(ag["prompt_bn"].endswith("’ গানটা চালিয়ে দাও।"), f"Day {d['day']}: {ag['prompt_bn']}")
                    self.assertIn("গানটার কথাগুলোর আসল মানে", ag.get("followup_prompt_bn", ""), f"Day {d['day']} followup")

        self.assertGreaterEqual(song_game_count, 40)

        joined = "\n".join(all_texts)
        for bad in BANNED_PHRASES:
            self.assertNotIn(bad, joined, f"Found banned/nagging/bloated phrase '{bad}' in content/")

        # Verify all tracked voice scripts synthesized by refresh_voices.py contain zero bloated numbering
        voice_items = collect_expected_audio_items()
        for rel_path, info in voice_items.items():
            txt = info["text"]
            for bad_voice in ("পার্ট ২", "পার্ট ১", "ধাপ ১", "ধাপ ২", "খেলা ১:", "দিন 1:", "দিন ১: দিন"):
                self.assertNotIn(bad_voice, txt, f"Bloated voice text '{bad_voice}' found in {rel_path}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
