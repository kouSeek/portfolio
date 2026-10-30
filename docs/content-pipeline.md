# Reusable Multi-Student Content Pipeline & Dynamic Evolution Architecture (`content-pipeline.md`)

This specification modularizes **🌸 কল্যাণী (Kalyani)** so the exact same engine can onboard **any new learner** (Ma, another elder, a child, or a friend) cleanly—while enforcing a strict **Human Review Gate before TTS generation** and defining how the companion evolves dynamically over time.

---

## 1. End-to-End 5-Stage Multi-Student Pipeline

```text
┌──────────────────────────┐
│ 1. Persona Specification │  students/<student_id>/persona.md
│    (Needs, fears, joys,  │  • Cognitive blocks, CBT targets, physical limits,
│     tone, wave rhythm)   │    language register, cultural & musical anchors
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ 2. Curriculum Generation │  students/<student_id>/curriculum_v2_draft.md
│    (Human-readable .md)  │  • Variable daily waves (e.g. 3 → 4 → 3 → 5 games)
│                          │  • Full verbatim scripts + downstream AI prompts
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ 3. HUMAN REVIEW GATE 🛑  │  Koushik reviews tone, depth, stories & English words
│    (ZERO TTS ALLOWED)    │  • Fast iteration in plain Markdown (0s audio cost)
└────────────┬─────────────┘
             ▼  (Explicit "Approved" signal)
┌──────────────────────────┐
│ 4. App & Data Promotion  │  content/part1_days.py, part2_days.py + src/
│    (python3 build_app.py)│  • Adaptive 2/3-col grid renders 2–6 games/day cleanly
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ 5. TTS, Test & Deploy    │  python3 scripts/refresh_voices.py --confirm
│                          │  • Incremental SHA-256 Aoede MP3s + Node VM tests + Git push
└──────────────────────────┘
```

### Folder Convention for Multiple Students (`students/`)
Each learner lives in an isolated profile directory under `students/<student_id>/`:
- `students/ma_kalyani/persona.md` — Psychological profile, CBT targets, anti-cringe language rules, and wave ratios for **Ma (Shikha Chakraborty)**.
- `students/ma_kalyani/curriculum_v2_draft.md` — Review-stage curriculum draft inspected and approved **before** compiling into `content/` and running TTS.
- Future learners simply add `students/<new_student_id>/persona.md` + `curriculum_draft.md` without touching `src/` UI code.

---

## 2. Architecture for a Dynamically Evolving Companion ("Friend, Philosopher & Guide")

Koushik's vision is for Kalyani not to feel like a static school workbook, but a **personal assistant, friend, philosopher, and gentle CBT guide** that Ma naturally turns to for her daily thoughts, curiosity, and wellbeing.

Because `index.html` currently runs as a zero-login static PWA, dynamic evolution works across **two complementary layers**:

### Layer A — Live Today (Zero-Server Hybrid Architecture)
1. **Unpredictable Dopamine Waves in `🌸 কল্যাণী`:**
   - Instead of a predictable, repetitive 6-slot checklist every day, daily volume breathes organically:
     - **Days 1–3 (Gentle Ignition):** `3 → 4 → 3` light, zero-friction games so starting feels effortless.
     - **3-Day Rolling Waves Thereafter:** Alternates **Light & Casual Days (`3` games)**, **Balanced Story Days (`4` games)**, and **Deep Exploration Days (`5` games)**.
   - Every game carries its own custom badge (`ag.short_bn`) and color accent (`ag.accent`), so Ma never knows what delightful mix awaits when tomorrow unlocks.
2. **Living Memory & Adaptation in Downstream Android Gemini (`client-side-gemini.md`):**
   - Android Gemini's **Saved Info** acts as the stateful brain. Every prompt sent from `🌸 কল্যাণী` invites open-ended two-way conversation (life philosophy, CBT reframing of worries, song meanings, walk observations, recipes), and Gemini remembers Ma's answers across days—adapting its depth, vocabulary, and encouragement automatically.

### Layer B — Optional Next-Step Upgrade (Live Cloud Dynamic Card Generator)
When Ma becomes comfortable completing her first 2–3 weeks and we want the **web app itself** to generate brand-new daily cards tailored to her mood and recent interests:
1. **1-Tap Mood Check-In Chip (`আজ মন কেমন আছে?`):** Calm / Slightly Worried / Tired / Curious.
2. **Lightweight Serverless Bridge (Cloudflare Worker or Google Cloud Run Function):**
   - Calls `gemini-2.5-flash` with `students/ma_kalyani/persona.md` + her completed game tags + today's mood to synthesize **1 custom "Today's Personal Companion Card"** on the fly.
   - Calls Gemini TTS (`Aoede`) and caches the audio in Cloud Storage/KV so even dynamically generated daily cards speak in the exact same natural Bengali voice without exposing API keys in client HTML.

---

## 3. Continuous Content Curation & Improvement Loop (`curate -> audit -> elaborate -> approve -> promote`)

