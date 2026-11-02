# -*- coding: utf-8 -*-
"""Thin Declarative Loader for Kalyani Part 1 Foundation Days (`personas/kalyani/days/part1_days.md`)."""

from pathlib import Path

from ..markdown_loader import load_days_markdown

PART1_MD_PATH = Path(__file__).resolve().parents[2] / "personas" / "kalyani" / "days" / "part1_days.md"
DAYS_21 = load_days_markdown(PART1_MD_PATH)
