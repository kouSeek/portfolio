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
        self.assertIn('href="jhalak.html"', hub_html)
        self.assertIn('href="zorba.html"', hub_html)
        self.assertIn('href="kalyani.html"', hub_html)
        self.assertIn('href="anondo.html"', hub_html)
        self.assertIn('id="pageFavicon"', hub_html)
        self.assertIn('data-emoji="🪷"', hub_html)
        self.assertIn("favicon-hub.png", hub_html)
        self.assertIn("data:image/png;base64,", hub_html)
        self.assertIn("<title>AI Companion — Kalyani (Ma) & Anondo (Koushik) 🪷</title>", hub_html)
        self.assertIn("navigator.wakeLock.request", hub_html)

        idx_html_path = APP_ROOT / "kalyani.html"
        self.assertTrue(idx_html_path.is_file())
        self.assertFalse((APP_ROOT / "ma-presentation.html").exists(), "Duplicate ma-presentation.html must not exist")

        ma_html = idx_html_path.read_text(encoding="utf-8")
        self.assertIn('id="pageFavicon"', ma_html)
        self.assertIn('data-emoji="🌸"', ma_html)
        self.assertIn("favicon-kalyani.png", ma_html)
        self.assertIn("data:image/png;base64,", ma_html)
        self.assertIn("<title>কল্যাণী — আজকের খেলা ও চিঠি 🌸</title>", ma_html)
        self.assertIn("navigator.wakeLock.request", ma_html)

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
  navigator: {
    wakeLock: {
      requested: 0,
      request(type) {
        if (type === 'screen') this.requested += 1;
        return Promise.resolve({ released: false, addEventListener() {} });
      }
    },
    serviceWorker: { register: () => Promise.resolve(), ready: Promise.resolve({ showNotification: () => {} }) }
  },
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
assert.strictEqual(navigator.wakeLock.requested >= 1, true, 'Screen wake lock must be requested on app open');

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
  assert.ok(getEl('tvHubStage').innerHTML.includes('স্বর্ণযুগের হিন্দি গান'));
  assert.ok(getEl('tvHubStage').innerHTML.includes('মিষ্টি ইংরেজি গান'));
  assert.ok(renderKalyaniInlineRichText('**সাহস**, *আদর*, [[হাসির ঝুলি|আনন্দ]]').includes('<strong class="kal-md-strong">সাহস</strong>'));
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
  navigator: {
    wakeLock: {
      requested: 0,
      request(type) {
        if (type === 'screen') this.requested += 1;
        return Promise.resolve({ released: false, addEventListener() {} });
      }
    },
    clipboard: { writeText: () => {} }
  },
  setTimeout, clearTimeout, setInterval, clearInterval, console, assert, audioListeners
};
const scriptAndTests = code + `
;(function() {
  assert.strictEqual(navigator.wakeLock.requested >= 1, true, 'Anondo must request screen wake lock on load');
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
        """Verify jhalak.html (✨ ঝলক) compiles cleanly with 11 categories (3 song sections by language), 119 pages, neuro-inclusive UX, Markdown/LaTeX rendering, and VM checks."""
        jh_path = APP_ROOT / "jhalak.html"
        self.assertTrue(jh_path.is_file(), "jhalak.html must exist")
        jh_html = jh_path.read_text(encoding="utf-8")
        # 1. Renamed to just ঝলক, no বায়োস্কোপ, no Kalyani link, no header TV tab, no Prev/Next buttons, no top page counter
        self.assertIn("<title>✨ ঝলক</title>", jh_html)
        self.assertIn('<meta name="mobile-web-app-capable" content="yes" />', jh_html)
        self.assertIn('<meta name="apple-mobile-web-app-capable" content="yes" />', jh_html)
        self.assertIn('<link rel="manifest" href="jhalak-manifest.json" />', jh_html)
        self.assertIn("favicon-jhalak.png", jh_html)
        self.assertIn("favicon-jhalak.ico", jh_html)
        self.assertIn("navigator.serviceWorker.register('kalyani-sw.js')", jh_html)
        self.assertIn("navigator.wakeLock.request", jh_html)
        self.assertTrue((APP_ROOT / "jhalak-manifest.json").is_file(), "jhalak-manifest.json must exist")
        self.assertTrue((APP_ROOT / "assets" / "icons" / "favicon-jhalak-192.png").is_file())
        self.assertTrue((APP_ROOT / "assets" / "icons" / "favicon-jhalak-512.png").is_file())
        self.assertNotIn("বায়োস্কোপ", jh_html)
        self.assertNotIn('href="kalyani.html"', jh_html)
        self.assertNotIn('id="tabJhTv"', jh_html)
        self.assertNotIn('id="btnJhPrevPage"', jh_html)
        self.assertNotIn('id="btnJhNextPage"', jh_html)
        self.assertNotIn('id="jhPageCounterBadge"', jh_html)
        self.assertNotIn("jh-bottom-lr-nav", jh_html)
        # 2. Category Dropdown + Header Listen button + Neuro-Inclusive UX + Markdown/LaTeX rendering + Sideways animations
        self.assertIn('id="btnJhCategoryDropdown"', jh_html)
        self.assertIn('id="jhCategoryDropdownMenu"', jh_html)
        self.assertIn('id="btnJhHeaderListen"', jh_html)
        self.assertIn('id="btnJhHeaderStop"', jh_html)
        self.assertIn('id="jhTopAudioProgressFill"', jh_html)
        self.assertIn("jh-pull-progress-fill", jh_html)
        self.assertIn("jh-dbltap-voice-toast", jh_html)
        self.assertIn("body.jh-audio-playing", jh_html)
        self.assertIn("jh-tts-sentence", jh_html)
        self.assertIn("jh-math-inline", jh_html)
        self.assertIn("jh-inline-code", jh_html)
        self.assertIn("jh-wikilink-pill", jh_html)
        self.assertIn("jh-md-em", jh_html)
        self.assertIn("jh-md-strong", jh_html)
        self.assertNotIn("activeEl.scrollIntoView", jh_html)
        self.assertNotIn('<header class="jh-topbar">', jh_html)
        self.assertIn("jh-floating-gear-btn", jh_html)
        self.assertLess(
            jh_html.index('id="jhSettingsDrawer"'),
            jh_html.index('id="jhCategoryDropdownWrap"'),
            "Category dropdown must live inside the Settings drawer so the entire screen is taken by content only",
        )
        self.assertIn("jh-page-bottom-actions", jh_html)
        self.assertIn("jh-slide-anim-next", jh_html)
        self.assertIn("jh-slide-anim-prev", jh_html)
        self.assertIn("jhProSidewaysInNext", jh_html)
        self.assertIn("jhProSidewaysOutLeft", jh_html)
        self.assertIn('id="jhStickyLikeBtn"', jh_html)
        self.assertIn("backdrop-filter: blur(10px)", jh_html)
        # 3. Settings controls: Auto-Reels, Auto-Voice, Single/Multi Category Select, Show Like Count, Chithi, Category Stats, Admin Done/Likes control
        for sid in (
            "btnJhSettings",
            "jhSettingsDrawer",
            "btnJhAutoFlow",
            "btnJhAutoVoice",
            "btnJhCatSelectMode",
            "btnJhShowLikeCount",
            "btnJhOpenChithi",
            "jhCategoryStatsBox",
            "jhAdminControlSection",
            "jhAdminItemsList",
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
      id, className: '', innerHTML: '', textContent: '', value: '', style: {}, src: '', scrollTop: 0,
      classList: {
        add(c) { if (!els[id].className.includes(c)) els[id].className = (els[id].className + ' ' + c).trim(); },
        remove(c) { els[id].className = els[id].className.replace(c, '').trim(); },
        toggle(c, b) { if (b) this.add(c); else this.remove(c); },
        contains(c) { return els[id].className.includes(c); }
      },
      querySelector: () => ({ textContent: '', classList: { remove() {}, add() {} }, offsetWidth: 100 }),
      play: () => Promise.resolve(),
      pause() {},
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
  setTimeout: () => 1, clearTimeout: () => {}, setInterval: () => 1, clearInterval: () => {}, console, assert, el
};
const suite = code + `
;(function() {
  // 1. All 11 categories (all + 3 separate song sections by language + 7 content categories = 119 zero-filler pages)
  const catIds = JHALAK_CATEGORIES.map(c => c.id);
  assert.deepStrictEqual(catIds, ['all', 'songs_bn', 'songs_hi', 'songs_en', 'gods', 'laugh', 'calm', 'curiosity', 'english', 'hindi', 'tv']);
  assert.strictEqual(ALL_JHALAK_REELS.length, 119, 'Total cleaned Jhalak pages must be 119');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['songs_bn'], 12, 'Bengali Songs category must have 12 verified songs');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['songs_hi'], 8, 'Hindi Songs category must have 8 verified songs');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['songs_en'], 8, 'English Songs category must have 8 verified songs');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['english'], 10, 'English conversation category must have 10 non-repetitive pages');
  catIds.forEach(cid => {
    assert.ok(JHALAK_CATEGORY_COUNTS[cid] >= 8, 'Category ' + cid + ' must have at least 8 rich pages');
  });

  // 2. Every page has multi-section long content, zero Day/progression burden labels, zero hallucinated lyrics, and points to its dedicated full-page audio URL
  const bannedProgressionPhrases = ['গত সপ্তাহে', 'প্রথম সপ্তাহে', 'দিন ২-এ শেখা', 'দিন ৪-এর', 'সপ্তম দিনের শেষে', 'একুশ দিন আগে'];
  assert.ok(ALL_JHALAK_REELS.every(r => Array.isArray(r.sections) && r.sections.length >= 2), 'Every page must have rich multi-section content');
  assert.ok(ALL_JHALAK_REELS.every(r => !JSON.stringify(r.sections).includes('জেমিনি, শোনো—')), 'Must strip raw Gemini voice-assistant prompts');
  assert.ok(ALL_JHALAK_REELS.every(r => r.audio_url === 'https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/audio/jhalak/reels/' + r.id + '.mp3' && r.story_end === 0), 'Every page must point to its dedicated full-page MP3 with story_end === 0');
  ALL_JHALAK_REELS.forEach(r => {
    const ser = JSON.stringify(r);
    bannedProgressionPhrases.forEach(bp => {
      assert.ok(!ser.includes(bp), 'Progression burden phrase "' + bp + '" must not appear in Jhalak card ' + r.id);
    });
  });

  // 3. Separate Bengali, Hindi, and English song categories have verified songs and unique Q&As
  const bnSongs = ALL_JHALAK_REELS.filter(r => r.vibe === 'songs_bn');
  const hiSongs = ALL_JHALAK_REELS.filter(r => r.vibe === 'songs_hi');
  const enSongs = ALL_JHALAK_REELS.filter(r => r.vibe === 'songs_en');
  assert.strictEqual(bnSongs.length, 12);
  assert.strictEqual(hiSongs.length, 8);
  assert.strictEqual(enSongs.length, 8);
  assert.ok(bnSongs.some(s => s.title_bn.includes('একদিন পাখি উড়ে যাবে') && s.sections[0].body_bn.includes('কিশোর কুমারের')));
  assert.ok(bnSongs.some(s => s.title_bn.includes('একটা গান লিখো আমার জন্য') && s.sections[0].body_bn.includes('প্রতিমা বন্দ্যোপাধ্যায়ের')));

  // 4. No page counts on top dropdown button + randomized next page + history back navigation + slide animations
  renderJhalakReelStream();
  syncJhSettingsButtonsUI();
  assert.strictEqual(jhHistoryStack.length, 1, 'Initial history stack must contain exactly 1 page so first page never repeats on first swipe');
  assert.strictEqual(jhHistoryPos, 0, 'Initial history position must be 0');
  assert.strictEqual(getSelectedCategorySummaryLabel(), '✨ সব ▾', 'Top category dropdown must not show page count');
  assert.ok(!el('jhCategoryDropdownMenu').innerHTML.includes('jh-cat-count-pill'), 'Category dropdown menu options must not display item counts');
  assert.ok(el('jhReelsViewport').innerHTML.includes('jh-page-bottom-actions'), 'Done and Like buttons must sit at the bottom of each page content');
  assert.ok(el('jhReelsViewport').innerHTML.includes('class="jh-tts-sentence"'), 'Body paragraphs must wrap sentences in .jh-tts-sentence spans');
  assert.ok(el('jhReelsViewport').innerHTML.includes('jh-curiosity-box revealed'), 'Curiosity takeaway box must be open by default with zero tap-to-reveal friction');
  const startId = jhFilteredReels[jhCurrentIdx].id;
  stepJhalakReel(1, false);
  const nextId = jhFilteredReels[jhCurrentIdx].id;
  assert.notStrictEqual(nextId, startId, 'Advancing must pick a randomized next page');
  assert.strictEqual(jhLastSlideDir, 'next', 'Advancing must set slide direction to next');
  assert.ok(el('jhReelsViewport').innerHTML.includes('jh-slide-anim-next'), 'Rendered card must have jh-slide-anim-next class');
  assert.ok(el('jhReelsViewport').innerHTML.includes('jh-outgoing-ghost out-left'), 'Advancing must render outgoing ghost card sliding left');
  stepJhalakReel(-1, false);
  assert.strictEqual(jhFilteredReels[jhCurrentIdx].id, startId, 'Stepping back must return to previous page in history stack');
  assert.strictEqual(jhLastSlideDir, 'prev', 'Stepping back must set slide direction to prev');
  assert.ok(el('jhReelsViewport').innerHTML.includes('jh-slide-anim-prev'), 'Rendered card must have jh-slide-anim-prev class');
  assert.ok(el('jhReelsViewport').innerHTML.includes('jh-outgoing-ghost out-right'), 'Stepping back must render outgoing ghost card sliding right');
  const articleTagsAfterMultiSteps = el('jhReelsViewport').innerHTML.match(/<article /g) || [];
  assert.strictEqual(articleTagsAfterMultiSteps.length, 1, 'Viewport must never join or accumulate multiple <article> pages');
  const stageBlocksAfterMultiSteps = el('jhReelsViewport').innerHTML.match(/class="jh-card-stage"/g) || [];
  assert.strictEqual(stageBlocksAfterMultiSteps.length, 2, 'Viewport must contain at most 1 outgoing ghost stage and 1 active stage');

  // 5. Mark as Done button excludes page from future reels, and Admin Settings can change Done & Likes counts
  const cardToDone = jhFilteredReels[jhCurrentIdx];
  assert.strictEqual(getReelDoneCount(cardToDone.id), 0);
  markCurrentJhalakReelDone();
  assert.strictEqual(getReelDoneCount(cardToDone.id), 1, 'Marking done must set done count to 1');
  assert.strictEqual(jhFilteredReels.length, 118, 'Done item must be excluded from active reels pool');
  assert.ok(!jhFilteredReels.some(r => r.id === cardToDone.id), 'Done card must not appear in future reels');

  // Admin Settings: restore Done count to 0 and adjust Likes count
  adjustReelDoneCount(cardToDone.id, -1);
  assert.strictEqual(getReelDoneCount(cardToDone.id), 0, 'Admin control must allow decreasing Done count back to 0');
  assert.strictEqual(jhFilteredReels.length, 119, 'Restoring Done count to 0 brings item back into reels pool');
  adjustReelLikeCount(cardToDone.id, 5);
  assert.strictEqual(getReelLikeCount(cardToDone.id), 5, 'Admin control must allow changing Likes count');
  setReelLikeCount(cardToDone.id, 2);
  assert.strictEqual(getReelLikeCount(cardToDone.id), 2, 'Admin direct input must set exact Likes count');

  // 6. Category Dropdown: Single-Select by default, toggleable to Multi-Select in Settings
  assert.strictEqual(jhMultiSelectCategories, false, 'Default category mode must be Single-Select');
  filterJhalakChannel('gods');
  assert.strictEqual(jhSelectedChannels.has('gods') && jhSelectedChannels.size === 1, true);
  assert.strictEqual(getSelectedCategorySummaryLabel(), '🪷 ভগবান ▾', 'Single category label has no count on top');
  filterJhalakChannel('songs_bn');
  assert.strictEqual(jhSelectedChannels.has('songs_bn') && jhSelectedChannels.size === 1, true, 'In Single-Select mode, choosing songs_bn replaces gods');

  toggleJhCategorySelectMode();
  assert.strictEqual(jhMultiSelectCategories, true, 'Settings toggle must enable Multi-Select mode');
  filterJhalakChannel('gods');
  assert.strictEqual(jhSelectedChannels.has('songs_bn') && jhSelectedChannels.has('gods'), true, 'In Multi-Select mode, both songs_bn and gods stay active');
  filterJhalakChannel('all');
  assert.strictEqual(jhFilteredReels.length, ALL_JHALAK_REELS.length);

  // 7. Translucent Sticky Like Button: same content can be liked several times + like count visibility toggle
  const currentCardId = jhFilteredReels[jhCurrentIdx].id;
  setReelLikeCount(currentCardId, 0);
  likeCurrentJhalakReel();
  likeCurrentJhalakReel();
  likeCurrentJhalakReel();
  assert.strictEqual(getReelLikeCount(currentCardId), 3, 'Same content must support being liked multiple times');
  assert.ok(el('jhStickyLikeBtn').innerHTML.includes('৩'), 'When jhShowLikeCount is true, sticky like button shows count ৩');

  toggleJhShowLikeCount();
  assert.strictEqual(jhShowLikeCount, false);
  assert.ok(!el('jhStickyLikeBtn').innerHTML.includes('jhStickyLikeCount'), 'When jhShowLikeCount is false, like count badge is hidden');
  assert.ok(el('jhCategoryStatsBox').innerHTML.includes('১১৯টি পাতা'), 'Category stats must display simple ১১৯টি পাতা without ১১৯/১১৯টি fraction');
  assert.ok(!el('jhCategoryStatsBox').innerHTML.includes('১১৯/১১৯টি পাতা'), 'Category stats must not show redundant ১১৯/১১৯টি পাতা fraction');
  assert.ok(el('jhAdminItemsList').innerHTML.includes('id="jhAdminCatSelect"'), 'Admin control must have category selector dropdown');
  assert.ok(el('jhAdminItemsList').innerHTML.includes('id="jhAdminItemSelect"'), 'Admin control must have item selector dropdown within category');
  assert.ok(!el('jhAdminItemsList').innerHTML.includes('বিভাগের ডান রিসেট'), 'Admin panel must not render the 4-button category bulk section');
  assert.ok(!el('jhReelsViewport').innerHTML.includes('jh-card-top'), 'Category badge must sit inline at the start of the title without a separate .jh-card-top row');
  assert.ok(/<h2[^>]*class="jh-hook-title"><span class="jh-vibe-badge">/.test(el('jhReelsViewport').innerHTML), 'Category badge must be placed right at the beginning of the title h2');
  const adminRowMatches = el('jhAdminItemsList').innerHTML.match(/class="jh-admin-row /g) || [];
  assert.strictEqual(adminRowMatches.length, 1, 'Admin panel must render only the 1 selected item row (no huge list)');

  // 8b. Listen button Play -> Pause -> Resume -> Stop lifecycle + Double-Tap anywhere on content
  stopJhAudio();
  assert.strictEqual(el('btnJhHeaderListen').textContent, '🔊 শোনো');
  assert.strictEqual(el('btnJhHeaderStop').style.display, 'none', 'Stop button hidden when idle');
  playReelAudioAtIndex();
  assert.strictEqual(jhAudioPlaying, true);
  assert.strictEqual(jhAudioPaused, false);
  assert.strictEqual(el('btnJhHeaderListen').textContent, '⏸️ বিরতি', 'While playing, Listen button shows Pause');
  assert.strictEqual(el('btnJhHeaderStop').style.display, 'inline-flex', 'While playing, Stop button is visible');
  syncJhWordHighlightToTime(4.0, 20.0);
  const pausedWordIdx = jhActiveWordIdx;
  assert.ok(pausedWordIdx > 0);
  playReelAudioAtIndex();
  assert.strictEqual(jhAudioPlaying, false, 'Clicking Listen while playing pauses audio');
  assert.strictEqual(jhAudioPaused, true, 'Paused flag set to true');
  assert.strictEqual(el('btnJhHeaderListen').textContent, '▶️ চালাও', 'While paused, Listen button shows Resume');
  assert.strictEqual(el('btnJhHeaderStop').style.display, 'inline-flex', 'While paused, Stop button remains visible');
  assert.strictEqual(jhActiveWordIdx, pausedWordIdx, 'Pausing preserves active word highlight index');
  playReelAudioAtIndex();
  assert.strictEqual(jhAudioPlaying, true, 'Clicking Listen while paused resumes audio');
  assert.strictEqual(jhAudioPaused, false);
  assert.strictEqual(el('btnJhHeaderListen').textContent, '⏸️ বিরতি');
  stopJhAudio();
  assert.strictEqual(jhAudioPlaying, false);
  assert.strictEqual(jhAudioPaused, false);
  assert.strictEqual(el('btnJhHeaderListen').textContent, '🔊 শোনো', 'Stopping resets Listen button to Play');
  assert.strictEqual(el('btnJhHeaderStop').style.display, 'none', 'Stopping hides Stop button');
  assert.strictEqual(jhActiveWordIdx, -1, 'Stopping clears active word highlight');

  jhLastDoubleTapToggleMs = 0;
  assert.strictEqual(handleJhContentDoubleTap({ target: { tagName: 'P', className: 'jh-sec-para' }, clientX: 180, clientY: 320 }, 'reel'), true, 'Double-tap on Jhalak paragraph starts voice');
  assert.strictEqual(jhAudioPlaying, true);
  stopJhAudio();

  // 8. Category-level Done & Likes bulk controls in Admin
  setCategoryDoneState('tv', 1);
  assert.strictEqual(ALL_JHALAK_REELS.filter(r => r.vibe === 'tv').every(r => isReelDone(r.id)), true, 'setCategoryDoneState(tv, 1) must mark all TV items done');
  setCategoryDoneState('tv', 0);
  assert.strictEqual(ALL_JHALAK_REELS.filter(r => r.vibe === 'tv').every(r => !isReelDone(r.id)), true, 'setCategoryDoneState(tv, 0) must reset all TV items');
  adjustCategoryLikeCounts('tv', 2);
  assert.strictEqual(ALL_JHALAK_REELS.filter(r => r.vibe === 'tv').every(r => getReelLikeCount(r.id) >= 2), true, 'adjustCategoryLikeCounts must add likes to category');
  resetCategoryLikeCounts('tv');
  assert.strictEqual(ALL_JHALAK_REELS.filter(r => r.vibe === 'tv').every(r => getReelLikeCount(r.id) === 0), true, 'resetCategoryLikeCounts must clear likes in category');

  // 9. KORTEX-inspired real-time word-by-word read-aloud highlighting across reel pages and Chithi letter slides
  renderJhalakReelStream();
  assert.ok(typeof JHALAK_AUDIO_TIMINGS === 'object' && Object.keys(JHALAK_AUDIO_TIMINGS).length === 119, 'All 119 Jhalak reels must have acoustic duration and silence maps');
  assert.ok(el('jhReelsViewport').innerHTML.includes('class="jh-tts-word"'), 'Reel page must wrap spoken words in .jh-tts-word spans');
  assert.ok(jhCurrentWordTimings.length > 20, 'Each reel page must build weighted word timing spans');
  assert.ok(jhCurrentTotalWeight > 2000, 'Total word weight must be positive');
  assert.ok(jhCurrentTimelineDur > 12, 'Acoustic timeline duration must match real MP3 length');
  const activeCardTimings = JHALAK_AUDIO_TIMINGS[jhFilteredReels[jhCurrentIdx].id];
  if (activeCardTimings && Array.isArray(activeCardTimings.silences) && activeCardTimings.silences.length > 1) {
    for (let wIdx = 1; wIdx < jhCurrentWordTimings.length; wIdx++) {
      const ws = jhCurrentWordTimings[wIdx].startSec;
      for (let sIdx = 0; sIdx < activeCardTimings.silences.length; sIdx++) {
        const silS = activeCardTimings.silences[sIdx][0];
        const silE = activeCardTimings.silences[sIdx][1];
        assert.ok(!(ws > silS + 0.02 && ws < silE - 0.02), 'No subsequent word may start inside an acoustic silence pause');
      }
    }
  }

  const midIdx = syncJhWordHighlightToTime(5.0, 20.0);
  assert.ok(midIdx > 0 && midIdx < jhCurrentWordTimings.length, 'syncJhWordHighlightToTime must resolve active word index');
  assert.strictEqual(jhActiveWordIdx, midIdx);
  assert.ok(el('jhWord_' + midIdx).classList.contains('jh-word-active'), 'Active word span must receive jh-word-active class');
  assert.ok(el('jhWord_0').classList.contains('jh-word-spoken'), 'Earlier word span must receive jh-word-spoken class');

  // Reaching the end of the audio (curiosity answer) keeps the curiosity box revealed and highlights its answer words
  const endIdx = syncJhWordHighlightToTime(19.95, 20.0);
  assert.strictEqual(endIdx, jhCurrentWordTimings.length - 1, 'Near end of duration must highlight final word');
  assert.ok(el('jhReelsViewport').innerHTML.includes('jh-curiosity-box revealed') && jhRevealedMap[jhFilteredReels[jhCurrentIdx].id] === true, 'Curiosity box remains revealed');

  stopJhAudio();
  assert.strictEqual(jhActiveWordIdx, -1, 'stopJhAudio must clear active word index');
  assert.ok(!el('jhWord_' + endIdx).classList.contains('jh-word-active'), 'stopJhAudio must clear jh-word-active class');

  // Chithi 8-slide Letter drawer also wraps words and highlights them during letter audio playback
  openJhalakLetterDrawer();
  assert.ok(el('jhLetterTitle').innerHTML.includes('id="jhLetterWord_0"'), 'Letter slide title must wrap words in jhLetterWord spans');
  assert.ok(el('jhLetterBody').innerHTML.includes('class="jh-tts-word"'), 'Letter slide body must wrap words in .jh-tts-word spans');
  playJhalakLetterAudio();
  const letterMidIdx = syncJhWordHighlightToTime(4.0, 16.0);
  assert.ok(letterMidIdx > 0, 'Letter audio playback must highlight active letter word');
  assert.ok(el('jhLetterWord_' + letterMidIdx).classList.contains('jh-word-active'), 'Active letter word must have jh-word-active class');
  stopJhAudio();

  // 10. Elastic Overscroll Pull-to-Turn Indicators (Top = Prev, Bottom = Next, Text-Free Progress Bar) & 3D Curtain-Lift transition
  const beforePullId = jhFilteredReels[jhCurrentIdx].id;
  updateJhOverscrollPullUI('next', 50);
  assert.ok(el('jhPullIndicatorBottom').classList.contains('visible'), 'Partial bottom pull must show bottom pull indicator');
  assert.ok(!el('jhPullIndicatorBottom').classList.contains('ready'), 'Partial bottom pull below threshold must not be ready');
  assert.strictEqual(el('jhPullBottomText').textContent, '', 'Pull progress bar must have no text');
  assert.strictEqual(commitOrResetJhOverscrollPull(), false, 'Releasing below threshold must spring back without changing page');
  assert.strictEqual(jhFilteredReels[jhCurrentIdx].id, beforePullId, 'Page must remain unchanged when released below threshold');

  el('jhReelsViewport').scrollTop = 320;
  updateJhOverscrollPullUI('next', 120);
  assert.ok(el('jhPullIndicatorBottom').classList.contains('ready'), 'Long bottom pull past threshold must mark indicator ready');
  assert.strictEqual(commitOrResetJhOverscrollPull(), true, 'Releasing past threshold must commit next-page transition');
  assert.notStrictEqual(jhFilteredReels[jhCurrentIdx].id, beforePullId, 'Long bottom pull must advance to next page');
  assert.strictEqual(el('jhReelsViewport').scrollTop, 0, 'Advancing to next page must land at the top of the next page');

  el('jhReelsViewport').scrollTop = 240;
  updateJhOverscrollPullUI('prev', 105);
  assert.ok(el('jhPullIndicatorTop').classList.contains('ready'), 'Top pull past threshold must mark top indicator ready');
  assert.strictEqual(commitOrResetJhOverscrollPull(), true, 'Releasing top pull past threshold must return to previous page');
  assert.strictEqual(jhFilteredReels[jhCurrentIdx].id, beforePullId, 'Top pull must return to previous page');
  assert.strictEqual(el('jhReelsViewport').scrollTop, 0, 'Returning to previous page must land at the top of the previous page');
  stopJhAudio();
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

    def test_zorba_dopamine_reels_app_and_vm_interactions(self) -> None:
        """Verify zorba.html (⚡ ZORBA) compiles cleanly with 148 Reels pages, Play/Pause/Resume/Stop, acoustic word-sync, elastic pull-to-turn, and PWA installability."""
        zb_path = APP_ROOT / "zorba.html"
        self.assertTrue(zb_path.is_file(), "zorba.html must exist")
        zb_html = zb_path.read_text(encoding="utf-8")
        self.assertIn("<title>⚡ ZORBA</title>", zb_html)
        self.assertIn('<link rel="manifest" href="zorba-manifest.json" />', zb_html)
        self.assertIn("favicon-zorba.png", zb_html)
        self.assertIn("favicon-zorba.ico", zb_html)
        self.assertIn("navigator.serviceWorker.register('kalyani-sw.js')", zb_html)
        self.assertIn("navigator.wakeLock.request", zb_html)
        self.assertNotIn('<header class="jh-topbar">', zb_html)
        self.assertIn("jh-floating-gear-btn", zb_html)
        self.assertLess(
            zb_html.index('id="jhSettingsDrawer"'),
            zb_html.index('id="jhCategoryDropdownWrap"'),
            "Category dropdown must live inside the Settings drawer so the entire screen is taken by content only",
        )
        self.assertIn('id="btnJhCategoryDropdown"', zb_html)
        self.assertIn('id="btnJhHeaderListen"', zb_html)
        self.assertIn('id="btnJhHeaderStop"', zb_html)
        self.assertIn('id="jhTopAudioProgressFill"', zb_html)
        self.assertIn("jh-pull-progress-fill", zb_html)
        self.assertIn("jh-dbltap-voice-toast", zb_html)
        self.assertIn("body.jh-audio-playing", zb_html)
        self.assertIn("jh-tts-sentence", zb_html)
        self.assertIn("jh-math-inline", zb_html)
        self.assertIn("jh-inline-code", zb_html)
        self.assertIn("jh-wikilink-pill", zb_html)
        self.assertIn("jh-md-em", zb_html)
        self.assertIn("jh-md-strong", zb_html)
        self.assertNotIn("activeEl.scrollIntoView", zb_html)
        refresh_py = (APP_ROOT / "scripts" / "refresh_voices.py").read_text(encoding="utf-8")
        self.assertIn("en-gb-gia-server-voicelm-xl#kix08", refresh_py)
        self.assertIn("attempt_sentence_splitting: false", refresh_py)
        self.assertIn("speaker_prompt_tokens", refresh_py)
        self.assertIn("uk_warm_female_prompt.json", refresh_py)
        self.assertIn("_humanize_english_tts_text", refresh_py)
        self.assertIn("_spoken_math_inner", refresh_py)
        self.assertNotIn("kix02", refresh_py)

        m = re.search(r"<script>([\s\S]*?)</script>", zb_html)
        self.assertIsNotNone(m, "Missing <script> block in zorba.html")

        vm_harness = r"""
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const code = fs.readFileSync(0, 'utf8');
const els = {};
function el(id) {
  if (!els[id]) {
    els[id] = {
      id, className: '', innerHTML: '', textContent: '', value: '', style: {}, src: '', scrollTop: 0,
      classList: {
        add(c) { if (!els[id].className.includes(c)) els[id].className = (els[id].className + ' ' + c).trim(); },
        remove(c) { els[id].className = els[id].className.replace(c, '').trim(); },
        toggle(c, b) { if (b) this.add(c); else this.remove(c); },
        contains(c) { return els[id].className.includes(c); }
      },
      querySelector: () => ({ textContent: '', classList: { remove() {}, add() {} }, offsetWidth: 100 }),
      play: () => Promise.resolve(),
      pause() {},
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
  setTimeout: () => 1, clearTimeout: () => {}, setInterval: () => 1, clearInterval: () => {}, console, assert, el
};
const suite = code + `
;(function() {
  const catIds = JHALAK_CATEGORIES.map(c => c.id);
  assert.deepStrictEqual(catIds, ['all', 'songs_en', 'songs_hi', 'songs_bn', 'science', 'clarity', 'listening', 'zorba']);
  assert.strictEqual(ALL_JHALAK_REELS.length, 76, 'Total cleaned Zorba pages must be 76');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['songs_en'], 8, 'English Songs category must have 8 songs');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['songs_hi'], 8, 'Hindi Songs category must have 8 songs');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['songs_bn'], 8, 'Bengali Songs category must have 8 verified songs');
  catIds.forEach(cid => {
    assert.ok(JHALAK_CATEGORY_COUNTS[cid] >= 8, 'Category ' + cid + ' must have at least 8 rich pages');
  });
  const dayLabelRe = new RegExp('\\\\bDay\\\\s+\\\\d+\\\\b', 'i');
  const bannedHallucinations = [
    'Jeconota',
    'shob pete naki',
    'Megh dekhe jeno bhoole na jai',
    'prothomobashar baranday',
    'Amar ekla akash thomke geche',
    'cholo sukhero sondhane',
    'tupur tapur brishti'
  ];
  ALL_JHALAK_REELS.forEach(r => {
    assert.ok(Array.isArray(r.sections) && r.sections.length >= 3, 'Every Zorba page must have at least 3 rich sections: ' + r.id);
    assert.ok(r.audio_url.includes('audio/zorba/reels/' + r.id + '.mp3'), 'Every Zorba page must use dedicated full-page Zorba reel audio: ' + r.id);
    assert.strictEqual(dayLabelRe.test(r.title_bn), false, 'Zero Day X progression labels allowed in Zorba title: ' + r.id);
    r.sections.forEach(s => {
      assert.ok(!s.body_bn.includes('Open Gemini Live'), 'No raw Gemini Live prompt boilerplate in Zorba section: ' + r.id);
      assert.strictEqual(dayLabelRe.test(s.heading_bn), false, 'Zero Day X progression labels allowed in Zorba heading: ' + r.id);
      assert.strictEqual(dayLabelRe.test(s.body_bn), false, 'Zero Day X progression labels allowed in Zorba body: ' + r.id);
    });
    const serialized = JSON.stringify(r);
    bannedHallucinations.forEach(bad => {
      assert.ok(!serialized.includes(bad), 'Hallucinated lyric phrase "' + bad + '" must never appear in ' + r.id);
    });
    assert.ok(JHALAK_AUDIO_TIMINGS[r.id] || JHALAK_AUDIO_TIMINGS[r.audio_rel], 'Every Zorba page must have acoustic timing metadata: ' + r.id);
  });

  renderJhalakReelStream();
  syncJhSettingsButtonsUI();
  assert.strictEqual(jhHistoryStack.length, 1, 'Initial history stack must contain exactly 1 page so first page never repeats on first swipe');
  assert.strictEqual(jhHistoryPos, 0, 'Initial history position must be 0');
  assert.strictEqual(getSelectedCategorySummaryLabel(), '✨ All ▾');
  assert.ok(/<h2[^>]*class="jh-hook-title"><span class="jh-vibe-badge">/.test(el('jhReelsViewport').innerHTML), 'Inline category badge at start of h2');
  assert.ok(/<h3 class="jh-sec-heading">[^<]*<span id="jhWord_/.test(el('jhReelsViewport').innerHTML), 'Section headings must be wrapped in .jh-tts-word spans');
  assert.ok(el('jhReelsViewport').innerHTML.includes('class="jh-tts-sentence"'), 'Body paragraphs must wrap sentences in .jh-tts-sentence spans for guided reading');
  assert.ok(el('jhReelsViewport').innerHTML.includes('jh-curiosity-box revealed'), 'Curiosity takeaway box must be open by default with zero tap-to-reveal friction');
  assert.ok(jhCurrentWordTimings.length > 60, 'Full-page Zorba reel must wrap all words on the page (title + 3 sections + curiosity Q&A)');
  assert.strictEqual(isSpokenWordToken('&'), true, 'Standalone & must be wrapped as a spoken word token ("and")');
  assert.strictEqual(isSpokenWordToken('+'), true, 'Standalone + must be wrapped as a spoken word token ("plus")');
  const wNumRange = computeCalibratedWordTimingWeights('2016–2026', 'Decade', false, false);
  assert.ok(wNumRange.syllableWeight >= 1800, 'Multi-digit number range 2016–2026 must receive >= 1800ms spoken weight');
  const wCurrency = computeCalibratedWordTimingWeights('₹2.61', 'Cr+', false, false);
  assert.ok(wCurrency.syllableWeight >= 1150, 'Currency decimal ₹2.61 must receive >= 1150ms spoken weight');
  const wUnitMs = computeCalibratedWordTimingWeights('ms).', 'Meanwhile,', false, false);
  assert.ok(wUnitMs.syllableWeight >= 650 && wUnitMs.pauseTier === 3, 'Unit ms). must expand to milliseconds weight and sentence pauseTier 3');
  const wAbbrev = computeCalibratedWordTimingWeights('A.R.', 'Rahman', true, false);
  assert.strictEqual(wAbbrev.pauseTier, 0, 'Abbreviation A.R. must not be misclassified as sentence-ending pauseTier 3');
  const wQuoteOpen = computeCalibratedWordTimingWeights('explicit', '"90%', false, false);
  assert.strictEqual(wQuoteOpen.pauseTier, 1, 'Word preceding opening quote must receive prosodic pauseTier 1');
  assert.ok(el('jhCategoryStatsBox').innerHTML.includes('76 Pages'), 'Category stats shows simple 76 Pages');
  assert.ok(!el('jhCategoryStatsBox').innerHTML.includes('76/76'), 'No fraction in category stats');

  // Play -> Pause -> Resume -> Stop lifecycle
  stopJhAudio();
  assert.strictEqual(el('btnJhHeaderListen').textContent, '🔊 Listen');
  assert.strictEqual(el('btnJhHeaderStop').style.display, 'none');
  playReelAudioAtIndex();
  assert.strictEqual(jhAudioPlaying, true);
  assert.strictEqual(el('btnJhHeaderListen').textContent, '⏸️ Pause');
  assert.strictEqual(el('btnJhHeaderStop').style.display, 'inline-flex');
  syncJhWordHighlightToTime(3.5, 18.0);
  const pausedIdx = jhActiveWordIdx;
  assert.ok(pausedIdx > 0);
  playReelAudioAtIndex();
  assert.strictEqual(jhAudioPlaying, false);
  assert.strictEqual(jhAudioPaused, true);
  assert.strictEqual(el('btnJhHeaderListen').textContent, '▶️ Resume');
  assert.strictEqual(jhActiveWordIdx, pausedIdx);
  playReelAudioAtIndex();
  assert.strictEqual(jhAudioPlaying, true);
  assert.strictEqual(el('btnJhHeaderListen').textContent, '⏸️ Pause');
  stopJhAudio();
  assert.strictEqual(el('btnJhHeaderListen').textContent, '🔊 Listen');
  assert.strictEqual(el('btnJhHeaderStop').style.display, 'none');
  assert.strictEqual(jhActiveWordIdx, -1);

  // Elastic overscroll swipe page progress bar (no text) + 3D Curtain-Lift transition
  const beforeId = jhFilteredReels[jhCurrentIdx].id;
  const activeSlideEl = el('jhSlide_' + jhCurrentIdx);
  updateJhOverscrollPullUI('next', 60);
  assert.strictEqual(el('jhPullIndicatorBottom').classList.contains('visible'), true, 'Pull below threshold must show progress bar');
  assert.strictEqual(el('jhPullIndicatorBottom').classList.contains('ready'), false, 'Pull below threshold must not mark progress bar ready');
  assert.strictEqual(el('jhPullBottomText').textContent, '', 'Progress bar indicator must have no text');
  assert.ok(activeSlideEl.style.transform.includes('translate3d(0, -') && activeSlideEl.style.transform.includes('scale('), 'Page must translate and scale smoothly with pull');
  assert.strictEqual(commitOrResetJhOverscrollPull(), false, 'Releasing before threshold must spring back');
  assert.strictEqual(activeSlideEl.classList.contains('jh-pull-springback'), true, 'Springback class applied when released before threshold');

  el('jhReelsViewport').scrollTop = 300;
  updateJhOverscrollPullUI('next', 120);
  assert.strictEqual(el('jhPullIndicatorBottom').classList.contains('ready'), true, 'Pull at/past threshold must mark progress bar ready');
  assert.strictEqual(el('jhPullBottomFill').style.width, '100%');
  assert.strictEqual(commitOrResetJhOverscrollPull(), true);
  assert.notStrictEqual(jhFilteredReels[jhCurrentIdx].id, beforeId);
  assert.strictEqual(el('jhReelsViewport').scrollTop, 0);

  // Double-tap anywhere on content toggles Play -> Pause -> Resume, ignoring interactive buttons
  stopJhAudio();
  jhLastDoubleTapToggleMs = 0;
  assert.strictEqual(handleJhContentDoubleTap({ target: { tagName: 'BUTTON', className: 'jh-done-btn' } }, 'reel'), false, 'Double-tap on interactive button must be ignored');
  assert.strictEqual(jhAudioPlaying, false);

  jhLastDoubleTapToggleMs = 0;
  assert.strictEqual(handleJhContentDoubleTap({ target: { tagName: 'P', className: 'jh-sec-para' }, clientX: 180, clientY: 320 }, 'reel'), true, 'Double-tap on paragraph content must start voice');
  assert.strictEqual(jhAudioPlaying, true);
  assert.strictEqual(jhAudioPaused, false);

  jhLastDoubleTapToggleMs = 0;
  assert.strictEqual(handleJhContentDoubleTap({ target: { tagName: 'SPAN', className: 'jh-tts-word' }, clientX: 180, clientY: 320 }, 'reel'), true, 'Second double-tap on content must pause voice');
  assert.strictEqual(jhAudioPlaying, false);
  assert.strictEqual(jhAudioPaused, true);

  jhLastDoubleTapToggleMs = 0;
  assert.strictEqual(handleJhContentDoubleTap({ target: { tagName: 'DIV', className: 'jh-card-stage' }, clientX: 180, clientY: 320 }, 'reel'), true, 'Third double-tap on content must resume voice');
  assert.strictEqual(jhAudioPlaying, true);
  assert.strictEqual(jhAudioPaused, false);
  stopJhAudio();

  // KORTEX-inspired Markdown & LaTeX visual rendering across all 148 Zorba reels (zero raw syntax leaks)
  const bt = String.fromCharCode(96);
  const sampleMathState = { words: [], totalWeight: 0, prefix: 'testM', sentCounter: 0 };
  const sampleHtml = wrapTextWithJhTtsWords(
    'Gravity ($R_{\\\\mu\\\\nu} u^\\\\mu u^\\\\nu \\\\ge 0$), $\\\\sqrt{2} \\\\approx 1.414$, $\\\\exp(-\\\\frac{1}{2} D_M^2)$, ' + bt + '< 350ms' + bt + ' in ' + bt + 'build_app.py' + bt + ', [[kortex-graph|KORTEX Graph]], **Bold Focus**, *Italic Bhaavna*, and Am -> G ($15 vs $0.30).',
    sampleMathState,
    { blockId: 'secTest', addHeadingPause: false, chunkSentences: true }
  );
  assert.ok(sampleHtml.includes('class="jh-math-inline"'), 'Inline LaTeX must render inside .jh-math-inline badge');
  assert.ok(sampleHtml.includes('<sub class="jh-math-sub">μν</sub>'), 'LaTeX subscripts must render inside .jh-math-sub');
  assert.ok(sampleHtml.includes('<sup class="jh-math-sup">μ</sup>'), 'LaTeX superscripts must render inside .jh-math-sup');
  assert.ok(sampleHtml.includes('class="jh-math-sqrt"'), 'LaTeX \\sqrt must render .jh-math-sqrt');
  assert.ok(sampleHtml.includes('class="jh-math-frac"'), 'LaTeX \\frac must render .jh-math-frac');
  assert.ok(sampleHtml.includes('class="jh-inline-code"'), 'Backtick code must render .jh-inline-code keycap');
  assert.ok(sampleHtml.includes('class="jh-wikilink-pill"'), 'Wikilinks [[...]] must render .jh-wikilink-pill');
  assert.ok(sampleHtml.includes('class="jh-md-strong"'), 'Markdown **bold** must render .jh-md-strong');
  assert.ok(sampleHtml.includes('class="jh-md-em"'), 'Markdown *italic* must render .jh-md-em');
  assert.ok(sampleHtml.includes('class="jh-md-arrow"'), 'ASCII arrows -> must render .jh-md-arrow');
  assert.ok(sampleHtml.includes('$15') && sampleHtml.includes('$0.30'), 'USD currency must remain intact outside math spans');

  ALL_JHALAK_REELS.forEach(r => {
    const st = { words: [], totalWeight: 0, prefix: 'chk', sentCounter: 0 };
    const chunks = [
      wrapTextWithJhTtsWords(r.title_bn, st, { addHeadingPause: true }),
      wrapTextWithJhTtsWords(r.curiosity_q_bn, st, { addHeadingPause: true }),
      wrapTextWithJhTtsWords(r.curiosity_a_bn, st, { inCuriosityA: true })
    ];
    r.sections.forEach(sec => {
      chunks.push(wrapTextWithJhTtsWords(sec.heading_bn, st, { addHeadingPause: true }));
      chunks.push(wrapTextWithJhTtsWords(sec.body_bn, st, { chunkSentences: true }));
    });
    const plainVisible = chunks.join(' ').replace(new RegExp('<code class="jh-inline-code">[^<]*</code>', 'g'), 'CODE_PILL').replace(new RegExp('<[^>]+>', 'g'), '');
    const leakRe = new RegExp('[\\\\\\\\*' + bt + ']|(?:\\\\[\\\\[)|(?:\\\\]\\\\])|->|<->|%%JH');
    assert.strictEqual(leakRe.test(plainVisible), false, 'Zero raw LaTeX/Markdown leaks allowed in rendered reel ' + r.id + ': ' + plainVisible);
  });
})();
`;
vm.runInNewContext(suite, ctx, {filename: 'zorba-bundle.js'});
"""
        proc = subprocess.run(
            [str(NODE_BIN), "-e", vm_harness],
            input=m.group(1),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, f"Zorba VM test failed: {proc.stderr}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
