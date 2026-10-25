# GEMINI.md — Kalyani App (মায়ের এআই শিক্ষা ও চিঠি) Master Rules & Schema

This file is the **single, canonical, Git-tracked source of truth** governing how the LLM agent develops, tests, and maintains the **Kalyani App** (`মায়ের এআই শিক্ষা ও চিঠি`), located in its dedicated repository at [`/usr/local/google/home/koushikchak/kalyani-app`](file:///usr/local/google/home/koushikchak/kalyani-app).

> **Strict Separation from `koushik-wiki`:** This project is 100% separate from `/usr/local/google/home/koushikchak/koushik-wiki`. Keep all Kalyani App preferences, rules, specs, scripts, audio, HTML, and tests strictly inside `/usr/local/google/home/koushikchak/kalyani-app`. Never place Kalyani App files or rules inside `koushik-wiki`.

---

## 1. CRITICAL RULE: Lazy / On-Demand TTS Voice Generation (NEVER Auto-Regenerate Voices)

1. **On-Device Web Speech API (`speechSynthesis`) is Forbidden:** Client-side/on-device browser voices sound robotic and unnatural in Bengali. Always use pre-generated **Gemini `Aoede` (`gemini-v4s-tts`)** Bengali female voice `.mp3` files stored in [`audio/`](file:///usr/local/google/home/koushikchak/kalyani-app/audio).
2. **NEVER Automatically Trigger TTS Voice Rebuilds During UI or Content Changes:**
   - When Koushik asks for **UI changes, layout tweaks, CSS/JS updates, or curriculum/data/content edits**, **DO NOT** run `scripts/refresh_voices.py` or invoke `generate tts` automatically.
   - Always run only [`scripts/build_app.py`](file:///usr/local/google/home/koushikchak/kalyani-app/scripts/build_app.py) (`< 0.5s` build time), which reuses existing `.mp3` files and checks [`audio/tts_manifest.json`](file:///usr/local/google/home/koushikchak/kalyani-app/audio/tts_manifest.json) to detect whether any text edits made specific `.mp3` files stale.
3. **Track Stale Voices & Remind / Ask Koushik Before Refreshing:**
   - Whenever `scripts/build_app.py` reports that `N` audio files have updated text (or are missing) relative to `audio/tts_manifest.json`, **do not regenerate them automatically**.
   - Instead, complete the UI/content edit immediately and **remind / ask Koushik in your response**:
     > *"Note: `N` section(s) had text updates and their TTS audio is currently pending refresh. Let me know when you are happy with the text/UI and want me to refresh those `N` voice files (`python3 scripts/refresh_voices.py --confirm`)."*
4. **Incremental Voice Refresh Only When Explicitly Requested:**
   - Only run [`scripts/refresh_voices.py --confirm`](file:///usr/local/google/home/koushikchak/kalyani-app/scripts/refresh_voices.py) when Koushik explicitly confirms he is ready to refresh the voices.
   - By default, `refresh_voices.py --confirm` only regenerates the exact `.mp3` files whose SHA-256 text hash in `audio/tts_manifest.json` changed (never all 246 files unless `--all` is explicitly requested).

---

## 2. Repository Architecture & Directory Layout

```text
/usr/local/google/home/koushikchak/kalyani-app/
├── GEMINI.md                  # Master rules, preferences & No-Auto-TTS policy
├── .gemini/
│   └── config/
│       └── rules/
│           └── kalyani_app_rules.md # Workspace-local agent rules
├── spec.md                    # End-to-end Product, Curriculum & Mobile UX Specification
├── index.html                 # Public CDN-audio standalone web app (served via GitHub / htmlpreview)
├── ma-presentation.html       # Canonical mobile web app (kept identical to index.html)
├── ma-manifest.json           # Android Chrome PWA Web App Manifest
├── ma-sw.js                   # Service Worker for offline caching & morning notifications
├── assets/
│   └── slides/                # Personalized family photos (slide_1.jpg .. slide_8.jpg)
├── audio/
│   ├── tts_manifest.json      # SHA-256 text-hash registry tracking which MP3s match current text
│   └── *.mp3                  # Gemini Aoede (gemini-v4s-tts) Bengali female voice MP3s
├── scripts/
│   ├── curriculum_data.py     # 8 Slides + Part 1 (21 Days x 10 Single-Task Games) + Part 2 (30 Days x 10 Games)
│   ├── build_app.py           # Instant (<0.5s) HTML compiler & stale-voice detector (zero TTS calls)
│   └── refresh_voices.py      # Explicit-only incremental Gemini Aoede TTS generator (--confirm required)
└── tests/
    ├── test_kalyani_app.py    # Unit & Node VM behavioral test suite
    └── run_tests.py           # Unified test runner
```

---

## 3. Core Product & UX Invariants

1. **Android Mobile-First, Distraction-Free Layout:**
   - Single-row ultra-compact sticky header (`46px` height) with **3 tabs**: `🎓 খেলা` (`#htabPlan`), `💌 চিঠি` (`#htabSlides`), and `☀️ অনুপ্রেরণা` (`#htabQuote`), plus the master play/pause button (`#topPlayBtn`).
   - **Zero bottom footer** (no Kalyani chat tab, no Diary tab).
   - **No theme toggle button** in the header (locked to the warm, high-contrast maternal daylight theme).
2. **10 Single-Focus Games Per Day (`2×5` Visual Navigator Grid):**
   - Every day in **Part 1 (`21` days = `210` games)** and **Part 2 (`30` days = `300` games)** has strictly **1 task per game** across 10 categories:
     1. `🧠 ১. মন` — CBT Therapy & Self-Confidence
     2. `📱 ২. রিমোট` — Single Appliance / Phone Mastery
     3. `🔤 ৩. শব্দ` — English Word Reading (3 words)
     4. `🗣️ ৪. ইংরেজি বলা` — Speaking 1 English Sentence Out Loud
     5. `🌍 ৫. খবর` — General Knowledge & Social News
     6. `🤖 ৬. এআই` — Everyday Personal AI Help
     7. `🏆 ৭. চ্যালেঞ্জ` — Comfort-Zone Action Challenge
     8. `💡 ৮. বুদ্ধি` — Loving Self-Realization & Mistake Reinforcement
     9. `🎵 ৯. গান` — Playing Today's Song in **YouTube Music** via Bengali Voice Prompt + Lyric Meaning
     10. `❓ ১০. কেন?` — Asking *"Why & How"* Critical Curiosity
3. **Smart Progression & Navigation:**
   - Completing all 10 games in a day automatically advances to the next day (`Day N -> Day N+1`) and scrolls the active day chip into view.
   - Opening the app automatically focuses the first incomplete day (`findInitialCurrentDayAndPart()`).
   - Clicking `☀️ অনুপ্রেরণা` (`#htabQuote`) displays a **new random morning quote** on every click.
4. **Unified Play/Pause/Resume Audio State Machine:**
   - Every `🔊 শোনো` button toggles to `⏸️ থামাও` while playing, pauses on second tap, and resumes cleanly from `currentTime`.
   - Every section's audio reads the **entire card verbatim**, including both Step 1 (`detail_bn`) and Step 2 (`prompt_bn` — the exact words Ma speaks into the Gemini mic).

---

## 4. Build, Test & Deployment Commands

- **Instant Build + Stale TTS Check (Default on Every Edit — `<0.5s`):**
  ```bash
  python3 /usr/local/google/home/koushikchak/kalyani-app/scripts/build_app.py
  ```
- **Run Unit & VM Test Suite:**
  ```bash
  python3 /usr/local/google/home/koushikchak/kalyani-app/tests/run_tests.py
  ```
- **Refresh Stale / Changed Voices (ONLY When Koushik Explicitly Asks):**
  ```bash
  python3 /usr/local/google/home/koushikchak/kalyani-app/scripts/refresh_voices.py --confirm
  ```
- **Public Hosting Remote & Link:**
  - Git Remote: `git@github.com:kouSeek/portfolio.git` (branch `ma-course`)
  - Direct Clickable Link (Never give `localhost` links):
    `https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/ma-course/ma-presentation.html`
  - Google Drive File ID: `16Qgl9PubSfevNx2fF3h_qVIaF3b9mDkr`
