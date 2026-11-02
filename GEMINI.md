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
├── docs/                               # Product, Pedagogy, Pipeline & Downstream AI Specifications
│   ├── spec.md                         # End-to-end Technical, Audio & Mobile UX Architecture
│   ├── content-pipeline.md             # Reusable 5-stage Multi-Student Pipeline & Dynamic Evolution Blueprint
│   └── client-side-gemini.md           # Downstream Android Gemini Master Prompt (English rules, strictly Bangla speech)
├── students/                           # Portable Per-Student Persona & Review-Stage Curriculum Drafts
│   └── ma_kalyani/
│       ├── persona.md                  # Single unified portable persona spec for Ma (profile, clinical CBT blockers, tone)
│       └── curriculum_v2_draft.md      # Human-reviewable curriculum draft
├── content/                            # Declarative Markdown Blueprints, Markdown Days & Thin Loaders
│   ├── __init__.py                     # Exports SLIDES, MORNING_QUOTES, GAME_META, DAYS_21, DAYS_PART2_30
│   ├── curriculum.md                   # Master 51-day syllabus, 60/30/10 language split & 3-pillar Gemini Live tech spec
│   ├── content_curation.md             # 12-Dimension Agentic Evaluator-Optimizer rubric & rewrite protocol
│   ├── curation_manifest.json          # 7-file MD5 state ledger + live Gemini LLM Critic evaluation
│   ├── markdown_loader.py              # Structured Markdown parser/serializer for daily curriculum files
│   ├── days/
│   │   ├── part1_days.md               # Markdown source of truth for Days 1–21 (126 games)
│   │   └── part2_days.md               # Markdown source of truth for Days 22–51 (180 games)
│   ├── slides_and_quotes.py            # 8 Thanksgiving letter slides + 7 morning quotes + 6 clean game slot labels
│   ├── part1_days.py                   # Thin 13-line declarative loader for content/days/part1_days.md
│   └── part2_days.py                   # Thin 13-line declarative loader for content/days/part2_days.md
├── src/                                # Modular Frontend Source Layer
│   ├── template.html                   # Semantic accessible HTML5 shell
│   ├── templates/
│   │   └── index.html.j2               # Jinja2 HTML5 shell rendered by scripts/build_app.py
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
├── audio/                              # Local Aoede Cache + Tracked Hash Registry (MP3s published to `ma-audio` orphan branch)
│   ├── tts_manifest.json               # Git-tracked SHA-256 text-hash registry for O(Δ) incremental voice refreshes
│   ├── slides/slide_1..8.mp3           # Local cache -> published to `ma-audio` orphan branch
│   ├── quotes/quote_0..6.mp3           # Local cache -> published to `ma-audio` orphan branch
│   ├── days/day_1..51.mp3              # Local cache -> published to `ma-audio` orphan branch
│   └── games/day_1..51_ag_*.mp3        # Local cache -> published to `ma-audio` orphan branch
├── scripts/                            # Fast Build, Content Quality Gate, Explicit TTS & Orphan Audio Branch Tooling
│   ├── build_app.py                    # <0.5s static bundler + mandatory 12-dimension quality gate + stale-voice detector
│   ├── curate_loop.py                  # Automated 12-Dimension Content Quality Gate & Continuous Improvement Auditor
│   ├── refresh_voices.py               # Explicit-only (--confirm) parallel Gemini Aoede TTS generator
│   └── sync_audio_branch.py            # Publishes `audio/` as a 1-commit snapshot to `ma-audio` orphan branch
├── tests/                              # Multi-Layer Automated Verification Suite
│   ├── run_tests.py                    # Unified test runner
│   ├── test_architecture_and_docs.py   # Enforces modular structure, docs & No-Auto-TTS rule
│   ├── test_curriculum_persona.py      # Enforces 6-game structure, ego-safety, zero number bloat & YT Music prompts
│   └── test_ui_and_vm_behavior.py      # Headless Node VM behavioral suite (locking, calendar unlock, proactive audio)
├── favicon.svg                         # Root PWA icon (synced automatically from assets/icons/favicon.svg)
├── ma-manifest.json                    # Android Chrome PWA Web App Manifest
├── ma-sw.js                            # Service Worker for notifications & window focus
└── index.html                          # Single compiled root PWA entrypoint (zero duplicate HTML bundles)
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
3. **Proactive Auto-Engage Audio & Seamless Stepper Voice (`src/js/audio.js`, `src/js/plan-view.js`):**
   - **On App Open:** Automatically focuses the current active day and **the next game right after the latest finished/done game** (`getNextOpenGameIdx(curDayNum)`), proactively plays the Day Voice (`days/day_{curDayNum}.mp3`) while preloading that open game's MP3, and chains immediately into reading the current open game (`games/day_{curDayNum}_ag_{curGameIdx}.mp3`).
   - **On Next Game / Prev Game / Game Tile Click:** Clicking `পরের খেলা ➡️`, `⬅️ আগের খেলা`, or any game tile immediately plays the voice for that game.
