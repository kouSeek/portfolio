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
