#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compiled UI & Headless Node VM Behavioral Test Suite for 🌸 কল্যাণী."""

from pathlib import Path
import re
import shutil
import subprocess
import unittest

APP_ROOT = Path(__file__).resolve().parent.parent


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


class TestUIAndVMBehavior(unittest.TestCase):

    def test_compiled_html_ux_and_node_vm_interactions(self) -> None:
        """Verify 🌸 কল্যাণী header, live progress bar, celebration toast, চিঠি quote+dots, and 6-game VM logic."""
        ma_html_path = APP_ROOT / "ma-presentation.html"
        idx_html_path = APP_ROOT / "index.html"
        self.assertTrue(ma_html_path.is_file())
        self.assertTrue(idx_html_path.is_file())

        ma_html = ma_html_path.read_text(encoding="utf-8")
        self.assertEqual(ma_html, idx_html_path.read_text(encoding="utf-8"))

        # Artisanal UX & Header Invariants
        self.assertIn('id="headerBrand"', ma_html)
        self.assertIn('🌸</span><span>কল্যাণী</span>', ma_html)
        self.assertIn('🎓 আজকের খেলা', ma_html)
        self.assertIn('💌 চিঠি', ma_html)
        self.assertIn('id="nowPlayingBar"', ma_html)
        self.assertIn('id="celebrationToast"', ma_html)
        self.assertIn('id="slideDotsRow"', ma_html)
        # Ensure slideBadge sits outside and above slide-img-wrap (never overlaid on top of the image)
        self.assertLess(ma_html.index('id="slideBadge"'), ma_html.index('class="slide-img-wrap"'))
        self.assertNotIn('id="htabQuote"', ma_html)
        self.assertNotIn('id="viewQuote"', ma_html)
        self.assertNotIn('<nav class="bottom-nav">', ma_html)
        self.assertNotIn('id="themeBtn"', ma_html)
        self.assertNotIn("speechSynthesis", ma_html)

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
    _html: '',
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); if (v === '') this.children = []; },
    textContent: '',
    src: '',
    disabled: false,
    paused: true,
    ended: false,
    duration: 42,
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
[
  'headerBrand','topPlayBtn','nowPlayingBar','npTrack','npFill','npTime',
  'permBanner','dailyQuoteText','btnQuotePlay','viewPlan','viewSlides',
  'htabPlan','htabSlides','segPart1','segPart2','progInlinePill','dayStrip',
  'activeDayStage','letterSlideCard','slideImg','slideBadge','slideDotsRow',
  'slideTitleBn','slideHighlight','slideBodyBn','btnSlideMainPlay',
  'prevBtn','nextBtn','autoAdvanceBtn','celebrationToast','audioPlayer'
].forEach(id => {
  const el = getEl(id);
  if (id === 'topPlayBtn' || id === 'btnQuotePlay') el.setAttribute('data-default-label', '🔊 শোনো');
  if (id === 'btnSlideMainPlay') el.setAttribute('data-default-label', '🔊 এই পাতাটা শোনো');
});
getEl('btnAgPlay_1_0').setAttribute('data-default-label', '🔊 শোনো');

const sandbox = {
  console, assert, process, getEl,
  setTimeout: () => 1, clearTimeout: () => {}, setInterval: () => 1,
  fetch: () => Promise.reject(new Error('offline')),
  alert: () => {},
  Notification: { permission: 'default', requestPermission: () => Promise.resolve('granted') },
  navigator: { serviceWorker: { register: () => Promise.resolve(), ready: Promise.resolve({ showNotification: () => {} }) } },
  localStorage: {
    _store: { 'ma_21day_done_v2': '{corrupted_json', 'ma_kalyani_profile_v1': '{bad_json' },
    getItem(k) { return this._store[k] || null; },
    setItem(k) { return null; }
  },
  window: { scrollTo: () => {} },
  document: {
    documentElement: { _theme: 'warm', getAttribute() { return this._theme; }, setAttribute(k, v) { this._theme = v; } },
    getElementById: (id) => getEl(id),
    createElement: (tag) => makeEl(tag),
    querySelectorAll: () => [getEl('topPlayBtn'), getEl('btnQuotePlay'), getEl('btnSlideMainPlay'), getEl('btnAgPlay_1_0')]
  }
};

vm.createContext(sandbox);
const testBlock = `
assert.strictEqual(DAYS_21.length, 21);
assert.strictEqual(DAYS_PART2_30.length, 30);

const audio = getEl('audioPlayer');
const agBtn0 = getEl('btnAgPlay_1_0');
(async () => {
  // 1. Play/Pause toggle + live Now-Playing Bar visibility
  await playAgendaByIdx(1, 0, agBtn0);
  assert.strictEqual(audio.paused, false);
  assert.strictEqual(agBtn0.innerHTML, '⏸️ থামাও');
  assert.strictEqual(getEl('nowPlayingBar').classList.contains('visible'), true);

  await playAgendaByIdx(1, 0, agBtn0);
  assert.strictEqual(audio.paused, true);
  assert.strictEqual(agBtn0.innerHTML, '🔊 শোনো');
  assert.strictEqual(getEl('nowPlayingBar').classList.contains('visible'), false);

  // 2. চিঠি view refreshes random quote & renders 8 slide dots
  const q0 = getEl('dailyQuoteText').textContent;
  switchView('slides');
  assert.ok(getEl('viewSlides').className.includes('active'));
  assert.notStrictEqual(getEl('dailyQuoteText').textContent, q0);
  assert.strictEqual(getEl('slideDotsRow').children.length, 8);

  // 3. Part 2 & Part 1 progress + 6-game navigator + celebration toast + Day 1->2 auto-advance
  switchView('plan');
  switchCoursePart(2);
  assert.ok(getEl('progInlinePill').textContent.includes('/ 180'));
  assert.ok(DAYS_PART2_30[0].audio_url.includes('audio/days/day_'));
  assert.ok(DAYS_PART2_30[0].agendas[0].audio_url.includes('audio/games/day_'));

  switchCoursePart(1);
  selectDay(1, false);
  selectGame(3);
  assert.ok(getEl('activeDayStage').innerHTML.includes('ফোনের জেমিনি নিজে থেকেই ইউটিউব মিউজিকে (YouTube Music) গান বাজাতে পারে!'));
  assert.ok(getEl('activeDayStage').innerHTML.includes('ধাপ ৩ — গানটা শোনা হয়ে গেলে এর মানে আর গল্পটা জানতে জেমিনিকে বলো:'));

  toggleAgendaDone(1, 0);
  assert.strictEqual(getEl('celebrationToast').classList.contains('show'), true);
  for (let g = 1; g < 6; g++) {
    toggleAgendaDone(1, g);
  }
  assert.strictEqual(curDayNum, 2);
  assert.strictEqual(getEl('dayChip_2').scrolledIntoView, true);
})().catch(err => { console.error(err); process.exit(1); });
`;
vm.runInContext(code + "\n" + testBlock, sandbox, {filename: 'kalyani-bundle.js'});
"""
        proc = subprocess.run(
            [str(NODE_BIN), "-e", vm_harness],
            input=m.group(1),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, f"VM test failed: {proc.stderr}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
