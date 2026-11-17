#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compiled UI & Headless Node VM Behavioral Test Suite for ✨ ঝলক (Jhalak) & ⚡ ZORBA."""

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

    def test_hub_html_and_removed_21day_apps(self) -> None:
        """Verify index.html Hub links to jhalak.html and zorba.html and removes kalyani.html and anondo.html."""
        hub_html = (APP_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="jhalak.html"', hub_html)
        self.assertIn('href="zorba.html"', hub_html)
        self.assertNotIn('href="kalyani.html"', hub_html)
        self.assertNotIn('href="anondo.html"', hub_html)
        self.assertFalse((APP_ROOT / "kalyani.html").exists())
        self.assertFalse((APP_ROOT / "anondo.html").exists())
        self.assertIn('id="pageFavicon"', hub_html)
        self.assertIn('data-emoji="🪷"', hub_html)
        self.assertIn("favicon-hub.png", hub_html)
        self.assertIn("navigator.wakeLock.request", hub_html)

    def test_jhalak_dopamine_reels_app_and_vm_interactions(self) -> None:
        """Verify jhalak.html (✨ ঝলক) compiles cleanly with 9 categories, 142 pages, single-tap Play/Pause, Markdown/LaTeX rendering, and VM checks."""
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
  // 1. All 9 categories (all + Bengali Songs + 7 content categories, zero English/Hindi songs or English movies/TV = 142 fun, relatable pages)
  const catIds = JHALAK_CATEGORIES.map(c => c.id);
  assert.deepStrictEqual(catIds, ['all', 'songs_bn', 'gods', 'laugh', 'calm', 'curiosity', 'english', 'hindi', 'tv']);
  assert.strictEqual(ALL_JHALAK_REELS.length, 142, 'Total cleaned Jhalak pages must be 142');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['songs_bn'], 27, 'Bengali Songs category must have 27 verified songs');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['gods'], 18, 'Gods category must have 18 devotional stories');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['laugh'], 20, 'Laugh category must have 20 comedy stories');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['calm'], 15, 'Calm category must have 15 calm stories');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['curiosity'], 18, 'Curiosity category must have 18 fun everyday wonders');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['english'], 18, 'English category must have 18 simple word & sentence pages');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['hindi'], 12, 'Hindi category must have 12 conversation pages');
  assert.strictEqual(JHALAK_CATEGORY_COUNTS['tv'], 14, 'TV category must have 14 non-song Bengali/Indian TV cards');
  catIds.forEach(cid => {
    assert.ok(JHALAK_CATEGORY_COUNTS[cid] >= 12, 'Category ' + cid + ' must have at least 12 rich pages');
  });

  // 2. Every page has multi-section long content, zero Day/progression burden labels, zero Hindi/English songs
  const bannedProgressionPhrases = ['গত সপ্তাহে', 'প্রথম সপ্তাহে', 'দিন ২-এ শেখা', 'দিন ৪-এর', 'সপ্তম দিনের শেষে', 'একুশ দিন আগে'];
  assert.ok(ALL_JHALAK_REELS.every(r => Array.isArray(r.sections) && r.sections.length >= 2), 'Every page must have rich multi-section content');
  assert.ok(ALL_JHALAK_REELS.every(r => !JSON.stringify(r.sections).includes('জেমিনি, শোনো—')), 'Must strip raw Gemini voice-assistant prompts');
  assert.ok(ALL_JHALAK_REELS.every(r => !['songs_hi', 'songs_en'].includes(r.vibe)), 'Must have zero Hindi/English song categories');
  assert.ok(ALL_JHALAK_REELS.every(r => r.audio_url === 'https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/audio/jhalak/reels/' + r.id + '.mp3' && r.story_end === 0), 'Every page must point to its dedicated full-page MP3 with story_end === 0');
  ALL_JHALAK_REELS.forEach(r => {
    const ser = JSON.stringify(r);
    bannedProgressionPhrases.forEach(bp => {
      assert.ok(!ser.includes(bp), 'Progression burden phrase "' + bp + '" must not appear in Jhalak card ' + r.id);
    });
  });

  // 3. Verified Bengali songs (lyrics + meaning) and Simple everyday English cards
  const bnSongs = ALL_JHALAK_REELS.filter(r => r.vibe === 'songs_bn');
  assert.strictEqual(bnSongs.length, 27);
  assert.ok(bnSongs.some(s => s.title_bn.includes('একদিন পাখি উড়ে যাবে') && s.sections[0].body_bn.includes('কিশোর কুমারের')));
  assert.ok(bnSongs.some(s => s.title_bn.includes('আগুনের পরশমণি') && s.sections[1].body_bn.includes('পরশমণির')));
  assert.ok(bnSongs.some(s => s.title_bn.includes('এই পথ যদি না শেষ হয়') && s.sections[0].body_bn.includes('সপ্তপদী')));
  assert.ok(bnSongs.some(s => s.title_bn.includes('আবার হবে তো দেখা') && s.sections[0].body_bn.includes('পুলক বন্দ্যোপাধ্যায়ের') && !s.sections[0].body_bn.includes('স্বয়ংসিদ্ধা')));
  const enCards = ALL_JHALAK_REELS.filter(r => r.vibe === 'english');
  assert.strictEqual(enCards.length, 18);
  assert.ok(enCards.some(c => c.title_bn.includes('GOOD MORNING') && c.sections[1].body_bn.includes('Good morning, have a nice day!')));
  assert.ok(enCards.some(c => c.title_bn.includes('THANK YOU') && c.sections[1].body_bn.includes('You are welcome.')));

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
  assert.strictEqual(jhFilteredReels.length, 141, 'Done item must be excluded from active reels pool');
  assert.ok(!jhFilteredReels.some(r => r.id === cardToDone.id), 'Done card must not appear in future reels');

  // Admin Settings: restore Done count to 0 and adjust Likes count
  adjustReelDoneCount(cardToDone.id, -1);
  assert.strictEqual(getReelDoneCount(cardToDone.id), 0, 'Admin control must allow decreasing Done count back to 0');
  assert.strictEqual(jhFilteredReels.length, 142, 'Restoring Done count to 0 brings item back into reels pool');
  adjustReelLikeCount(cardToDone.id, 5);
  assert.strictEqual(getReelLikeCount(cardToDone.id), 5, 'Admin control must allow changing Likes count');
  setReelLikeCount(cardToDone.id, 2);
  assert.strictEqual(getReelLikeCount(cardToDone.id), 2, 'Admin direct input must set exact Likes count');

  // 6. Category Dropdown: Single-Select by default, toggleable to Multi-Select in Settings
  assert.strictEqual(jhMultiSelectCategories, false, 'Default category mode must be Single-Select');
  filterJhalakChannel('gods');
  assert.strictEqual(jhSelectedChannels.has('gods') && jhSelectedChannels.size === 1, true);
  assert.strictEqual(getSelectedCategorySummaryLabel(), '🪷 ভগবান ▾', 'Single category label has no count on top');
  filterJhalakChannel('laugh');
  assert.strictEqual(jhSelectedChannels.has('laugh') && jhSelectedChannels.size === 1, true, 'In Single-Select mode, choosing laugh replaces gods');

  toggleJhCategorySelectMode();
  assert.strictEqual(jhMultiSelectCategories, true, 'Settings toggle must enable Multi-Select mode');
  filterJhalakChannel('gods');
  assert.strictEqual(jhSelectedChannels.has('laugh') && jhSelectedChannels.has('gods'), true, 'In Multi-Select mode, both laugh and gods stay active');
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
  assert.ok(el('jhCategoryStatsBox').innerHTML.includes('১৪২টি পাতা'), 'Category stats must display simple ১৪২টি পাতা without ১৪২/১৪২টি fraction');
  assert.ok(!el('jhCategoryStatsBox').innerHTML.includes('১৪২/১৪২টি পাতা'), 'Category stats must not show redundant ১৪২/১৪২টি পাতা fraction');
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
  assert.strictEqual(handleJhContentSingleTap({ target: { tagName: 'P', className: 'jh-sec-para' }, clientX: 180, clientY: 320 }, 'reel'), true, 'Single-tap on Jhalak paragraph starts voice');
  assert.strictEqual(jhAudioPlaying, true);
  jhLastDoubleTapToggleMs = 0;
  assert.strictEqual(handleJhContentSingleTap({ target: { tagName: 'P', className: 'jh-sec-para' }, clientX: 180, clientY: 320 }, 'reel'), true, 'Second single-tap pauses voice');
  assert.strictEqual(jhAudioPlaying, false);
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
  assert.ok(typeof JHALAK_AUDIO_TIMINGS === 'object' && Object.keys(JHALAK_AUDIO_TIMINGS).length === 142, 'All 142 Jhalak reels must have acoustic duration and silence maps');
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
  assert.strictEqual(el('jhReelsViewport').style.overflowY, 'hidden', 'Page turn must temporarily lock overflowY to hidden to kill inertial momentum carry-over');
  assert.ok(jhPageTurnTopLockUntil > Date.now(), 'Page turn must set active top-lock timestamp window');

  el('jhReelsViewport').scrollTop = 240;
  updateJhOverscrollPullUI('prev', 105);
  assert.ok(el('jhPullIndicatorTop').classList.contains('ready'), 'Top pull past threshold must mark top indicator ready');
  assert.strictEqual(commitOrResetJhOverscrollPull(), true, 'Releasing top pull past threshold must return to previous page');
  assert.strictEqual(jhFilteredReels[jhCurrentIdx].id, beforePullId, 'Top pull must return to previous page');
  assert.strictEqual(el('jhReelsViewport').scrollTop, 0, 'Returning to previous page must land at the top of the previous page');
  assert.strictEqual(el('jhReelsViewport').style.overflowY, 'hidden', 'Prev page turn must also lock overflowY to hidden');
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
  const wEg = computeCalibratedWordTimingWeights('e.g.,', 'fast', false, false);
  assert.strictEqual(wEg.pauseTier, 1, 'Abbreviation e.g., must receive prosodic comma pauseTier 1');
  assert.ok(wEg.syllableWeight >= 450, 'Abbreviation e.g., must receive expanded "for example" spoken syllable weight');
  const wParenNoPause = computeCalibratedWordTimingWeights('Breathe', '(Reprise)', false, false);
  assert.strictEqual(wParenNoPause.pauseTier, 0, 'Word before parenthetical must not create a false pauseTier 1 that steals sentence boundaries');
  const emState = { words: [], totalWeight: 0, prefix: 'emChk', sentCounter: 0 };
  wrapTextWithJhTtsWords('Pink Floyd — Time and real life—real life.', emState, { chunkSentences: true });
  const floydWord = emState.words.find(w => w.word === 'Floyd');
  const lifeDashWord = emState.words.find(w => w.word === 'life—');
  assert.ok(floydWord && floydWord.pauseTier === 2, 'Word followed by standalone em-dash must be promoted to pauseTier 2');
  assert.ok(lifeDashWord && lifeDashWord.pauseTier === 2, 'Internal unspaced em-dash (life—real) must split into life— (pauseTier 2) + real');
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
  assert.strictEqual(el('jhReelsViewport').scrollTop, 0, 'Advancing to next page must land at scrollTop 0 so header is clearly visible at the top');
  assert.strictEqual(el('jhReelsViewport').style.overflowY, 'hidden', 'Page turn must temporarily lock overflowY to hidden to kill inertial momentum carry-over');
  assert.ok(jhPageTurnTopLockUntil > Date.now(), 'Page turn must set active top-lock timestamp window');

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
