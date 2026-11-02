#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Curriculum, Persona, 5-Pillar Cadence & Agentic LLM Improvement Loop Tests for 🌸 কল্যাণী."""

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

    def test_four_to_six_games_per_day_and_one_in_two_days_cbt_cadence(self) -> None:
        """Verify every day has 4..6 deep games, covers the 5 pillars, and Covert CBT is strictly 1 in 2 days."""
        all_days = DAYS_21 + DAYS_PART2_30
        for d in all_days:
            day_num = int(d["day"])
            ags = d["agendas"]
            self.assertGreaterEqual(len(ags), 4, f"Day {day_num} has fewer than 4 games ({len(ags)})")
            self.assertLessEqual(len(ags), 6, f"Day {day_num} has more than 6 games ({len(ags)})")

            pillars = [classify_game_pillar(ag) for ag in ags]
            for daily_pillar in ("english", "hindi", "music", "gk_inspiring", "tech_65"):
                self.assertIn(daily_pillar, pillars, f"Day {day_num} missing daily pillar '{daily_pillar}'")

            cbt_count = pillars.count("covert_cbt")
            pt_count = pillars.count("personal_therapy")
            if day_num % 2 == 0:
                self.assertEqual(cbt_count, 1, f"Even Day {day_num} must have exactly 1 covert_cbt game")
            else:
                self.assertEqual(cbt_count, 0, f"Odd Day {day_num} must have 0 covert_cbt games (1-in-2-days rule)")
                self.assertEqual(pt_count, 1, f"Odd Day {day_num} must have 1 personal_therapy game")

        cbt_days = [int(d["day"]) for d in all_days if is_covert_cbt_day(d)]
        self.assertEqual(cbt_days, [d_num for d_num in range(1, 52) if d_num % 2 == 0])

        passed, issues, dim_scores = run_quality_gate(verbose=False)
        self.assertTrue(passed, f"12-Dimension Agentic Quality Gate failed: {issues}")
        self.assertEqual(len(dim_scores), 12)
        for k, score in dim_scores.items():
            self.assertGreaterEqual(score, 9, f"Dimension {k} scored below 9/10")

    def test_agentic_llm_improvement_loop_critique_and_refine(self) -> None:
        """Verify run_agentic_improvement_loop iteratively critiques a weak game, refines it via LLM, and re-evaluates."""
        sample_day = copy.deepcopy(DAYS_21[0])
        # Introduce a shallow game defect on Game 0 so Iteration 1 fails and triggers the Refiner Agent
        sample_day["agendas"][0]["detail_bn"] = "খুব ছোট লেখা।"
        call_log: list[str] = []

        def mock_llm_agent(prompt: str) -> str:
            if "Critic Agent" in prompt:
                call_log.append("critic")
                if call_log.count("critic") == 1:
                    return json.dumps({
                        "passed": False,
                        "dimension_scores": {k: 8 for k, _ in DIMENSIONS},
                        "weak_games": [{
                            "game_idx": 0,
                            "pillar": "tech_65",
                            "critique": "Game 0 detail_bn is too brief and lacks a concrete 65yo technology reassurance.",
                        }],
                        "summary_critique": "Iteration 1 found shallow detail on Game 0.",
                    })
                return json.dumps({
                    "passed": True,
                    "dimension_scores": {k: 10 for k, _ in DIMENSIONS},
                    "weak_games": [],
                    "summary_critique": "Iteration 2 verified deep concrete target achieved.",
                })
            call_log.append("refiner")
            return json.dumps({
                "title_bn": "ফোনে হাত দিলে কিচ্ছু বিগড়ায় না — চায়ের আড্ডার মতো প্রথম কথা",
                "detail_bn": (
                    "অনেক সময় মনে অজানা ভয় হয়—‘ফোনে হাত দিলে যদি কিছু বিগড়ে যায়!’ জেনে রেখো মা, আধুনিক ফোনে বা জেমিনিতে "
                    "হাত দিলে কোনোদিন কিছু নষ্ট হয় না—যেমন হারমোনিয়ামের রিডে হাত দিলে সুর বাজে, হারমোনিয়াম ভেঙে যায় না। "
                    "আজ নিশ্চিন্তে মাইক ছুঁয়ে বিকেলের জলখাবারের একটা ছোট্ট প্রশ্ন করো।"
                ),
                "prompt_bn": "জেমিনি, বিকেলের চায়ের সাথে কী ভালো খাবার খাওয়া যায় বলো তো?",
                "followup_prompt_bn": "জেমিনি, ঘরে থাকা জিনিস দিয়ে দুটো সুস্বাদু বাঙালি জলখাবারের নাম বলো তো।",
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
        self.assertEqual(report["days"]["1"]["iterations_run"], 2)
        self.assertGreaterEqual(len(refined_days[0]["agendas"][0]["detail_bn"]), 120)

    def test_spoken_english_every_day_and_core_words(self) -> None:
        """Verify every single day in Part 1 has a spoken English game and reinforces core vocabulary."""
        core_words = ("comfortable", "peaceful", "actually", "prefer", "choice", "definitely", "relax", "manage")
        word_hits = {w: 0 for w in core_words}
        eng_prompts: list[str] = []

        for d in DAYS_21:
            day_eng = [ag for ag in d["agendas"] if classify_game_pillar(ag) == "english"]
            day_hin = [ag for ag in d["agendas"] if classify_game_pillar(ag) == "hindi"]
            self.assertGreaterEqual(len(day_eng), 1, f"Day {d['day']} must have a Spoken English game")
            self.assertGreaterEqual(len(day_hin), 1, f"Day {d['day']} must have a Spoken Hindi game")
            for ag in d["agendas"]:
                txt = (ag["title_bn"] + " " + ag["detail_bn"] + " " + ag["prompt_bn"]).lower()
                for w in core_words:
                    if w in txt:
                        word_hits[w] += 1
                if classify_game_pillar(ag) == "english" and "জেমিনি, শোনো—" in ag["prompt_bn"]:
                    eng_prompts.append(ag["prompt_bn"])
                    self.assertTrue(
                        ag.get("followup_prompt_bn", "").startswith("জেমিনি,"),
                        f"Day {d['day']} English game must have a 2nd-turn follow-up prompt",
                    )

        self.assertEqual(len(eng_prompts), 21, "Every day in DAYS_21 must have a 1-breath spoken English prompt")
        for w, cnt in word_hits.items():
            self.assertGreaterEqual(cnt, 3, f"Core word '{w}' only appeared {cnt} times across 21 days")
        self.assertGreaterEqual(sum(word_hits.values()), 28)

    def test_youtube_music_integration_every_day(self) -> None:
        """Verify every day in Part 1 and Part 2 has a YouTube Music song lyrics curiosity game."""
        for d in DAYS_21 + DAYS_PART2_30:
            song_games = [ag for ag in d["agendas"] if classify_game_pillar(ag) == "music"]
            self.assertGreaterEqual(len(song_games), 1, f"Day {d['day']} must have a Song Lyrics game")
            for ag in song_games:
                self.assertIn("ইউটিউব মিউজিকে", ag["prompt_bn"])
                self.assertIn("গানটার কথাগুলোর আসল মানে", ag.get("followup_prompt_bn", ""))

    def test_part1_days_have_unique_stories_and_zero_clones(self) -> None:
        """Verify all 21 Part 1 days have unique titles and 10 even-day third-person Ericksonian stories."""
        self.assertEqual(len(DAYS_21), 21)
        day_titles = [d["title_bn"] for d in DAYS_21]
        self.assertEqual(len(day_titles), len(set(day_titles)), "Duplicate day title_bn in DAYS_21")

        stories = [
            ag["title_bn"]
            for d in DAYS_21
            for ag in d["agendas"]
            if "📖" in ag["category"]
        ]
        self.assertEqual(len(stories), 10, "Part 1 must include 10 alternate-day Ericksonian CBT stories")
        self.assertEqual(len(stories), len(set(stories)), "All Part 1 stories must be unique")

    def test_part2_30_days_have_180_unique_non_cloned_games(self) -> None:
        """Verify Extended 30-Day Course (Days 22-51) has 180 unique games with 2-turn prompts."""
        self.assertEqual(len(DAYS_PART2_30), 30)
        day_titles = [d["title_bn"] for d in DAYS_PART2_30]
        self.assertEqual(len(day_titles), len(set(day_titles)), "Duplicate day title_bn in DAYS_PART2_30")

        seen_cat_titles: set[tuple[str, str]] = set()
        for idx, d in enumerate(DAYS_PART2_30, start=22):
            self.assertEqual(d["day"], idx)
            self.assertEqual(d["part"], 2)
            self.assertEqual(len(d["agendas"]), 6)
            for ag in d["agendas"]:
                pair = (ag["category"], ag["title_bn"])
                self.assertNotIn(pair, seen_cat_titles, f"Cloned game card on Day {idx}: {pair}")
                seen_cat_titles.add(pair)
                self.assertTrue(ag.get("followup_prompt_bn", "").startswith("জেমিনি,"))

        self.assertEqual(len(seen_cat_titles), 180)

    def test_letter_slides_and_client_side_gemini_master_prompt(self) -> None:
        """Verify Slide 1..8 and the comprehensive Client-Side Gemini Master Prompt in docs/client-side-gemini.md."""
        self.assertEqual(len(SLIDES), 8)
        all_slide_bn = " ".join(
            s["badge"] + " " + s["title_bn"] + " " + s["highlight_bn"] + " " + s["text_bn"] for s in SLIDES
        )
        self.assertIn("রানাঘাট", all_slide_bn)
        self.assertIn("এক মাটির মানুষ", all_slide_bn)

        client_doc = (APP_ROOT / "docs" / "client-side-gemini.md").read_text(encoding="utf-8")
        for required_phrase in (
            "IRONCLAD LANGUAGE RULE (SPEAK TO MA STRICTLY IN BENGALI)",
            "MANDATORY PERSISTENT MEMORY & PROACTIVE PROFILING PROTOCOL",
            "EXTRAORDINARY PSYCHOTHERAPIST PROTOCOL (PERSONAL CONVERSATION AS THERAPY)",
            "HOW TO BEHAVE vs. HOW NOT TO BEHAVE",
            "Proper, Confident Everyday Spoken Hindi",
            "Covert CBT Therapy",
            "লেবুর তিতো খোসা",
            "একই নরম মাটির মানুষ",
        ):
            self.assertIn(required_phrase, client_doc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
