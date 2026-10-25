# GEMINI.md — 🌸 কল্যাণী (Kalyani App) Master Architecture, UX Artistry & Governance

This file is the **single, canonical, Git-tracked source of truth** governing how any AI engineer/agent designs, architects, tests, and maintains **🌸 কল্যাণী** (`মায়ের আজকের খেলা ও চিঠি`), located in its dedicated repository at [`/usr/local/google/home/koushikchak/kalyani-app`](file:///usr/local/google/home/koushikchak/kalyani-app).

> **Strict Isolation from `koushik-wiki`:** This project is 100% separate from `/usr/local/google/home/koushikchak/koushik-wiki`. Keep all Kalyani App rules, specs, content, frontend source, audio, scripts, and tests strictly inside `/usr/local/google/home/koushikchak/kalyani-app`.

---

## 1. Principal Software Architecture Mandate (Strict Modular Separation)

Maintain the codebase like a **Principal Software Architect**: every file must have a single, crisp responsibility with clean boundaries between **Specifications (`docs/`)**, **Declarative Content (`content/`)**, **Artisanal Frontend Source (`src/`)**, **Structured Media (`assets/`, `audio/`)**, **Build/TTS Tooling (`scripts/`)**, and **Verification (`tests/`)**.

- **Zero Monoliths Rule:**
  - **NEVER** inline raw CSS, HTML, or JavaScript application logic inside Python scripts (`scripts/build_app.py` is strictly a fast assembler `< 200` lines).
  - **NEVER** mix UI rendering logic with curriculum data (`content/` holds pure declarative Python data structures).
  - **NEVER** dump flat untracked `.mp3` files into the root of `audio/`; keep voices organized in `audio/{slides,quotes,days,games}/`.

### Canonical Repository Topology

```text
/usr/local/google/home/koushikchak/kalyani-app/
├── GEMINI.md                           # Master Governance: Architecture, UX Artistry & No-Auto-TTS Policy
├── .gemini/config/rules/
│   └── kalyani_app_rules.md            # Workspace-local agent rule synced with GEMINI.md
├── docs/                               # Product, Pedagogy & Downstream AI Specifications
│   ├── spec.md                         # End-to-end Technical, Audio & Mobile UX Architecture
│   ├── student-persona.md              # Ma's cognitive/emotional profile, ego-safety & 6-game ratio blueprint
│   └── client-side-gemini.md           # Downstream Android Gemini Saved-Info prompt & memory handshake
├── content/                            # Pure Declarative Content & Curriculum Package (Zero UI/Build Code)
│   ├── __init__.py                     # Exports SLIDES, MORNING_QUOTES, GAME_META, DAYS_21, DAYS_PART2_30
│   ├── slides_and_quotes.py            # 8 Thanksgiving letter slides + 7 morning quotes + 6 clean game slot labels
│   ├── part1_days.py                   # Days 1–21 Foundation Journey (21 × 6 = 126 ego-safe games)
│   └── part2_days.py                   # Days 22–51 Extended Journey (30 × 6 = 180 ego-safe games, zero "পার্ট ২" nagging)
├── src/                                # Modular Frontend Source Layer
│   ├── template.html                   # Semantic accessible HTML5 shell (Noto Sans Bengali + Noto Serif Bengali)
│   ├── styles/
│   │   ├── tokens.css                  # "Shantiniketan Handloom Ivory & Shiuli" design tokens & crisp Bengali typography
│   │   ├── layout.css                  # 42px single-row sticky glass header, live audio bar & micro-toast
│   │   └── components.css              # Sequential lock chips, collapsible calendar grids, 2×3 game tiles & letter
│   └── js/
│       ├── state.js                    # State store, localStorage resilience, sequential day-lock & 21-day unlock logic
│       ├── audio.js                    # Proactive auto-engage welcome audio, Aoede play/pause/resume & morning chime
│       ├── plan-view.js                # 🎓 আজকের খেলা renderer (locked days, collapsible calendar grids, clean 2×3 tiles)
│       ├── letter-view.js              # 💌 চিঠি renderer (☀️ অনুপ্রেরণা quote + above-image header badge + 8-slide album)
│       └── boot.js                     # View router, notification scheduler & proactive welcome startup
├── assets/
│   ├── icons/favicon.svg               # Handcrafted Bengali Shiuli flower vector emblem
│   └── slides/slide_1..8.jpg           # Personalized family photographs
├── audio/                              # Domain-Partitioned Gemini Aoede (`gemini-v4s-tts`) Voice Library
│   ├── tts_manifest.json               # SHA-256 text-hash registry for O(Δ) incremental voice refreshes
│   ├── slides/slide_1..8.mp3           # 8 letter slide narrations
│   ├── quotes/quote_0..6.mp3           # 7 morning inspiration narrations
│   ├── days/day_1..51.mp3              # All 51 warm, welcoming day narrations (zero duplicate number readouts)
│   └── games/day_1..51_ag_0..5.mp3     # All 306 natural, number-bloat-free game narrations
├── scripts/                            # Fast Build & Explicit TTS CLI Tooling
│   ├── build_app.py                    # <0.5s static bundler + non-blocking stale-voice detector
│   └── refresh_voices.py               # Explicit-only (--confirm) parallel Gemini Aoede TTS generator
├── tests/                              # Multi-Layer Automated Verification Suite
│   ├── run_tests.py                    # Unified test runner
│   ├── test_architecture_and_docs.py   # Enforces modular structure, docs & No-Auto-TTS rule
│   ├── test_curriculum_persona.py      # Enforces 6-game structure, ego-safety, zero number bloat & YT Music prompts
│   └── test_ui_and_vm_behavior.py      # Headless Node VM behavioral suite (locking, calendar unlock, proactive audio)
├── favicon.svg                         # Root PWA icon (synced automatically from assets/icons/favicon.svg)
├── ma-manifest.json                    # Android Chrome PWA Web App Manifest
├── ma-sw.js                            # Service Worker for notifications & window focus
├── ma-presentation.html                # Compiled public CDN-backed mobile web app
└── index.html                          # Compiled root entrypoint (kept identical to ma-presentation.html)
```

---

## 2. Genius Artist UX Design System (*"Shantiniketan Handloom Ivory & Shiuli"*)

Design every screen and interaction like a **Genius Artist UX Designer** crafting an heirloom gift for a sensitive 64-year-old Bengali mother:

1. **Cultural Warmth, Unclipped Bengali `১` (`U+09E7`) & AAA Readability (`src/styles/tokens.css`):**
   - **Palette:** Handloom Ivory canvas (`#FBF7F0`), crisp Sandalwood surfaces (`#FFFFFF`, `#F5EDE0`), deep espresso ink (`#1C140E`, `>14:1` contrast), Shiuli-stem vermilion (`#D8522E`), Tulsi emerald (`#0E8358`), and Temple brass gold (`#AE630C`)—plus 6 harmonious category accents (`terra`, `emerald`, `indigo`, `rose`, `amber`, `plum`).
   - **Crisp Bengali Glyph Rendering:** Always use **`Noto Sans Bengali`** + **`Noto Serif Bengali`** (never `Hind Siliguri`, never `font-variant-numeric: tabular-nums`, and never `overflow: hidden` on text pills/tiles) with generous `line-height >= 1.48–1.6` so Bengali `১` (`U+09E7`) and *matra* ascenders/descenders are never half-cut on Android Chrome.
2. **Zero Distracting Tickers & Sequential Curiosity Locking (`src/js/state.js`, `src/js/plan-view.js`):**
   - **No Part 1/Part 2 Switcher & No Task Completion Counters:** Never display task-completion tickers (`0 / 126`, `খেলা 1 / 6`, `আজকের অগ্রগতি`) or `পার্ট ১` / `পার্ট ২` tabs/labels—they create pressure and distraction.
   - **Sequential Day Locking:** Future days (`Day N` for `N > 1`) stay locked (`🔒 দিন N`) until all 6 games of every previous day (`Day 1 .. Day N-1`) are ticked off (`✅`). Tapping a locked day shows an encouraging Bengali curiosity toast motivating Ma to tick off her current day's games to unlock tomorrow's surprise.
   - **Auto-Unlocked Collapsible Calendar Grid (`Days 22–51`):** `Days 22–51` remain hidden until `Days 1–21` are 100% completed; upon finishing Day 21, `🌿 নতুন ৩০ দিনের ক্যালেন্ডার (দিন ২২ – ৫১)` automatically appears in the days list as a comfortable **Collapsible Calendar Grid View** (alongside the `🗓️ ক্যালেন্ডার` grid toggle for `Days 1–21`).
3. **Proactive Auto-Engage Audio on App Open (`src/js/audio.js`, `src/js/boot.js`):**
   - On app open/load, `engageProactiveWelcomeAudio()` proactively starts reading out today's welcoming day inspiration (`days/day_{curDayNum}.mp3`) and chains automatically into the active incomplete game—with a synchronous first-gesture unlock fallback if a mobile browser blocks cold unmuted autoplay.
4. **Clean Single-Label Game Tiles & Zero Voice Number Bloat:**
   - Game buttons show a single clean label (`🧠 মনের আনন্দ`, `📱 হাতের যন্ত্র`, `🔤 ইংরেজি খেলা`, `🎵 গান ও অর্থ`, `🌍 জানাশোনা`, `🎨 মজার খেলা`)—never duplicate numbers like `খেলা ১` + `১. মনের আনন্দ`.
   - Spoken voice scripts (`scripts/refresh_voices.py` & `content/`) must sound like a real Bengali son speaking warmly at home—never read out bloated number sequences (`1.1`, `১) ... ২)`, `ধাপ ১`) and never mention `"পার্ট ২"`.
   - In `💌 চিঠি`, `#slideBadge` sits cleanly in `.slide-top-header` above `.slide-img-wrap` (never overlaid on top of family photos).

---

## 3. CRITICAL RULE: Lazy / Explicit-Only TTS Voice Generation

1. **On-Device Web Speech API (`speechSynthesis`) is Forbidden:** Always use pre-generated **Gemini `Aoede` (`gemini-v4s-tts`)** `.mp3` files under `audio/`.
2. **NEVER Auto-Regenerate Voices on UI or Content Edits:**
   - During UI, CSS, JS, layout, or curriculum text edits, run **only** `python3 scripts/build_app.py` (`< 0.5s`).
   - `build_app.py` checks `audio/tts_manifest.json` without calling TTS. If `N` files have updated text, finish your edit immediately and **ask/remind Koushik** before running `refresh_voices.py --confirm`.
3. **Explicit Incremental Refresh Command (Only When Requested by Koushik):**
   ```bash
   # Refresh all stale/missing day & game voices (or --scope all / part1 / part2):
   python3 /usr/local/google/home/koushikchak/kalyani-app/scripts/refresh_voices.py --confirm --scope days-and-games
   ```

---

## 4. Build, Test & Deployment Workflow

```bash
# 1. Compile modular src/ + content/ -> ma-presentation.html & index.html (<0.5s):
python3 /usr/local/google/home/koushikchak/kalyani-app/scripts/build_app.py

# 2. Run all modular architecture, persona & Node VM behavioral tests:
python3 /usr/local/google/home/koushikchak/kalyani-app/tests/run_tests.py
```

- **Public Git Remote:** `git@github.com:kouSeek/portfolio.git` (branch `ma-course`)
- **Public Clickable Mobile Link (Never output `localhost` links):**
  https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/ma-course/ma-presentation.html
- **Video Letter MP4 in `Kortex` Drive (linked inside `💌 চিঠি`, zero website HTML/MP3 artifacts in `Kortex`):**
  https://drive.google.com/file/d/1gzEnSqp72VlguNK0YirZHRARGmJFR-4g/view
