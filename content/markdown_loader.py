# -*- coding: utf-8 -*-
"""Structured Markdown Loader & Serializer for 🌸 কল্যাণী Curriculum Days.

Stores all daily curriculum content cleanly in human-readable Markdown files
(`personas/kalyani/days/part1_days.md` and `personas/anondo/days/anondo_days.md`) so `part1_days.py`
and `anondo_days.py` remain tiny declarative loaders with zero hardcoded Python dict walls.
"""

from __future__ import annotations

from pathlib import Path
import re

DAY_HEADER_RE = re.compile(r"^## Day (\d+)\s*$")
GAME_HEADER_RE = re.compile(r"^### Game (\d+)\s*$")
KV_LINE_RE = re.compile(r"^- \*\*([a-zA-Z0-9_]+)\*\*:\s*(.*)$")


def parse_days_markdown(md_text: str) -> list[dict]:
    """Parse structured curriculum Markdown into a list of day dictionaries."""
    days: list[dict] = []
    cur_day: dict | None = None
    cur_game: dict | None = None

    for raw_line in md_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("# ") or line == "---":
            continue

        m_day = DAY_HEADER_RE.match(line)
        if m_day:
            if cur_game is not None and cur_day is not None:
                cur_day["agendas"].append(cur_game)
                cur_game = None
            if cur_day is not None:
                days.append(cur_day)
            cur_day = {"day": int(m_day.group(1)), "agendas": []}
            continue

        m_game = GAME_HEADER_RE.match(line)
        if m_game and cur_day is not None:
            if cur_game is not None:
                cur_day["agendas"].append(cur_game)
            cur_game = {}
            continue

        m_kv = KV_LINE_RE.match(line)
        if m_kv:
            key, val = m_kv.group(1), m_kv.group(2).strip()
            target = cur_game if cur_game is not None else cur_day
            if target is not None:
                if key in ("day", "part", "part_day", "audio_ref_day", "phase_id"):
                    target[key] = int(val)
                else:
                    target[key] = val

    if cur_game is not None and cur_day is not None:
        cur_day["agendas"].append(cur_game)
    if cur_day is not None:
        days.append(cur_day)

    return days


def load_days_markdown(path: Path) -> list[dict]:
    """Load curriculum days from a Markdown file."""
    return parse_days_markdown(path.read_text(encoding="utf-8"))


def dump_days_markdown(title: str, days: list[dict]) -> str:
    """Serialize curriculum day dictionaries into clean, readable Markdown."""
    lines: list[str] = [f"# {title}", ""]
    day_keys = (
        "part",
        "part_day",
        "audio_ref_day",
        "phase",
        "phase_id",
        "title_bn",
        "title_en",
        "summary_bn",
        "summary_en",
        "voice_script_bn",
        "reward",
    )
    game_keys = (
        "pillar",
        "short_bn",
        "accent",
        "category",
        "title_bn",
        "detail_bn",
        "prompt_bn",
        "followup_prompt_bn",
    )

    for d in days:
        lines.append(f"## Day {d['day']}")
        for k in day_keys:
            if k in d and str(d[k]).strip():
                val = " ".join(str(d[k]).splitlines()).strip()
                lines.append(f"- **{k}**: {val}")
        lines.append("")
        for idx, ag in enumerate(d.get("agendas", []), start=1):
            lines.append(f"### Game {idx}")
            for gk in game_keys:
                if gk in ag and str(ag[gk]).strip():
                    gval = " ".join(str(ag[gk]).splitlines()).strip()
                    lines.append(f"- **{gk}**: {gval}")
            lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
