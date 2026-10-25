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
- **Single-Row Sticky Header (`46px`):**
  - Left: 3 compact tabs (`🎓 খেলা`, `💌 চিঠি`, `☀️ অনুপ্রেরণা`) that fit on a single row on `360px` Android screens.
  - Right: Master Play/Pause button (`🔊 শোনো` / `⏸️ থামাও`).
  - No footer bar, no theme toggle button.
- **10 Single-Focus Games Per Day (`2×5` Visual Navigator Grid):**
  - Every game card contains:
    1. Category pill & `খেলা X / 10` counter.
    2. `📋 ধাপ ১ — মা আজ যা করবেন ও শিখবেন (বিস্তারিত নির্দেশ)`
    3. For Game 9 (`🎵 ৯. গান`): Highlighted **YouTube Music Bengali Voice-Prompt Guide** (`🎵 ইউটিউব মিউজিকে বাংলায় গান চালানোর সহজ নিয়ম`).
    4. `🗣️ ধাপ ২ — মা, ফোনে জেমিনি (Gemini) অ্যাপ খুলে মাইক 🎙️ বোতাম ছুঁয়ে ঠিক এই কথাটি মুখে বলো:`
    5. `🔊 শোনো` / `⏸️ থামাও` toggle button and `⬜ আমি এটি করেছি` / `✅ করা হয়েছে` completion button.
- **Auto-Advance & Startup Focus:**
  - Checking off an item jumps to the next incomplete game in the day.
  - Completing all 10 games in Day `N` automatically advances to Day `N+1` and scrolls `#dayChip_{N+1}` into view.
  - On app load, `findInitialCurrentDayAndPart()` automatically selects the first day with any incomplete game.
