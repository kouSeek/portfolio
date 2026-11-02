# GEMINI.md — ✨ AI Companion (`kalyani` + `anondo`) Master Architecture, UX Artistry & Governance

This file is the **single, canonical, Git-tracked source of truth** governing how any AI engineer/agent designs, architects, tests, and maintains **✨ AI Companion**, located in its dedicated repository at [`/usr/local/google/home/koushikchak/ai-companion`](file:///usr/local/google/home/koushikchak/ai-companion) (published on branch `ai-companion` of `git@github.com:kouSeek/portfolio.git`).

It hosts **two modular, self-contained companion personas**:
1. **`kalyani` (Ma — `🌸 কল্যাণী` -> `kalyani.html`):** 51-day Bengali companion (`306` games) for Ma (Shikha Chakraborty).
2. **`anondo` (Me — `⚡ ANONDO` -> `anondo.html`):** 21-day English high-IQ companion (`105` explorations) for Koushik Chakraborty.

> **Strict Isolation from `koushik-wiki`:** Keep all AI Companion rules, specs, persona packages, frontend source, audio, scripts, and tests strictly inside `/usr/local/google/home/koushikchak/ai-companion`.

---

## 1. Principal Software Architecture Mandate (Modular Two-Persona Separation)

Every persona (`kalyani`, `anondo`, and any future persona) is organized symmetrically across **Persona Specs (`personas/<id>/`)**, **Thin Loaders (`content/<id>/`)**, **Modular Frontend (`src/<id>/` + `src/templates/`)**, **Structured Media (`assets/<id>/`, `audio/<id>/`)**, **Unified Build/TTS Tooling (`scripts/`)**, and **Verification (`tests/`)**.

- **Zero Monoliths Rule:**
  - **NEVER** inline raw CSS, HTML, or JavaScript application logic inside Python scripts (`scripts/build_app.py` is strictly a fast `< 220`-line Jinja2 assembler).
  - **NEVER** hardcode curriculum dicts inside Python loaders (`content/<id>/*.py` are thin loaders reading `personas/<id>/days/*.md`).
  - **NEVER** dump flat untracked `.mp3` files into `audio/`; keep voices organized per persona in `audio/<persona>/{slides,quotes,pillars,days,games}/`.

### Canonical Repository Topology

```text
/usr/local/google/home/koushikchak/ai-companion/
├── GEMINI.md                                  # Master Governance: Modular 2-Persona Architecture & No-Auto-TTS Rule
├── .gemini/config/rules/
│   └── ai_companion_rules.md                  # Workspace-local agent rule synced with GEMINI.md
├── docs/                                      # Shared Technical & Pipeline Specifications
│   ├── spec.md                                # Mobile UX, Audio & PWA Architecture
│   └── content-pipeline.md                    # Reusable 5-stage Multi-Persona Pipeline Blueprint
├── personas/                                  # Self-Contained Modular Persona Packages
│   ├── kalyani/                               # Ma (`kalyani`) — Bengali Companion
│   │   ├── persona.md                         # Unified student persona, clinical blockers & tone
│   │   ├── curriculum.md                      # 51-day syllabus, 60/30/10 language split & 3-pillar Gemini Live tech
│   │   ├── content_curation.md                # 12-Dimension Agentic Evaluator-Optimizer rubric
│   │   ├── client-side-gemini.md              # Android Gemini Master Prompt (English rules, strictly Bangla speech)
│   │   ├── curation_manifest.json             # 6-file MD5 state ledger + live Gemini LLM Critic evaluation
│   │   └── days/
│   │       ├── part1_days.md                  # Days 1–21 Foundation Markdown (126 games)
│   │       └── part2_days.md                  # Days 22–51 Extended Calendar Markdown (180 games)
│   └── anondo/                                # Me (`anondo`) — Koushik's English Companion
│       ├── persona.md                         # Wiki-grounded 2e-ADHD/High-IQ persona & 10 Covert CBT targets
│       ├── curriculum.md                      # 21-day English syllabus (1-in-2-days CBT, Active Listening, Song Bhaavna, Frontier GK)
│       ├── content_curation.md                # 12-Dimension Agentic Evaluator-Optimizer rubric
│       ├── client-side-gemini.md              # Gemini Live sparring partner Master Prompt
│       ├── curation_manifest.json             # 5-file MD5 state ledger + live Gemini LLM Critic evaluation
│       └── days/
│           └── anondo_days.md                 # Days 1–21 English Markdown (105 unique explorations)
├── content/                                   # Thin Python Loaders & Shared Markdown Parser
│   ├── __init__.py                            # Re-exports kalyani & anondo declarative data
│   ├── markdown_loader.py                     # Structured Markdown parser/serializer
│   ├── kalyani/
│   │   ├── __init__.py
│   │   ├── slides_and_quotes.py               # 8 Thanksgiving letter slides + 7 morning quotes + 6 slot labels
│   │   ├── part1_days.py                      # Thin loader -> personas/kalyani/days/part1_days.md
│   │   └── part2_days.py                      # Thin loader -> personas/kalyani/days/part2_days.md
│   └── anondo/
│       ├── __init__.py
│       └── anondo_days.py                     # Thin loader -> personas/anondo/days/anondo_days.md + Slides/Quotes/7 Keys
├── src/                                       # Modular Frontend Source Layer
│   ├── templates/
│   │   ├── index.html.j2                      # Two-Persona AI Companion Hub shell
│   │   ├── kalyani.html.j2                    # Ma's 🌸 কল্যাণী Jinja2 shell
│   │   └── anondo.html.j2                     # Koushik's ⚡ ANONDO Jinja2 shell
│   ├── kalyani/
│   │   ├── styles/{tokens,layout,components}.css
│   │   └── js/{state,audio,plan-view,letter-view,boot}.js
│   └── anondo/
│       ├── styles/{tokens,components}.css
│       └── js/{audio,views}.js
├── assets/
│   ├── icons/favicon.svg
│   ├── kalyani/slides/slide_1..8.jpg          # Family photographs for Ma's letter
│   └── anondo/slides/slide_1..8.jpg           # Personalized illustrations for Koushik's letter
├── audio/                                     # Per-Persona Aoede Cache -> published to `ai-companion-audio` orphan branch
│   ├── kalyani/
│   │   ├── tts_manifest.json                  # SHA-256 text-hash registry (372 Bengali voices)
│   │   └── {slides,quotes,days,games}/*.mp3
│   └── anondo/
│       ├── tts_manifest.json                  # SHA-256 text-hash registry (148 English voices)
│       └── {slides,quotes,pillars,days,games}/*.mp3
├── scripts/
│   ├── build_app.py                           # <0.5s multi-persona Jinja2 compiler (`--persona {all,kalyani,anondo}`)
│   ├── curate_loop.py                         # Multi-persona (`--persona {all,kalyani,anondo}`) 12-Dimension LLM Gate
│   ├── refresh_voices.py                      # Explicit-only (`--persona {kalyani,anondo} --confirm`) Aoede TTS generator
│   └── sync_audio_branch.py                   # Publishes `audio/` snapshot to 1-commit `ai-companion-audio` branch
├── tests/
│   ├── run_tests.py
│   ├── test_architecture_and_docs.py
│   ├── test_curriculum_persona.py
│   └── test_ui_and_vm_behavior.py
├── favicon.svg
├── kalyani-manifest.json
├── kalyani-sw.js
├── index.html                                 # Compiled Two-Persona Hub (`🌸 Kalyani` & `⚡ Anondo`)
├── kalyani.html                               # Compiled Ma's Companion App (`🌸 কল্যাণী`)
└── anondo.html                                # Compiled Koushik's Companion App (`⚡ ANONDO`)
```

---

## 2. Genius Artist UX Design System

- **Persona `kalyani` (`kalyani.html` — *"Shantiniketan Handloom Ivory & Shiuli"*):**
  - Unclipped `Noto Sans Bengali` + `Noto Serif Bengali` typography (`line-height >= 1.48–1.6`, zero `Hind Siliguri`, zero `tabular-nums`), zero task-completion tickers or `"পার্ট ১"`/`"পার্ট ২"` labels, sequential day locking (`🔒 দিন N`), auto-unlocked collapsible calendar grid for `Days 22–51`, `#slideBadge` above photos, `#videoLetterCard` at the bottom of `💌 চিঠি`, and proactive auto-engage `Aoede` voice.
- **Persona `anondo` (`anondo.html` — *High-IQ Clarity, Active Listening & Zorba Flow*):**
  - Clean `Inter` + `Playfair Display` palette, non-judgmental freely accessible 21-day strip (*"As the day, so is the day"*), 2-turn Gemini Live conversational prompts (`Turn 1` + `Turn 2`), `@YouTube Music` `3-Pass Meaning-First` listening cards, 8-slide illustrated Letter, 7 Diagnostic Keys, and 60-Second Hardware Calm Switch modal.

---

## 3. CRITICAL RULE: Portable Persona Reference Contract, Pure Agentic LLM Gate & Explicit-Only TTS

1. **Mandatory Reference Files per Persona (`personas/<persona_id>/`):**
   - Every content creation or curation run (`python3 scripts/curate_loop.py --persona <kalyani|anondo> --live-loop`) **MUST read and MD5-verify**:
     1. [`personas/kalyani/persona.md`](personas/kalyani/persona.md) / [`personas/anondo/persona.md`](personas/anondo/persona.md)
     2. [`personas/kalyani/curriculum.md`](personas/kalyani/curriculum.md) / [`personas/anondo/curriculum.md`](personas/anondo/curriculum.md)
     3. [`personas/kalyani/content_curation.md`](personas/kalyani/content_curation.md) / [`personas/anondo/content_curation.md`](personas/anondo/content_curation.md)
   - Co-curating and MD5-tracking:
     4. [`personas/kalyani/days/part1_days.md`](personas/kalyani/days/part1_days.md) & [`personas/kalyani/days/part2_days.md`](personas/kalyani/days/part2_days.md) (or [`personas/anondo/days/anondo_days.md`](personas/anondo/days/anondo_days.md))
     5. [`personas/kalyani/client-side-gemini.md`](personas/kalyani/client-side-gemini.md) (or [`personas/anondo/client-side-gemini.md`](personas/anondo/client-side-gemini.md))
2. **On-Device Web Speech API (`speechSynthesis`) is Forbidden:** Always use pre-generated **Gemini `Aoede` (`gemini-v4s-tts`)** `.mp3` files under `audio/<persona>/`.
3. **NEVER Auto-Regenerate Voices Before Content Approval:**
   - During UI, CSS, JS, or curriculum edits, run **only** `python3 scripts/build_app.py` (`< 0.5s`).
   - Only run `python3 scripts/refresh_voices.py --persona <kalyani|anondo> --confirm --publish` after Koushik explicitly approves.

---

## 4. Build, Test & 3-Branch Deployment Architecture

```bash
# 1. Compile kalyani.html, anondo.html, and index.html (<0.5s):
python3 /usr/local/google/home/koushikchak/ai-companion/scripts/build_app.py

# 2. Run all modular architecture, persona & Node VM behavioral tests:
python3 /usr/local/google/home/koushikchak/ai-companion/tests/run_tests.py

# 3. Publish audio/ snapshot to 1-commit `ai-companion-audio` orphan branch:
python3 /usr/local/google/home/koushikchak/ai-companion/scripts/sync_audio_branch.py
```

- **Public Git Remote (`git@github.com:kouSeek/portfolio.git`) — Branch Topology:**
  1. **`ai-companion` (Main App Branch):** Code, docs, modular `personas/{kalyani,anondo}/`, `audio/{kalyani,anondo}/tts_manifest.json`, and compiled `index.html`, `kalyani.html`, `anondo.html`.
  2. **`ai-companion-audio` (1-Commit Orphan Audio Branch):** Stores active `Aoede` `.mp3` assets (`raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/audio/{kalyani,anondo}/...`).
  3. **`kalyani-app-v0` (Preserved v0 Fallback Branch):** Untouched historical snapshot.
- **Public Clickable Links (Never output `localhost` links):**
  - Persona Hub: https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/ai-companion/index.html
  - Ma (`kalyani`): https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/ai-companion/kalyani.html
  - Me (`anondo`): https://htmlpreview.github.io/?https://github.com/kouSeek/portfolio/blob/ai-companion/anondo.html
