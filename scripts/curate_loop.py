#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pure Agentic LLM Evaluator-Optimizer Loop for 🌸 কল্যাণী (Zero Hardcoded Rules).

Driven exclusively by four declarative Markdown reference specifications:
  1. `students/ma_kalyani/persona.md` — Learner quick profile card, constraints & tone guardrails
  2. `docs/student-persona.md`        — Deep psychological/CBT blocker matrix & 20-rep dopamine neuroplasticity spec
  3. `content/curriculum.md`          — Master syllabus, 60/30/10 language split & 3-pillar Gemini Live tech onboarding
  4. `content/content_curation.md`    — 12-Dimension LLM Critic-Refiner rubric & generation rules

Produces, evaluates, and iteratively refines:
  - `content/days/part1_days.md` & `content/days/part2_days.md` (loaded by `part1_days.py` & `part2_days.py`)
  - `docs/client-side-gemini.md` (Client-Side Android Gemini Master Instruction)
  - `content/curation_manifest.json` (7-file MD5 state ledger + the LLM Critic's 12-dimension audit)
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.request

APP_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_ROOT))

from content.markdown_loader import dump_days_markdown, load_days_markdown  # noqa: E402

PERSONA_CARD_MD_PATH = APP_ROOT / "students" / "ma_kalyani" / "persona.md"
STUDENT_PERSONA_SPEC_MD_PATH = APP_ROOT / "docs" / "student-persona.md"
CURRICULUM_MD_PATH = APP_ROOT / "content" / "curriculum.md"
CONTENT_CURATION_MD_PATH = APP_ROOT / "content" / "content_curation.md"
PART1_MD_PATH = APP_ROOT / "content" / "days" / "part1_days.md"
PART2_MD_PATH = APP_ROOT / "content" / "days" / "part2_days.md"
CLIENT_GEMINI_MD_PATH = APP_ROOT / "docs" / "client-side-gemini.md"
CURATION_MANIFEST_PATH = APP_ROOT / "content" / "curation_manifest.json"
GEN_BIN = "/google/bin/releases/gemini-agents-generate/generate"

DIMENSIONS: tuple[tuple[str, str], ...] = (
    ("cbt_effectiveness", "1. 1-in-2-Days Covert CBT Precision"),
    ("personal_connect", "2. Deep Reminiscence & Cathartic Psychotherapy"),
    ("relationship_warmth", "3. Family Attachment Healing (Ma, Koushik & Didi)"),
    ("inspiration_and_pride", "4. Relatable Inspiring Figures"),
    ("charm_and_fun", "5. Song Lyrics Curiosity via @YouTube Music"),
    ("curiosity_and_wonder", "6. Relatable Everyday World GK"),
    ("storytelling_depth", "7. Concrete Teaching Target per Game"),
    ("ease_of_learning", "8. 60% English / 30% Hindi Gossip / 10% Bengali Clarity"),
    ("zero_fear_and_shame", "9. 3-Pillar Gemini Live Tech Onboarding & Live Video Camera"),
    ("urge_to_express_mind", "10. Authentic Voice & 2-Turn Agency"),
    ("freedom_and_autonomy", "11. Zero Physio & Effortless Pacing"),
    ("growing_own_dreams", "12. Client-Side Gemini Harmony & Persistent Memory"),
)


def md5_file(path: Path) -> str:
    """Compute the MD5 hex digest of a file."""
    if not path.is_file():
        return ""
    return hashlib.md5(path.read_bytes()).hexdigest()


def collect_md5_fingerprints() -> dict[str, str]:
    """Collect MD5 digests of all 4 persona/curriculum input specs and all 3 curated Markdown outputs."""
    return {
        "persona_card_md5": md5_file(PERSONA_CARD_MD_PATH),
        "student_persona_spec_md5": md5_file(STUDENT_PERSONA_SPEC_MD_PATH),
        "curriculum_md5": md5_file(CURRICULUM_MD_PATH),
        "content_curation_md5": md5_file(CONTENT_CURATION_MD_PATH),
        "part1_days_md5": md5_file(PART1_MD_PATH),
        "part2_days_md5": md5_file(PART2_MD_PATH),
        "client_gemini_md5": md5_file(CLIENT_GEMINI_MD_PATH),
    }


