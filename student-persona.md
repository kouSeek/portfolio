# Student Persona & Curriculum Design Specification (`student-persona.md`)

This document is the canonical psychological, pedagogical, and content-distribution blueprint for the learner (**Ma — Shikha Chakraborty**) in the **Kalyani (`🌸 কল্যাণী`)** app. Every game, instruction, story, and prompt in `scripts/curriculum_data.py` and `scripts/build_app.py` must strictly follow this specification.

---

## 1. Learner Profile & Life Context

- **Name & Age:** Shikha Chakraborty ("Ma"), ~64 years old.
- **Roots & Home:** Grew up and raised her children in Ranaghat; currently lives in Dumdum Cantonment, Kolkata (right next to Koushik's sanctuary flat).
- **Family Anchors:**
  - Deeply proud of her son **Koushik** (AI Engineer at Google) and daughter **Kankana (Didi)**; lovingly cares for **Aishee** and little **Ayush**.
  - Lost her husband (**Baba**) suddenly in 2016, who previously sheltered her from external administrative and technical complexities.
- **Physical Context:** Has asthma/cold sensitivity (AC at `26°C` is safest, never freezing `18°C`) and chronic pain in her knees, feet, and waist (activities must be physically gentle and doable while seated comfortably).
- **Cognitive & Emotional Traits:**
  - Innocent, affectionate, sincere, and attentive like the diligent Ranaghat schoolgirl she once was.
  - Shares Koushik's sensitive, anxious/ADHD-like tendency toward cognitive overwhelm when hurried, pressured, or handed multi-step technical jargon.
  - **High Sensitivity to Direct Criticism (`অভিমান`):** If a lesson points out her real-life habits as "mistakes" or makes her feel judged, scolded, or exposed, she feels hurt (`অভিমান`), loses confidence, and withdraws from learning.

---

## 2. Personal Tastes, Joys & Positive Anchors

Use these authentic personal anchors organically across lessons so the app feels warm, familiar, and joyful:
- **Music:** Golden-era Bengali songs (Hemanta Mukherjee, Sandhya Mukherjee, Manna Dey, Lata Mangeshkar), Rabindra Sangeet, devotional songs, and her Carvaan / YouTube Music.
- **Spiritual Calm:** Lighting incense (`ধূপকাঠি`) in her quiet puja corner, stories of **Maa Sarada**, **Sri Ramakrishna**, **Rani Rashmoni**, Dakshineswar, and Belur Math.
- **Creative Play:** Drawing and shading flowers, birds, rural scenery, and alpana in her notebook with pencils/colors.
- **Food Preferences:** Loves tasty, flavorful Bengali snacks, fruits, sweets, and good Zomato treats. **Strongly dislikes bland soya bean (`সয়াবিন`) and mushroom (`মাশরুম`)**—never recommend those positively.
- **Nature & Travel:** Birds, flowers, monsoon rain, Puri sea waves, Darjeeling hills, and peaceful morning sunshine.

---

## 3. Strict Ego-Safety & Indirect Learning Protocol

### Rule A — Zero Direct Mistake Callouts (`0%` Tolerance)
- **NEVER** write any game that says or implies Ma has done something wrong in real life (e.g., never mention *"তুমি ভালো ফল রেখে পচা ফল খাও"*, *"তুমি বারবার ফোন করো"*, *"তুমি কাপড় প্লাস্টিকের ব্যাগে রাখো"*, *"তুমি অন্যের কথা না শুনেই মাঝখানে বলো"*, or *"তুমি নাতি-নাতনিকে নিয়ে শুয়ে ঘুম না হওয়ার নালিশ করো"*).
- Never use labels like *"ভুল থেকে শিক্ষা"* (Learning from Mistakes) or *"বদভ্যাস পরিবর্তন"* (Changing Bad Habits).

### Rule B — The "Wise Advisor" Third-Person Story Method
Whenever a reasoning principle or life habit is taught, **hide it inside a completely different, playful third-person scenario** (a flower-seller puzzle, a sweet-shop story, a detective mystery, a temple-kitchen arrangement game, or a music analogy) where **Ma is cast as the smart advisor giving counsel to someone else**:
- *Instead of pointing out eating bruised fruit first:* Present a fun riddle about a flower-seller (`ফুলওয়ালা`) who keeps freshhibiscus flowers locked away every day and only strings yesterday's wilted ones—ask Ma to tell Gemini what funny thing happens to the fresh flowers!
- *Instead of pointing out losing items in plastic bags:* Ask Gemini how a smart spice-shop or temple puja room arranges daily items on an open tray so anything can be found in 2 seconds!
- *Instead of pointing out interrupting mid-sentence:* Share a fascinating musical secret about why Hemanta Mukherjee or classical singers listen to the entire instrumental pause before singing the first note.
- *Instead of pointing out ticket/travel panic:* Tell a cozy travel story about how WhatsApp's ★ Starred Message acts like a magic iron locker in a purse so a train ticket never gets lost.

### Rule C — Keep Behavioral-Nudge Volume Low (`<= 5%` of All Games)
- Indirect behavioral/wisdom story puzzles must appear **at most once every 3–4 days** (`~5–6` times across all `126` games in Part 1, i.e., **< 5% of total games**).
- The remaining **95%+ of games** must focus purely on joyful skill-building, phone/appliance mastery, English confidence, YouTube Music & song appreciation, general knowledge, curiosity, sketching, and everyday AI fun.

---

## 4. Daily Cognitive Load & The 6-Game Sweet Spot

### Why 6 Games Per Day
- `10` games per day creates scroll fatigue and decision overwhelm.
- **Strictly `6` cohesive games per day** (`খেলা ১` to `খেলা ৬`, rendered in a compact `2×3` tile grid) is the sweet spot: completable in `12–15` relaxed minutes while covering 100% of curriculum goals (`21 × 6 = 126` games in Part 1; `30 × 6 = 180` games in Part 2).

### Daily 6-Game Distribution & Clubbing Architecture

| Slot | Tile Label | Category Name (Natural Bangla) | Share | Purpose & Natural Clubbing Strategy |
| :--- | :--- | :--- | :---: | :--- |
| **খেলা ১** | `🧠 ১. মনের আনন্দ` | `🧠 ১. মনের আনন্দ ও নিজের ওপর ভরসা` | `16.7%` | Warm self-belief, calm joy, Maa Sarada / Rabindranath inspiration, overcoming hesitation with tech. |
| **খেলা ২** | `📱 ২. হাতের যন্ত্র` | `📱 ২. ফোন, এসি ও টিভি রিমোট হাতের মুঠোয়` | `16.7%` | 1 practical appliance or phone skill per day (Volume, AC `26°C`, TV Input, WhatsApp voice/photo, Torch, Camera, Scam safety). |
| **খেলা ৩** | `🔤 ৩. ইংরেজি খেলা` | `🔤 ৩. ইংরেজি শব্দ চেনা ও মুখে বলা` | `16.7%` | **Clubbed seamlessly:** Learn `2–3` practical uppercase English words AND speak `1` short, happy English sentence out loud to Gemini in a single natural flow. |
| **খেলা ৪** | `🎵 ৪. গান ও অর্থ` | `🎵 ৪. ইউটিউব মিউজিকে গান চালানো ও কথাগুলো বোঝা` | `16.7%` | **Clubbed seamlessly:** Command Android Gemini in Bengali to play today's song on **YouTube Music** (`“জেমিনি, ইউটিউব মিউজিকে ‘...’ গানটা চালিয়ে দাও।”`), listen mindfully, and ask Gemini about the song's deep meaning/story. |
| **খেলা ৫** | `🌍 ৫. জানাশোনা ও কেন?` | `🌍 ৫. দেশ-দুনিয়ার খবর ও ‘কেন-কীভাবে’ কৌতূহল` | `16.7%` | **Clubbed seamlessly:** Positive GK / history / science story paired with asking *"Why / How"* (`কেন ও কীভাবে`) so Ma builds active critical curiosity instead of accepting things at face value. |
| **খেলা ৬** | `🎨 ৬. মজার খেলা` | `🎨 ৬. রোজকার কাজে এআই, শখ ও মজার চ্যালেঞ্জ` | `16.7%` | Everyday personal AI help (recipes, pencil sketching ideas, health comfort, puja prep) + playful comfort-zone mini-challenges (and on `<= 1 in 4` days, a fun third-person wisdom riddle). |

---

## 5. Native Bengali Language Style Guide

1. **Everyday Spoken West Bengal Bangla (*চলিত বাংলা*):** Write exactly how a loving Bengali son from Ranaghat/Kolkata speaks at home (`গানটা`, `কথাটা`, `বোতামটা`, `পাতাটা`, `একটু সহজ করে বলো তো`, `মাথাটা তাজা থাকে`).
2. **Banned Stiff / Translated Words:** Never use `দয়া করে` ("kindly/please"), `মস্তিষ্ক` (use `মাথা` or `মন`), `সংকোচ`, `বিস্তারিত নির্দেশ`, `স্বাবলম্বী চেষ্টা`, `আমাকে আদর করে বোঝাও`, or formal *apni* verbs (`করবেন`, `শিখবেন`) mixed with *tumi* (`তুমি`, `করো`, `বলো`).
3. **Direct Android Gemini Addressing:** Every voice prompt addresses **`জেমিনি`** (never `"কল্যাণী"`), matching the real Gemini app on Ma's Android phone.
