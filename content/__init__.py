"""Self-contained seed data for Jhalak Reels (`jhalak.html`) and Zorba Reels (`zorba.html`)."""
import json
from pathlib import Path

_DATA = json.loads((Path(__file__).resolve().parent / "reels_seed.json").read_text(encoding="utf-8"))
LETTER_VIDEO_URL = _DATA["LETTER_VIDEO_URL"]
SLIDES = _DATA["SLIDES"]
DAYS_21 = _DATA["DAYS_21"]
ANONDO_SLIDES = _DATA["ANONDO_SLIDES"]

__all__ = ["LETTER_VIDEO_URL", "SLIDES", "DAYS_21", "ANONDO_SLIDES"]
