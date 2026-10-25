# 🌸 কল্যাণী (Kalyani App) — Technical Architecture & Artisanal UX Specification (`docs/spec.md`)

## 1. Product Vision
- **Learner:** Ma — Shikha Chakraborty (~64, Dumdum Cantonment; see [`student-persona.md`](student-persona.md)).
- **Companion Architecture:** Works hand-in-hand with the Android Gemini app on Ma's phone (configured via [`client-side-gemini.md`](client-side-gemini.md)).
- **Experience:** A calm, zero-shame, heirloom-quality Bengali mobile Progressive Web App combining:
  1. **`🎓 আজকের খেলা`:** Part 1 (`21` days × `6` games = `126` games) + Part 2 (`30` days × `6` games = `180` games) navigated via a tactile `2×3` category-accented grid.
  2. **`💌 চিঠি`:** Random `☀️ আজকের অনুপ্রেরণা` inspiration card + Koushik's 8-slide illustrated Thanksgiving & apology letter with swipe + slide-dot navigation.

---

## 2. Layered Software Architecture

```text
content/ (Declarative Data) ──┐
                              ├──▶ scripts/build_app.py (<0.5s) ──▶ index.html, ma-presentation.html & Drive HTML
src/ (Template + CSS + JS)  ──┘           │
                                          ▼ (SHA-256 read-only check)
audio/{slides,quotes,days,games}/ + tts_manifest.json ◀── scripts/refresh_voices.py --confirm (Explicit Only)
```

- **Data Layer (`content/`):** `slides_and_quotes.py`, `part1_days.py`, `part2_days.py`.
- **Presentation Layer (`src/styles/`):**
  - `tokens.css` — *Shantiniketan Handloom Ivory & Shiuli* palette, `AAA` ink contrast, 6 category color tokens.
  - `layout.css` — `42px` single-row sticky glass header, live `#nowPlayingBar` scrubbable progress ribbon, `#celebrationToast`.
  - `components.css` — Day hero card, `2×3` game navigator, voice-bubble prompt boxes, `@YouTube Music` helper card, letter album.
- **Interaction Layer (`src/js/`):** `state.js`, `audio.js`, `plan-view.js`, `letter-view.js`, `boot.js`.
- **Voice Layer (`audio/`):** `372` pre-generated `24kHz` mono `-16 LUFS` MP3s (`8` slides + `7` quotes + `51` days + `306` games) voiced by Gemini `Aoede` (`gemini-v4s-tts`).
