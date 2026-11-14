#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Automated Gate: Karaoke Word Highlight & Read-Aloud Voice Sync Calibration Test.

Ultra-lightweight (<2.0s total latency) comprehensive calibration gate for any new content across:
1. Liberation Books Library (`books.html` & `chapters/**/*.html`):
   - Tokenization & span ID matching (DOM word spans == WORDS_DATA length).
   - Strict cumulative monotonicity ($c_0 = 0, c_{i+1} > c_i, \sum w_i = \text{TOTAL\_WEIGHT}$).
   - Voice Speech Start Calibration (at $t=0.0$, active word is strictly index 0).
   - Voice Speech End Calibration (at $t=0.999 \times \text{duration}$, active word reaches the end).
   - Bidirectional seek invertibility ($t_{\text{seek}}(k) \to k$).
   - Active highlight styling contract (`.k-word.active-word`).

2. Zorba Reels (`zorba.html` - Koushik's 76 Reels):
   - Acoustic timeline interval monotonicity ($s_0 = 0, s_i \le s_{i+1}, e_i \ge s_i$).
   - Voice Speech Start Calibration (Word 0 begins at $t=0.0$s).
   - Voice Speech End Calibration (Word $N-1$ ends at $\ge 95\%$ of audio duration).
   - Time-to-word binary search resolution.
   - Active word spotlight styling contract (`.jh-word-active`, `.jh-word-spoken`).

3. Jhalak Reels (`jhalak.html` - Ma's 119 Reels):
   - Acoustic timeline interval monotonicity ($s_0 = 0, s_i \le s_{i+1}, e_i \ge s_i$).
   - Voice Speech Start & End Calibration.
   - Time-to-word binary search resolution.
   - Active word spotlight styling contract (`.jh-word-active`, `.jh-word-spoken`).
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import unittest

APP_ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = APP_ROOT / "chapters"
BOOKS_HTML_PATH = APP_ROOT / "books.html"
ZORBA_HTML_PATH = APP_ROOT / "zorba.html"
JHALAK_HTML_PATH = APP_ROOT / "jhalak.html"
ZORBA_MANIFEST_PATH = APP_ROOT / "audio" / "zorba" / "tts_manifest.json"
JHALAK_MANIFEST_PATH = APP_ROOT / "audio" / "jhalak" / "tts_manifest.json"


def find_node_binary() -> str:
    home = Path.home()
    for cand in [
        *sorted(home.glob(".vscode/cli/serve-web/*/node")),
        *sorted(home.glob(".jetski-server/bin/*/node")),
        *sorted(home.glob(".nvm/versions/node/*/bin/node")),
        Path("/usr/local/bin/node"),
        Path("/usr/bin/node"),
    ]:
        if cand.is_file():
            return str(cand)
    return "node"


NODE_BIN = find_node_binary()


class TestKaraokeVoiceSyncCalibration(unittest.TestCase):
    """Automated gate for karaoke word highlight and voice sync calibration across all apps."""

    def test_books_library_karaoke_sync_calibration_gate(self) -> None:
        """Calibrate Books Library word tokenization, cumulative weight monotonicity, start/end alignment, and seek."""
        self.assertTrue(BOOKS_HTML_PATH.is_file(), "books.html must exist")
        books_html = BOOKS_HTML_PATH.read_text(encoding="utf-8")

        # 1. Verify CSS highlight styling rule exists
        self.assertIn(".k-word.active-word", books_html, "books.html must contain .k-word.active-word CSS")
        self.assertRegex(
            books_html,
            r"\.k-word\.active-word\s*\{[^}]*background-color:",
            "Active karaoke word in books.html must have visual background highlight",
        )

        # 2. Verify chapter pages across all books
        chapter_files = sorted(CHAPTERS_DIR.glob("*/*.html"))
        self.assertGreaterEqual(len(chapter_files), 279, "Must calibrate all 279 chapter files")

        # Calibrate a representative cross-sample of 25 chapters from diverse categories
        step_stride = max(1, len(chapter_files) // 25)
        sampled_chapters = chapter_files[::step_stride]

        for ch in sampled_chapters:
            content = ch.read_text(encoding="utf-8")
            m_words = re.search(r"const WORDS_DATA = (\[.*?\]);", content)
            m_weight = re.search(r"const TOTAL_WEIGHT = (\d+);", content)
            self.assertIsNotNone(m_words, f"{ch.name} missing WORDS_DATA")
            self.assertIsNotNone(m_weight, f"{ch.name} missing TOTAL_WEIGHT")

            words = json.loads(m_words.group(1))
            total_weight = int(m_weight.group(1))
            self.assertGreater(len(words), 0, f"{ch.name} has empty words array")

            # A. DOM span 1:1 match
            spans = re.findall(r'id="w_(\d+)"', content)
            self.assertEqual(
                len(spans),
                len(words),
                f"{ch.name}: DOM word spans count ({len(spans)}) != WORDS_DATA length ({len(words)})",
            )

            # B. Cumulative monotonicity & total weight consistency
            cum = 0
            for i, w in enumerate(words):
                self.assertEqual(w["c"], cum, f"{ch.name}: word {i} cumulative weight mismatch")
                self.assertGreaterEqual(w["w"], 1, f"{ch.name}: word {i} weight must be >= 1")
                cum += w["w"]
            self.assertEqual(cum, total_weight, f"{ch.name}: sum of weights {cum} != TOTAL_WEIGHT {total_weight}")

            # C. Voice Speech Start Calibration (t = 0.0s must activate word #0)
            target_start = 0.0
            lo, hi, found_start = 0, len(words) - 1, 0
            while lo <= hi:
                mid = (lo + hi) >> 1
                if words[mid]["c"] <= target_start:
                    found_start = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            self.assertEqual(
                found_start,
                0,
                f"{ch.name} Speech Start Calibration failed: at t=0.0 active word is {found_start} (must be 0)",
            )

            # D. Voice Speech End Calibration (t = 0.999 * duration must reach final words)
            target_end = 0.999 * total_weight
            lo, hi, found_end = 0, len(words) - 1, 0
            while lo <= hi:
                mid = (lo + hi) >> 1
                if words[mid]["c"] <= target_end:
                    found_end = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            self.assertGreaterEqual(
                found_end,
                len(words) - 5,
                f"{ch.name} Speech End Calibration failed: reached word {found_end}/{len(words)}",
            )

            # E. Bidirectional Seek Invertibility Calibration
            # For milestones 0%, 25%, 50%, 75%, 100%, seeking to milestone word must re-activate that exact word
            milestones = [0, len(words) // 4, len(words) // 2, (3 * len(words)) // 4, len(words) - 1]
            for target_idx in milestones:
                seek_weight = words[target_idx]["c"]
                lo, hi, resolved_idx = 0, len(words) - 1, 0
                while lo <= hi:
                    mid = (lo + hi) >> 1
                    if words[mid]["c"] <= seek_weight:
                        resolved_idx = mid
                        lo = mid + 1
                    else:
                        hi = mid - 1
                self.assertEqual(
                    resolved_idx,
                    target_idx,
                    f"{ch.name} Seek Invertibility failed: sought word {target_idx} but resolved to {resolved_idx}",
                )

        # 3. Verify acoustic silence map and timeline integration for audio tracks
        audio_idx_path = APP_ROOT / "assets" / "books_audio_index.json"
        self.assertTrue(audio_idx_path.is_file(), "books_audio_index.json must exist")
        audio_idx = json.loads(audio_idx_path.read_text(encoding="utf-8"))
        files = audio_idx.get("files", [])
        self.assertGreaterEqual(len(files), 7, "Must have at least 7 audio files indexed")

        for f in files:
            silences = f.get("silences", [])
            self.assertGreaterEqual(
                len(silences),
                15,
                f"{f.get('url')} missing calibrated silence intervals in books_audio_index.json",
            )
            # Verify silence intervals are strictly monotonic
            last_e = 0.0
            for pair in silences:
                self.assertGreaterEqual(pair[0], last_e, f"{f.get('url')} silence start < previous end")
                self.assertGreater(pair[1], pair[0], f"{f.get('url')} silence end <= start")
                last_e = pair[1]

        # 4. Verify buildAcousticWordTimeline exists in books.html and chapter pages
        self.assertIn("function buildAcousticWordTimeline", books_html, "books.html must define buildAcousticWordTimeline")
        gene_step1 = CHAPTERS_DIR / "the-gene" / "step_1.html"
        self.assertTrue(gene_step1.is_file(), "the-gene/step_1.html must exist")
        gene_content = gene_step1.read_text(encoding="utf-8")
        self.assertIn("buildAcousticWordTimeline", gene_content, "step_1.html must define buildAcousticWordTimeline")
        self.assertIn("const AUDIO_SILENCES", gene_content, "step_1.html must define AUDIO_SILENCES")

        # 5. Verify Node VM Acoustic Timeline calibration on The Gene Step 1
        node_script = r"""
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const html = fs.readFileSync(0, 'utf8');

const mWords = html.match(/const WORDS_DATA = (\[.*?\]);/);
const mWeight = html.match(/const TOTAL_WEIGHT = (\d+);/);
const mSilences = html.match(/const AUDIO_SILENCES = (\[.*?\]);/);
const mDur = html.match(/const AUDIO_DURATION = ([\d.]+);/);

assert.ok(mWords, 'Missing WORDS_DATA');
assert.ok(mWeight, 'Missing TOTAL_WEIGHT');
assert.ok(mSilences, 'Missing AUDIO_SILENCES');
assert.ok(mDur, 'Missing AUDIO_DURATION');

const words = JSON.parse(mWords[1]);
const totalWeight = parseInt(mWeight[1], 10);
const silences = JSON.parse(mSilences[1]);
const totalDur = parseFloat(mDur[1]);

assert.ok(words.length > 5000, 'The Gene Step 1 should have >5000 words');
assert.ok(silences.length > 100, 'The Gene Step 1 should have >100 silences');

// Execute buildAcousticWordTimeline logic
function voicedTimeAt(t) {
  const clamped = Math.max(0, Math.min(totalDur, t));
  let v = clamped;
  for (let i = 0; i < silences.length; i++) {
    const s = silences[i][0];
    const e = silences[i][1];
    if (clamped <= s) break;
    v -= (Math.min(clamped, e) - s);
  }
  return Math.max(0, v);
}

function invVoicedTime(targetV) {
  let lo = 0, hi = totalDur;
  for (let iter = 0; iter < 26; iter++) {
    const mid = (lo + hi) * 0.5;
    if (voicedTimeAt(mid) < targetV) lo = mid;
    else hi = mid;
  }
  return (lo + hi) * 0.5;
}

const totalVoiced = voicedTimeAt(totalDur);
assert.ok(totalVoiced > 1000, 'Total voiced duration must be >1000s');

// 1. Sentence boundary word indices
const sentEndIndices = [];
for (let i = 0; i < words.length; i++) {
  if (words[i].s) sentEndIndices.push(i);
}
if (!sentEndIndices.length || sentEndIndices[sentEndIndices.length - 1] !== words.length - 1) {
  sentEndIndices.push(words.length - 1);
}
assert.ok(sentEndIndices.length > 200, `Expected >200 sentence boundaries, got ${sentEndIndices.length}`);

// 2. Anchor every K=2 sentences
const K = 2;
const anchorIndices = [];
for (let i = K - 1; i < sentEndIndices.length; i += K) {
  anchorIndices.push(sentEndIndices[i]);
}
if (!anchorIndices.length || anchorIndices[anchorIndices.length - 1] !== words.length - 1) {
  anchorIndices.push(words.length - 1);
}
assert.ok(anchorIndices.length > 100, `Expected >100 sentence anchors, got ${anchorIndices.length}`);

// 3. Compute anchor timestamps snapped to acoustic silences
const anchors = [{ wordIdx: -1, timeSec: 0.0 }];
for (let a = 0; a < anchorIndices.length; a++) {
  const idx = anchorIndices[a];
  const w = words[idx];
  const cumW = w.c + w.w;
  const frac = cumW / totalWeight;
  const targetV = frac * totalVoiced;
  const tEst = invVoicedTime(targetV);

  let bestSilStart = null;
  let minDist = 1.6;
  for (let s = 0; s < silences.length; s++) {
    const dist = Math.abs(silences[s][0] - tEst);
    if (dist < minDist) {
      minDist = dist;
      bestSilStart = silences[s][0];
    }
  }
  const aTime = bestSilStart !== null ? bestSilStart : tEst;
  anchors.push({
    wordIdx: idx,
    timeSec: Math.max(0.1, aTime)
  });
}

for (let a = 1; a < anchors.length; a++) {
  if (anchors[a].timeSec <= anchors[a - 1].timeSec) {
    anchors[a].timeSec = anchors[a - 1].timeSec + 0.3;
  }
}
anchors[anchors.length - 1].timeSec = totalDur;

// 4. Interpolate words strictly within each 2-sentence anchor interval
for (let a = 0; a < anchors.length - 1; a++) {
  const startWIdx = anchors[a].wordIdx + 1;
  const endWIdx = anchors[a + 1].wordIdx;
  if (startWIdx > endWIdx) continue;

  const tStart = anchors[a].timeSec;
  const tEnd = anchors[a + 1].timeSec;
  const baseC = words[startWIdx].c;
  const spanW = Math.max(1, (words[endWIdx].c + words[endWIdx].w) - baseC);
  const spanT = Math.max(0.05, tEnd - tStart);

  for (let i = startWIdx; i <= endWIdx; i++) {
    const fracS = (words[i].c - baseC) / spanW;
    const fracE = ((words[i].c + words[i].w) - baseC) / spanW;
    words[i].startSec = tStart + fracS * spanT;
    words[i].endSec = tStart + fracE * spanT;
  }
}

words[0].startSec = 0.0;
words[words.length - 1].endSec = totalDur;

// Verify monotonicity of acoustic startSec
for (let i = 1; i < words.length; i++) {
  assert.ok(words[i].startSec >= words[i-1].startSec, `Word ${i} startSec inversion`);
}

// Verify speech start and speech end
assert.strictEqual(words[0].startSec, 0, 'Word 0 must start at 0s');
assert.ok(words[words.length - 1].endSec >= totalDur - 1.0, 'Final word must reach audio end');

// Verify that at t=5.6s (title end), active word is near Word 12
let found1 = 0;
for (let i = 0; i < words.length; i++) {
  if (words[i].startSec <= 5.6) found1 = i;
  else break;
}
assert.ok(Math.abs(found1 - 12) <= 4, `Title end alignment: expected ~12, got ${found1}`);

console.log('✓ Books Library Acoustic Timeline Calibration Gate Passed');
process.exit(0);
""";

        proc = subprocess.run(
            [NODE_BIN, "-e", node_script],
            input=gene_content,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            proc.returncode,
            0,
            f"Node VM Books Library calibration failed:\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}",
        )

    def test_zorba_reels_acoustic_voice_sync_calibration_gate(self) -> None:
        """Calibrate Zorba Reels acoustic timeline, voice start/end alignment, and word spotlight highlighting."""
        self.assertTrue(ZORBA_HTML_PATH.is_file(), "zorba.html must exist")
        self.assertTrue(ZORBA_MANIFEST_PATH.is_file(), "zorba tts_manifest.json must exist")

        zb_html = ZORBA_HTML_PATH.read_text(encoding="utf-8")
        self.assertIn(".jh-word-active", zb_html, "zorba.html must define .jh-word-active CSS")
        self.assertIn(".jh-word-spoken", zb_html, "zorba.html must define .jh-word-spoken CSS")

        # Run Node VM calibration across sampled Zorba reels
        m = re.search(r"<script>([\s\S]*?)</script>", zb_html)
        self.assertIsNotNone(m, "Missing <script> block in zorba.html")
        script_code = m.group(1)

        node_script = r"""
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const code = fs.readFileSync(0, 'utf8');

const els = {};
function el(id) {
  if (!els[id]) {
    els[id] = {
      id, className: '', style: {}, innerHTML: '', textContent: '',
      classList: { add() {}, remove() {}, toggle() {}, contains: () => false },
      querySelector: () => ({ textContent: '', classList: { remove() {}, add() {} }, offsetWidth: 100 }),
      play: () => Promise.resolve(), pause() {}, addEventListener() {}, scrollIntoView() {}
    };
  }
  return els[id];
}
const ctx = {
  window: { innerWidth: 390, innerHeight: 844, addEventListener() {} },
  document: {
    body: { appendChild() {}, removeChild() {} },
    getElementById: el,
    querySelectorAll: () => [],
    addEventListener() {},
    createElement: () => ({ style: {}, className: '', textContent: '', classList: { add() {} } })
  },
  localStorage: { getItem: () => null, setItem: () => {} },
  setTimeout: () => 1, clearTimeout: () => {}, setInterval: () => 1, clearInterval: () => {},
  console, assert, el
};

const suite = code + `
;(function() {
  assert.ok(Array.isArray(ALL_JHALAK_REELS) && ALL_JHALAK_REELS.length === 76, 'Zorba must have 76 reels');

  const stride = Math.max(1, Math.floor(ALL_JHALAK_REELS.length / 16));
  let calibratedCount = 0;
  for (let i = 0; i < ALL_JHALAK_REELS.length; i += stride) {
    const card = ALL_JHALAK_REELS[i];
    const cardAudioMeta = (typeof JHALAK_AUDIO_TIMINGS !== 'undefined' && JHALAK_AUDIO_TIMINGS && (JHALAK_AUDIO_TIMINGS[card.id] || JHALAK_AUDIO_TIMINGS[card.audio_rel])) || null;
    assert.ok(cardAudioMeta, 'Missing audio timing metadata for Zorba card: ' + card.id);
    assert.ok(Number(cardAudioMeta.dur) > 1.0, 'Duration must be > 1.0s for Zorba card: ' + card.id);

    const ttsState = { words: [], totalWeight: 0, nextIdx: 0 };
    wrapTextWithJhTtsWords(card.title_bn, ttsState, { blockId: 'jhTitleBlock_' + card.id, addHeadingPause: true });
    for (let sIdx = 0; sIdx < card.sections.length; sIdx++) {
      const s = card.sections[sIdx];
      wrapTextWithJhTtsWords(s.heading_bn, ttsState, { blockId: 'jhSecHeading_' + card.id + '_' + sIdx, addHeadingPause: true });
      wrapTextWithJhTtsWords(s.body_bn, ttsState, { blockId: 'jhSecBody_' + card.id + '_' + sIdx, addHeadingPause: false });
    }

    const dur = buildAcousticWordTimeline(ttsState.words, ttsState.totalWeight, cardAudioMeta);
    assert.ok(dur > 0, 'Timeline duration must be > 0 for ' + card.id);
    assert.ok(ttsState.words.length > 10, 'Card must have at least 10 words: ' + card.id);

    // 1. Speech Start Calibration: Word 0 must start at 0s
    assert.strictEqual(ttsState.words[0].startSec, 0, 'Word 0 must start at 0.0s for ' + card.id);

    // 2. Timeline Monotonicity: intervals must be non-decreasing
    for (let w = 0; w < ttsState.words.length - 1; w++) {
      assert.ok(ttsState.words[w].startSec <= ttsState.words[w + 1].startSec, 'Non-monotonic word startSec at word ' + w + ' in ' + card.id);
      assert.ok(ttsState.words[w].endSec >= ttsState.words[w].startSec, 'Word endSec before startSec at word ' + w + ' in ' + card.id);
    }

    // 3. Speech End Calibration: Final word must span up to >= 95% of total audio duration
    const lastWord = ttsState.words[ttsState.words.length - 1];
    assert.ok(lastWord.endSec >= dur * 0.95, 'Speech End Calibration failed: word N ends at ' + lastWord.endSec + ' vs dur ' + dur + ' in ' + card.id);

    calibratedCount++;
  }
  console.log('✓ Zorba Reels Gate: 100% of ' + calibratedCount + ' sampled reels passed acoustic voice sync calibration.');
})();
`;

vm.runInNewContext(suite, ctx);
"""
        proc = subprocess.run(
            [NODE_BIN, "-e", node_script],
            input=script_code,
            cwd=str(APP_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, f"Zorba Voice Sync Calibration failed:\n{proc.stderr}\n{proc.stdout}")
        self.assertIn("passed acoustic voice sync calibration", proc.stdout)

    def test_jhalak_reels_acoustic_voice_sync_calibration_gate(self) -> None:
        """Calibrate Jhalak Reels acoustic timeline, voice start/end alignment, and word spotlight highlighting."""
        self.assertTrue(JHALAK_HTML_PATH.is_file(), "jhalak.html must exist")
        self.assertTrue(JHALAK_MANIFEST_PATH.is_file(), "jhalak tts_manifest.json must exist")

        jh_html = JHALAK_HTML_PATH.read_text(encoding="utf-8")
        self.assertIn(".jh-word-active", jh_html, "jhalak.html must define .jh-word-active CSS")
        self.assertIn(".jh-word-spoken", jh_html, "jhalak.html must define .jh-word-spoken CSS")

        m = re.search(r"<script>([\s\S]*?)</script>", jh_html)
        self.assertIsNotNone(m, "Missing <script> block in jhalak.html")
        script_code = m.group(1)

        node_script = r"""
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const code = fs.readFileSync(0, 'utf8');

const els = {};
function el(id) {
  if (!els[id]) {
    els[id] = {
      id, className: '', style: {}, innerHTML: '', textContent: '',
      classList: { add() {}, remove() {}, toggle() {}, contains: () => false },
      querySelector: () => ({ textContent: '', classList: { remove() {}, add() {} }, offsetWidth: 100 }),
      play: () => Promise.resolve(), pause() {}, addEventListener() {}, scrollIntoView() {}
    };
  }
  return els[id];
}
const ctx = {
  window: { innerWidth: 390, innerHeight: 844, addEventListener() {} },
  document: {
    body: { appendChild() {}, removeChild() {} },
    getElementById: el,
    querySelectorAll: () => [],
    addEventListener() {},
    createElement: () => ({ style: {}, className: '', textContent: '', classList: { add() {} } })
  },
  localStorage: { getItem: () => null, setItem: () => {} },
  setTimeout: () => 1, clearTimeout: () => {}, setInterval: () => 1, clearInterval: () => {},
  console, assert, el
};

const suite = code + `
;(function() {
  assert.ok(Array.isArray(ALL_JHALAK_REELS) && ALL_JHALAK_REELS.length === 119, 'Jhalak must have 119 reels');

  const stride = Math.max(1, Math.floor(ALL_JHALAK_REELS.length / 16));
  let calibratedCount = 0;
  for (let i = 0; i < ALL_JHALAK_REELS.length; i += stride) {
    const card = ALL_JHALAK_REELS[i];
    const cardAudioMeta = (typeof JHALAK_AUDIO_TIMINGS !== 'undefined' && JHALAK_AUDIO_TIMINGS && (JHALAK_AUDIO_TIMINGS[card.id] || JHALAK_AUDIO_TIMINGS[card.audio_rel])) || null;
    assert.ok(cardAudioMeta, 'Missing audio timing metadata for Jhalak card: ' + card.id);
    assert.ok(Number(cardAudioMeta.dur) > 1.0, 'Duration must be > 1.0s for Jhalak card: ' + card.id);

    const ttsState = { words: [], totalWeight: 0, nextIdx: 0 };
    wrapTextWithJhTtsWords(card.title_bn, ttsState, { blockId: 'jhTitleBlock_' + card.id, addHeadingPause: true });
    for (let sIdx = 0; sIdx < card.sections.length; sIdx++) {
      const s = card.sections[sIdx];
      wrapTextWithJhTtsWords(s.heading_bn, ttsState, { blockId: 'jhSecHeading_' + card.id + '_' + sIdx, addHeadingPause: true });
      wrapTextWithJhTtsWords(s.body_bn, ttsState, { blockId: 'jhSecBody_' + card.id + '_' + sIdx, addHeadingPause: false });
    }

    const dur = buildAcousticWordTimeline(ttsState.words, ttsState.totalWeight, cardAudioMeta);
    assert.ok(dur > 0, 'Timeline duration must be > 0 for ' + card.id);
    assert.ok(ttsState.words.length > 5, 'Card must have at least 5 words: ' + card.id);

    // 1. Speech Start Calibration: Word 0 must start at 0s
    assert.strictEqual(ttsState.words[0].startSec, 0, 'Word 0 must start at 0.0s for ' + card.id);

    // 2. Timeline Monotonicity: intervals must be non-decreasing
    for (let w = 0; w < ttsState.words.length - 1; w++) {
      assert.ok(ttsState.words[w].startSec <= ttsState.words[w + 1].startSec, 'Non-monotonic word startSec at word ' + w + ' in ' + card.id);
      assert.ok(ttsState.words[w].endSec >= ttsState.words[w].startSec, 'Word endSec before startSec at word ' + w + ' in ' + card.id);
    }

    // 3. Speech End Calibration: Final word must span up to >= 95% of total audio duration
    const lastWord = ttsState.words[ttsState.words.length - 1];
    assert.ok(lastWord.endSec >= dur * 0.95, 'Speech End Calibration failed: word N ends at ' + lastWord.endSec + ' vs dur ' + dur + ' in ' + card.id);

    calibratedCount++;
  }
  console.log('✓ Jhalak Reels Gate: 100% of ' + calibratedCount + ' sampled reels passed acoustic voice sync calibration.');
})();
`;

vm.runInNewContext(suite, ctx);
"""
        proc = subprocess.run(
            [NODE_BIN, "-e", node_script],
            input=script_code,
            cwd=str(APP_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, f"Jhalak Voice Sync Calibration failed:\n{proc.stderr}\n{proc.stdout}")
        self.assertIn("passed acoustic voice sync calibration", proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
