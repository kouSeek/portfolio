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
        """Verify crisp Bengali typography, zero tickers, sequential lock, auto-unlocked calendar grid, and proactive audio."""
        idx_html_path = APP_ROOT / "index.html"
        self.assertTrue(idx_html_path.is_file())
        self.assertFalse((APP_ROOT / "ma-presentation.html").exists(), "Duplicate ma-presentation.html must not exist")

        ma_html = idx_html_path.read_text(encoding="utf-8")

        # 1. Crisp Bengali ১ (U+09E7) Font & Anti-Clipping Invariants
        self.assertIn("Noto+Sans+Bengali", ma_html)
        self.assertIn("Noto+Serif+Bengali", ma_html)
        self.assertNotIn("Hind+Siliguri", ma_html)
        self.assertNotIn("tabular-nums", ma_html)

        # 2. Zero Part 1/Part 2 Switcher & Zero Task Completion Tickers
        self.assertNotIn('id="segPart1"', ma_html)
        self.assertNotIn('id="segPart2"', ma_html)
        self.assertNotIn('id="progInlinePill"', ma_html)
        self.assertNotIn("আজকের অগ্রগতি", ma_html)
        self.assertNotIn("পার্ট ২", ma_html)

        # 3. Header, Above-Image Letter Badge & Collapsible Calendar Containers
        self.assertIn('id="headerBrand"', ma_html)
        self.assertIn('🌸</span><span>কল্যাণী</span>', ma_html)
        self.assertIn('🎓 আজকের খেলা', ma_html)
        self.assertIn('💌 চিঠি', ma_html)
        self.assertIn('id="daysNavigatorWrap"', ma_html)
        self.assertIn('id="primaryCalGridWrap"', ma_html)
        self.assertIn('id="extendedPart2CalWrap"', ma_html)
        self.assertIn('id="nowPlayingBar"', ma_html)
        self.assertIn('id="celebrationToast"', ma_html)
        self.assertIn('id="videoLetterCard"', ma_html)
        self.assertIn('id="btnWatchMovieLetter"', ma_html)
        self.assertIn('https://drive.google.com/file/d/1gzEnSqp72VlguNK0YirZHRARGmJFR-4g/view', ma_html)
        self.assertIn('id="slideDotsRow"', ma_html)
        self.assertLess(ma_html.index('id="slideBadge"'), ma_html.index('class="slide-img-wrap"'))
        self.assertNotIn("speechSynthesis", ma_html)

        m = re.search(r"<script>([\s\S]*?)</script>", ma_html)
        self.assertIsNotNone(m, "Missing <script> block in index.html")

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
  'htabPlan','htabSlides','daysNavigatorWrap','dayStrip','btnToggleCalGrid',
  'primaryCalGridWrap','extendedPart2CalWrap','activeDayStage','videoLetterCard','btnWatchMovieLetter','letterSlideCard',
  'slideImg','slideBadge','slideDotsRow','slideTitleBn','slideHighlight',
  'slideBodyBn','btnSlideMainPlay','prevBtn','nextBtn','autoAdvanceBtn',
  'celebrationToast','audioPlayer'
].forEach(id => {
  const el = getEl(id);
  if (id === 'topPlayBtn' || id === 'btnQuotePlay') el.setAttribute('data-default-label', '🔊 শোনো');
  if (id === 'btnSlideMainPlay') el.setAttribute('data-default-label', '🔊 এই পাতাটা শোনো');
});
getEl('btnDayMainPlay').setAttribute('data-default-label', '🔊 আজকের কথাগুলো শোনো');
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
    setItem(k, v) { this._store[k] = v; }
  },
  window: { scrollTo: () => {} },
  document: {
    documentElement: { _theme: 'warm', getAttribute() { return this._theme; }, setAttribute(k, v) { this._theme = v; } },
    addEventListener: () => {},
    removeEventListener: () => {},
    getElementById: (id) => getEl(id),
    createElement: (tag) => makeEl(tag),
    querySelectorAll: () => [getEl('topPlayBtn'), getEl('btnQuotePlay'), getEl('btnSlideMainPlay'), getEl('btnDayMainPlay'), getEl('btnAgPlay_1_0')]
  }
};

