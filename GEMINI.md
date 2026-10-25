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
│   ├── slides_and_quotes.py            # 8 Thanksgiving letter slides + 7 morning quotes + 6 game slot metadata
│   ├── part1_days.py                   # Part 1: 21-Day Foundation Course (21 × 6 = 126 ego-safe games)
│   └── part2_days.py                   # Part 2: 30-Day Self-Mastery Course (30 × 6 = 180 ego-safe games)
├── src/                                # Modular Frontend Source Layer
│   ├── template.html                   # Semantic accessible HTML5 shell
│   ├── styles/
│   │   ├── tokens.css                  # "Shantiniketan Handloom Ivory & Shiuli" design tokens & typography
│   │   ├── layout.css                  # 42px single-row sticky glass header, live audio bar & micro-toast
│   │   └── components.css              # Tactile cards, 2×3 game navigator, voice bubbles & heirloom letter
│   └── js/
│       ├── state.js                    # State store, localStorage resilience, Bengali numerals & progression
│       ├── audio.js                    # Unified Aoede play/pause/resume engine, scrub bar & morning chime
│       ├── plan-view.js                # 🎓 আজকের খেলা renderer (hero card, 2×3 tile grid, step-by-step card)
│       ├── letter-view.js              # 💌 চিঠি renderer (☀️ অনুপ্রেরণা quote + 8-slide album & touch swipe)
│       └── boot.js                     # View router, notification scheduler & Service Worker bootstrap
├── assets/
│   ├── icons/favicon.svg               # Handcrafted Bengali Shiuli flower vector emblem
│   └── slides/slide_1..8.jpg           # Personalized family photographs
├── audio/                              # Domain-Partitioned Gemini Aoede (`gemini-v4s-tts`) Voice Library
│   ├── tts_manifest.json               # SHA-256 text-hash registry for O(Δ) incremental voice refreshes
│   ├── slides/slide_1..8.mp3           # 8 letter slide narrations
│   ├── quotes/quote_0..6.mp3           # 7 morning inspiration narrations
│   ├── days/day_1..51.mp3              # All 51 day overview narrations (Part 1 + Part 2)
│   └── games/day_1..51_ag_0..5.mp3     # All 306 verbatim game narrations (Step 1 + Step 2 + Step 3)
├── scripts/                            # Fast Build & Explicit TTS CLI Tooling
│   ├── build_app.py                    # <0.5s static bundler + non-blocking stale-voice detector
│   └── refresh_voices.py               # Explicit-only (--confirm) parallel Gemini Aoede TTS generator
├── tests/                              # Multi-Layer Automated Verification Suite
│   ├── run_tests.py                    # Unified test runner
│   ├── test_architecture_and_docs.py   # Enforces modular structure, docs & No-Auto-TTS rule
│   ├── test_curriculum_persona.py      # Enforces 6-game structure, ego-safety, natural Bangla & YT Music prompts
│   └── test_ui_and_vm_behavior.py      # Headless Node VM behavioral & edge-case suite
├── favicon.svg                         # Root PWA icon (synced automatically from assets/icons/favicon.svg)
├── ma-manifest.json                    # Android Chrome PWA Web App Manifest
├── ma-sw.js                            # Service Worker for notifications & window focus
├── ma-presentation.html                # Compiled public CDN-backed mobile web app
└── index.html                          # Compiled root entrypoint (kept identical to ma-presentation.html)
```

---

## 2. Genius Artist UX Design System (*"Shantiniketan Handloom Ivory & Shiuli"*)

Design every screen and interaction like a **Genius Artist UX Designer** crafting an heirloom gift for a sensitive 64-year-old Bengali mother:

1. **Cultural Warmth & AAA Senior Readability (`src/styles/tokens.css`):**
   - **Palette:** Handloom Ivory canvas (`#FBF7F0`) with subtle warm radial glow, crisp Sandalwood surfaces (`#FFFFFF`, `#F5EDE0`), deep espresso ink (`#1C140E`, `>14:1` contrast), Shiuli-stem vermilion (`#D8522E`), Tulsi emerald (`#0E8358`), and Temple brass gold (`#AE630C`)—plus 6 harmonious category accents (`terra`, `emerald`, `indigo`, `rose`, `amber`, `plum`).
   - **Typography & Ergonomics:** `Hind Siliguri` + `Noto Serif Bengali` with generous line-height (`1.6+`), Bengali numerals (`১–৬`) across UI badges, and **`48px+` tactile touch targets** so nothing feels cramped or intimidating.
   - **Artisanal Details:** Handcrafted 7-petal **Shiuli flower `favicon.svg`**, delicate *Alpana* divider (`❈`), zero visual clutter, zero bottom footer, and no distracting theme toggle.
2. **Single-Row Sticky Glass Header (`42px`):**
   - Left: **`🌸 কল্যাণী`** brand (`#headerBrand`).
   - Center: **`🎓 আজকের খেলা`** (`#htabPlan`) and **`💌 চিঠি`** (`#htabSlides`) fitting on a single row even on `320px–360px` phones.
   - Right: Master Play/Pause button (`#topPlayBtn`).
   - Beneath header (when audio plays): Live **Now-Playing Equalizer & Scrubbable Progress Ribbon (`#nowPlayingBar`)** showing animated voice bars and Bengali elapsed/total time (`০:১২ / ১:০৫`).
3. **Cognitive Ease & Joyful Micro-Interactions:**
   - **6 Cohesive Games/Day (`2×3` Grid):** Color-accented tiles let Ma jump to any of today's 6 games in 1 tap without scrolling.
   - **Crystal-Clear Voice Prompts:** Numbered step pills (`📋 ধাপ ১`, `🎙️ ধাপ ২`, `🗣️ ধাপ ৩`), highlighted `@YouTube Music` helper card on Game 4, and natural spoken West Bengal Bangla (*চলিত বাংলা* — never stiff translated words like `দয়া করে` or `মস্তিষ্ক`).
   - **Ego-Safe Pedagogy (`docs/student-persona.md`):** `0%` direct mistake callouts; `<= 5%` behavioral lessons disguised inside playful third-person Wise-Advisor stories.
   - **Celebration & Auto-Progression:** Checking off a game triggers a warm celebratory micro-toast (`🌸 সাবাশ মা!...`) and advances to the next incomplete game; finishing all 6 games celebrates and auto-advances to the next day.

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
# 1. Compile modular src/ + content/ -> ma-presentation.html, index.html & Drive HTML (<0.5s):
python3 /usr/local/google/home/koushikchak/kalyani-app/scripts/build_app.py

# 2. Run all modular architecture, persona & Node VM behavioral tests:
python3 /usr/local/google/home/koushikchak/kalyani-app/tests/run_tests.py
```

- **Public Git Remote:** `git@github.com:kouSeek/portfolio.git` (branch `ma-course`)
- **Public Clickable Mobile Link (Never output `localhost` links):**
  https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/ma-course/ma-presentation.html
- **Google Drive Standalone HTML File ID:** `16Qgl9PubSfevNx2fF3h_qVIaF3b9mDkr`
