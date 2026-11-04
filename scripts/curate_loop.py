#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pure Agentic LLM Evaluator-Optimizer Loop for AI Companion (`kalyani` + `anondo`).

Driven exclusively by portable Markdown reference specifications inside `personas/<persona_id>/`:
  1. `personas/<persona_id>/persona.md`            — Unified persona, clinical blockers & tone guardrails
  2. `personas/<persona_id>/curriculum.md`         — Master syllabus & daily pillar blueprint
  3. `personas/<persona_id>/content_curation.md`   — 12-Dimension LLM Critic-Refiner rubric

Produces, evaluates, and iteratively refines:
  - `personas/<persona_id>/days/*.md`
  - `personas/<persona_id>/client-side-gemini.md`
  - `personas/<persona_id>/curation_manifest.json`
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

DEFAULT_PERSONA_ID = "kalyani"
PERSONA_ALIASES = {"ma_kalyani": "kalyani", "ma": "kalyani", "koushik": "anondo", "me": "anondo"}
GEN_BIN = "/google/bin/releases/gemini-agents-generate/generate"


def normalize_persona_id(persona_id: str = DEFAULT_PERSONA_ID) -> str:
    return PERSONA_ALIASES.get(persona_id, persona_id)


def resolve_persona_spec_paths(persona_id: str = DEFAULT_PERSONA_ID) -> dict[str, Path | list[Path]]:
    """Resolve the 3 input specs, Markdown day file(s), client-side Gemini doc, and manifest path."""
    pid = normalize_persona_id(persona_id)
    pdir = APP_ROOT / "personas" / pid
    days_dir = pdir / "days"
    if pid == "kalyani":
        days_files = [days_dir / "part1_days.md"]
    else:
        days_files = sorted(days_dir.glob("*.md")) or [days_dir / f"{pid}_days.md"]

    return {
        "persona": pdir / "persona.md",
        "curriculum": pdir / "curriculum.md",
        "curation": pdir / "content_curation.md",
        "days_files": days_files,
        "client_gemini": pdir / "client-side-gemini.md",
        "manifest": pdir / "curation_manifest.json",
    }


DIMENSIONS: tuple[tuple[str, str], ...] = (
    ("cbt_effectiveness", "1. 1-in-2-Days Covert CBT Precision"),
    ("personal_connect", "2. Deep Reminiscence / Inner-Child Clarity"),
    ("relationship_warmth", "3. Family Attachment & Healthy Differentiation"),
    ("inspiration_and_pride", "4. Inspiring Figures & First-Principles Pride"),
    ("charm_and_fun", "5. Song Lyrics Curiosity via @YouTube Music"),
    ("curiosity_and_wonder", "6. World & Frontier Polymathic GK"),
    ("storytelling_depth", "7. Concrete Teaching Target & 2-Turn Depth"),
    ("ease_of_learning", "8. Language / Active Listening Mastery"),
    ("zero_fear_and_shame", "9. Zero Shame, Tech Ease & Plain Clarity"),
    ("urge_to_express_mind", "10. Authentic Voice & 2-Turn Agency"),
    ("freedom_and_autonomy", "11. Effortless Pacing & Zorba Autonomy"),
    ("growing_own_dreams", "12. Client-Side Gemini Harmony & Memory"),
)


def md5_file(path: Path) -> str:
    if not path.is_file():
        return ""
    return hashlib.md5(path.read_bytes()).hexdigest()


def collect_md5_fingerprints(persona_id: str = DEFAULT_PERSONA_ID) -> dict[str, str]:
    """Collect MD5 digests of the 3 unified input specs and curated Markdown outputs."""
    pid = normalize_persona_id(persona_id)
    paths = resolve_persona_spec_paths(pid)
    days_files: list[Path] = paths["days_files"]  # type: ignore[assignment]
    if pid == "kalyani":
        return {
            "persona_md5": md5_file(paths["persona"]),  # type: ignore[arg-type]
            "curriculum_md5": md5_file(paths["curriculum"]),  # type: ignore[arg-type]
            "content_curation_md5": md5_file(paths["curation"]),  # type: ignore[arg-type]
            "part1_days_md5": md5_file(days_files[0]),
            "client_gemini_md5": md5_file(paths["client_gemini"]),  # type: ignore[arg-type]
        }

    return {
        "persona_md5": md5_file(paths["persona"]),  # type: ignore[arg-type]
        "curriculum_md5": md5_file(paths["curriculum"]),  # type: ignore[arg-type]
        "content_curation_md5": md5_file(paths["curation"]),  # type: ignore[arg-type]
        "days_md5": md5_file(days_files[0]),
        "client_gemini_md5": md5_file(paths["client_gemini"]),  # type: ignore[arg-type]
    }


def classify_game_pillar(ag: dict) -> str:
    return str(ag.get("pillar", "")).strip() or "gk_inspiring"


def is_covert_cbt_day(day_obj: dict) -> bool:
    return any(classify_game_pillar(ag) == "covert_cbt" for ag in day_obj.get("agendas", []))


