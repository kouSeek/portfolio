# 🌸 কল্যাণী (Kalyani App) — Technical Architecture & Artisanal UX Specification (`docs/spec.md`)

## 1. Product Vision
- **Learner:** Ma — Shikha Chakraborty (~64, Dumdum Cantonment; see [`student-persona.md`](student-persona.md)).
- **Companion Architecture:** Works hand-in-hand with the Android Gemini app on Ma's phone (configured via [`client-side-gemini.md`](client-side-gemini.md)).
- **Experience:** A calm, zero-shame, heirloom-quality Bengali mobile Progressive Web App combining:
  1. **`🎓 আজকের খেলা`:**
     - **Proactive Auto-Engage Welcome:** Automatically begins speaking today's warm welcoming day audio (`days/day_N.mp3`) on app open/load, chaining smoothly into the active incomplete game.
     - **Sequential Curiosity Locking & Zero Distracting Tickers:** No Part 1 / Part 2 switcher and no task-completion tickers. Days unlock strictly in sequence (`Day N` unlocks only when all 6 games of `Day 1 .. Day N-1` are ticked off `✅`).
     - **Auto-Unlocked Collapsible Calendar Grid (`Days 22–51`):** `Days 1–21` appear in the primary strip + optional `🗓️ ক্যালেন্ডার` grid; once `Days 1–21` are 100% completed, `Days 22–51` automatically appear in the days list as a comfortable collapsible calendar grid (`🌿 নতুন ৩০ দিনের ক্যালেন্ডার`).
     - **Single-Label `2×3` Game Grid:** Six clean buttons (`🧠 মনের আনন্দ`, `📱 হাতের যন্ত্র`, `🔤 ইংরেজি খেলা`, `🎵 গান ও অর্থ`, `🌍 জানাশোনা`, `🎨 মজার খেলা`) with zero duplicate numbers.
  2. **`💌 চিঠি`:** Random `☀️ আজকের অনুপ্রেরণা` inspiration card + `🎬 মায়ের জন্য ভিডিও চিঠি` card pointing to `Ma_Thanksgiving_Bengali_Video.mp4` (`https://drive.google.com/file/d/1gzEnSqp72VlguNK0YirZHRARGmJFR-4g/view`) + Koushik's 8-slide illustrated Thanksgiving & apology letter (with `.slide-top-header` badge cleanly above the photo, plus swipe + slide-dot navigation).

---

## 2. Layered Software Architecture

```text
content/ (Declarative Data) ──┐
                              ├──▶ scripts/build_app.py (<0.5s) ──▶ index.html
src/ (Template + CSS + JS)  ──┘           │
                                          ▼ (SHA-256 read-only check)
audio/{slides,quotes,days,games}/ + tts_manifest.json ◀── scripts/refresh_voices.py --confirm (Explicit Only)
```

- **Data Layer (`content/`):** `slides_and_quotes.py`, `part1_days.py`, `part2_days.py`.
- **Presentation Layer (`src/styles/`):**
  - `tokens.css` — *Shantiniketan Handloom Ivory & Shiuli* palette, `Noto Sans Bengali` + `Noto Serif Bengali` (prevents clipped `১` `U+09E7` glyphs on Android Skia), `AAA` ink contrast, 6 category color tokens.
  - `layout.css` — `42px` single-row sticky glass header, live `#nowPlayingBar` scrubbable progress ribbon, `#celebrationToast`.
  - `components.css` — Sequential lock chips, collapsible `.calendar-grid`, day hero card, `2×3` game navigator, voice-bubble prompt boxes, `@YouTube Music` helper card, letter album.
- **Interaction Layer (`src/js/`):** `state.js`, `audio.js`, `plan-view.js`, `letter-view.js`, `boot.js`.
- **Voice Layer (`audio/`):** `372` pre-generated `24kHz` mono `-16 LUFS` MP3s (`8` slides + `7` quotes + `51` days + `306` games) voiced by Gemini `Aoede` (`gemini-v4s-tts`) with zero bloated number readouts and zero `"পার্ট ২"` nagging.