4. **Clean Single-Label Game Tiles & Zero Voice Number Bloat:**
   - Game buttons show a single clean label (`🧠 মনের আনন্দ`, `📱 হাতের যন্ত্র`, `🔤 ইংরেজি খেলা`, `🎵 গান ও অর্থ`, `🌍 জানাশোনা`, `🎨 মজার খেলা`)—never duplicate numbers like `খেলা ১` + `১. মনের আনন্দ`.
   - Spoken voice scripts (`scripts/refresh_voices.py` & `content/`) must sound like a real Bengali son speaking warmly at home—never read out bloated number sequences (`1.1`, `১) ... ২)`, `ধাপ ১`) and never mention `"পার্ট ২"`.
   - In `💌 চিঠি`, `#slideBadge` sits cleanly in `.slide-top-header` above `.slide-img-wrap` (never overlaid on top of family photos).

---

## 3. CRITICAL RULE: Mandatory Persona/Blueprint Reference Set, Pure Agentic LLM Curation Gate & Explicit-Only TTS

1. **Mandatory Reference Files for Every Content Creation & Curation Run (`6-File Portable MD5 Contract`):**
   - Whenever any agent or script (`scripts/curate_loop.py --student <student_id>`) creates, edits, or evaluates curriculum games or downstream prompts, it **MUST read, cross-reference, and MD5-verify all 3 canonical input specifications**:
     1. [`students/ma_kalyani/persona.md`](students/ma_kalyani/persona.md) (`persona_md5` — or `students/<student_id>/persona.md` for any new student) — Single unified portable student persona containing learner profile, asthma/`25–26°C` & joint constraints, dietary exclusions, 11 clinical emotional/scarcity blockers, 4 subconscious procedures, 20-repetition dopamine neuroplasticity spiral, and banned stiff Bengali words (`দয়া করে`, `মস্তিষ্ক`, `সংকোচ`, `ভুল থেকে শিক্ষা`, `পার্ট ১`, `পার্ট ২`).
     2. [`content/curriculum.md`](content/curriculum.md) (`curriculum_md5`) — Master 51-day syllabus blueprint (`60%` Day-to-Day English / `30%` Fluent Hindi Gossip / `10%` Clear Bengali Mind-Expression, 3-pillar Gemini Live Tech Onboarding for Voice Therapy + Phone Control [`@YouTube Music`, `@Phone` Calling, `@Google Photos`] + `Live Streaming Video Camera 📹`, 1-in-2-days Covert CBT on Even Days, and Personal Psychotherapy on Odd Days).
     3. [`content/content_curation.md`](content/content_curation.md) (`content_curation_md5`) — The 12-Dimension Agentic Evaluator-Optimizer rubric and Critic -> Refiner rewrite rules (alongside workflow governance in [`docs/content-pipeline.md`](docs/content-pipeline.md)).
   - From these 3 input specifications, the Agentic Loop co-curates and MD5-tracks the **3 canonical output files**:
     4. [`content/days/part1_days.md`](content/days/part1_days.md) (`part1_days_md5`) — Days 1–21 Foundation Markdown content (loaded by `content/part1_days.py`).
     5. [`content/days/part2_days.md`](content/days/part2_days.md) (`part2_days_md5`) — Days 22–51 Extended Calendar Markdown content (loaded by `content/part2_days.py`).
     6. [`docs/client-side-gemini.md`](docs/client-side-gemini.md) (`client_gemini_md5`) — Downstream Android Gemini Master Prompt (English rules, strictly Bengali speech to Ma, mandatory persistent memory profiling, and master psychotherapist protocol).