To ensure every game in **🌸 কল্যাণী** stays deeply engaging, zero-cringe, and aligned with the **20-Repetition Dopamine Neuroplasticity Rule** (`20` fun, rewarding exposures vs. `100+` days of boring repetition), content curation follows a repeatable 4-step improvement loop:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. OBSERVE & COLLECT SIGNALS                                            │
│    • Koushik's notes in Kortex dump / real-life observations of Ma      │
│    • Which games made Ma smile, laugh, or talk more vs. feel hesitant   │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. AUTOMATED QUALITY & NEUROPLASTICITY AUDIT (`scripts/curate_loop.py`) │
│    • Checks 20-Repetition Dopamine Coverage across the 8 English words, │
│      4 AI habits, and 6 CBT/Abundance/Family-Empathy reflexes           │
│    • Audits Game Elaboration Depth (4-layer arc: Nostalgic Hook ->      │
│      Surprising Insight -> 1-Breath Prompt [6-9 words] -> Follow-Up)    │
│    • Scans for banned stiff/cringe words or unwanted food triggers      │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. MARKDOWN DRAFT REFINEMENT (`students/ma_kalyani/curriculum_v2_draft`)│
│    • Enriches thin games into multi-step storytelling + song/GK depth   │
│    • Weaves family empathy (Ma, Koushik & Didi's shared sensitive heart)│
│    • STOP at Human Review Gate (0 TTS cost while iterating on text)     │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. PROMOTE & INCREMENTAL VOICE BUILD (After Koushik's Approval)         │
│    • Compile into `content/part1_days.py` & `part2_days.py`             │
│    • Run `python3 scripts/build_app.py` + `scripts/refresh_voices.py`   │
│      (regenerates ONLY changed SHA-256 audio hashes) + `run_tests.py`   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Mandatory 12-Dimension Content Quality Gate (`scripts/curate_loop.py`)
Every time content curation happens (and automatically on every `scripts/build_app.py` and `tests/run_tests.py` invocation), `scripts/curate_loop.py` enforces all **12 Pedagogical, Emotional & Empowerment Quality Gates**:
1. **CBT Effectiveness & Subconscious Reprogramming** (`>= 18` touches) — Indirect Ericksonian metaphors, third-person stories, zero clinical/preachy terms.
2. **Personalization & Personal-Level Connect** (`>= 12` touches) — Anchored in Ma's real life (Ranaghat, Dum Dum, Koushik, Didi, Aishee, Ayush, Maa Sarada, Dakshineswar, Santiniketan).
3. **Relationship Warmth & Ma–Koushik–Didi Empathy** (`>= 6` touches) — Deep emotional warmth showing how Ma, Koushik, and Didi share the same sensitive heart.
4. **Inspiration, Resilience & Pride** (`>= 10` touches) — Honoring Ma's strength, quiet sacrifice, and lifelong wisdom.
5. **Charm, Playfulness & Fun** (`>= 15` touches) — Lighthearted *adda*, humor, riddles, and storytelling joy.
6. **Curiosity & Wonder** (`>= 18` touches) — Fascinating *Why/How* world/science facts and deep song lyric meanings.
7. **Engagement & Multi-Step Storytelling Depth** (`>= 20` touches + `>= 45` 2-turn games in Part 1) — Rich 2-turn conversations rather than flat one-off commands.
8. **Ease of Learning & Spaced Dopamine Reinforcement** (`>= 15` touches + `>= 5` exposures per English word) — Effortless 1-breath primary prompts (`6–9` words) and spaced repetition.
9. **Zero Fear of Mistakes & Zero Shame for Not Knowing / Forgetting** (`>= 10` touches) — Explicit psychological safety: touching the phone never breaks anything, and asking 100 times or forgetting is welcomed with warmth.
10. **Urge to Express Her Own Mind & Preferences** (`>= 10` touches) — Encouraging Ma to share her own perspective, interpretation, and choices.
11. **Freedom, Autonomy & High-Quality Living** (`>= 12` touches) — Permission to live comfortably, peacefully, and generously for herself.
12. **Growing as Per Her Own Dreams** (`>= 10` touches) — Nurturing her personal creative dreams (painting/sketching, music, travel, and learning at 64).

### Every Game's 4-Layer Elaboration Standard
Whenever a game is created or upgraded in the improvement loop, it must contain all **4 layers of depth**:
1. **Nostalgic or Real-Life Hook (`স্মৃতি বা ঘরোয়া শুরু`):** Connects the activity to Ranaghat, Dum Dum, Maa Sarada, Santiniketan, favorite Bengali songs, or how Ma, Koushik, and Didi share the same warm heart.
2. **Playful Discovery / Subconscious Reframe (`মজার নতুন ভাবনা`):** An Ericksonian metaphor, fun science/GK secret, or zero-fear tech insight that sparks a smile (`dopamine + BDNF`).
3. **1-Breath Primary Voice Turn (`🎙️ এক নিঃশ্বাসে ১ম কথা — 6–9 Words`):** Effortless for a 64yo working memory to hold and speak aloud in one breath.
4. **2-Way Follow-Up Curiosity Turn (`💬 উত্তরের পর ২য় কথা`):** Turns a one-off command into a real two-way conversation with Gemini (`Friend, Philosopher & Guide`).
