# ✨ ঝলক (Jhalak) — Content Guidelines & Extension Requirements

Canonical reference for curating, updating, or extending content and UX in **Ma's Jhalak (`✨ ঝলক` -> `jhalak.html`)** inside `/usr/local/google/home/koushikchak/ai-companion`.

---

## 1. Audience, Voice & Core Philosophy

- **Target Reader & Listener:** Ma (Shikha Chakraborty) — warm, affectionate, respectful everyday Kolkata Bengali (`মা`, `তুমি`).
- **Engagement Goal:** Every page must feel fun, cozy, immediately relatable, and effortless to stay glued to—never like a school lesson, textbook, or chore.
- **Zero Burden Rule:**
  - Never include Day numbers, week numbers, streaks, tests, or progression labels (`গত সপ্তাহে`, `দিন ২-এ`, `প্রথম সপ্তাহে`, etc.).
  - Never lecture, scold, or sound clinical. Keep life reflections gentle, playful, and reassuring.

---

## 2. Hard Exclusions (Never Include)

1. **Zero English Songs, English Movies, or English TV Series** anywhere in `Jhalak` (including `tv`, `curiosity`, or `english`).
2. **Zero Hindi Songs** (`songs_hi` is permanently removed).
3. **Zero Song Jukeboxes in `📺 টিভি` (`tv`)** — `tv` is strictly for shows, comedy, family films, cooking, devotional darshan, and audio stories.
4. **Zero Heavy / Unrelatable Knowledge:** Never add rocket telemetry, quantum physics, aerodynamics, deep history dates, or abstract technical concepts that Ma cannot relate to or use in her daily life.

---

## 3. Category-by-Category Content Requirements (`9` Categories)

All categories live in [`src/jhalak/js/curated-content.js`](../src/jhalak/js/curated-content.js) and [`src/jhalak/js/feed-engine.js`](../src/jhalak/js/feed-engine.js):

1. **`🎵 বাংলা গান` (`songs_bn`) — Evergreen Bengali Songs (Lyrics + Story + Meaning):**
   - **Mandatory Web Cross-Reference Rule:** NEVER write song lyrics, singer, lyricist, composer, or film name from memory. Always cross-reference every song via web search (`search_web`) to verify:
     1. Exact song title and verbatim Bengali lyrics.
     2. Exact singer, lyricist, composer, and film/year (or non-film status).
   - Choose popular, nostalgic, Ma-beloved classics (Hemanta, Sandhya, Manna Dey, Kishore Kumar, Lata Mangeshkar, Geeta Dutt, Pannalal Bhattacharya, Pratima Banerjee, Rabindra Sangeet, Ramprasad Sen, Rajanikanta Sen).
   - Required card structure:
     - `🎼 গানের আসল কথা ও নেপথ্যের ইতিহাস` (authentic lyrics + verified credits/context)
     - `🌺 গানের কথার অপূর্ব অর্থ ও ভাবার্থ` (warm, relatable meaning)
     - `curiosity_q_bn` / `curiosity_a_bn` grounded in real lines from the song
     - `yt_query` & `yt_label_bn`

2. **`🔤 ইংরেজি` (`english`) — Ultra-Simple Day-to-Day Words & Tiny Sentences:**
   - Teach **only** very simple, practical everyday words (`Good Morning`, `Thank You`, `Please`, `Sorry`, `Water`, `Tea`, `Fresh`, `Sweet`, `Hot/Cold`, `Open/Close`, `How much?`, `Doctor/Medicine`, `Left/Right/Straight`, `Slowly`, `Smile`, etc.).
   - Each card must include:
     - `🔤 সহজ ইংরেজি শব্দ ও বাংলা মানে`: 2–3 words with Bengali pronunciation + meaning.
     - `🗣️ মুখে বলার ছোট্ট ও সহজ বাক্য`: 2 tiny sentences (4–6 words each) with Bengali pronunciation + translation.
     - `🌟 রোজকার জীবনে মজার ব্যবহার`: 1 warm, relatable moment at home, on the phone, or at a shop where she can immediately use it.
   - No complex grammar terms, no long/abstract vocabulary.

