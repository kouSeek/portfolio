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
        hub_html = (APP_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="kalyani.html"', hub_html)
        self.assertIn('href="anondo.html"', hub_html)
        self.assertIn('id="pageFavicon"', hub_html)
        self.assertIn('data-emoji="🪷"', hub_html)
        self.assertIn("favicon-hub.png", hub_html)
        self.assertIn("data:image/png;base64,", hub_html)
        self.assertIn("<title>AI Companion — Kalyani (Ma) & Anondo (Koushik) 🪷</title>", hub_html)

        idx_html_path = APP_ROOT / "kalyani.html"
        self.assertTrue(idx_html_path.is_file())
        self.assertFalse((APP_ROOT / "ma-presentation.html").exists(), "Duplicate ma-presentation.html must not exist")

        ma_html = idx_html_path.read_text(encoding="utf-8")
        self.assertIn('id="pageFavicon"', ma_html)
        self.assertIn('data-emoji="🌸"', ma_html)
        self.assertIn("favicon-kalyani.png", ma_html)
        self.assertIn("data:image/png;base64,", ma_html)
        self.assertIn("<title>কল্যাণী — আজকের খেলা ও চিঠি 🌸</title>", ma_html)

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
        self.assertIn('🎓 খেলা', ma_html)
        self.assertIn('📺 টিভি', ma_html)
        self.assertIn('💌 চিঠি', ma_html)
        self.assertIn('id="daysNavigatorWrap"', ma_html)
        self.assertIn('id="primaryCalGridWrap"', ma_html)
        self.assertNotIn('id="extendedPart2CalWrap"', ma_html)
        self.assertNotIn('DAYS_PART2_30', ma_html)
        self.assertNotIn('নতুন ৩০ দিনের ক্যালেন্ডার', ma_html)
        self.assertIn('id="nowPlayingBar"', ma_html)
        self.assertIn('id="celebrationToast"', ma_html)
        self.assertIn('id="videoLetterCard"', ma_html)
        self.assertIn('id="btnWatchMovieLetter"', ma_html)
        self.assertIn('https://drive.google.com/file/d/1gzEnSqp72VlguNK0YirZHRARGmJFR-4g/view', ma_html)
        self.assertIn('id="slideDotsRow"', ma_html)
        self.assertLess(ma_html.index('id="slideBadge"'), ma_html.index('class="slide-img-wrap"'))
        self.assertGreater(ma_html.index('id="videoLetterCard"'), ma_html.index('id="letterSlideCard"'))
        self.assertGreater(ma_html.index('id="dailyQuoteCard"'), ma_html.index('id="videoLetterCard"'))
        self.assertGreater(ma_html.index('id="koushikAdminSection"'), ma_html.index('id="dailyQuoteCard"'))
        self.assertIn("মা, এই নিচের অংশটায় তোমার হাত দেওয়ার বা কিছু করার একেবারেই দরকার নেই।", ma_html)
        self.assertNotIn('type="file"', ma_html)
        self.assertNotIn("requestMicAndNotificationPermission", ma_html)
        self.assertNotIn("clearKalyaniThreadsAndMemory", ma_html)
        self.assertNotIn("btnAdminNotifPerm", ma_html)
        self.assertNotIn("btnAdminClearThreads", ma_html)
        self.assertIn("object-fit: contain", ma_html)
        self.assertNotIn("object-fit: cover", ma_html)
        self.assertNotIn("aspect-ratio: 16 / 10", ma_html)
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
  'permBanner','dailyQuoteText','btnQuotePlay','viewPlan','viewTv','viewSlides',
  'htabPlan','htabTv','htabSlides','tvHubStage','daysNavigatorWrap','dayStrip','btnToggleCalGrid',
  'primaryCalGridWrap','activeDayStage','videoLetterCard','btnWatchMovieLetter','letterSlideCard',
  'slideImg','slideBadge','slideDotsRow','slideTitleBn','slideHighlight',
  'slideBodyBn','btnSlideMainPlay','prevBtn','nextBtn','autoAdvanceBtn',
  'celebrationToast','audioPlayer','koushikAdminSection','koushikAdminDrawer','koushikAdminBody'
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
assert.strictEqual(ALL_DAYS.length, 21);

const audio = getEl('audioPlayer');
(async () => {
  // 1. Proactive Auto-Engage Audio on App Open/Load (plays Day voice -> Current Open Game) & uses ma-audio orphan branch!
  assert.strictEqual(curDayNum, 1);
  assert.strictEqual(curGameIdx, 0);
  assert.strictEqual(audio.paused, false, 'Proactive welcome audio should engage immediately on load');
  assert.strictEqual(activeAudioKey, 'day_main_1');
  assert.ok(audio.src.includes('ai-companion-audio/audio/kalyani/days/day_1.mp3'), 'Audio URL must point to ai-companion-audio orphan branch');
  assert.strictEqual(getEl('nowPlayingBar').classList.contains('visible'), true);

  // Chaining: when day_main_1 finishes, it automatically reads out Current Open Game (ag_1_0)
  audio.listeners['ended']();
  assert.strictEqual(activeAudioKey, 'ag_1_0');
  assert.ok(audio.src.includes('ai-companion-audio/audio/kalyani/games/day_1_ag_0.mp3'));

  // Next Game & Prev Game buttons automatically play the voice for that game!
  selectGame(curGameIdx + 1, true);
  assert.strictEqual(curGameIdx, 1);
  assert.strictEqual(activeAudioKey, 'ag_1_1');
  assert.strictEqual(audio.paused, false, 'Clicking Next Game must automatically play that game voice');
  assert.ok(audio.src.includes('ai-companion-audio/audio/kalyani/games/day_1_ag_1.mp3'));

  selectGame(curGameIdx - 1, true);
  assert.strictEqual(curGameIdx, 0);
  assert.strictEqual(activeAudioKey, 'ag_1_0');
  assert.strictEqual(audio.paused, false, 'Clicking Prev Game must automatically play that game voice');
  assert.ok(audio.src.includes('ai-companion-audio/audio/kalyani/games/day_1_ag_0.mp3'));

  // 2. Game Tiles have ZERO duplicate numbers and support custom 7-pillar badges & 6-game waves!
  const stageHtml = getEl('activeDayStage').innerHTML;
  assert.ok(stageHtml.includes('💬 মনের কথা') && stageHtml.includes('🔤 ইংরেজি কথা') && stageHtml.includes('🗣️ হিন্দি আড্ডা'));
  assert.ok(stageHtml.includes('data-count="6"'), 'Day 1 should render a 6-game wave across the 7 pillars');
  assert.ok(!stageHtml.includes('খেলা ১'), 'Game buttons must not contain duplicate খেলা ১');
  assert.ok(!stageHtml.includes('১. '), 'Game buttons must not contain ১. prefix');

  // 2b. Card Inner Headers match game type (Personal therapy / Hindi / Song game):
  assert.ok(
    stageHtml.includes('💬 মা, আজকের মনের গভীর কথা ও স্মৃতির ঝাঁপি:'),
    'Personal therapy game must show deep reminiscence & emotional unburdening header'
  );
  assert.ok(
    stageHtml.includes('💬 জেমিনির উত্তরটা শোনার পর গল্পটা আরও জমাতে দ্বিতীয় কথায় বলো:'),
    'Non-song 2-turn game must show conversational follow-up header, NEVER song follow-up header'
  );
  assert.ok(
    !stageHtml.includes('গানটা শোনা হয়ে গেলে এর মানে আর গল্পটা জানতে জেমিনিকে বলো:'),
    'Non-song game card must NEVER display the song follow-up header'
  );
  // Select Day 1 Game 5 (Song game) and verify song headers + direct YouTube button appear on song card:
  selectGame(5, false);
  const songStageHtml = getEl('activeDayStage').innerHTML;
  assert.ok(songStageHtml.includes('🎵 মা, আজকের গান ও মনের টান:'));
  assert.ok(songStageHtml.includes('🎵 ইউটিউবে এই গানটা সরাসরি চালাও ▶️'));
  assert.ok(songStageHtml.includes('💬 গানটা শোনা হয়ে গেলে এর মানে আর গল্পটা জানতে জেমিনিকে বলো:'));
  assert.ok(songStageHtml.includes('optional-prompt-drawer'));
  selectGame(0, false);

  // 2c. Zero-Pressure Defaults: All 21 days unlocked by default, Story-Only cutoff active, Radio Auto-Play chains ag_1_0 -> ag_1_1, and 📺 টিভি ও গান view renders 8 channels!
  assert.strictEqual(unlockAllDaysMode, true);
  assert.strictEqual(radioAutoPlay, true);
  assert.strictEqual(storyOnlyAudio, true);
  assert.strictEqual(isDayUnlocked(25), true);
  assert.ok(DAYS_21[0].agendas[0].story_end > 10, 'Each game must carry a precomputed story_end silence cutoff');
  playAgendaByIdx(1, 0, null);
  assert.strictEqual(activeAudioKey, 'ag_1_0');
  assert.ok(activeStoryEndSec > 10, 'Playing game in story-only mode must arm activeStoryEndSec');
  audio.currentTime = activeStoryEndSec + 0.1;
  audio.listeners['timeupdate']();
  assert.strictEqual(activeAudioKey, 'ag_1_1', 'Reaching story_end in Radio Mode must auto-advance to ag_1_1 without speaking Gemini instructions');

  switchView('tv');
  assert.ok(getEl('viewTv').className.includes('active'));
  assert.ok(getEl('tvHubStage').innerHTML.includes('উত্তম-সুচিত্রার চিরকালের বাংলা ছবি'));
  assert.ok(getEl('tvHubStage').innerHTML.includes('মান্না দে ও রবীন্দ্রসঙ্গীতের শান্ত আসর'));
  switchView('plan');
  selectGame(0, false);

  // 2d. Proactive Agent Card & 21 Delight Stories at top of TV tab (#tvHubStage), while #activeDayStage keeps only daily games:
  assert.ok(typeof KALYANI_SYSTEM_PROMPT === 'string' && KALYANI_SYSTEM_PROMPT.includes('IRONCLAD LANGUAGE RULE'));
  assert.strictEqual(DELIGHT_STORIES_21.length, 21);
  assert.ok(!getEl('activeDayStage').innerHTML.includes('id="kalyaniAgentCard"'), 'Game tab must keep only daily games (no agent card)');
  assert.ok(!getEl('activeDayStage').innerHTML.includes('id="dailyDelightCard"'), 'Game tab must keep only daily games (no delight story card)');
  assert.ok(getEl('tvHubStage').innerHTML.includes('id="kalyaniAgentCard"'), 'Proactive Agent Companion Card must render at top of TV tab');
  assert.ok(getEl('tvHubStage').innerHTML.includes('id="dailyDelightCard"'), 'Daily Delight Story card must render at top of TV tab');
  assert.ok(
    getEl('tvHubStage').innerHTML.indexOf('id="kalyaniAgentCard"') < getEl('tvHubStage').innerHTML.indexOf('tv-hub-grid'),
    'Agent and Short Story cards must appear at the top of TV tab above TV channel grid'
  );
  assert.ok(getEl('activeDayStage').innerHTML.includes('id="vnStudio_1_0"'));
  assert.ok(getEl('activeDayStage').innerHTML.includes('কল্যাণীকে ভয়েস মেসেজ বা ভিডিও তুলে পাঠাও:'), 'Studio header must match requested text');
  assert.ok(getEl('activeDayStage').innerHTML.includes('🎙️ ভয়েস পাঠাও'), 'Send Voice button must be present');
  assert.ok(getEl('activeDayStage').innerHTML.includes('📹 ভিডিও পাঠাও'), 'Send Video button must be present');
  assert.ok(getEl('activeDayStage').innerHTML.includes('id="btnVnLiveCam_1_0"'), 'Live Video Camera button must be present');
  assert.ok(getEl('activeDayStage').innerHTML.includes('id="btnAgDone_1_0"'), 'Mark as Done button must be present');
  assert.ok(getEl('activeDayStage').innerHTML.includes('⬜ হয়ে গেছে'), 'Mark as Done button label must be present');
  assert.ok(getEl('activeDayStage').innerHTML.includes('game-sub-drawer'), 'Game subsections must be collapsible');
  assert.ok(!getEl('activeDayStage').innerHTML.includes('type="file"'), 'Gallery photo upload must not exist');
  assert.ok(
    getEl('activeDayStage').innerHTML.indexOf('optional-prompt-drawer') < getEl('activeDayStage').innerHTML.indexOf('id="vnStudio_1_0"'),
    'Interactive Gemini Walkie-Talkie Studio must be inside the collapsible optional-prompt-drawer'
  );
  await generateDynamicAgentStory(1, 'comedy');
  assert.ok(kalyaniWikiVault.dynamicCards['1'] && kalyaniWikiVault.dynamicCards['1'].title_bn);
  await startVoiceNoteRecording(1, 0);
  assert.strictEqual(vnRecordingState.active, true);
  assert.ok(getEl('activeDayStage').innerHTML.includes('id="vnListenProgress_1_0"'), 'Listening progressbar must be shown while Gemini listens');
  assert.ok(getEl('activeDayStage').innerHTML.includes('🟢 জেমিনি এখন মন দিয়ে তোমার কথা শুনছে...'));
  assert.ok(getEl('activeDayStage').innerHTML.includes('বলা শেষ — কল্যাণীকে পাঠাও'));
  vnRecordingState.liveTranscript = 'আমার গোপাল ভাঁড়ের হাসির গল্প খুব ভালো লাগে';
  await finishAndSendVoiceNote(1, 0);
  assert.strictEqual(vnRecordingState.active, false);
  assert.strictEqual((kalyaniThreads['1_0'] || []).length, 1);
  assert.ok(getEl('activeDayStage').innerHTML.includes('✨ জেমিনি (কল্যাণীর ভয়েস মেসেজ উত্তর):'));
  assert.ok(kalyaniThreads['1_0'][0].reply_bn.includes('মা, জেমিনি বলছি—'), 'Reply must clearly identify that it came from Gemini');
  assert.strictEqual(kalyaniWikiVault.pages.length, 7);
  assert.ok(kalyaniWikiVault.pages[0].entries.join(' ').includes('[[হাসি, ভগবান ও প্রিয় গল্প]]'), 'Obsidian-style Ma Wiki Vault must contain [[wikilinks]]');
  assert.ok(getEl('koushikAdminBody').innerHTML.includes('id="maObsidianWikiPanel"'), 'Koushik Admin Panel in Chithi tab must render Obsidian Wiki & API Key controls');
  assert.ok(getEl('koushikAdminBody').innerHTML.includes('id="btnAdminAutoVoice"'), 'Admin Panel must include Auto Voice Play toggle');
  delete doneMap['1_0'];
  delete kalyaniThreads['1_0'];

  // 3. Sequential Day Locking (when unlockAllDaysMode = false): Day 2..21 are locked until Day 1 is finished
  unlockAllDaysMode = false;
  renderPlanView();
  assert.strictEqual(isDayUnlocked(1), true);
  assert.strictEqual(isDayUnlocked(2), false);
  assert.ok(getEl('dayChip_2').innerHTML.includes('🔒 দিন ২'));

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

  // 5. Completing all games of Day 1 unlocks Day 2 (6-game wave) and auto-advances!
  for (let g = 0; g < DAYS_21[0].agendas.length; g++) {
    toggleAgendaDone(1, g);
  }
  assert.strictEqual(isDayUnlocked(2), true);
  assert.strictEqual(isDayUnlocked(3), false);
  assert.strictEqual(curDayNum, 2);
  assert.ok(getEl('activeDayStage').innerHTML.includes('data-count="6"'), 'Day 2 should render a 6-game wave');

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

  // 6. Completing Days 2..21 finishes the 21-day curriculum cleanly!
  for (let d = 2; d <= 21; d++) {
    const dayCount = DAYS_21[d - 1].agendas.length;
    for (let g = 0; g < dayCount; g++) {
      toggleAgendaDone(d, g);
    }
  }
  assert.strictEqual(curDayNum, 21);
  assert.strictEqual(isDayFullyDone(21), true);

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

    def test_anondo_app_vm_rendering_and_inline_audio_controls(self) -> None:
        """Verify anondo.html (🌻 ANONDO) compiles cleanly, renders all game & slide content, and has inline audio controls."""
        k_path = APP_ROOT / "anondo.html"
        self.assertTrue(k_path.is_file(), "anondo.html must exist")
        k_html = k_path.read_text(encoding="utf-8")
        self.assertNotIn("position: fixed;\n      bottom: 0", k_html)
        self.assertIn('id="topPlayBtn"', k_html)
        self.assertIn('id="nowPlayingBar"', k_html)
        self.assertIn('🌻 ANONDO', k_html)
        self.assertIn('id="pageFavicon"', k_html)
        self.assertIn('data-emoji="🌻"', k_html)
        self.assertIn("favicon-anondo.png", k_html)
        self.assertIn("data:image/png;base64,", k_html)
        self.assertIn("Zorba Companion 🌻</title>", k_html)
        self.assertIn("object-fit: contain", k_html)
        self.assertNotIn("object-fit: cover", k_html)

        m = re.search(r"<script>([\s\S]*?)</script>", k_html)
        self.assertIsNotNone(m, "Missing <script> block in anondo.html")

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
assert.ok(els['dayStrip'].innerHTML.includes('Day 1'), 'dayStrip must render English Day 1');
assert.ok(els['gameGrid'].innerHTML.length > 50, 'gameGrid must render game tiles');
assert.ok(els['activeGameStage'].innerHTML.includes('card-top-bar'), 'activeGameStage must render top inline controls');
assert.ok(els['activeGameStage'].innerHTML.includes('Turn 2'), 'activeGameStage must render Turn 2 follow-up prompt');
assert.ok(els['activeGameStage'].innerHTML.includes('agenda-actions'), 'activeGameStage must render bottom actions');
assert.ok(els['letterStage'].innerHTML.includes('btnSlideTopPlay'), 'letterStage must render top slide play button');
assert.ok(els['pillarsContainer'].innerHTML.includes('Guilt Amnesty'), 'pillarsContainer must render 7 English pillars');
"""
        proc = subprocess.run(
            [str(NODE_BIN), "-e", vm_harness],
            input=m.group(1),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, f"koushik.html VM test failed: {proc.stderr}")

    def test_kalyani_gemini_live_video_and_audio_weird_edge_cases(self) -> None:
        html = (APP_ROOT / "kalyani.html").read_text(encoding="utf-8")
        m = re.search(r"<script>([\s\S]*)</script>", html)
        self.assertIsNotNone(m, "Compiled kalyani.html must contain inline <script>")

        vm_harness = r"""
const vm = require('vm');
const assert = require('assert');
const fs = require('fs');
const code = fs.readFileSync(0, 'utf8');

const els = {};
const audioListeners = {};
const docListeners = {};
const testEnv = {
  lastPlayedSrc: '',
  playCallCount: 0,
  fetchRequests: [],
  nextFetchHandler: null,
  mockMediaRecorderShouldHangOnStop: false,
  mockGetUserMediaShouldReject: false,
  mockVideoWidth: 0, // Weird edge case: videoWidth === 0 before first frame metadata!
  stoppedTracksCount: 0
};

function makeEl(id) {
  return {
    id,
    innerHTML: '',
    textContent: '',
    value: '',
    width: 640,
    height: 480,
    videoWidth: testEnv.mockVideoWidth,
    videoHeight: testEnv.mockVideoWidth ? 480 : 0,
    srcObject: null,
    style: { cssText: '', width: '' },
    classList: {
      _set: new Set(),
      add(c) { this._set.add(c); },
      remove(c) { this._set.delete(c); },
      toggle(c, f) {
        if (f === undefined) {
          if (this._set.has(c)) this._set.delete(c);
          else this._set.add(c);
        } else if (f) this._set.add(c);
        else this._set.delete(c);
      },
      contains(c) { return this._set.has(c); }
    },
    setAttribute() {},
    appendChild() {},
    getBoundingClientRect() { return { top: 0 }; },
    scrollIntoView() {},
    focus() {},
    play() {
      testEnv.playCallCount += 1;
      testEnv.lastPlayedSrc = this.src || '';
      return Promise.resolve();
    },
    pause() {},
    load() {},
    addEventListener(ev, fn) { audioListeners[ev] = fn; },
    getContext() {
      return {
        drawImage() {}
      };
    },
    toDataURL(mime) {
      return 'data:' + (mime || 'image/jpeg') + ';base64,ZmFrZV9qcGVnX2ZyYW1l';
    }
  };
}

class MockFileReader {
  readAsDataURL(blob) {
    this.result = 'data:' + (blob.type || 'audio/webm') + ';base64,ZmFrZV9hdWRpb19ieXRlcw==';
    if (this.onloadend) this.onloadend();
  }
}

class MockMediaRecorder {
  constructor(stream, opts) {
    this.stream = stream;
    this.mimeType = (opts && opts.mimeType) || 'audio/webm;codecs=opus';
    this.state = 'inactive';
    this.ondataavailable = null;
    this.onstop = null;
  }
  static isTypeSupported(t) { return true; }
  start() {
    this.state = 'recording';
    if (this.ondataavailable) {
      this.ondataavailable({ data: { size: 128, type: this.mimeType } });
    }
  }
  stop() {
    this.state = 'inactive';
    if (!testEnv.mockMediaRecorderShouldHangOnStop && this.onstop) {
      this.onstop();
    }
  }
}

const store = {
  ma_kalyani_gemini_key_v1: 'AIzaSyFakeTestKeyForUnitTests12345'
};

const ctx = {
  assert,
  process,
  Buffer,
  els,
  audioListeners,
  testEnv,
  console,
  Date,
  Math,
  JSON,
  Promise,
  Array,
  Object,
  String,
  Number,
  Boolean,
  RegExp,
  Error,
  Uint8Array,
  DataView,
  Blob: class {
    constructor(parts, opts) {
      this.parts = parts;
      this.size = 128;
      this.type = (opts && opts.type) || '';
    }
  },
  FileReader: MockFileReader,
  MediaRecorder: MockMediaRecorder,
  URL: {
    createObjectURL() { return 'blob:mock-wav-url'; },
    revokeObjectURL() {}
  },
  atob: (b64) => Buffer.from(b64, 'base64').toString('binary'),
  btoa: (bin) => Buffer.from(bin, 'binary').toString('base64'),
  setTimeout: (fn, ms) => {
    // Immediately invoke short race timers during tests when needed
    if (ms === 450 && testEnv.mockMediaRecorderShouldHangOnStop) {
      fn();
    }
    return 1;
  },
  clearTimeout: () => {},
  setInterval: () => 1,
  clearInterval: () => {},
  alert: () => {},
  confirm: () => true,
  fetch: async (url, opts) => {
    testEnv.fetchRequests.push({ url, opts });
    if (testEnv.nextFetchHandler) {
      return await testEnv.nextFetchHandler(url, opts);
    }
    return {
      ok: true,
      status: 200,
      json: async () => ({})
    };
  },
  window: {
    scrollTo() {},
    addEventListener() {},
    speechSynthesis: { cancel() {}, getVoices() { return []; }, speak() {} }
  },
  navigator: {
    mediaDevices: {
      getUserMedia: async (constraints) => {
        if (testEnv.mockGetUserMediaShouldReject) {
          throw new Error('NotAllowedError: Permission denied');
        }
        return {
          getTracks() {
            return [
              { stop() { testEnv.stoppedTracksCount += 1; } },
              { stop() { testEnv.stoppedTracksCount += 1; } }
            ];
          }
        };
      }
    }
  },
  localStorage: {
    getItem(k) { return Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null; },
    setItem(k, v) { store[k] = String(v); },
    removeItem(k) { delete store[k]; }
  },
  document: {
    body: makeEl('body'),
    getElementById(id) {
      if (!els[id]) els[id] = makeEl(id);
      return els[id];
    },
    querySelector() { return makeEl('qs'); },
    querySelectorAll() { return []; },
    createElement(tag) { return makeEl(tag); },
    addEventListener(ev, fn) { docListeners[ev] = fn; },
    removeEventListener() {}
  }
};
ctx.window.document = ctx.document;
ctx.window.navigator = ctx.navigator;
ctx.window.MediaRecorder = MockMediaRecorder;

const edgeCaseTestSuite = code + `
;(async function() {
  // 1. Edge cases for normalizeAudioMime (critical fix for HTTP 400 audio/webm;codecs=opus)
  assert.strictEqual(normalizeAudioMime('audio/webm;codecs=opus'), 'audio/webm');
  assert.strictEqual(normalizeAudioMime('audio/mp4;codecs=mp4a.40.2'), 'audio/mp4');
  assert.strictEqual(normalizeAudioMime('AUDIO/OGG; codecs=opus'), 'audio/ogg');
  assert.strictEqual(normalizeAudioMime(''), 'audio/webm');
  assert.strictEqual(normalizeAudioMime(null), 'audio/webm');
  assert.strictEqual(normalizeAudioMime('video/webm;codecs=vp8'), 'audio/webm');

  // 2. Edge cases for parseGeminiJsonSafely (markdown fences, prose wrapping, array wrapping, malformed)
  const p1 = parseGeminiJsonSafely('\`\`\`json\\n{"transcriptBn":"হ্যালো","replyBn":"মা, আমি শুনছি"}\\n\`\`\`');
  assert.strictEqual(p1.transcriptBn, 'হ্যালো');
  assert.strictEqual(p1.replyBn, 'মা, আমি শুনছি');

  const p2 = parseGeminiJsonSafely('Here is the JSON response:\\n{"transcriptBn":"গল্প","replyBn":"দারুণ গল্প!"}\\nHope that helps!');
  assert.strictEqual(p2.transcriptBn, 'গল্প');
  assert.strictEqual(p2.replyBn, 'দারুণ গল্প!');

  const p3 = parseGeminiJsonSafely('[{"transcript":"নমস্কার","reply":"নমস্কার মা"}]');
  assert.strictEqual(p3.transcript, 'নমস্কার');
  assert.strictEqual(p3.reply, 'নমস্কার মা');

  assert.strictEqual(parseGeminiJsonSafely('plain text non-json reply'), null);
  assert.strictEqual(parseGeminiJsonSafely('{broken json'), null);
  assert.strictEqual(parseGeminiJsonSafely(''), null);

  // 3. Edge cases for formatGeminiReplyText (clear Gemini attribution without double prefixing)
  assert.ok(formatGeminiReplyText('তোমার কথা শুনে খুব ভালো লাগলো!').startsWith('মা, জেমিনি বলছি—'));
  const alreadyPrefixed = 'মা, জেমিনি বলছি— তুমি কেমন আছো?';
  assert.strictEqual(formatGeminiReplyText(alreadyPrefixed), alreadyPrefixed);

  // 4. Edge cases for pcm24kBase64ToWavUrl (whitespace/newlines in base64, empty string)
  assert.strictEqual(pcm24kBase64ToWavUrl(''), '');
  const wavUrl = pcm24kBase64ToWavUrl('AAAA\\n  AAAA\\tAAAA');
  assert.ok(wavUrl.startsWith('data:audio/wav;base64,UklGR'), 'Must produce valid RIFF WAV base64 data URI');

  // 5. Auto Voice Play ON/OFF setting & Mark as Done button behavior
  assert.strictEqual(autoVoicePlay, true, 'autoVoicePlay defaults to true');
  toggleAutoVoicePlay();
  assert.strictEqual(autoVoicePlay, false, 'toggleAutoVoicePlay switches autoVoicePlay to false');
  assert.strictEqual(localStorage.getItem('ma_kalyani_auto_voice_v1'), 'false');

  const countBeforeDisabledNav = testEnv.playCallCount;
  selectGame(1);
  selectDay(2);
  switchView('letter');
  switchView('pillars');
  switchView('plan');
  handleAudioTrackCompleted('day_main_2');
  assert.strictEqual(testEnv.playCallCount, countBeforeDisabledNav, 'When autoVoicePlay is OFF, navigation and track completion must NOT auto-play audio');

  // Mark as Done button toggles done state & updates green card/tile class
  assert.strictEqual(Boolean(doneMap['2_0']), false);
  toggleAgendaDone(2, 0);
  assert.strictEqual(Boolean(doneMap['2_0']), true, 'toggleAgendaDone must mark game 2_0 as done');
  assert.ok(els['activeDayStage'].innerHTML.includes('done-tile'), 'Active day stage must show done-tile green class when game 2_0 is done');
  selectGame(0);
  assert.ok(els['activeDayStage'].innerHTML.includes('✅ হয়ে গেছে'), 'Active game card must show ✅ হয়ে গেছে when done');

  // Re-enable autoVoicePlay
  toggleAutoVoicePlay();
  assert.strictEqual(autoVoicePlay, true);

  // 6. Live Video + Voice unified one-tap flow (with videoWidth === 0 fallback & audio/webm;codecs=opus strip)
  selectDay(1);
  selectGame(0);
  testEnv.fetchRequests = [];
  testEnv.nextFetchHandler = async (url, opts) => {
    const body = JSON.parse(opts.body);
    if (body.generationConfig && body.generationConfig.responseModalities && body.generationConfig.responseModalities[0] === 'AUDIO') {
      return {
        ok: true,
        status: 200,
        json: async () => ({
          candidates: [{
            content: { parts: [{ inlineData: { data: 'AAAAAAAA' } }] }
          }]
        })
      };
    }
    return {
      ok: true,
      status: 200,
      json: async () => ({
        candidates: [{
          content: {
            parts: [{
              text: JSON.stringify({
                heard_bn: 'এই দেখো আমার ঘরের ফুলদানি',
                reply_bn: 'মা, তোমার ফুলদানিটা কী সুন্দর দেখাচ্ছে!',
                memory_note: 'মা ঘরের ফুলদানি দেখাতে ভালোবাসেন',
                wiki_page: 'joy_gods_and_stories',
                boost_topic: 'comedy'
              })
            }]
          }
        }]
      })
    };
  };

  await toggleCardLiveVideo(1, 0);
  assert.strictEqual(vnLiveCamState.active, true, 'toggleCardLiveVideo must activate live camera');
  assert.strictEqual(vnRecordingState.active, true, 'toggleCardLiveVideo must also start voice recording in one tap');
  assert.ok(els['activeDayStage'].innerHTML.includes('vnListenProgress_1_0'), 'Recording state must display Gemini listening progressbar');
  assert.ok(els['activeDayStage'].innerHTML.includes('জেমিনি এখন মন দিয়ে তোমার কথা শুনছে'), 'Progressbar must tell Ma Gemini is listening now');

  await finishAndSendVoiceNote(1, 0);
  assert.strictEqual(testEnv.fetchRequests.length, 2, 'Must call Gemini multimodal flash + Gemini TTS');
  const multimodalBody = JSON.parse(testEnv.fetchRequests[0].opts.body);
  const sentParts = multimodalBody.contents[0].parts;
  const imagePart = sentParts.find(p => p.inlineData && p.inlineData.mimeType === 'image/jpeg');
  const audioPart = sentParts.find(p => p.inlineData && p.inlineData.mimeType.startsWith('audio/'));
  assert.ok(imagePart && imagePart.inlineData.data.length > 5, 'Must include captured live video JPEG frame even when videoWidth === 0');
  assert.ok(audioPart, 'Must include recorded audio inlineData');
  assert.strictEqual(audioPart.inlineData.mimeType, 'audio/webm', 'Must strip ;codecs=opus from audio mimeType');

  const threads = kalyaniThreads['1_0'] || [];
  assert.strictEqual(threads.length, 1, 'Must save conversation turn in thread');
  assert.ok(threads[0].reply_bn.startsWith('মা, জেমিনি বলছি—'), 'Saved reply must clearly identify Gemini');
  assert.strictEqual(threads[0].has_live_video, true, 'Saved turn must flag has_live_video = true');
  assert.ok(els['activeDayStage'].innerHTML.includes('জেমিনি (কল্যাণীর ভয়েস মেসেজ উত্তর)'), 'Rendered reply card must show Gemini response badge');
  assert.ok(kalyaniMemoryNotes.some(f => f.includes('ফুলদানি')), 'Must learn new fact into Kalyani Memory & Ma Wiki');

  // 7. Weird Edge Case: Live Video sent with 0 seconds of audio (vnRecordingState.active = false, vnLiveCamState.active = true)
  testEnv.fetchRequests = [];
  vnLiveCamState = { active: true, dayNum: 1, agIdx: 0, facingMode: 'environment', lastFrameB64: 'ZmFrZV9jYWNoZWRfZnJhbWU=' };
  vnRecordingState = { active: false, sending: false, dayNum: 1, agIdx: 0, seconds: 0, liveTranscript: '', errorMsg: '' };
  await finishAndSendVoiceNote(1, 0);
  assert.strictEqual(testEnv.fetchRequests.length, 2, 'Live video with 0s audio must still send frame to Gemini');
  assert.strictEqual((kalyaniThreads['1_0'] || []).length, 2, 'Second turn must be appended');

  // 8. Weird Edge Case: Double-click re-entrancy guard when vnRecordingState.sending === true
  testEnv.fetchRequests = [];
  vnRecordingState.sending = true;
  await finishAndSendVoiceNote(1, 0);
  assert.strictEqual(testEnv.fetchRequests.length, 0, 'Must ignore duplicate finishAndSendVoiceNote calls while sending === true');
  vnRecordingState.sending = false;

  // 9. Weird Edge Case: Switching games/days while camera & mic are active must stop hardware tracks
  const tracksBefore = testEnv.stoppedTracksCount;
  await toggleCardLiveVideo(1, 0);
  assert.strictEqual(vnLiveCamState.active, true);
  selectGame(1);
  assert.strictEqual(vnLiveCamState.active, false, 'Switching game must deactivate live camera');
  assert.strictEqual(vnRecordingState.active, false, 'Switching game must deactivate voice recording');
  assert.ok(testEnv.stoppedTracksCount > tracksBefore, 'Switching game must stop active camera/mic MediaStream tracks');

  // 10. Weird Edge Case: Camera permission denied (NotAllowedError)
  testEnv.mockGetUserMediaShouldReject = true;
  await toggleCardLiveVideo(1, 1);
  assert.strictEqual(vnLiveCamState.active, false, 'Permission denial must keep live camera inactive');
  assert.ok(vnRecordingState.errorMsg.includes('ক্যামেরা চালু করা যায়নি'), 'Permission denial must show helpful Bengali message');
  testEnv.mockGetUserMediaShouldReject = false;

  // 11. Weird Edge Case: MediaRecorder.stop() hangs and never fires onstop (450ms race timeout recovery)
  testEnv.mockMediaRecorderShouldHangOnStop = true;
  await startVoiceNoteRecording(1, 1);
  await finishAndSendVoiceNote(1, 1);
  assert.strictEqual(vnRecordingState.sending, false, 'Must recover cleanly via timeout race even if MediaRecorder.onstop hangs');
  testEnv.mockMediaRecorderShouldHangOnStop = false;

  // 12. Story Listen Button: Instant Clicked Loading State + Small Chunks + Parallel Pre-Fetch + Seamless Chaining
  const sampleStory = 'গোপাল ভাঁড় ও মিষ্টি জলের কুঁজো। একবার গরমকালে মহারাজ কৃষ্ণচন্দ্র গোপাল ভাঁড়কে বললেন— গোপাল, এমন জল খাওয়াও যা অমৃতের মতো মিষ্টি লাগে! গোপাল রাজামশাইকে বাগানের চারপাশে হাঁটিয়ে মাটির কুঁজোর ঠান্ডা জল দিল। রাজামশাই খেয়ে খুশি হয়ে হাসলেন।';
  const chunks = splitBengaliStoryIntoChunks(sampleStory);
  assert.ok(chunks.length >= 3, 'Multi-sentence story must split into small chunks for fast first-audio start');
  assert.ok(chunks[0].length <= 60, 'First chunk must be short so Gemini TTS responds in ~0.8s');

  let resolveChunk0 = null;
  let ttsCallCount = 0;
  testEnv.nextFetchHandler = (url, opts) => {
    ttsCallCount += 1;
    if (ttsCallCount === 1) {
      return new Promise((resolve) => {
        resolveChunk0 = () => resolve({
          ok: true,
          status: 200,
          json: async () => ({
            candidates: [{ content: { parts: [{ inlineData: { data: 'AAAAAAAA' } }] } }]
          })
        });
      });
    }
    return Promise.resolve({
      ok: true,
      status: 200,
      json: async () => ({
        candidates: [{ content: { parts: [{ inlineData: { data: 'BBBBBBBB' } }] } }]
      })
    });
  };

  const delightBtn = document.getElementById('btnDelightPlay_3');
  delightBtn.setAttribute('data-default-label', '🔊 শোনো');
  const playStoryPromise = playDelightStoryAudio(3);

  // Immediately after clicking, before Chunk 0 finishes network fetch:
  assert.strictEqual(activeAudioLoading, true, 'Must set activeAudioLoading = true immediately on click');
  assert.ok(delightBtn.innerHTML.includes('⏳ জেমিনি পড়তে শুরু করছে'), 'Button must immediately show that it was clicked and Gemini is about to read');
  assert.ok(delightBtn.classList.contains('loading-audio'), 'Button must have loading-audio class while preparing');
  assert.ok(els['nowPlayingBar'].classList.contains('visible'), 'Top bar must be visible immediately on click');
  assert.ok(els['npTime'].textContent.includes('জেমিনি তোমার জন্য পড়তে শুরু করছে'), 'Top bar must tell Ma Gemini is starting to read');
  assert.ok(ttsCallCount >= 2, 'Must fire parallel lookahead pre-fetching for chunk 0 and chunk 1+ immediately');

  // Now resolve Chunk 0 and verify playback starts immediately while subsequent chunks are already cached
  resolveChunk0();
  await playStoryPromise;
  assert.strictEqual(activeAudioLoading, false, 'Once Chunk 0 resolves, loading indicator must clear');
  assert.strictEqual(delightBtn.innerHTML, '⏸️ থামাও', 'Button must transition to ⏸️ থামাও once Chunk 0 starts playing');
  assert.ok(activeChunkSession && activeChunkSession.idx === 0, 'Must be playing Chunk 0');
  assert.ok(Boolean(vnAudioCache['delight_3_c1']), 'Chunk 1 must already be pre-fetched in vnAudioCache');

  // Simulate Chunk 0 finishing -> must seamlessly chain into pre-fetched Chunk 1 without extra TTS network calls!
  const callsBeforeNextChunk = ttsCallCount;
  audioListeners['ended']();
  assert.strictEqual(activeChunkSession.idx, 1, 'Ending Chunk 0 must advance to Chunk 1');
  assert.strictEqual(ttsCallCount, callsBeforeNextChunk, 'Chunk 1 must play from pre-fetched cache with zero wait');
})().catch(err => {
  console.error(err);
  process.exit(1);
});
`;
vm.runInNewContext(edgeCaseTestSuite, ctx, {filename: 'kalyani-edge-cases.js'});
"""
        proc = subprocess.run(
            [str(NODE_BIN), "-e", vm_harness],
            input=m.group(1),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, f"Kalyani weird edge-cases VM test failed: {proc.stderr}")

    def test_jhalak_dopamine_reels_app_and_vm_interactions(self) -> None:
        """Verify jhalak.html (✨ ঝলক) compiles cleanly with long-page scroll, L/R nav, 9 categories, sticky multi-like, and VM checks."""
        jh_path = APP_ROOT / "jhalak.html"
        self.assertTrue(jh_path.is_file(), "jhalak.html must exist")
        jh_html = jh_path.read_text(encoding="utf-8")
        # 1. Renamed to just ঝলক, no বায়োস্কোপ, no Kalyani link, no header TV tab
        self.assertIn("<title>✨ ঝলক</title>", jh_html)
        self.assertNotIn("বায়োস্কোপ", jh_html)
        self.assertNotIn('href="kalyani.html"', jh_html)
        self.assertNotIn('id="tabJhTv"', jh_html)
        # 2. Category Dropdown + Left/Right page navigation + Translucent Sticky Like button
        self.assertIn('id="btnJhCategoryDropdown"', jh_html)
        self.assertIn('id="jhCategoryDropdownMenu"', jh_html)
        self.assertIn('id="btnJhPrevPage"', jh_html)
        self.assertIn('id="btnJhNextPage"', jh_html)
        self.assertIn('id="jhStickyLikeBtn"', jh_html)
        self.assertIn("backdrop-filter: blur(10px)", jh_html)
        # 3. Settings controls: Auto-Reels, Auto-Voice, Single/Multi Category Select, Show Like Count, Chithi, Category Stats
        for sid in (
            "btnJhSettings",
            "jhSettingsDrawer",
            "btnJhAutoFlow",
            "btnJhAutoVoice",
            "btnJhCatSelectMode",
            "btnJhShowLikeCount",
            "btnJhOpenChithi",
            "jhCategoryStatsBox",
        ):
            self.assertIn(f'id="{sid}"', jh_html)

        m = re.search(r"<script>([\s\S]*?)</script>", jh_html)
        self.assertIsNotNone(m, "Missing <script> block in jhalak.html")

        vm_harness = r"""
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const code = fs.readFileSync(0, 'utf8');
const els = {};
function el(id) {
  if (!els[id]) {
    els[id] = {
      id, className: '', innerHTML: '', textContent: '', style: {}, src: '', scrollTop: 0,
      classList: {
        add(c) { if (!els[id].className.includes(c)) els[id].className = (els[id].className + ' ' + c).trim(); },
        remove(c) { els[id].className = els[id].className.replace(c, '').trim(); },
        toggle(c, b) { if (b) this.add(c); else this.remove(c); },
        contains(c) { return els[id].className.includes(c); }
      },
      querySelector: () => ({ textContent: '' }),
      addEventListener() {},
      scrollIntoView() {}
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
    createElement: () => ({ style: {}, className: '', textContent: '' })
  },
  localStorage: { getItem: () => null, setItem: () => {} },
  setTimeout, clearTimeout, console, assert, el
};
const suite = code + `
;(function() {
  // 1. All 9 categories (all + 8 content categories including gods, english, hindi, music, tv)
  const catIds = JHALAK_CATEGORIES.map(c => c.id);
  assert.deepStrictEqual(catIds, ['all', 'gods', 'laugh', 'calm', 'curiosity', 'music', 'english', 'hindi', 'tv']);
  catIds.forEach(cid => {
    assert.ok(JHALAK_CATEGORY_COUNTS[cid] > 0, 'Category ' + cid + ' must have non-zero content count');
  });

  // 2. Nonsensical tech_65 phone/camera tutorials and raw Gemini prompts removed; every page has multi-section long content
  assert.ok(ALL_JHALAK_REELS.every(r => Array.isArray(r.sections) && r.sections.length >= 2), 'Every page must have rich multi-section content');
  assert.ok(ALL_JHALAK_REELS.every(r => !JSON.stringify(r.sections).includes('জেমিনি, শোনো—')), 'Must strip raw Gemini voice-assistant prompts');

  // 3. Songs category has inspiration & right question hook for understanding song meaning
  const musicCards = ALL_JHALAK_REELS.filter(r => r.vibe === 'music');
  assert.strictEqual(musicCards.length, 21);
  assert.ok(musicCards.every(m => m.sections.some(s => s.heading_bn.includes('গানের আসল অর্থ বোঝার সঠিক প্রশ্ন'))));

  // 4. Left / Right page navigation (stepJhalakReel)
  renderJhalakReelStream();
  syncJhSettingsButtonsUI();
  assert.strictEqual(jhCurrentIdx, 0);
  stepJhalakReel(1, false);
  assert.strictEqual(jhCurrentIdx, 1, 'Right navigation must advance to next page');
  stepJhalakReel(-1, false);
  assert.strictEqual(jhCurrentIdx, 0, 'Left navigation must return to previous page');

  // 5. Category Dropdown: Single-Select by default, toggleable to Multi-Select in Settings
  assert.strictEqual(jhMultiSelectCategories, false, 'Default category mode must be Single-Select');
  filterJhalakChannel('gods');
  assert.strictEqual(jhSelectedChannels.has('gods') && jhSelectedChannels.size === 1, true);
  filterJhalakChannel('music');
  assert.strictEqual(jhSelectedChannels.has('music') && jhSelectedChannels.size === 1, true, 'In Single-Select mode, choosing music replaces gods');

  toggleJhCategorySelectMode();
  assert.strictEqual(jhMultiSelectCategories, true, 'Settings toggle must enable Multi-Select mode');
  filterJhalakChannel('gods');
  assert.strictEqual(jhSelectedChannels.has('music') && jhSelectedChannels.has('gods'), true, 'In Multi-Select mode, both music and gods stay active');
  filterJhalakChannel('all');
  assert.strictEqual(jhFilteredReels.length, ALL_JHALAK_REELS.length);

  // 6. Translucent Sticky Like Button: same content can be liked several times + like count visibility toggle
  const firstId = jhFilteredReels[0].id;
  assert.strictEqual(getReelLikeCount(firstId), 0);
  likeCurrentJhalakReel();
  likeCurrentJhalakReel();
  likeCurrentJhalakReel();
  assert.strictEqual(getReelLikeCount(firstId), 3, 'Same content must support being liked multiple times');
  assert.ok(el('jhStickyLikeBtn').innerHTML.includes('৩'), 'When jhShowLikeCount is true, sticky like button shows count ৩');

  toggleJhShowLikeCount();
  assert.strictEqual(jhShowLikeCount, false);
  assert.ok(!el('jhStickyLikeBtn').innerHTML.includes('jhStickyLikeCount'), 'When jhShowLikeCount is false, like count badge is hidden');
  assert.ok(el('jhCategoryStatsBox').innerHTML.includes('পাতা'), 'Category stats must display content counts');
})();
`;
vm.runInNewContext(suite, ctx, {filename: 'jhalak-bundle.js'});
"""
        proc = subprocess.run(
            [str(NODE_BIN), "-e", vm_harness],
            input=m.group(1),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, f"Jhalak VM test failed: {proc.stderr}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
