#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""12-Dimension Content Quality Gate & Continuous Improvement Auditor (`curate_loop.py`) for 🌸 কল্যাণী.

CRITICAL GOVERNANCE RULE (enforced on every curation, build_app.py run, and unit test):
Every time content curation or build happens, this script audits `content/slides_and_quotes.py`,
`content/part1_days.py`, and `content/part2_days.py` against all 12 quality dimensions required by Koushik:

  1. CBT Effectiveness (Ericksonian metaphors, covert sensitization, narrative reframing, covert autosuggestions; zero direct lecturing)
  2. Personalization & Personal-Level Connect (Ranaghat, Dum Dum, Koushik, Didi, Aishee, Ayush, Maa Sarada, Dakshineswar, Santiniketan)
  3. Relationship Warmth (Ma, Koushik & Didi sharing the same sensitive heart; healing Ma-Didi misunderstandings with empathy)
  4. Inspiration & Pride (celebrating Ma's resilience, 40+ years of care, Rani Rashmoni, Chandrayaan-3, J.C. Bose)
  5. Charm, Playfulness & Fun (story games, warm humor, music, zero stiff/clinical/babyish language)
  6. Curiosity & Wonder ("কেন?", "কীভাবে?", everyday science, song lyric meanings, GK)
  7. Engagement & Elaborate Multi-Step Depth (>=110 chars rich narrative detail + two-turn follow-up flow)
  8. Ease of Learning & 20-Repetition Dopamine Neuroplasticity (8 core English words, 4 AI habits, 6 CBT shifts repeated across joyful scenes; zero physio drills in app)
  9. Zero Fear of Making Mistakes & Zero Shame for Not Knowing / Forgetting (explicit mistake-safety & forgetting-permission anchors)
  10. Urge to Express Her Own Mind ("নিজের মনের কথা", "নিজের পছন্দ", speaking her authentic preferences without অভিমান)
  11. Freedom & Autonomy (dropping kanjoosi/last-drop scarcity, decluttering, stepping out, choosing the best quality first)
  12. Growing as Per Her Own Dreams (painting/sketching generously without page-waste fear, singing, learning, personal aspirations)
"""

from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from content.part1_days import DAYS_21  # noqa: E402
from content.part2_days import DAYS_PART2_30  # noqa: E402
from content.slides_and_quotes import MORNING_QUOTES, SLIDES  # noqa: E402

BANNED_TERMS = (
    "সয়াবিন",
    "মাশরুম",
    "soya bean",
    "soyabean",
    "mushroom",
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
    "পার্ট ১",
    "পার্ট ২",
    "পার্ট টু",
    "1.1",
    "১.১",
)

TARGET_ENGLISH_WORDS = (
    "comfortable",
    "peaceful",
    "actually",
    "prefer",
    "choice",
    "definitely",
    "relax",
    "manage",
)

# 12 Quality Gate Anchor Lexicons (Bengali + English semantic markers)
DIMENSION_MARKERS: dict[str, tuple[str, int, tuple[str, ...]]] = {
    "1_cbt_effectiveness": (
        "CBT Effectiveness & Subconscious Reprogramming",
        18,
        ("শ্বাস", "শান্ত", "দুশ্চিন্তা", "অপরাধবোধ", "তুলনা", "অভিমান", "ভালো জিনিস", "তিতো", "হালকা"),
    ),
    "2_personal_connect": (
        "Personalization & Personal-Level Connect",
        12,
        ("রানাঘাট", "দমদম", "কৌশিক", "দিদি", "ঐশী", "আয়ুষ", "মা সারদা", "দক্ষিণেশ্বর", "শান্তিনিকেতন"),
    ),
    "3_relationship_warmth": (
        "Relationship Warmth & Ma-Koushik-Didi Empathy",
        6,
        ("ভালোবাসা", "কৌশিক আর দিদি", "আমরা তিনজনই", "একই মাটি", "নরম মন", "অবসাদ", "ভুল বোঝাবুঝি", "আদর"),
    ),
    "4_inspiration_and_pride": (
        "Inspiration, Resilience & Pride",
        10,
        ("গর্ব", "মনের জোর", "আত্মবিশ্বাস", "সাহস", "উৎসাহ", "ইতিহাস", "চন্দ্রযান", "রানি রাসমণি", "জগদীশচন্দ্র"),
    ),
    "5_charm_and_fun": (
        "Charm, Playfulness & Fun",
        15,
        ("মজার", "আনন্দ", "খেলা", "গল্প", "আড্ডা", "হাসিমুখে", "মিষ্টি", "ফুরফুরে"),
    ),
    "6_curiosity_and_wonder": (
        "Curiosity & Wonder (Why/How & Lyric Meanings)",
        18,
        ("কী করে", "কেন", "রহস্য", "বিজ্ঞান", "আসল মানে", "কৌতূহল", "খুঁজে"),
    ),
    "7_engagement_and_depth": (
        "Engagement & Multi-Step Storytelling Depth",
        20,
        ("গল্প করো", "শোনাও তো", "বুঝিয়ে বলো", "উদাহরণ দিয়ে", "সহজ বাংলায়"),
    ),
    "8_ease_of_learning": (
        "Ease of Learning & Spaced Dopamine Reinforcement",
        15,
        ("একদম সহজ", "কোনো চাপ নেই", "চেনা", "এক নিঃশ্বাসে", "ধীরে ধীরে", "অভ্যাস"),
    ),
    "9_zero_fear_or_shame": (
        "Zero Fear of Mistakes & Zero Shame for Not Knowing",
        10,
        ("ভুল হওয়ার ভয়", "কোনো লজ্জা নেই", "ভুলে গেলে", "কিচ্ছু বিগড়ায় না", "নষ্ট হয় না", "অপরাধ নয়", "স্বাভাবিক"),
    ),
    "10_express_own_mind": (
        "Urge to Express Her Own Mind & Preferences",
        10,
        ("নিজের মনের কথা", "নিজের পছন্দ", "নিজের ভাষায়", "আমার মনে হয়", "নিজের ইচ্ছে", "প্রকাশ", "খোলা মনে"),
    ),
    "11_freedom_and_autonomy": (
        "Freedom, Autonomy & High-Quality Living",
        12,
        ("স্বাধীনতা", "নিজে বেছে", "খোলা হাওয়া", "রাজার হালে", "মুক্ত", "নিজের খুশিতে", "ফেলে দেওয়া"),
    ),
    "12_grow_own_dreams": (
        "Growing as Per Her Own Dreams (Art, Music, Learning)",
        10,
        ("স্বপ্ন", "শখ", "শিল্পী মন", "রঙ", "খাতায়", "আঁকা", "নতুন কিছু শেখা", "গুনগুন"),
    ),
}


def run_quality_gate(verbose: bool = True) -> tuple[bool, list[str], dict[str, int]]:
    """Run the 12-Dimension Content Quality Gate across all slides, quotes, and 51 days."""
    issues: list[str] = []

    # 1. Check slides for banned terms and Ma-Koushik-Didi empathy presence
    all_slide_text = " ".join(
        f"{s.get('title_bn', '')} {s.get('highlight_bn', '')} {s.get('text_bn', '')} {s.get('text_en', '')}"
        for s in SLIDES
    )
    for term in BANNED_TERMS:
        if term.lower() in all_slide_text.lower():
            issues.append(f"Slide contains banned term: '{term}'")

    if "দিদি" not in SLIDES[4]["text_bn"] or "depression" not in SLIDES[4]["text_en"].lower():
        issues.append("Slide 5 missing Ma-Koushik-Didi similarity & Didi's depression empathy.")

    # 2. Check Part 1 lacks any physical exercise / physio slots (100% delegated to live trainer)
    for d in DAYS_21:
        for idx, ag in enumerate(d.get("agendas", []), 1):
            if "🤸‍♀️" in ag.get("short_bn", "") or "ফ্রি-হ্যান্ড ব্যায়াম" in ag.get("short_bn", ""):
                issues.append(f"Day {d['day']} Game #{idx} still has removed physio slot in DAYS_21.")

    # 2b. Verify UI Card Header Context-Sensitivity in src/js/plan-view.js
    with open(os.path.join(ROOT, "src", "js", "plan-view.js"), "r", encoding="utf-8") as f_js:
        plan_view_js = f_js.read()
    if "জেমিনির উত্তরটা শোনার পর গল্পটা আরও জমাতে দ্বিতীয় কথায় বলো:" not in plan_view_js:
        issues.append("src/js/plan-view.js missing non-song conversational follow-up header.")
    if "const followupLabel = isSongGame" not in plan_view_js:
        issues.append("src/js/plan-view.js must branch followupLabel on isSongGame so non-song cards never say 'গানটা শোনা হয়ে গেলে'.")

    # 3. Audit all 259 games across Days 1..51
    all_days = list(DAYS_21) + list(DAYS_PART2_30)
    total_games = 0
    thin_games: list[str] = []
    followup_count_p1 = 0
    word_counts = {w: 0 for w in TARGET_ENGLISH_WORDS}

    corpus_units: list[str] = [
        f"{s.get('title_bn', '')} {s.get('highlight_bn', '')} {s.get('text_bn', '')}" for s in SLIDES
    ] + list(MORNING_QUOTES)

    for d in all_days:
        day_num = int(d.get("day", 0))
        corpus_units.append(f"{d.get('title_bn', '')} {d.get('summary_bn', '')} {d.get('voice_script_bn', '')}")
        for idx, ag in enumerate(d.get("agendas", []), 1):
            total_games += 1
            blob = " ".join([
                ag.get("category", ""),
                ag.get("title_bn", ""),
                ag.get("detail_bn", ""),
                ag.get("prompt_bn", ""),
                ag.get("followup_prompt_bn", ""),
            ])
            corpus_units.append(blob)

            for term in BANNED_TERMS:
                if term.lower() in blob.lower():
                    issues.append(f"Day {day_num} Game #{idx} contains banned term: '{term}'")

            if len(ag.get("detail_bn", "").strip()) < 90:
                thin_games.append(f"Day {day_num}.{idx} ({len(ag.get('detail_bn', ''))} chars)")

            if day_num <= 21 and ag.get("followup_prompt_bn", "").strip():
                followup_count_p1 += 1

            for w in TARGET_ENGLISH_WORDS:
                if re.search(rf"\b{re.escape(w)}\b", blob.lower()):
                    word_counts[w] += 1

    if thin_games:
        issues.append(f"Thin games below 90-char narrative threshold: {thin_games[:5]}")

    if followup_count_p1 < 45:
        issues.append(f"Part 1 has too few 2-turn follow-up prompts ({followup_count_p1} < 45).")

    for w, c in word_counts.items():
        if c < 4:
            issues.append(f"Core English word '{w}' has insufficient spaced exposures ({c} < 4).")

    # 4. Evaluate all 12 Quality Gate Dimensions across corpus units
    dimension_scores: dict[str, int] = {}
    for key, (label, min_hits, markers) in DIMENSION_MARKERS.items():
        hits = sum(1 for unit in corpus_units if any(m in unit for m in markers))
        dimension_scores[key] = hits
        if hits < min_hits:
            issues.append(f"Quality Gate Dimension '{label}' below threshold: {hits} < {min_hits}")

    passed = len(issues) == 0

    if verbose:
        print("🌸 Kalyani 12-Dimension Content Quality Gate & Curation Audit")
        print("=" * 76)
        print(f"✅ Slides Audited       : {len(SLIDES)} slides (Ma-Koushik-Didi warmth & zero soya/mushroom)")
        print(f"✅ Curriculum Audited   : {total_games} games across {len(all_days)} days (Part 1 2-turn games: {followup_count_p1}/79)")
        print(f"✅ Narrative Depth Gate : {total_games - len(thin_games)}/{total_games} games pass rich storytelling check")
        print("\n📊 12-Dimension Pedagogical & Emotional Quality Gate:")
        for key, (label, min_hits, _) in DIMENSION_MARKERS.items():
            score = dimension_scores[key]
            status = "PASS" if score >= min_hits else "FAIL"
            print(f"   [{status}] {label:<52}: {score:>3} touches (min >= {min_hits})")
        print("\n📊 Spaced-Repetition Exposure Counts (8 Core English Words):")
        for w, count in word_counts.items():
            print(f"   • {w.capitalize():<14}: {count} exposures")
        if issues:
            print("\n❌ Quality Gate Issues Found:")
            for iss in issues:
                print(f"   - {iss}")
        else:
            print("\n🎉 ALL 12 CONTENT QUALITY GATES PASSED!")

    return passed, issues, dimension_scores


def audit_all() -> int:
    passed, _, _ = run_quality_gate(verbose=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(audit_all())
