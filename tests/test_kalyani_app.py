#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dedicated unit & Node VM behavioral test suite for Kalyani App (/usr/local/google/home/koushikchak/kalyani-app)."""

import json
from pathlib import Path
import py_compile
import re
import shutil
import subprocess
import sys
import unittest

APP_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = APP_ROOT / "scripts"
AUDIO_DIR = APP_ROOT / "audio"


def find_node_binary() -> str:
    from_path = shutil.which("node") or shutil.which("nodejs")
    if from_path:
        return from_path
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


class TestKalyaniApp(unittest.TestCase):

    def test_dedicated_repo_docs_and_no_auto_tts_rule_present(self) -> None:
        """Verify GEMINI.md, .gemini/config/rules/kalyani_app_rules.md, and spec.md exist and enforce the No-Auto-TTS-Rebuild rule."""
        for rel in ("GEMINI.md", "spec.md", ".gemini/config/rules/kalyani_app_rules.md"):
            p = APP_ROOT / rel
            self.assertTrue(p.is_file(), f"Missing {rel} in {APP_ROOT}")
            content = p.read_text(encoding="utf-8")
            self.assertIn("refresh_voices.py", content)

        build_src = (SCRIPTS_DIR / "build_app.py").read_text(encoding="utf-8")
        self.assertNotIn("gemini-agents-generate/generate", build_src, "build_app.py must NEVER invoke generate tts")
        self.assertNotIn("build_one(", build_src, "build_app.py must NEVER trigger TTS generation")

    def test_python_scripts_compile_and_tts_manifest_tracks_all_246_mp3s(self) -> None:
        """Verify all Python scripts compile cleanly and audio/tts_manifest.json tracks all 246 Aoede MP3s."""
        for py_file in SCRIPTS_DIR.glob("*.py"):
            py_compile.compile(str(py_file), doraise=True)

        manifest_path = AUDIO_DIR / "tts_manifest.json"
        self.assertTrue(manifest_path.is_file(), "Missing audio/tts_manifest.json")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest.get("total_tracked"), 246, "Expected 246 tracked MP3s (8 slides + 7 quotes + 21 days + 210 games)")

        proc = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "refresh_voices.py"), "--status"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("246", proc.stdout)

    def test_ma_presentation_html_and_node_vm_behavioral_suite(self) -> None:
        """Verify ma-presentation.html has zero JS syntax errors, 10 single-focus games/day, YouTube Music Bengali guide, random Quote tab, and Play/Pause/Resume."""
        ma_html_path = APP_ROOT / "ma-presentation.html"
        self.assertTrue(ma_html_path.is_file(), "Missing ma-presentation.html")
        ma_html = ma_html_path.read_text(encoding="utf-8")

        self.assertIn('id="htabPlan"', ma_html)
        self.assertIn('id="htabSlides"', ma_html)
        self.assertIn('id="htabQuote"', ma_html)
        self.assertNotIn('id="bnavKalyani"', ma_html)
        self.assertNotIn('id="bnavProgress"', ma_html)
        self.assertNotIn('<nav class="bottom-nav">', ma_html)
        self.assertNotIn('id="themeBtn"', ma_html)
        self.assertNotIn("speechSynthesis", ma_html)
        self.assertNotIn("SpeechSynthesisUtterance", ma_html)

        self.assertIn("ধাপ ১ — মা আজ যা করবেন ও শিখবেন (বিস্তারিত নির্দেশ):", ma_html)
        self.assertIn("ধাপ ২ — মা, ফোনে জেমিনি (Gemini) অ্যাপ খুলে মাইক 🎙️ বোতাম ছুঁয়ে ঠিক এই কথাটি মুখে বলো:", ma_html)

        m = re.search(r"<script>([\s\S]*?)</script>", ma_html)
        self.assertIsNotNone(m, "Missing <script> block in ma-presentation.html")

        vm_harness = r"""
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const code = fs.readFileSync(0, 'utf8');

const elements = {};
function makeEl(id) {
  return {
    id: id,
    className: '',
    innerHTML: '',
    textContent: '',
    src: '',
    disabled: false,
    paused: true,
    ended: false,
    currentTime: 0,
    scrolledIntoView: false,
    style: {},
    attrs: {},
    children: [],
    listeners: {},
    classList: {
      _set: new Set(),
      add(c) { this._set.add(c); },
      remove(c) { this._set.delete(c); },
      contains(c) { return this._set.has(c); }
    },
    getAttribute(k) { return this.attrs[k] || ''; },
    setAttribute(k, v) { this.attrs[k] = v; },
    appendChild(child) { this.children.push(child); if (child && child.id) elements[child.id] = child; },
    addEventListener(ev, fn) { this.listeners[ev] = fn; },
    scrollIntoView() { this.scrolledIntoView = true; },
    play() { this.paused = false; this.ended = false; return Promise.resolve(); },
    pause() { this.paused = true; }
  };
}
function getEl(id) {
  if (!elements[id]) elements[id] = makeEl(id);
  return elements[id];
}
['topPlayBtn','permBanner','dailyQuoteText','btnQuotePlay','viewPlan','viewSlides','viewQuote','htabPlan','htabSlides','htabQuote','segPart1','segPart2','progInlinePill','dayStrip','activeDayStage','slideImg','slideBadge','slideTitleBn','slideHighlight','slideBodyBn','btnSlideMainPlay','prevBtn','nextBtn','autoAdvanceBtn','audioPlayer'].forEach(id => {
  const el = getEl(id);
  if (id === 'topPlayBtn' || id === 'btnQuotePlay') el.setAttribute('data-default-label', '🔊 শোনো');
  if (id === 'btnSlideMainPlay') el.setAttribute('data-default-label', '🔊 এই পাতাটি কল্যাণীর গলায় শোনো');
});

const sandbox = {
  console, assert, process, getEl, setTimeout: () => 1, clearTimeout: () => {}, setInterval: () => 1,
  AbortController: function() { this.signal = {}; this.abort = () => {}; },
  fetch: () => Promise.reject(new Error('offline')),
  alert: () => {},
  Notification: { permission: 'default', requestPermission: () => Promise.resolve('granted') },
  navigator: { serviceWorker: { register: () => Promise.resolve(), ready: Promise.resolve({ showNotification: () => {} }) } },
  localStorage: {
    _store: { 'ma_21day_done_v2': '{corrupted_json', 'ma_kalyani_profile_v1': '{bad_json' },
    getItem(k) { return this._store[k] || null; },
    setItem(k, v) { this._store[k] = String(v); }
  },
  window: { scrollTo: () => {} },
  document: {
    documentElement: {
      _theme: 'warm',
      getAttribute() { return this._theme; },
      setAttribute(k, v) { this._theme = v; }
    },
    getElementById: (id) => getEl(id),
    createElement: (tag) => makeEl(tag),
    querySelectorAll: () => [getEl('topPlayBtn'), getEl('btnQuotePlay'), getEl('btnSlideMainPlay'), getEl('btnAgPlay_1_0'), getEl('btnAgPlay_1_1')]
  }
};
getEl('btnAgPlay_1_0').setAttribute('data-default-label', '🔊 শোনো');
getEl('btnAgPlay_1_1').setAttribute('data-default-label', '🔊 শোনো');

vm.createContext(sandbox);
const testBlock = `
assert.strictEqual(DAYS_21.length, 21);
assert.strictEqual(DAYS_PART2_30.length, 30);
DAYS_21.forEach(d => {
  assert.strictEqual(d.agendas.length, 10, 'Every Part 1 day must have 10 single-task games');
  assert.ok(d.agendas[8].detail_bn.includes('ইউটিউব মিউজিক'), 'Game 9 must include YouTube Music Bengali instructions');
  assert.ok(d.agendas[8].prompt_bn.includes('ইউটিউব মিউজিকে'), 'Game 9 prompt must ask Gemini about YouTube Music in Bengali');
  assert.ok(d.agendas[9].category.includes('কৌতূহল'), 'Game 10 must be the dedicated Why/How curiosity game');
  d.agendas.forEach((ag, idx) => {
    assert.ok(ag.audio_url.endsWith('day_' + d.day + '_ag_' + idx + '.mp3'), 'Every Part 1 section must use its verbatim day_X_ag_Y.mp3: ' + ag.audio_url);
    const fullText = buildFullSectionSpeechText(d, ag, idx);
    assert.ok(fullText.includes(ag.title_bn));
    assert.ok(fullText.includes(ag.detail_bn));
    assert.ok(fullText.includes(ag.prompt_bn));
  });
});
DAYS_PART2_30.forEach(d => {
  assert.strictEqual(d.agendas.length, 10, 'Every Part 2 day must have 10 single-task games');
  assert.ok(d.agendas[8].detail_bn.includes('ইউটিউব মিউজিক'));
});

const audio = getEl('audioPlayer');
const agBtn0 = getEl('btnAgPlay_1_0');
const agBtn1 = getEl('btnAgPlay_1_1');
(async () => {
  await playAgendaByIdx(1, 0, agBtn0);
  assert.strictEqual(audio.paused, false);
  assert.strictEqual(agBtn0.innerHTML, '⏸️ থামাও');
  assert.strictEqual(getEl('topPlayBtn').innerHTML, '⏸️ থামাও');

  await playAgendaByIdx(1, 0, agBtn0);
  assert.strictEqual(audio.paused, true);
  assert.strictEqual(agBtn0.innerHTML, '🔊 শোনো');

  const qBefore = getEl('dailyQuoteText').textContent;
  switchView('quote');
  const qClick1 = getEl('dailyQuoteText').textContent;
  assert.notStrictEqual(qClick1, qBefore);
  switchView('quote');
  const qClick2 = getEl('dailyQuoteText').textContent;
  assert.notStrictEqual(qClick2, qClick1);

  switchView('plan');
  switchCoursePart(2);
  assert.ok(getEl('progInlinePill').textContent.includes('/ 300'));
  toggleAgendaDone(22, 0);
  assert.ok(getEl('progInlinePill').textContent.includes('1 / 300'));

  switchCoursePart(1);
  selectDay(1, false);
  selectGame(8);
  assert.ok(getEl('activeDayStage').innerHTML.includes('ইউটিউব মিউজিকে (YouTube Music) বাংলায় গান চালানোর সহজ নিয়ম:'));
  selectGame(9);
  assert.strictEqual(curGameIdx, 9);
  assert.ok(getEl('activeDayStage').innerHTML.includes('খেলা 10 / 10'));

  for (let g = 0; g < 10; g++) {
    if (!doneMap['1_' + g]) toggleAgendaDone(1, g);
  }
  assert.strictEqual(curDayNum, 2);
  assert.strictEqual(getEl('dayChip_2').scrolledIntoView, true);

  curDayNum = 1;
  findInitialCurrentDayAndPart();
  assert.strictEqual(curDayNum, 2);
})().catch(err => { console.error(err); process.exit(1); });
`;
vm.runInContext(code + "\n" + testBlock, sandbox, {filename: 'ma-presentation.js'});
"""
        proc = subprocess.run(
            [str(NODE_BIN), "-e", vm_harness],
            input=m.group(1),
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 0, f"VM test failed in ma-presentation.html: {proc.stderr}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