vm.createContext(sandbox);
const testBlock = `
assert.strictEqual(DAYS_21.length, 21);
assert.strictEqual(DAYS_PART2_30.length, 30);

const audio = getEl('audioPlayer');
(async () => {
  // 1. Proactive Auto-Engage Audio on App Open/Load (plays Day voice -> Current Open Game) & uses ma-audio orphan branch!
  assert.strictEqual(curDayNum, 1);
  assert.strictEqual(curGameIdx, 0);
  assert.strictEqual(audio.paused, false, 'Proactive welcome audio should engage immediately on load');
  assert.strictEqual(activeAudioKey, 'day_main_1');
  assert.ok(audio.src.includes('ma-audio/audio/days/day_1.mp3'), 'Audio URL must point to ma-audio orphan branch');
  assert.strictEqual(getEl('nowPlayingBar').classList.contains('visible'), true);

  // Chaining: when day_main_1 finishes, it automatically reads out Current Open Game (ag_1_0)
  audio.listeners['ended']();
  assert.strictEqual(activeAudioKey, 'ag_1_0');
  assert.ok(audio.src.includes('ma-audio/audio/games/day_1_ag_0.mp3'));

  // Next Game & Prev Game buttons automatically play the voice for that game!
  selectGame(curGameIdx + 1, true);
  assert.strictEqual(curGameIdx, 1);
  assert.strictEqual(activeAudioKey, 'ag_1_1');
  assert.strictEqual(audio.paused, false, 'Clicking Next Game must automatically play that game voice');
  assert.ok(audio.src.includes('ma-audio/audio/games/day_1_ag_1.mp3'));

  selectGame(curGameIdx - 1, true);
  assert.strictEqual(curGameIdx, 0);
  assert.strictEqual(activeAudioKey, 'ag_1_0');
  assert.strictEqual(audio.paused, false, 'Clicking Prev Game must automatically play that game voice');
  assert.ok(audio.src.includes('ma-audio/audio/games/day_1_ag_0.mp3'));

  // 2. Game Tiles have ZERO duplicate numbers and support custom v2 badges & variable wave counts!
  const stageHtml = getEl('activeDayStage').innerHTML;
  assert.ok(stageHtml.includes('এআই বন্ধু') && stageHtml.includes('🌿 মনের আরাম'));
  assert.ok(stageHtml.includes('data-count="3"'), 'Day 1 should render a 3-game gentle wave');
  assert.ok(!stageHtml.includes('খেলা ১'), 'Game buttons must not contain duplicate খেলা ১');
  assert.ok(!stageHtml.includes('১. '), 'Game buttons must not contain ১. prefix');

  // 2b. Card Inner Headers match game type (Non-song Gemini task vs. Song game):
  assert.ok(
    stageHtml.includes('💬 জেমিনির উত্তরটা শোনার পর গল্পটা আরও জমাতে দ্বিতীয় কথায় বলো:'),
    'Non-song 2-turn game must show conversational follow-up header, NEVER song follow-up header'
  );
  assert.ok(
    !stageHtml.includes('গানটা শোনা হয়ে গেলে এর মানে আর গল্পটা জানতে জেমিনিকে বলো:'),
    'Non-song game card must NEVER display the song follow-up header'
  );
  // Select Day 1 Game 2 (Song game) and verify song headers appear on song card:
  selectGame(2, false);
  const songStageHtml = getEl('activeDayStage').innerHTML;
  assert.ok(songStageHtml.includes('🎵 মা, আজকের গান ও মনের টান:'));
  assert.ok(songStageHtml.includes('💬 গানটা শোনা হয়ে গেলে এর মানে আর গল্পটা জানতে জেমিনিকে বলো:'));
  selectGame(0, false);

  // 3. Sequential Day Locking: Day 2..51 are locked until Day 1 is finished
  assert.strictEqual(isDayUnlocked(1), true);
  assert.strictEqual(isDayUnlocked(2), false);
  assert.ok(getEl('dayChip_2').innerHTML.includes('🔒 দিন ২'));
  assert.strictEqual(getEl('extendedPart2CalWrap').style.display, 'none', 'Days 22-51 stay hidden before Day 21 finishes');

  const blockedJump = selectDay(2, false);
  assert.strictEqual(blockedJump, false);
  assert.strictEqual(curDayNum, 1);
  assert.ok(getEl('celebrationToast').textContent.includes('দিন ১'));

  // 4. Primary Calendar Grid Toggle (Days 1-21)
  togglePrimaryCalendarGrid();
  assert.strictEqual(getEl('primaryCalGridWrap').style.display, 'block');
  assert.ok(getEl('primaryCalGridWrap').innerHTML.includes('🔒 দিন ২'));
  togglePrimaryCalendarGrid();
  assert.strictEqual(getEl('primaryCalGridWrap').style.display, 'none');

  // 5. Completing all games of Day 1 unlocks Day 2 (4-game wave) and auto-advances!
  for (let g = 0; g < DAYS_21[0].agendas.length; g++) {
    toggleAgendaDone(1, g);
  }
  assert.strictEqual(isDayUnlocked(2), true);
  assert.strictEqual(isDayUnlocked(3), false);
  assert.strictEqual(curDayNum, 2);
  assert.ok(getEl('activeDayStage').innerHTML.includes('data-count="4"'), 'Day 2 should render a 4-game wave');

  // 5b. App Re-Open Simulation: if Day 2 Game 0 was skipped and Game 1 is the latest finished game,
  // opening the app focuses Game 2 (next game after latest done = index 2) and plays day_main_2 -> ag_2_2!
  doneMap['2_1'] = true;
  findInitialCurrentDay();
  renderPlanView();
  engageProactiveWelcomeAudio();
  assert.strictEqual(curDayNum, 2);
  assert.strictEqual(curGameIdx, 2, 'Should open the next game strictly after the latest finished game');
  assert.strictEqual(activeAudioKey, 'day_main_2');
  audio.listeners['ended']();
  assert.strictEqual(activeAudioKey, 'ag_2_2', 'After Day 2 voice finishes, should play current open game (index 2)');
  delete doneMap['2_1'];

  // 6. Completing Days 2..21 automatically unlocks Days 22-51 as a Collapsible Calendar Grid View!
  for (let d = 2; d <= 21; d++) {
    const dayCount = DAYS_21[d - 1].agendas.length;
    for (let g = 0; g < dayCount; g++) {
      toggleAgendaDone(d, g);
    }
  }
  assert.strictEqual(areFirst21DaysComplete(), true);
  assert.strictEqual(curDayNum, 22);
  assert.strictEqual(isDayUnlocked(22), true);
  assert.strictEqual(isDayUnlocked(23), false);
  assert.strictEqual(getEl('extendedPart2CalWrap').style.display, 'block');
  assert.ok(getEl('extendedPart2CalWrap').innerHTML.includes('নতুন ৩০ দিনের ক্যালেন্ডার (দিন ২২ – ৫১)'));
  assert.ok(getEl('extendedPart2CalWrap').innerHTML.includes('দিন ২২'));
  assert.ok(getEl('extendedPart2CalWrap').innerHTML.includes('🔒 দিন ২৩'));

  // Collapsing and re-expanding the Extended 30-Day Calendar Grid works smoothly
  toggleExtendedCalendarGrid();
  assert.ok(!getEl('extendedPart2CalWrap').innerHTML.includes('id="extCalendarGrid"'));
  toggleExtendedCalendarGrid();
  assert.ok(getEl('extendedPart2CalWrap').innerHTML.includes('id="extCalendarGrid"'));

  // 7. চিঠি view refreshes random quote & renders 8 slide dots
  const q0 = getEl('dailyQuoteText').textContent;
  switchView('slides');
  assert.ok(getEl('viewSlides').className.includes('active'));
  assert.notStrictEqual(getEl('dailyQuoteText').textContent, q0);
  assert.strictEqual(getEl('slideDotsRow').children.length, 8);
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

    def test_koushik_app_vm_rendering_and_inline_audio_controls(self) -> None:
        """Verify koushik.html (⚡ আনন্দ) compiles cleanly, renders all game & slide content, and has inline audio controls."""
        k_path = APP_ROOT / "koushik.html"
        self.assertTrue(k_path.is_file(), "koushik.html must exist")
        k_html = k_path.read_text(encoding="utf-8")
        self.assertNotIn("position: fixed;\n      bottom: 0", k_html)
        self.assertIn('id="topPlayBtn"', k_html)
        self.assertIn('id="nowPlayingBar"', k_html)

        m = re.search(r"<script>([\s\S]*?)</script>", k_html)
        self.assertIsNotNone(m, "Missing <script> block in koushik.html")

        vm_harness = r"""
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const code = fs.readFileSync(0, 'utf8');
const els = {};
function el(id) {
  if (!els[id]) {
    els[id] = {
      id, className: '', innerHTML: '', textContent: '', style: {}, disabled: false,
      classList: {
        add(c) { if (!els[id].className.includes(c)) els[id].className += ' ' + c; },
        remove(c) { els[id].className = els[id].className.replace(c, '').trim(); },
        toggle(c, b) { if (b) this.add(c); else this.remove(c); }
      },
      addEventListener() {}
    };
  }
  return els[id];
}
const audioListeners = {};
const ctx = {
  window: {},
  document: { getElementById: el, querySelectorAll: () => [], addEventListener() {}, removeEventListener() {} },
  Audio: function() {
    return {
      preload: '', paused: true, ended: false, duration: 30, currentTime: 0,
      addEventListener(ev, fn) { audioListeners[ev] = fn; },
      pause() { this.paused = true; },
      play() { this.paused = false; return Promise.resolve(); }
    };
  },
  localStorage: { getItem: () => null, setItem: () => {} },
  navigator: { clipboard: { writeText: () => {} } },
  setTimeout, clearTimeout, setInterval, clearInterval, console, assert, audioListeners
};
const scriptAndTests = code + `
;(function() {
  // 1. Initial page load auto-starts day_main_1 and chains into ag_1_0 on ended
  assert.strictEqual(activeAudioKey, 'day_main_1', 'Initial load must auto-start day_main_1');
  audioListeners['ended']();
  assert.strictEqual(activeAudioKey, 'ag_1_0', 'After day_main_1 ends, must auto-start ag_1_0');

  // 2. Selecting any game auto-starts its voice
  selectGame(1);
  assert.strictEqual(activeAudioKey, 'ag_1_1', 'selectGame(1) must auto-start ag_1_1');

  // 3. Selecting any day auto-starts its day overview voice and chains into its first open game
  selectDay(2);
  assert.strictEqual(activeAudioKey, 'day_main_2', 'selectDay(2) must auto-start day_main_2');
  audioListeners['ended']();
  assert.strictEqual(activeAudioKey, 'ag_2_0', 'After day_main_2 ends, must auto-start ag_2_0');

  // 4. Switching tabs auto-starts voice on every page (letter, pillars, play)
  switchTab('letter');
  assert.strictEqual(activeAudioKey, 'slide_1', 'switchTab(letter) must auto-start slide_1');
  switchTab('pillars');
  assert.strictEqual(activeAudioKey, 'pillar_0', 'switchTab(pillars) must auto-start pillar_0');
  switchTab('play');
  assert.strictEqual(activeAudioKey, 'day_main_2', 'switchTab(play) must auto-start active day voice');
})();
`;
vm.runInNewContext(scriptAndTests, ctx, {filename: 'koushik-bundle.js'});
assert.ok(els['dayStrip'].innerHTML.includes('দিন ১'), 'dayStrip must render');
assert.ok(els['gameGrid'].innerHTML.length > 50, 'gameGrid must render game tiles');
assert.ok(els['activeGameStage'].innerHTML.includes('card-top-bar'), 'activeGameStage must render top inline controls');
assert.ok(els['activeGameStage'].innerHTML.includes('agenda-actions'), 'activeGameStage must render bottom actions');
assert.ok(els['letterStage'].innerHTML.includes('btnSlideTopPlay'), 'letterStage must render top slide play button');
assert.ok(els['pillarsContainer'].innerHTML.includes('অপরাধবোধ থেকে মুক্তি'), 'pillarsContainer must render 7 pillars');
"""
        proc = subprocess.run(
            [str(NODE_BIN), "-e", vm_harness],
            input=m.group(1),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, f"koushik.html VM test failed: {proc.stderr}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
