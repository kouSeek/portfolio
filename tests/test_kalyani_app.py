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

    def test_dedicated_repo_docs_persona_downstream_and_no_auto_tts_rule(self) -> None:
        """Verify GEMINI.md, student-persona.md, client-side-gemini.md, spec.md, and No-Auto-TTS-Rebuild rule exist."""
        for rel in (
            "GEMINI.md",
            "spec.md",
            "student-persona.md",
            "client-side-gemini.md",
            ".gemini/config/rules/kalyani_app_rules.md",
        ):
            p = APP_ROOT / rel
            self.assertTrue(p.is_file(), f"Missing {rel} in {APP_ROOT}")

        persona_txt = (APP_ROOT / "student-persona.md").read_text(encoding="utf-8")
        self.assertIn("6", persona_txt)
        self.assertIn("Zero Direct Mistake Callouts", persona_txt)

        downstream_txt = (APP_ROOT / "client-side-gemini.md").read_text(encoding="utf-8")
        self.assertIn("YouTube Music", downstream_txt)
        self.assertIn("কল্যাণী", downstream_txt)

        build_src = (SCRIPTS_DIR / "build_app.py").read_text(encoding="utf-8")
        self.assertNotIn("gemini-agents-generate/generate", build_src, "build_app.py must NEVER invoke generate tts")
        self.assertNotIn("build_one(", build_src, "build_app.py must NEVER trigger TTS generation")

    def test_python_scripts_compile_and_tts_status_runs_cleanly(self) -> None:
        """Verify all Python scripts compile cleanly and refresh_voices.py --status runs without regenerating audio."""
        for py_file in SCRIPTS_DIR.glob("*.py"):
            py_compile.compile(str(py_file), doraise=True)

        manifest_path = AUDIO_DIR / "tts_manifest.json"
        self.assertTrue(manifest_path.is_file(), "Missing audio/tts_manifest.json")

        proc = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "refresh_voices.py"), "--status"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("162", proc.stdout, "Expected 162 tracked items (8 slides + 7 quotes + 21 days + 126 games)")

    def test_ma_presentation_html_and_node_vm_behavioral_suite(self) -> None:
        """Verify 🌸 কল্যাণী header, আজকের খেলা tab, অনুপ্রেরণা inside চিঠি, 6 ego-safe games/day, and Node VM behavior."""
        ma_html_path = APP_ROOT / "ma-presentation.html"
        self.assertTrue(ma_html_path.is_file(), "Missing ma-presentation.html")
        ma_html = ma_html_path.read_text(encoding="utf-8")

        # Header checks: 🌸 কল্যাণী brand, 🎓 আজকের খেলা, 💌 চিঠি, no separate #htabQuote or #viewQuote
        self.assertIn('id="headerBrand"', ma_html)
        self.assertIn('<span>🌸</span><span>কল্যাণী</span>', ma_html)
        self.assertIn('🎓 আজকের খেলা', ma_html)
        self.assertIn('💌 চিঠি', ma_html)
        self.assertNotIn('id="htabQuote"', ma_html, "Quote tab must be removed from header and placed inside চিঠি")
        self.assertNotIn('id="viewQuote"', ma_html, "Separate viewQuote must be merged inside viewSlides (চিঠি)")
        self.assertNotIn('id="bnavKalyani"', ma_html)
        self.assertNotIn('<nav class="bottom-nav">', ma_html)
        self.assertNotIn('id="themeBtn"', ma_html)
        self.assertNotIn("speechSynthesis", ma_html)

        # Natural Bengali & Ego-Safety checks
        self.assertNotIn("দয়া করে", ma_html)
        self.assertNotIn("মস্তিষ্ক", ma_html)
        self.assertNotIn("ভুল থেকে শিক্ষা", ma_html)
        self.assertNotIn("পচা ফলটা আগে", ma_html)
        self.assertNotIn("ভবঘুরের মতো", ma_html)
        self.assertNotIn("Kiptemi", ma_html)

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
['headerBrand','topPlayBtn','permBanner','dailyQuoteText','btnQuotePlay','viewPlan','viewSlides','htabPlan','htabSlides','segPart1','segPart2','progInlinePill','dayStrip','activeDayStage','slideImg','slideBadge','slideTitleBn','slideHighlight','slideBodyBn','btnSlideMainPlay','prevBtn','nextBtn','autoAdvanceBtn','audioPlayer'].forEach(id => {
  const el = getEl(id);
  if (id === 'topPlayBtn' || id === 'btnQuotePlay') el.setAttribute('data-default-label', '🔊 শোনো');
  if (id === 'btnSlideMainPlay') el.setAttribute('data-default-label', '🔊 এই পাতাটা শোনো');
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
  assert.strictEqual(d.agendas.length, 6, 'Every Part 1 day must have 6 cohesive games');
  assert.ok(d.agendas[3].detail_bn.includes('ইউটিউব মিউজিক'), 'Game 4 must include YouTube Music instructions');
  assert.ok(d.agendas[3].prompt_bn.startsWith('জেমিনি, ইউটিউব মিউজিকে ‘'), 'Game 4 prompt must directly command YouTube Music');
  assert.ok(d.agendas[3].prompt_bn.endsWith('’ গানটা চালিয়ে দাও।'));
  assert.ok(d.agendas[3].followup_prompt_bn.includes('গানটার কথাগুলোর আসল মানে'));
});
DAYS_PART2_30.forEach(d => {
  assert.strictEqual(d.agendas.length, 6, 'Every Part 2 day must have 6 cohesive games');
  assert.ok(d.agendas[3].prompt_bn.startsWith('জেমিনি, ইউটিউব মিউজিকে ‘'));
});

