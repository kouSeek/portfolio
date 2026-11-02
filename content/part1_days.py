# -*- coding: utf-8 -*-
"""Smart Declarative Loader for Part 1 Foundation Days (Days 1–21).

All curriculum text lives cleanly in Markdown (`content/days/part1_days.md`),
curated from `content/curriculum.md` and `content/content_curation.md`.
"""

from pathlib import Path

from .markdown_loader import load_days_markdown

PART1_MD_PATH = Path(__file__).resolve().parent / "days" / "part1_days.md"
DAYS_21 = load_days_markdown(PART1_MD_PATH)