def call_gemini_llm(prompt: str, timeout_s: int = 75) -> str:
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
        last_err = ""
        for _attempt in range(3):
            proc = subprocess.run(
                [GEN_BIN, f"-timeout={timeout_s}s", "text", prompt],
                capture_output=True,
                text=True,
                timeout=timeout_s + 5,
                check=False,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                return proc.stdout.strip()
            last_err = proc.stderr[:240]
        raise RuntimeError(f"Gemini CLI failed after 3 attempts: {last_err}")

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
    persona_md: str,
    curriculum_md: str,
    curation_md: str,
    days_payload: list[dict],
    client_gemini_md: str,
) -> str:
    dim_keys = [k for k, _ in DIMENSIONS]
    pillar_counts: dict[str, int] = {}
    for d in days_payload:
        for ag in d.get("agendas", []):
            p = classify_game_pillar(ag)
            pillar_counts[p] = pillar_counts.get(p, 0) + 1

    sampled_days = days_payload if len(days_payload) <= 6 else (days_payload[:3] + days_payload[-2:])
    return (
        "You are the Autonomous Critic Agent for the AI Companion Multi-Persona Architecture.\n\n"
        "=== REFERENCE 1: personas/<persona_id>/persona.md ===\n"
        f"{persona_md}\n\n"
        "=== REFERENCE 2: personas/<persona_id>/curriculum.md ===\n"
        f"{curriculum_md}\n\n"
        "=== REFERENCE 3: personas/<persona_id>/content_curation.md ===\n"
        f"{curation_md}\n\n"
        "=== GLOBAL CURRICULUM TELEMETRY ===\n"
        f"Total days: {len(days_payload)} | Game counts per day: {[len(d.get('agendas', [])) for d in days_payload]}\n"
        f"Pillar totals across all games: {json.dumps(pillar_counts, ensure_ascii=False)}\n"
        f"CBT day numbers: {[d['day'] for d in days_payload if is_covert_cbt_day(d)]}\n\n"
        "=== SAMPLED / TARGET DAYS PAYLOAD ===\n"
        f"{json.dumps(sampled_days, ensure_ascii=False)}\n\n"
        "=== CLIENT-SIDE GEMINI INSTRUCTION ===\n"
        f"{client_gemini_md[:3500]}\n\n"
        "Evaluate the curriculum days and client-side Gemini prompt strictly against all 3 reference specifications above.\n"
        "Return ONLY valid JSON matching this schema:\n"
        "{\n"
        '  "passed": true,\n'
        f'  "dimension_scores": {{{", ".join(f"{json.dumps(k)}: 10" for k in dim_keys)}}},\n'
        '  "weak_games": [{"day": 1, "game_idx": 0, "pillar": "music", "critique": "..."}],\n'
        '  "summary_critique": "Holistic clinical and pedagogical evaluation"\n'
        "}"
    )


def build_agentic_refiner_prompt(
    persona_md: str,
    curriculum_md: str,
    curation_md: str,
    day_obj: dict,
    game_idx: int,
    critique: str,
) -> str:
    ag = day_obj["agendas"][game_idx]
    return (
        "You are the Autonomous Refiner Agent for AI Companion.\n\n"
        f"=== persona.md ===\n{persona_md[:2500]}\n\n"
        f"=== curriculum.md ===\n{curriculum_md[:2000]}\n\n"
        f"=== content_curation.md ===\n{curation_md[:2000]}\n\n"
        f"Rewrite Day {day_obj['day']} Game #{game_idx} to resolve this Critic feedback:\n"
        f"Critique: {critique}\n\n"
        f"Current Game JSON:\n{json.dumps(ag, ensure_ascii=False)}\n\n"
        "Return ONLY valid JSON with keys: title_bn, detail_bn, prompt_bn, followup_prompt_bn."
    )