3. **`🗣️ হিন্দি` (`hindi`) — Everyday Spoken Hindi:**
   - Practical, polite phrases Ma actually uses (auto/cab driver, delivery helper, vegetable/fruit vendor, neighbor didis, society/temple gatherings) with easy Bengali pronunciation.

4. **`🔍 কৌতূহল` (`curiosity`) — Fun Everyday Wonders:**
   - Relatable domestic, kitchen, nature, animal, and inspiring human stories Ma sees around her (why milk boils over, why onions make us cry, crows recognizing faces, lemon & tamarind shining brass, cats landing on their feet, pressure cookers, turmeric & neem, rainbows, Kolkata Ganga metro, inspiring Indian women).

5. **`🪷 ভগবান` (`gods`) — Joyful Devotional Stories:**
   - Heartwarming lila and bhakti stories (Maa Sarada, Thakur Sri Ramakrishna, Little Krishna, Sabari, Rukmini's tulsi leaf, Little Ganesha) emphasizing love, warmth, and inner peace without fear.

6. **`😂 হাসি` (`laugh`) — Clean, Joyful Comedy:**
   - Short, punchy belly-laugh stories (Gopal Bhar, Tenali Rama, Nasiruddin Hodja, Birbal, Bengali household humor) with a light smile-inducing takeaway.

7. **`🦋 শান্তি` (`calm`) — Gentle Nostalgia & Comfort:**
   - Warm memories (Ranaghat childhood, afternoon tea on the balcony, Durga Puja mornings) and gentle reframes encouraging her to enjoy fresh food, good sarees, and rest today.

8. **`📺 টিভি` (`tv`) — Bengali & Classic Indian TV / Cinema / Audio Stories:**
   - Non-song Bengali/Indian favorites (*Gopal Bhar* cartoons, *Uttam-Suchitra*, *Dadagiri*, *Feluda/Satyajit Ray*, *Bengali Rannaghar*, *Mahalaya*, *Ramayan & Mahabharat*, *Bhanu-Jahar-Rabi Ghosh*, *Puri Jagannath*, *Tarun Majumdar*, *Santiniketan*, *Bengali Shrutinatak*).

---

## 4. UX & Interaction Standards

- **Single-Tap Play / Pause:** Like Instagram, YouTube Shorts, and TikTok, **a single tap anywhere on the page content** (`handleJhContentSingleTap` in [`src/jhalak/js/player-ui.js`](../src/jhalak/js/player-ui.js)) immediately toggles Play / Pause with an ephemeral `🔊` / `⏸️` toast, while ignoring interactive buttons/links/text selection and de-duplicating `touchend` + synthetic `click`.
- **Minimalistic Screen Real Estate:** Keep 100% of the viewport for content; keep controls tucked cleanly inside the floating `⚙️` Settings drawer; keep the bottom cue clear (`👆 পাতার যেকোনো জায়গায় একবার ছুঁলেই ভয়েস চলবে/থামবে • 🧲 নিচ থেকে টানলে পরের পাতা`).

---

## 5. Extension & Verification Workflow

Whenever adding or editing Jhalak content:
1. Cross-reference all Bengali song lyrics and credits via web search (`search_web`).
2. Update [`src/jhalak/js/curated-content.js`](../src/jhalak/js/curated-content.js) and/or [`src/jhalak/js/feed-engine.js`](../src/jhalak/js/feed-engine.js).
3. Update counts and content assertions in [`tests/test_ui_and_vm_behavior.py`](../tests/test_ui_and_vm_behavior.py) and [`tests/test_karaoke_voice_sync_calibration.py`](../tests/test_karaoke_voice_sync_calibration.py).
4. Rebuild with `python3 scripts/build_app.py --persona jhalak` (never auto-run TTS without Koushik's explicit `--confirm` approval).
5. Run `python3 tests/run_tests.py` (all 7 test suites must pass).
6. Invoke `koushik-verifier` to audit `jhalak.html` before presenting changes.
7. Run `python3 scripts/refresh_voices.py --persona jhalak --confirm --publish` **only** after Koushik approves the new content.