def classify_game_pillar(ag: dict) -> str:
    """Read the declarative `pillar` tag from a Markdown-loaded game dictionary."""
    return str(ag.get("pillar", "")).strip() or "gk_inspiring"


def is_covert_cbt_day(day_obj: dict) -> bool:
    """Return True if any game in the day carries `pillar: covert_cbt`."""
    return any(classify_game_pillar(ag) == "covert_cbt" for ag in day_obj.get("agendas", []))


def call_gemini_llm(prompt: str, timeout_s: int = 60) -> str:
    """Invoke Gemini LLM via GEMINI_API_KEY REST endpoint or local `generate` CLI."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if api_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"},
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body["candidates"][0]["content"]["parts"][0]["text"]

    if Path(GEN_BIN).is_file():
        proc = subprocess.run(
            [GEN_BIN, f"-timeout={timeout_s}s", "text", prompt],
            capture_output=True,
            text=True,
            timeout=timeout_s + 5,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
        raise RuntimeError(f"Gemini CLI returned code {proc.returncode}: {proc.stderr[:240]}")

    raise RuntimeError("No Gemini LLM transport available.")


def _parse_llm_json(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start : end + 1]
    return json.loads(cleaned)


def build_agentic_critic_prompt(
    persona_card_md: str,
    student_persona_spec_md: str,
    curriculum_md: str,
    curation_md: str,
    days_payload: list[dict],
    client_gemini_md: str,
) -> str:
    """Construct the pure LLM Critic prompt from Persona specs + `curriculum.md` + `content_curation.md`."""
    dim_keys = [k for k, _ in DIMENSIONS]
    pillar_counts: dict[str, int] = {}
    for d in days_payload:
        for ag in d.get("agendas", []):
            p = classify_game_pillar(ag)
            pillar_counts[p] = pillar_counts.get(p, 0) + 1

    sampled_days = days_payload if len(days_payload) <= 6 else (days_payload[:3] + days_payload[-2:])
    return (
        "You are the Autonomous Critic Agent for Kalyani.\n\n"
        "=== REFERENCE 1: students/ma_kalyani/persona.md ===\n"
        f"{persona_card_md}\n\n"
        "=== REFERENCE 2: docs/student-persona.md ===\n"
        f"{student_persona_spec_md}\n\n"
        "=== REFERENCE 3: content/curriculum.md ===\n"
        f"{curriculum_md}\n\n"
        "=== REFERENCE 4: content/content_curation.md ===\n"
        f"{curation_md}\n\n"
        "=== GLOBAL CURRICULUM TELEMETRY ===\n"
        f"Total days: {len(days_payload)} | Game counts per day: {[len(d.get('agendas', [])) for d in days_payload]}\n"
        f"Pillar totals across all games: {json.dumps(pillar_counts, ensure_ascii=False)}\n"
        f"CBT day numbers: {[d['day'] for d in days_payload if is_covert_cbt_day(d)]}\n\n"
        "=== SAMPLED / TARGET DAYS PAYLOAD ===\n"
        f"{json.dumps(sampled_days, ensure_ascii=False)}\n\n"
        "=== CLIENT-SIDE GEMINI INSTRUCTION (docs/client-side-gemini.md) ===\n"
        f"{client_gemini_md[:3500]}\n\n"
        "Evaluate the curriculum days and client-side Gemini prompt strictly against all 4 reference specifications above.\n"
        "Return ONLY valid JSON matching this schema:\n"
        "{\n"
        '  "passed": true,\n'
        f'  "dimension_scores": {{{", ".join(f"{json.dumps(k)}: 10" for k in dim_keys)}}},\n'
        '  "weak_games": [{"day": 1, "game_idx": 0, "pillar": "tech_65", "critique": "..."}],\n'
        '  "summary_critique": "Holistic clinical and pedagogical evaluation"\n'
        "}"
    )


def build_agentic_refiner_prompt(
    persona_card_md: str,
    student_persona_spec_md: str,
    curriculum_md: str,
    curation_md: str,
    day_obj: dict,
    game_idx: int,
    critique: str,
) -> str:
    """Construct the pure LLM Refiner prompt from Persona specs + `curriculum.md` + `content_curation.md`."""
    ag = day_obj["agendas"][game_idx]
    return (
        "You are the Autonomous Refiner Agent for Kalyani.\n\n"
        f"=== students/ma_kalyani/persona.md ===\n{persona_card_md}\n\n"
        f"=== docs/student-persona.md (Excerpt) ===\n{student_persona_spec_md[:2000]}\n\n"
        f"=== content/curriculum.md ===\n{curriculum_md[:2000]}\n\n"
        f"=== content/content_curation.md ===\n{curation_md[:2000]}\n\n"
        f"Rewrite Day {day_obj['day']} Game #{game_idx} to resolve this Critic feedback:\n"
        f"Critique: {critique}\n\n"
        f"Current Game JSON:\n{json.dumps(ag, ensure_ascii=False)}\n\n"
        "Return ONLY valid JSON with keys: title_bn, detail_bn, prompt_bn, followup_prompt_bn."
    )


def run_agentic_improvement_loop(
    days_list: list[dict] | None = None,
    llm_callable: Callable[[str], str] | None = None,
    max_iterations: int = 3,
    min_score: int = 9,
    persist_markdown: bool = False,
    verbose: bool = False,
) -> tuple[bool, list[dict], dict]:
    """Run the pure LLM Critic -> Refiner -> Re-Evaluate loop driven by Persona specs + `curriculum.md` & `content_curation.md`."""
    caller = llm_callable or call_gemini_llm
    persona_card_md = PERSONA_CARD_MD_PATH.read_text(encoding="utf-8")
    student_persona_spec_md = STUDENT_PERSONA_SPEC_MD_PATH.read_text(encoding="utf-8")
    curriculum_md = CURRICULUM_MD_PATH.read_text(encoding="utf-8")
    curation_md = CONTENT_CURATION_MD_PATH.read_text(encoding="utf-8")
    client_gemini_md = CLIENT_GEMINI_MD_PATH.read_text(encoding="utf-8")

    if days_list is None:
        target_days = load_days_markdown(PART1_MD_PATH) + load_days_markdown(PART2_MD_PATH)
    else:
        target_days = copy.deepcopy(days_list)

    day_map = {int(d["day"]): d for d in target_days}
    total_refinements = 0
    eval_result: dict = {}
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        critic_prompt = build_agentic_critic_prompt(
            persona_card_md=persona_card_md,
            student_persona_spec_md=student_persona_spec_md,
            curriculum_md=curriculum_md,
            curation_md=curation_md,
            days_payload=list(day_map.values()),
            client_gemini_md=client_gemini_md,
        )
        eval_result = _parse_llm_json(caller(critic_prompt))
        raw_scores = eval_result.get("dimension_scores") or {}
        norm_scores = {k: max(1, min(10, int(raw_scores.get(k, 10)))) for k, _ in DIMENSIONS}
        eval_result["dimension_scores"] = norm_scores

        weak_games = eval_result.get("weak_games") or []
        scores_ok = all(v >= min_score for v in norm_scores.values())
        passed = bool(eval_result.get("passed", True)) and not weak_games and scores_ok
        eval_result["passed"] = passed

        if passed or not weak_games or iteration >= max_iterations:
            break

        for wg in weak_games:
            d_num = int(wg.get("day", list(day_map.keys())[0]))
            g_idx = int(wg.get("game_idx", 0))
            if d_num in day_map and 0 <= g_idx < len(day_map[d_num]["agendas"]):
                if verbose:
                    print(f"[Agentic Refiner] Iter {iteration} -> Day {d_num} Game #{g_idx}: {wg.get('critique')}")
                ref_prompt = build_agentic_refiner_prompt(
                    persona_card_md=persona_card_md,
                    student_persona_spec_md=student_persona_spec_md,
                    curriculum_md=curriculum_md,
                    curation_md=curation_md,
                    day_obj=day_map[d_num],
                    game_idx=g_idx,
                    critique=wg.get("critique", "Deepen pedagogical clarity per persona and curriculum specs"),
                )
                rewritten = _parse_llm_json(caller(ref_prompt))
                for field in ("title_bn", "detail_bn", "prompt_bn", "followup_prompt_bn"):
                    if isinstance(rewritten.get(field), str) and rewritten[field].strip():
                        day_map[d_num]["agendas"][g_idx][field] = rewritten[field].strip()
                total_refinements += 1

    refined_days = list(day_map.values())
    if persist_markdown and total_refinements > 0 and days_list is None:
        p1 = [d for d in refined_days if int(d["day"]) <= 21]
        p2 = [d for d in refined_days if int(d["day"]) > 21]
        PART1_MD_PATH.write_text(
            dump_days_markdown("🌸 কল্যাণী — Part 1 Foundation Curriculum (Days 1–21 · Markdown Source of Truth)", p1),
            encoding="utf-8",
        )
        PART2_MD_PATH.write_text(
            dump_days_markdown("🌸 কল্যাণী — Part 2 Extended Calendar Curriculum (Days 22–51 · Markdown Source of Truth)", p2),
            encoding="utf-8",
        )

    report = {
        "engine": "Pure Agentic LLM Evaluator-Optimizer Loop (Blueprint-Driven via curriculum.md + content_curation.md)",
        "iterations_run": iteration,
        "total_refinements_applied": total_refinements,
        "passed": bool(eval_result.get("passed", False)),
        "dimension_scores": eval_result.get("dimension_scores", {k: 10 for k, _ in DIMENSIONS}),
        "summary_critique": eval_result.get("summary_critique", ""),
        "md5_fingerprints": collect_md5_fingerprints(),
        "days": {
            str(d["day"]): {"iterations_run": iteration, "passed": bool(eval_result.get("passed", False))}
            for d in refined_days
        },
    }
    return report["passed"], refined_days, report


def load_curation_manifest() -> dict:
    if not CURATION_MANIFEST_PATH.is_file():
        return {}
    try:
        return json.loads(CURATION_MANIFEST_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_curation_manifest(report: dict) -> None:
    CURATION_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    CURATION_MANIFEST_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_quality_gate(
    verbose: bool = False,
    live_llm: bool = False,
    llm_callable: Callable[[str], str] | None = None,
) -> tuple[bool, list[str], dict[str, int]]:
    """Verify MD5 blueprint/content state or run the live Agentic LLM Critic-Refiner Loop."""
    issues: list[str] = []
    current_md5s = collect_md5_fingerprints()

    for key, digest in current_md5s.items():
        if not digest:
            issues.append(f"Missing required Markdown file for {key}")

    manifest = load_curation_manifest()
    recorded_md5s = manifest.get("md5_fingerprints", {}) if isinstance(manifest, dict) else {}
    md5_in_sync = (recorded_md5s == current_md5s) and bool(manifest.get("passed", False))

    if live_llm or llm_callable is not None:
        passed_loop, _, report = run_agentic_improvement_loop(
            llm_callable=llm_callable,
            persist_markdown=(llm_callable is None),
            verbose=verbose,
        )
        if llm_callable is None:
            save_curation_manifest(report)
        manifest = report
        if not passed_loop:
            issues.append(f"Agentic LLM Critic rejected content: {report.get('summary_critique')}")
    elif not md5_in_sync:
        mismatched = [k for k in current_md5s if recorded_md5s.get(k) != current_md5s[k]]
        issues.append(
            f"MD5 state out of sync for {mismatched}. Run `python3 scripts/curate_loop.py --live-loop`."
        )

    dim_scores = {
        k: int(manifest.get("dimension_scores", {}).get(k, 0 if issues else 10))
        for k, _ in DIMENSIONS
    }
    passed = len(issues) == 0 and all(v >= 9 for v in dim_scores.values())

    if verbose:
        print("=" * 78)
        print("🌸 কল্যাণী — Blueprint-Driven Agentic LLM Loop (curriculum.md + content_curation.md)")
        print("=" * 78)
        for k_md5, v_md5 in collect_md5_fingerprints().items():
            print(f"  • {k_md5:22s}: {v_md5}")
        print("-" * 78)
        for k, label in DIMENSIONS:
            sc = dim_scores[k]
            print(f"  {'✅ PASS' if sc >= 9 else '❌ FAIL'} [{sc:2d}/10] {label}")
        print("-" * 78)
        if manifest.get("summary_critique"):
            print(f"LLM Critic Summary: {manifest['summary_critique']}")
        if issues:
            for iss in issues:
                print(f"  - {iss}")

    return passed, issues, dim_scores


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blueprint-Driven Agentic LLM Content Loop.")
    parser.add_argument("--live-loop", action="store_true", help="Run live Gemini LLM Critic-Refiner loop and update MD5 state.")
    args = parser.parse_args()

    ok, _, _ = run_quality_gate(verbose=True, live_llm=args.live_loop)
    raise SystemExit(0 if ok else 1)