def run_agentic_improvement_loop(
    days_list: list[dict] | None = None,
    llm_callable: Callable[[str], str] | None = None,
    persona_id: str = DEFAULT_PERSONA_ID,
    student_id: str | None = None,
    max_iterations: int = 3,
    min_score: int = 9,
    persist_markdown: bool = False,
    verbose: bool = False,
) -> tuple[bool, list[dict], dict]:
    pid = normalize_persona_id(student_id or persona_id)
    caller = llm_callable or call_gemini_llm
    spec_paths = resolve_persona_spec_paths(pid)
    persona_md = Path(spec_paths["persona"]).read_text(encoding="utf-8")  # type: ignore[arg-type]
    curriculum_md = Path(spec_paths["curriculum"]).read_text(encoding="utf-8")  # type: ignore[arg-type]
    curation_md = Path(spec_paths["curation"]).read_text(encoding="utf-8")  # type: ignore[arg-type]
    client_gemini_md = Path(spec_paths["client_gemini"]).read_text(encoding="utf-8")  # type: ignore[arg-type]
    days_files: list[Path] = spec_paths["days_files"]  # type: ignore[assignment]

    if days_list is None:
        target_days: list[dict] = []
        for md_path in days_files:
            target_days.extend(load_days_markdown(md_path))
    else:
        target_days = copy.deepcopy(days_list)

    day_map = {int(d["day"]): d for d in target_days}
    total_refinements = 0
    eval_result: dict = {}
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        critic_prompt = build_agentic_critic_prompt(
            persona_md=persona_md,
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
                    print(f"[Agentic Refiner ({pid})] Iter {iteration} -> Day {d_num} Game #{g_idx}: {wg.get('critique')}")
                ref_prompt = build_agentic_refiner_prompt(
                    persona_md=persona_md,
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
        if pid == "kalyani":
            days_files[0].write_text(
                dump_days_markdown("🌸 কল্যাণী — 21-Day Foundation Curriculum (Days 1–21 · Markdown Source of Truth)", refined_days),
                encoding="utf-8",
            )
        else:
            days_files[0].write_text(
                dump_days_markdown(f"⚡ {pid.upper()} — Companion Curriculum", refined_days),
                encoding="utf-8",
            )

    report = {
        "engine": "Pure Agentic LLM Evaluator-Optimizer Loop (Modular Persona Package)",
        "persona_id": pid,
        "iterations_run": iteration,
        "total_refinements_applied": total_refinements,
        "passed": bool(eval_result.get("passed", False)),
        "dimension_scores": eval_result.get("dimension_scores", {k: 10 for k, _ in DIMENSIONS}),
        "summary_critique": eval_result.get("summary_critique", ""),
        "md5_fingerprints": collect_md5_fingerprints(pid),
        "days": {
            str(d["day"]): {"iterations_run": iteration, "passed": bool(eval_result.get("passed", False))}
            for d in refined_days
        },
    }
    return report["passed"], refined_days, report


def load_curation_manifest(persona_id: str = DEFAULT_PERSONA_ID) -> dict:
    manifest_path = Path(resolve_persona_spec_paths(persona_id)["manifest"])  # type: ignore[arg-type]
    if not manifest_path.is_file():
        return {}
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_curation_manifest(report: dict, persona_id: str = DEFAULT_PERSONA_ID) -> None:
    manifest_path = Path(resolve_persona_spec_paths(persona_id)["manifest"])  # type: ignore[arg-type]
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_quality_gate(
    verbose: bool = False,
    live_llm: bool = False,
    llm_callable: Callable[[str], str] | None = None,
    persona_id: str = DEFAULT_PERSONA_ID,
    student_id: str | None = None,
) -> tuple[bool, list[str], dict[str, int]]:
    pid = normalize_persona_id(student_id or persona_id)
    issues: list[str] = []
    current_md5s = collect_md5_fingerprints(pid)

    for key, digest in current_md5s.items():
        if not digest:
            issues.append(f"Missing required Markdown file for {pid}:{key}")

    manifest = load_curation_manifest(pid)
    recorded_md5s = manifest.get("md5_fingerprints", {}) if isinstance(manifest, dict) else {}
    md5_in_sync = (recorded_md5s == current_md5s) and bool(manifest.get("passed", False))

    if live_llm or llm_callable is not None:
        passed_loop, _, report = run_agentic_improvement_loop(
            llm_callable=llm_callable,
            persona_id=pid,
            persist_markdown=(llm_callable is None),
            verbose=verbose,
        )
        if llm_callable is None:
            save_curation_manifest(report, pid)
        manifest = report
        if not passed_loop:
            issues.append(f"Agentic LLM Critic rejected {pid} content: {report.get('summary_critique')}")
    elif not md5_in_sync:
        mismatched = [k for k in current_md5s if recorded_md5s.get(k) != current_md5s[k]]
        issues.append(
            f"MD5 state out of sync for {pid}:{mismatched}. Run `python3 scripts/curate_loop.py --persona {pid} --live-loop`."
        )

    dim_scores = {
        k: int(manifest.get("dimension_scores", {}).get(k, 0 if issues else 10))
        for k, _ in DIMENSIONS
    }
    passed = len(issues) == 0 and all(v >= 9 for v in dim_scores.values())

    if verbose:
        print("=" * 78)
        print(f"⚡ AI Companion — Agentic LLM Loop (persona='{pid}')")
        print("=" * 78)
        for k_md5, v_md5 in collect_md5_fingerprints(pid).items():
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
    parser = argparse.ArgumentParser(description="Multi-Persona Agentic LLM Content Loop (`kalyani` & `anondo`).")
    parser.add_argument("--persona", default="all", choices=("all", "kalyani", "anondo"), help="Target persona (default: all).")
    parser.add_argument("--live-loop", action="store_true", help="Run live Gemini LLM Critic-Refiner loop and update MD5 state.")
    args = parser.parse_args()

    targets = ("kalyani", "anondo") if args.persona == "all" else (args.persona,)
    all_ok = True
    for p_target in targets:
        ok, _, _ = run_quality_gate(verbose=True, live_llm=args.live_loop, persona_id=p_target)
        all_ok = all_ok and ok
    raise SystemExit(0 if all_ok else 1)
