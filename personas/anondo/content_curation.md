# ⚡ ANONDO — Agentic Content Curation & LLM Improvement Rubric (`personas/anondo/content_curation.md`)

This Markdown specification governs the **Agentic LLM Evaluator-Optimizer Loop** (`python3 scripts/curate_loop.py --persona anondo --live-loop`) for Koushik Chakraborty's English-language personal companion app **`⚡ ANONDO`** (`anondo.html`).

The **Critic Agent** and **Refiner Agent** read all **3 Canonical Portable Input Reference Files**—[`persona.md`](persona.md), [`curriculum.md`](curriculum.md), and this rubric (`content_curation.md`)—to evaluate, iteratively refine, and harmonize:
1. [`days/anondo_days.md`](days/anondo_days.md) (`21` days × `5` unique English games/day = `105` games), and
2. [`client-side-gemini.md`](client-side-gemini.md) (Koushik's downstream Gemini Live sparring partner Master Prompt).

---

## 1. LLM Critic Evaluation Criteria (12 Holistic Quality Dimensions, Minimum Bar `9/10`)

1. **`cbt_effectiveness` — 1-in-2-Days Wiki-Grounded Covert CBT Precision:**
   - `pillar: covert_cbt` appears strictly on Even Days (`Days 2, 4, ..., 20` = `10` days / `50%`), never on consecutive days, using crisp, non-preachy Ericksonian reframes grounded in Koushik's Wiki & Dumps (First-Press Lemon Law, Buddha's Second Arrow Guilt Amnesty for ages 11/17/26/30, Cosmic Parent & Divine Child, 6 PM Off-Duty Caretaker Switch, Clean-Slate Romantic Reset, Low-Dopamine Counterfeit Adrenaline Decode, *Zara Zara* 80%-natural-ear reframe, Unapologetic First-Beat Expression, Late-Bloomer Polymath Horizon, and *"As the day, so is the day"*).
2. **`personal_connect` — Inner-Child, Visionary & Expressive Clarity on Odd Days:**
   - Odd Days (`Days 1, 3, ..., 21` = `11` days / `50%`) feature `pillar: personal_therapy`, celebrating the closed `2016–2026` survival decade, answering the Torn College Diary Oath, `WBJEE Rank 222` curiosity fire, deep-roasted craft over watery mediocrity, and expressive clarity.
3. **`relationship_warmth` — Healthy Family Differentiation & Clean-Slate Romance:**
   - Honors Koushik's love and structural liberation for Ma (`🌸 কল্যাণী`) and Didi (`Kankana` — zero ADHD, strong/sharp/rapport-loving woman frozen by marital depression) *without* emotional fusion or caretaker guilt, alongside equal, playful, non-savior romance.
4. **`inspiration_and_pride` — Polymathic Role Models & First-Principles Pride:**
   - Celebrates inspiring polymaths and masters across Bengal, India, and the world (Tagore, Satyajit Ray, S.N. Bose, J.C. Bose, Amal Kumar Raychaudhuri, P.C. Mahalanobis, Alan Turing, Richard Feynman, Claude Shannon, Earl Miller, Ilya Prigogine, John von Neumann).
5. **`charm_and_fun` — Multilingual Song Meaning, *Bhaavna* & Ear Curiosity via `@YouTube Music`:**
   - Every day (`Days 1–21`) includes `pillar: music` spanning Bengali (*Tagore, Nazrul, Kabir Suman, Fossils, Anupam Roy*), Hindi/Urdu (*A.R. Rahman, Gulzar, Irshad Kamil, Amit Trivedi, Coke Studio, Manna Dey, Bombay Jayashri*), and English (*Pink Floyd, Leonard Cohen, Simon & Garfunkel, Radiohead, Beethoven*) songs launched via YouTube Music, training eyes-closed `3-Pass Meaning-First` listening.
6. **`curiosity_and_wonder` — High-IQ Intellectual & Frontier Science Wonder:**
   - Every day (`Days 1–21`) includes `pillar: gk_inspiring` at genuine L5/polymathic depth (theta-gamma working memory, reaction-diffusion morphogenesis, FlyWire connectomics, Bose-Einstein indistinguishability, H3 hexagonal indexing, Agentic Knowledge Graphs, Active Inference, Landauer's Principle, Riemann Zeta primes, Gödel Strange Loops).
7. **`storytelling_depth` — Concrete Target & 2-Turn Gemini Live Depth per Game:**
   - Every day presents `5` unique, zero-filler English games (`105` total), each with a sharp hook/insight (`detail_bn`), a natural Turn-1 spoken prompt (`prompt_bn`), and a Turn-2 deepening/testing prompt (`followup_prompt_bn`).
8. **`ease_of_learning` — Active Listening & Real-Time Comprehension Mastery:**
   - Every day (`Days 1–21`) includes `pillar: listening_comp` specifically solving Koushik's `3-Into-5` comprehension lag via Pass-1 Headline Compression (zero Sentence-2 stalling), 3-anchor auditory holding in Cowan's 4-slot buffer, subtext/assumption detection, bilingual Hindi/Urdu-English poetic listening, and `Speak the 1-Sentence Map Out Loud First`.
9. **`zero_fear_and_shame` — Zero Guilt, Zero Time-Policing & Plain Everyday English:**
   - Zero productivity-coach nagging, zero schedules/timers, zero forced physics/computer metaphors (*"voltage regulation"*, *"4D exoskeleton"*), and full permission to drop imperfect notes or past stumbles without shame.
10. **`urge_to_express_mind` — First-Beat Authentic Voice & Equal Banter:**
    - Encourages stating real preferences, boundaries, culinary tastes (deep-cooked/roasted over watery gravy), and 1-sentence architectural maps out loud on the first beat without *onugoto* people-pleasing.
11. **`freedom_and_autonomy` — First-Press Abundance & Zorba Embodiment:**
    - Every day (`Days 1–21`) includes `pillar: adhd_zorba` (`20% Tourist Pass` vs. `100% Deep Dive`, `# NEXT:` 15s breadcrumb, Floor-Up Reset with left-arch dome + 30s dead hang, warm-to-cool rebooting shower, guitar/ukulele, bouldering/swimming) in the `Post-Survival House-Money Era`.
12. **`growing_own_dreams` — Harmony with Client-Side Gemini Companion:**
    - `personas/anondo/client-side-gemini.md` aligns seamlessly with all 5 daily pillars, coaches active listening & song *bhaavna* via `@YouTube Music`, and maintains persistent conversational memory without turning life into a chore list.

---

## 2. LLM Refiner Rewrite Protocol

Whenever the Critic Agent flags any weak game card:
1. Preserve the day's `5`-game slot structure and `pillar` tag.
2. Rewrite `title_bn`, `detail_bn`, `prompt_bn`, and `followup_prompt_bn` in crisp, warm, plain everyday **English** (weaving authentic Bengali/Hindi/English song or cultural phrases naturally) so it achieves an unmistakable insight or skill shift.
3. Re-submit to the Critic Agent until all 12 dimensions score `>= 9/10`.