const audio = getEl('audioPlayer');
const agBtn0 = getEl('btnAgPlay_1_0');
(async () => {
  await playAgendaByIdx(1, 0, agBtn0);
  assert.strictEqual(audio.paused, false);
  assert.strictEqual(agBtn0.innerHTML, '⏸️ থামাও');

  await playAgendaByIdx(1, 0, agBtn0);
  assert.strictEqual(audio.paused, true);
  assert.strictEqual(agBtn0.innerHTML, '🔊 শোনো');

  // Opening চিঠি ('slides') refreshes the random quote inside চিঠি
  const qBefore = getEl('dailyQuoteText').textContent;
  switchView('slides');
  assert.ok(getEl('viewSlides').className.includes('active'));
  const qClick1 = getEl('dailyQuoteText').textContent;
  assert.notStrictEqual(qClick1, qBefore);
  switchView('slides');
  const qClick2 = getEl('dailyQuoteText').textContent;
  assert.notStrictEqual(qClick2, qClick1);

  switchView('plan');
  switchCoursePart(2);
  assert.ok(getEl('progInlinePill').textContent.includes('/ 180'));
  toggleAgendaDone(22, 0);
  assert.ok(getEl('progInlinePill').textContent.includes('1 / 180'));

  // Test 6-Game 2x3 Visual Navigator Grid & Song Game (index 3) + Last Game (index 5)
  switchCoursePart(1);
  selectDay(1, false);
  assert.ok(getEl('progInlinePill').textContent.includes('/ 126'));
  selectGame(3);
  assert.ok(getEl('activeDayStage').innerHTML.includes('ফোনের জেমিনি নিজে থেকেই ইউটিউব মিউজিকে (YouTube Music) গান বাজাতে পারে!'));
  assert.ok(getEl('activeDayStage').innerHTML.includes('ধাপ ৩ — গানটা শোনা হয়ে গেলে এর মানে আর গল্পটা জানতে জেমিনিকে বলো:'));
  selectGame(5);
  assert.strictEqual(curGameIdx, 5);
  assert.ok(getEl('activeDayStage').innerHTML.includes('খেলা 6 / 6'));

  // Completing all 6 games of Day 1 auto-advances to Day 2
  for (let g = 0; g < 6; g++) {
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
