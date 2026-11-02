# -*- coding: utf-8 -*-
"""Thin Declarative Loader for Kalyani Part 2 Extended Days (`personas/kalyani/days/part2_days.md`)."""

from pathlib import Path

from ..markdown_loader import load_days_markdown

PART2_MD_PATH = Path(__file__).resolve().parents[2] / "personas" / "kalyani" / "days" / "part2_days.md"
DAYS_PART2_30 = load_days_markdown(PART2_MD_PATH)
