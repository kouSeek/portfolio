# 🌸 কল্যাণী (Kalyani) — Agentic Content Curation & LLM Improvement Rubric (`content_curation.md`)

This Markdown document governs the **Agentic LLM Evaluator-Optimizer Loop** (`scripts/curate_loop.py`). Instead of brittle hardcoded regexes or character counters, the **Critic Agent** and **Refiner Agent** read all **4 Canonical Input Reference Files**—[`students/ma_kalyani/persona.md`](../students/ma_kalyani/persona.md), [`docs/student-persona.md`](../docs/student-persona.md), [`curriculum.md`](curriculum.md), and this rubric (`content_curation.md`)—to evaluate, iteratively refine, and harmonize:
1. The Markdown curriculum content (`content/days/part1_days.md` & `content/days/part2_days.md`), and
2. The Client-Side Android Gemini Master Instruction (`docs/client-side-gemini.md`).

---

## 1. Agentic Evaluator-Optimizer Workflow (7-File MD5 Reference Contract)

```text
┌────────────────────────────────────┐
│  students/ma_kalyani/persona.md    │────┐
├────────────────────────────────────┤    │
│  docs/student-persona.md           │────┤
├────────────────────────────────────┤    ▼
│  content/curriculum.md             │───▶┌─────────────────────────────┐
├────────────────────────────────────┤    │   Agentic LLM Orchestrator  │
│  content/content_curation.md       │───▶│   (scripts/curate_loop.py)  │
└────────────────────────────────────┘    │                             │
                                          │  1. 7-File MD5 Detection    │
                                          │  2. LLM Critic Evaluation   │
                                          │  3. LLM Refiner Rewrite     │
                                          │  4. Re-Evaluate Until Pass  │
                                          └──────────────┬──────────────┘
                                                         │
                 ┌───────────────────────────────────────┴───────────────────────┐
                 ▼                                                               ▼
┌─────────────────────────────────────────┐                     ┌─────────────────────────────────────────┐
│  content/days/{part1,part2}_days.md     │                     │  docs/client-side-gemini.md             │
│  Loaded by part1_days.py & part2_days.py│                     │  English rules, Bengali speech output,  │
│  Rendered via Jinja2 -> index.html      │                     │  Persistent Memory & Psychotherapist AI │
└─────────────────────────────────────────┘                     └─────────────────────────────────────────┘
```

---

## 2. LLM Critic Evaluation Criteria (12 Holistic Quality Dimensions)

When evaluating any day or batch of days from `part1_days.md` / `part2_days.md`, and when verifying `docs/client-side-gemini.md`, the LLM Critic scores these **12 Pedagogical & Clinical Dimensions (`1–10`, minimum passing bar `9/10`)**:

1. **`cbt_effectiveness` — 1-in-2-Days Covert CBT Precision:**
   - Covert CBT stories (`pillar: covert_cbt`) appear strictly on alternate days (Even Days `2, 4, ..., 50`), never on consecutive days, using warm third-person storytelling rather than preachy lecturing.
2. **`personal_connect` — Deep Reminiscence & Cathartic Psychotherapy:**
   - Odd Days (`1, 3, ..., 51`) feature `pillar: personal_therapy`, gently guiding Ma to revisit golden Ranaghat/family memories and safely release buried grief, loneliness, or unspoken *abhiman* with warm closure.
3. **`relationship_warmth` — Family Attachment Healing:**
   - Reinforces unconditional warmth among Ma, Koushik, and Didi (`একই নরম মাটির মানুষ`), dissolving guilt and past misunderstandings.
4. **`inspiration_and_pride` — Relatable Inspiring Figures:**
   - Highlights relatable role models (Maa Sarada, Rani Rashmoni, Kadambini Ganguly, Subhasini Mistry, J.C. Bose, Sudha Murty, Nandalal Bose, Sister Nivedita, Satyajit Ray, Sunita Williams) that affirm age is never a barrier.
5. **`charm_and_fun` — Song Lyrics Curiosity via `@YouTube Music`:**
   - Every day explores an evocative song lyric (`pillar: music`), plays it hands-free via YouTube Music, and unpacks the poetic meaning and composer backstory.
6. **`curiosity_and_wonder` — Relatable Everyday World GK:**
   - Explains world wonders and science using warm household/kitchen analogies (`pillar: gk_inspiring`).
7. **`storytelling_depth` — Concrete Teaching Target per Game:**
   - Every single game (`4–6` per day) achieves a concrete skill, insight, or emotional shift—no empty filler cards—with a natural Turn-1 spoken prompt (`prompt_bn`) and Turn-2 deepening prompt (`followup_prompt_bn`).
8. **`ease_of_learning` — `60% / 30% / 10%` Language Balance:**
   - Maintains the **60% Day-to-Day Spoken English (`english`)**, **30% Fluent Hindi Gossip & Warm Chatting (`hindi`)**, and **10% Clear Bengali Self-Expression (`bengali_expr`)** balance across the curriculum, using effortless 1-breath phrases.
9. **`zero_fear_and_shame` — 3-Pillar Gemini Live Tech Onboarding & Spaced Repetition:**
   - Early onboarding (Days 1–3) + spaced repetition across all 51 days for: (a) Gemini Live voice therapy sessions, (b) Gemini phone control (`@YouTube Music`, calling people via `@Phone`, showing family/people photos from `@Google Photos`, alarms/utilities), and (c) **Gemini Live Video Camera (`📹`)** for random day-to-day visual questions.
10. **`urge_to_express_mind` — Authentic Voice & Agency:**
    - Invites Ma to share her own opinions, preferences, and feelings openly without passive hesitation.
11. **`freedom_and_autonomy` — Zero Physio & Effortless Pacing:**
    - Zero physical exercise/physiotherapy instructions; zero exam pressure or shaming.
12. **`growing_own_dreams` —Harmony with Client-Side Gemini & Persistent Memory:**
    - `docs/client-side-gemini.md` is written in clear English rules, mandates speaking to Ma strictly in Bengali, enforces proactive persistent memory storage of all biographical/emotional patterns, and mirrors every Kalyani pillar.

---

## 3. LLM Refiner Rewrite Protocol

Whenever the Critic Agent flags any weak game card or misalignment:
1. Preserve the day's overall slot structure and `pillar` assignment.
2. Rewrite `title_bn`, `detail_bn`, `prompt_bn`, and `followup_prompt_bn` in natural, affectionate West Bengal `চলিত বাংলা` (zero stiff translationese) so the game achieves a clear, memorable teaching or therapeutic outcome.
3. Re-submit the updated Markdown day to the Critic Agent until all 12 dimensions score `>= 9/10`.
