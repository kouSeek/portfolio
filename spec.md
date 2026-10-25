# Kalyani App (`মায়ের এআই শিক্ষা ও চিঠি`) — Technical & UX Specification

## 1. Vision & Target User
- **User:** Ma (64 years old, Dumdum Cantonment; Bengali native speaker).
- **Goal:** A warm, zero-shame, Android-first Progressive Web App (PWA) combining an 8-slide personalized Thanksgiving letter (`💌 চিঠি`), a daily random inspiration & morning alarm card (`☀️ অনুপ্রেরণা`), and a 2-part AI & life-confidence curriculum (`🎓 খেলা`: Part 1 = 21-day crash course, Part 2 = 30-day self-paced mastery).

## 2. Audio & TTS Architecture (Hash-Tracked Gemini `Aoede` Voice)
- **Voice Model:** Pre-recorded **Gemini `Aoede` (`gemini-v4s-tts`)** Bengali female voice (`24kHz` mono MP3, normalized to `-16 LUFS`).
- **Zero Auto-Rebuild Rule:**
  - `audio/tts_manifest.json` stores the SHA-256 hash of the exact Bengali speech string for every `.mp3` file (`slide_1..8.mp3`, `quote_0..6.mp3`, `day_1..21.mp3`, `day_1..21_ag_0..9.mp3`).
  - `scripts/build_app.py` compiles `ma-presentation.html` and `index.html` in `< 0.5s` without ever invoking TTS generation. It compares current text hashes against `audio/tts_manifest.json` and prints a summary of any stale/modified sections so the agent can ask Koushik when he wants to refresh them.
  - `scripts/refresh_voices.py --confirm` performs an incremental TTS refresh of only the stale/missing `.mp3` files when explicitly requested by Koushik.

## 3. Mobile-First UI & Navigation Spec
- **Single-Row Sticky Header (`42px`):**
  - Left: **`🌸 কল্যাণী`** brand + 2 compact tabs (`🎓 আজকের খেলা`, `💌 চিঠি`) that fit cleanly on a single row on `360px` Android screens.
  - Right: Master Play/Pause button (`🔊 শোনো` / `⏸️ থামাও`).
  - Inside `💌 চিঠি`: Displays the `☀️ আজকের অনুপ্রেরণা` random quote card above the 8-slide Thanksgiving letter.
  - No footer bar, no separate `অনুপ্রেরণা` header tab, no theme toggle button.
- **6 Cohesive Games Per Day (`2×3` Visual Navigator Grid — See `student-persona.md`):**
  - Strictly `6` games per day (`126` in Part 1, `180` in Part 2), with zero direct mistake callouts (`<= 5%` indirect third-person Wise-Advisor story puzzles).
  - Game 4 (`🎵 ৪. গান ও অর্থ`) includes the highlighted **YouTube Music Bengali Voice-Prompt Guide** (`“জেমিনি, ইউটিউব মিউজিকে ‘...’ গানটা চালিয়ে দাও।”`) + follow-up lyric-meaning prompt (`followup_prompt_bn`).
- **Auto-Advance & Startup Focus:**
  - Checking off an item jumps to the next incomplete game in the day.
  - Completing all 10 games in Day `N` automatically advances to Day `N+1` and scrolls `#dayChip_{N+1}` into view.
  - On app load, `findInitialCurrentDayAndPart()` automatically selects the first day with any incomplete game.