2. **Pure Agentic LLM 12-Dimension Quality Gate (`scripts/curate_loop.py`):**
   - **Zero hardcoded regex/character-length rules** in `scripts/curate_loop.py`—quality evaluation and iterative rewriting (`Critic Agent -> Refiner Agent -> Re-Evaluate`) are driven purely by the LLM reading the 3 Markdown specifications above (`python3 scripts/curate_loop.py --live-loop`), storing the verified 6-file MD5 ledger in `content/curation_manifest.json`:
     1. **CBT Effectiveness & Subconscious Reprogramming** (Indirect Ericksonian metaphors, third-person stories, zero clinical/scolding words).
     2. **Personalization & Personal-Level Connect** (Ranaghat, Dum Dum, Koushik, Didi, Aishee, Ayush, Maa Sarada, Dakshineswar, Santiniketan).
     3. **Relationship Warmth & Ma–Koushik–Didi Empathy** (How Ma, Koushik, and Didi share the exact same sensitive heart and deep unspoken love).
     4. **Inspiration, Resilience & Pride** (Celebrating Ma's quiet sacrifice, teaching, and lifelong curiosity).
     5. **Charm, Playfulness & Fun** (*Adda* warmth, humor, nostalgic stories, playful puzzles).
     6. **Curiosity & Wonder** (Why/How science & GK wonders, deep song lyric meanings).
     7. **Engagement & Multi-Step Storytelling Depth** (4-layer elaboration: Nostalgic Hook -> Surprising Insight -> 1-Breath Prompt -> Follow-Up).
     8. **Ease of Learning & Spaced Dopamine Reinforcement** (Short 1-breath primary prompts + >=5x spaced repetition across the 8 core English words).
     9. **Zero Fear of Mistakes & Zero Shame for Not Knowing / Forgetting** (Explicit reassurance that nothing breaks on the phone, repeating 100 times is welcome, and forgetting is completely natural).
     10. **Urge to Express Her Own Mind & Preferences** (Inviting Ma to voice her own opinions, song/story interpretations, and likes/dislikes).
     11. **Freedom, Autonomy & High-Quality Living** (Choosing comfort, peace, generous self-care, and unhurried living).
     12. **Growing as Per Her Own Dreams** (Reigniting her personal dreams in painting/sketching, music, travel, and lifelong learning).
2. **Reusable Multi-Student Content Pipeline (`docs/content-pipeline.md`):**
   - Always follow the 5-stage pipeline for Ma (`students/ma_kalyani/`) or any future learner (`students/<student_id>/`):
     `1. Persona Spec` -> `2. Human-Readable Draft (curriculum_v2_draft.md) + 12-Dimension Quality Gate` -> `3. Koushik Reviews & Approves Content (ZERO TTS)` -> `4. Promote to content/ + Adjust UI` -> `5. Run refresh_voices.py --confirm + Build & Deploy`.
2. **On-Device Web Speech API (`speechSynthesis`) is Forbidden:** Always use pre-generated **Gemini `Aoede` (`gemini-v4s-tts`)** `.mp3` files under `audio/`.
3. **NEVER Auto-Regenerate Voices Before Content Approval:**
   - Always show new or updated curriculum content first and wait for Koushik's explicit approval before generating TTS.
   - During UI, CSS, JS, layout, or draft edits, run **only** `python3 scripts/build_app.py` (`< 0.5s`).
   - `build_app.py` checks `audio/tts_manifest.json` without calling TTS. If `N` files have updated text, finish your edit immediately and **ask/remind Koushik** before running `refresh_voices.py --confirm`.
4. **Explicit Incremental Refresh & Single-Commit `ma-audio` Publish (Only After Koushik Approves Content):**
   ```bash
   # Refresh stale/missing voices AND force-push 1-commit snapshot to `ma-audio` orphan branch:
   python3 /usr/local/google/home/koushikchak/kalyani-app/scripts/refresh_voices.py --confirm --scope all --publish
   ```

---

## 4. Build, Test & 3-Branch Deployment Architecture

```bash
# 1. Compile modular src/ + content/ -> index.html (<0.5s):
python3 /usr/local/google/home/koushikchak/kalyani-app/scripts/build_app.py

# 2. Run all modular architecture, persona & Node VM behavioral tests:
python3 /usr/local/google/home/koushikchak/kalyani-app/tests/run_tests.py

# 3. Publish audio/ snapshot to 1-commit `ma-audio` orphan branch (whenever MP3s changed):
python3 /usr/local/google/home/koushikchak/kalyani-app/scripts/sync_audio_branch.py
```

- **Public Git Remote (`git@github.com:kouSeek/portfolio.git`) — 3-Branch Topology:**
  1. **`ma-course` (Main App Branch):** Code, docs, curriculum, `audio/tts_manifest.json`, and single compiled `index.html` (`audio/**/*.mp3` gitignored so code commits stay tiny).
  2. **`ma-audio` (1-Commit Orphan Audio Branch):** Stores active `Aoede` `.mp3` assets (`raw.githubusercontent.com/kouSeek/portfolio/ma-audio/audio/...`) as a single-commit snapshot—zero historical MP3 bloat, zero Git LFS pointer/quota issues.
  3. **`kalyani-app-v0` (Backup & Fallback Branch):** Preserved v0 snapshot from commit `279e36f2d9851608444ffd34177dea174abda6d0` (`https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/kalyani-app-v0/index.html`).
- **Public Clickable Mobile Link (Never output `localhost` links):**
  https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/ma-course/index.html
- **Video Letter MP4 in `Kortex` Drive (linked inside `💌 চিঠি`, zero website HTML/MP3 artifacts in `Kortex`):**
  https://drive.google.com/file/d/1gzEnSqp72VlguNK0YirZHRARGmJFR-4g/view
