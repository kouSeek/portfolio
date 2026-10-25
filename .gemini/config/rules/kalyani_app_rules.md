# Kalyani App Workspace Rules

All rules, preferences, and specifications for the **Kalyani App** (`মায়ের এআই শিক্ষা ও চিঠি`) are governed by [`/usr/local/google/home/koushikchak/kalyani-app/GEMINI.md`](file:///usr/local/google/home/koushikchak/kalyani-app/GEMINI.md) and [`/usr/local/google/home/koushikchak/kalyani-app/spec.md`](file:///usr/local/google/home/koushikchak/kalyani-app/spec.md).

## Mandatory Operating Rules
1. **Strict Repository Isolation:** Keep all Kalyani App code, scripts, audio, specs, and rules inside `/usr/local/google/home/koushikchak/kalyani-app`. Never mix Kalyani App files into `/usr/local/google/home/koushikchak/koushik-wiki`.
2. **NO Automatic TTS Voice Regeneration:**
   - Never run `scripts/refresh_voices.py` or `generate tts` automatically when making UI changes, CSS/JS edits, or curriculum/data text edits.
   - Always run `python3 /usr/local/google/home/koushikchak/kalyani-app/scripts/build_app.py` (`<0.5s`) and `python3 /usr/local/google/home/koushikchak/kalyani-app/tests/run_tests.py`.
   - If `build_app.py` detects that text changes made `N` audio files stale relative to `audio/tts_manifest.json`, **do not regenerate them automatically**—remind/ask Koushik if he wants to refresh those `N` voices once he finishes reviewing the text/UI changes.
3. **No `localhost` Links:** Always provide the public clickable link (`https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/ma-course/ma-presentation.html`) and clickable `file://` links.
