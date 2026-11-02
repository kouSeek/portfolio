#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Curriculum, 60/30/10 Language Split, Gemini Live Tech Onboarding & Blueprint-Driven Agentic Loop Tests."""

import copy
import json
from pathlib import Path
import sys
import unittest

APP_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_ROOT))
sys.path.insert(0, str(APP_ROOT / "scripts"))

from content import DAYS_21, DAYS_PART2_30, SLIDES  # noqa: E402
from curate_loop import (  # noqa: E402
    DIMENSIONS,
    classify_game_pillar,
    collect_md5_fingerprints,
    is_covert_cbt_day,
    run_agentic_improvement_loop,
    run_quality_gate,
)


class TestCurriculumAndPersona(unittest.TestCase):

    def test_zero_physio_exercises_across_curriculum(self) -> None:
        """Verify 100% zero physical exercises inside Kalyani App (delegated to Ma's personal trainer)."""
        forbidden_physio_tokens = (
            "সকালের ব্যায়াম",
            "ফিজিওথেরাপি",
            "পায়ের গোড়ালি ঘোরানো",
            "হাঁটুর নিচে তোয়ালে",
            "কাঁধ ও ঘাড়ের আরাম",
        )
        for d in DAYS_21 + DAYS_PART2_30:
            for ag in d["agendas"]:
                blob = f"{ag['category']} {ag['title_bn']} {ag['detail_bn']} {ag['prompt_bn']}"
                for tok in forbidden_physio_tokens:
                    self.assertNotIn(tok, blob, f"Day {d['day']} contains forbidden physio token: {tok}")

    def test_six_games_per_day_and_one_in_two_days_cbt_cadence(self) -> None:
        """Verify every day has 6 deep games (within 4..6), daily pillars, and Covert CBT strictly 1 in 2 days."""
        all_days = DAYS_21 + DAYS_PART2_30
        for d in all_days:
            day_num = int(d["day"])
            ags = d["agendas"]
            self.assertGreaterEqual(len(ags), 4)
            self.assertLessEqual(len(ags), 6)

            pillars = [classify_game_pillar(ag) for ag in ags]
            for daily_pillar in ("english", "music", "gk_inspiring", "tech_65"):
                self.assertIn(daily_pillar, pillars, f"Day {day_num} missing daily pillar '{daily_pillar}'")

            cbt_count = pillars.count("covert_cbt")
            pt_count = pillars.count("personal_therapy")
            if day_num % 2 == 0:
                self.assertEqual(cbt_count, 1, f"Even Day {day_num} must have 1 covert_cbt game")
            else:
                self.assertEqual(cbt_count, 0, f"Odd Day {day_num} must have 0 covert_cbt games")
                self.assertEqual(pt_count, 1, f"Odd Day {day_num} must have 1 personal_therapy game")

        cbt_days = [int(d["day"]) for d in all_days if is_covert_cbt_day(d)]
        self.assertEqual(cbt_days, [d_num for d_num in range(1, 52) if d_num % 2 == 0])

        md5s = collect_md5_fingerprints()
        for k in (
            "persona_card_md5",
            "student_persona_spec_md5",
            "curriculum_md5",
            "content_curation_md5",
            "part1_days_md5",
            "part2_days_md5",
            "client_gemini_md5",
        ):
            self.assertEqual(len(md5s[k]), 32, f"Missing MD5 digest for {k}")

        gemini_md = (APP_ROOT / "GEMINI.md").read_text(encoding="utf-8")
        for ref_file in (
            "students/ma_kalyani/persona.md",
            "docs/student-persona.md",
            "content/curriculum.md",
            "content/content_curation.md",
            "content/days/part1_days.md",
            "content/days/part2_days.md",
            "docs/client-side-gemini.md",
        ):
            self.assertIn(ref_file, gemini_md, f"GEMINI.md must mandate reading {ref_file}")

        passed, issues, dim_scores = run_quality_gate(verbose=False)
        self.assertTrue(passed, f"Blueprint-Driven Agentic Quality Gate failed: {issues}")
        self.assertEqual(len(dim_scores), 12)

    def test_language_focus_split_60_english_30_hindi_10_bengali(self) -> None:
        """Verify the 60% English, 30% Fluent Hindi Gossip, and 10% Clear Bengali Mind-Expression split."""
        all_days = DAYS_21 + DAYS_PART2_30
        eng = sum(1 for d in all_days for a in d["agendas"] if classify_game_pillar(a) == "english")
        hin = sum(1 for d in all_days for a in d["agendas"] if classify_game_pillar(a) == "hindi")
        ben = sum(1 for d in all_days for a in d["agendas"] if classify_game_pillar(a) == "bengali_expr")
        total = eng + hin + ben

        self.assertEqual(total, 102)
        self.assertAlmostEqual(eng / total, 0.60, delta=0.02)
        self.assertAlmostEqual(hin / total, 0.30, delta=0.02)
        self.assertAlmostEqual(ben / total, 0.10, delta=0.02)

    def test_gemini_live_tech_onboarding_and_live_video_camera_repetition(self) -> None:
        """Verify Tech Onboarding covers Google Photos, Calling, YouTube Music, and repeated Live Video Camera."""
        all_tech_text = " ".join(
            a["title_bn"] + " " + a["detail_bn"] + " " + a["prompt_bn"]
            for d in (DAYS_21 + DAYS_PART2_30)
            for a in d["agendas"]
            if classify_game_pillar(a) == "tech_65"
        )
        self.assertIn("গুগল ফটোস", all_tech_text)
        self.assertIn("লাইভ ভিডিও ক্যামেরা", all_tech_text)
        self.assertIn("ইউটিউব মিউজিক", all_tech_text)
        live_cam_days = [
            d["day"]
            for d in (DAYS_21 + DAYS_PART2_30)
            if any("ক্যামেরা" in (a["title_bn"] + a["detail_bn"]) for a in d["agendas"] if classify_game_pillar(a) == "tech_65")
        ]
        self.assertGreaterEqual(len(live_cam_days), 18, "Live Camera usage must be reinforced via spaced repetition")

    def test_blueprint_driven_agentic_llm_loop_critique_and_refine(self) -> None:
        """Verify pure LLM Critic -> Refiner -> Re-Evaluate loop driven by curriculum.md & content_curation.md."""
        curate_src = (APP_ROOT / "scripts" / "curate_loop.py").read_text(encoding="utf-8")
        self.assertNotIn("len(detail) <", curate_src, "curate_loop.py must not contain hardcoded character-length gates")

        sample_day = copy.deepcopy(DAYS_21[0])
        call_log: list[str] = []

        def mock_llm_agent(prompt: str) -> str:
            if "Autonomous Critic Agent" in prompt:
                call_log.append("critic")
                if call_log.count("critic") == 1:
                    return json.dumps({
                        "passed": False,
                        "dimension_scores": {k: 8 for k, _ in DIMENSIONS},
                        "weak_games": [{
                            "day": 1,
                            "game_idx": 3,
                            "pillar": "tech_65",
                            "critique": "Mention Google Photos and calling family more vividly in onboarding.",
                        }],
                        "summary_critique": "Iteration 1 requested richer Google Photos onboarding.",
                    })
                return json.dumps({
                    "passed": True,
                    "dimension_scores": {k: 10 for k, _ in DIMENSIONS},
                    "weak_games": [],
                    "summary_critique": "Iteration 2 passed all 12 blueprint dimensions.",
                })
            call_log.append("refiner")
            return json.dumps({
                "title_bn": "জেমিনি দিয়ে গান চালানো, কল করা ও গুগল ফটোসে ছবি দেখা!",
                "detail_bn": "মা, মুখে বললেই জেমিনি ইউটিউব মিউজিকে গান বাজাবে, কৌশিককে কল করবে আর গুগল ফটোস থেকে ছবি দেখাবে!",
                "prompt_bn": "জেমিনি, গুগল ফটোস থেকে আমাদের পরিবারের ছবি কীভাবে দেখাবো বলো তো!",
                "followup_prompt_bn": "জেমিনি, কৌশিককে মুখে বলে স্পিকারে কল করার নিয়মটাও শেখাও তো।",
            })

        passed, refined_days, report = run_agentic_improvement_loop(
            days_list=[sample_day],
            llm_callable=mock_llm_agent,
            max_iterations=3,
            min_score=9,
        )
        self.assertTrue(passed)
        self.assertEqual(call_log, ["critic", "refiner", "critic"])
        self.assertEqual(report["total_refinements_applied"], 1)
        self.assertIn("গুগল ফটোস", refined_days[0]["agendas"][3]["detail_bn"])

    def test_youtube_music_and_part2_180_unique_games(self) -> None:
        """Verify YouTube Music integration every day and 180 unique Part 2 games loaded from Markdown."""
        for d in DAYS_21 + DAYS_PART2_30:
            song_games = [ag for ag in d["agendas"] if classify_game_pillar(ag) == "music"]
            self.assertEqual(len(song_games), 1)
            self.assertIn("ইউটিউব মিউজিকে", song_games[0]["prompt_bn"])

        seen_pairs: set[tuple[str, str]] = set()
        for d in DAYS_PART2_30:
            self.assertEqual(len(d["agendas"]), 6)
            for ag in d["agendas"]:
                pair = (ag["category"], ag["title_bn"])
                self.assertNotIn(pair, seen_pairs, f"Duplicate game on Day {d['day']}: {pair}")
                seen_pairs.add(pair)
        self.assertEqual(len(seen_pairs), 180)

    def test_letter_slides_and_client_side_gemini_master_prompt(self) -> None:
        """Verify Slide 1..8 and updated Client-Side Gemini Master Prompt in docs/client-side-gemini.md."""
        self.assertEqual(len(SLIDES), 8)
        client_doc = (APP_ROOT / "docs" / "client-side-gemini.md").read_text(encoding="utf-8")
        for required_phrase in (
            "IRONCLAD LANGUAGE RULE (SPEAK TO MA STRICTLY IN BENGALI)",
            "MANDATORY PERSISTENT MEMORY & PROACTIVE PROFILING PROTOCOL",
            "EXTRAORDINARY PSYCHOTHERAPIST PROTOCOL",
            "60% ENGLISH · 30% HINDI GOSSIP · 10% BENGALI CLARITY",
            "GEMINI LIVE TECH ONBOARDING & SPACED REPETITION",
            "@Google Photos",
            "Live Video Camera",
        ):
            self.assertIn(required_phrase, client_doc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
