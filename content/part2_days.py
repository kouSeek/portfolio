# -*- coding: utf-8 -*-
"""Smart Declarative Loader for Part 2 Extended Calendar Days (Days 22–51).

All curriculum text lives cleanly in Markdown (`content/days/part2_days.md`),
curated from `content/curriculum.md` and `content/content_curation.md`.
"""

from pathlib import Path

from .markdown_loader import load_days_markdown

PART2_MD_PATH = Path(__file__).resolve().parent / "days" / "part2_days.md"
DAYS_PART2_30 = load_days_markdown(PART2_MD_PATH)
