/* ============================================================================
   ✨ ঝলক (JHALAK) — MODULE 2: RANDOMIZED REELS ENGINE, LEFT/RIGHT SLIDE
   ANIMATION, DONE FILTERING, STICKY MULTI-LIKE, AND ADMIN SETTINGS
   ============================================================================ */

let jhSelectedChannels = new Set(['all']);
let jhMultiSelectCategories = false;
let jhCategoryDropdownOpen = false;
let jhFilteredReels = [];
let jhCurrentIdx = 0;
let jhHistoryStack = [];
let jhHistoryPos = -1;
let jhVisitedIds = new Set();
let jhLastSlideDir = 'next';
let jhAutoFlow = true;
let jhAutoPlayVoices = true;
let jhShowLikeCount = true;
let jhAudioPlaying = false;
let jhAutoAdvanceTimer = null;
let jhSlideLetterIdx = 0;
let jhRevealedMap = {};
let jhLikesMap = {};
let jhDoneMap = {};
let jhAdminFilterCat = 'gods';
let jhAdminSelectedItemId = '';
let jhOutgoingCardHtml = '';
let jhCurrentWordTimings = [];
let jhCurrentTotalWeight = 0;
let jhLetterWordTimings = [];
let jhLetterTotalWeight = 0;
let jhAudioMode = 'reel';
let jhActiveWordIdx = -1;
let jhWordHighlightTimer = null;
let jhAudioStartedAtMs = 0;
let jhActiveCutSec = 0;
let jhTouchStartX = 0;
let jhTouchStartY = 0;
let jhMouseDownX = null;
let jhMouseDownY = null;
let jhWheelLock = false;

try {
  const savedFlow = localStorage.getItem('ma_jhalak_auto_flow_v1');
  if (savedFlow === '0') jhAutoFlow = false;
  const savedVoice = localStorage.getItem('ma_jhalak_auto_voice_v1');
  if (savedVoice === '0') jhAutoPlayVoices = false;
  const savedMulti = localStorage.getItem('ma_jhalak_cat_multiselect_v1');
  if (savedMulti === '1') jhMultiSelectCategories = true;
  const savedShowLikes = localStorage.getItem('ma_jhalak_show_likes_v1');
  if (savedShowLikes === '0') jhShowLikeCount = false;
  const savedLikes = localStorage.getItem('ma_jhalak_likes_v1');
  if (savedLikes) {
    const parsedL = JSON.parse(savedLikes);
    if (parsedL && typeof parsedL === 'object') jhLikesMap = parsedL;
  }
  const savedDone = localStorage.getItem('ma_jhalak_done_v1');
  if (savedDone) {
    const parsedD = JSON.parse(savedDone);
    if (parsedD && typeof parsedD === 'object') jhDoneMap = parsedD;
  }
} catch (e) {}

function isReelDone(cardId) {
  return (Number(jhDoneMap[cardId]) || 0) > 0;
}

function getReelDoneCount(cardId) {
  return Number(jhDoneMap[cardId]) || 0;
}

function getReelLikeCount(cardId) {
  return Number(jhLikesMap[cardId]) || 0;
}

function saveJhDoneAndLikes() {
  try {
    localStorage.setItem('ma_jhalak_likes_v1', JSON.stringify(jhLikesMap));
    localStorage.setItem('ma_jhalak_done_v1', JSON.stringify(jhDoneMap));
  } catch (e) {}
}

/* BUILD ACTIVE UN-DONE POOL FOR CURRENT CATEGORY SELECTION */
function rebuildJhFilteredPool() {
  const catMatched = jhSelectedChannels.has('all')
    ? ALL_JHALAK_REELS.slice()
    : ALL_JHALAK_REELS.filter(r => jhSelectedChannels.has(r.vibe));

  const undone = catMatched.filter(r => !isReelDone(r.id));
  jhFilteredReels = undone;
}

rebuildJhFilteredPool();
if (jhFilteredReels.length > 0 && jhFilteredReels[jhCurrentIdx]) {
  jhVisitedIds.add(jhFilteredReels[jhCurrentIdx].id);
  jhHistoryStack.push(jhFilteredReels[jhCurrentIdx].id);
  jhHistoryPos = 0;
}

/* PICK NEXT RANDOM REEL INDEX AUTOMATICALLY */
function pickRandomNextReelIndex() {
  const len = jhFilteredReels.length;
  if (len <= 1) return 0;

  let candidates = [];
  for (let i = 0; i < len; i++) {
    const c = jhFilteredReels[i];
    if (i !== jhCurrentIdx && !jhVisitedIds.has(c.id)) {
      candidates.push(i);
    }
  }
  if (candidates.length === 0) {
    jhVisitedIds.clear();
    if (jhFilteredReels[jhCurrentIdx]) {
      jhVisitedIds.add(jhFilteredReels[jhCurrentIdx].id);
    }
    for (let i = 0; i < len; i++) {
      if (i !== jhCurrentIdx) candidates.push(i);
    }
  }
  const randPos = Math.floor(Math.random() * candidates.length);
  return candidates[randPos] !== undefined ? candidates[randPos] : 0;
}

function getJhAudioEl() {
  return document.getElementById('jhAudioPlayer');
}

/* ============================================================================
   KORTEX-INSPIRED WORD-BY-WORD READ-ALOUD HIGHLIGHTING ENGINE
   ============================================================================ */
function isSpokenWordToken(token) {
  if (!token) return false;
  const cleaned = String(token)
    .replace(/[\u{10000}-\u{10FFFF}\u2600-\u27BF\uFE0F]/gu, '')
    .replace(/[•*#_`~↗"'“”‘’()\[\]{}]/g, '');
  return /[\u0980-\u09FF\u0900-\u097FA-Za-z0-9]/.test(cleaned);
}

function wrapTextWithJhTtsWords(text, state, opts) {
  const raw = String(text || '');
  if (!raw) return '';
  const parts = raw.split(/(\s+)/);
  let lastSpokenPartIdx = -1;
  for (let i = 0; i < parts.length; i++) {
    if (isSpokenWordToken(parts[i])) {
      lastSpokenPartIdx = i;
    }
  }
  const prefix = (state && state.prefix) || 'jhWord';
  const blockId = (opts && opts.blockId) || '';
  const inCuriosityA = Boolean(opts && opts.inCuriosityA);
  const addHeadingPause = Boolean(opts && opts.addHeadingPause);

  return parts.map((part, pIdx) => {
    if (!isSpokenWordToken(part)) return part;

    const cleanWord = part
      .replace(/[\u{10000}-\u{10FFFF}\u2600-\u27BF\uFE0F]/gu, '')
      .replace(/[।.!?;:?!—–\-,،•*#_`~↗"'“”‘’()\[\]{}]/g, '');
    const charCount = Math.max(1, cleanWord.length);
    let weight = Math.max(130, charCount * 44 + 95);

    if (/[।.!?;:?!—–-]["'”’)\]]*$/.test(part)) {
      weight += 260;
    } else if (/[,،]["'”’)\]]*$/.test(part)) {
      weight += 130;
    }
    if (addHeadingPause && pIdx === lastSpokenPartIdx) {
      weight += 240;
    }

    const wIdx = state.words.length;
    const startWeight = state.totalWeight;
    const endWeight = startWeight + weight;
    state.totalWeight = endWeight;
    state.words.push({
      idx: wIdx,
      word: part,
      weight: weight,
      startWeight: startWeight,
      endWeight: endWeight,
      blockId: blockId,
      inCuriosityA: inCuriosityA
    });

    const curAttr = inCuriosityA ? ' data-curiosity-a="1"' : '';
    return `<span id="${prefix}_${wIdx}" class="jh-tts-word" data-widx="${wIdx}"${curAttr}>${part}</span>`;
  }).join('');
}

function stopJhWordHighlightLoop() {
  if (jhWordHighlightTimer) {
    clearInterval(jhWordHighlightTimer);
    jhWordHighlightTimer = null;
  }
}

function clearJhWordHighlight() {
  stopJhWordHighlightLoop();
  const words = jhAudioMode === 'letter' ? jhLetterWordTimings : jhCurrentWordTimings;
  const prefix = jhAudioMode === 'letter' ? 'jhLetterWord' : 'jhWord';
  const clearedBlocks = new Set();

  for (let i = 0; i < words.length; i++) {
    const el = document.getElementById(prefix + '_' + i);
    if (el && el.classList) {
      el.classList.remove('jh-word-active');
      el.classList.remove('jh-word-spoken');
    }
    const bId = words[i] && words[i].blockId;
    if (bId && !clearedBlocks.has(bId)) {
      clearedBlocks.add(bId);
      const bEl = document.getElementById(bId);
      if (bEl && bEl.classList) bEl.classList.remove('jh-block-active');
    }
  }
  jhActiveWordIdx = -1;
}

function syncJhWordHighlightToTime(currentTimeSec, durationSec) {
  const isLetter = jhAudioMode === 'letter';
  const words = isLetter ? jhLetterWordTimings : jhCurrentWordTimings;
  const totalWeight = isLetter ? jhLetterTotalWeight : jhCurrentTotalWeight;
  const prefix = isLetter ? 'jhLetterWord' : 'jhWord';

  if (!words || !words.length || totalWeight <= 0) return -1;

  const estDurSec = Math.max(1.5, totalWeight / 1000);
  let effDur = (Number.isFinite(durationSec) && durationSec > 0.5) ? durationSec : estDurSec;
  if (!isLetter && jhActiveCutSec > 2 && effDur > jhActiveCutSec) {
    effDur = jhActiveCutSec;
  }

  const curSec = (Number.isFinite(currentTimeSec) && currentTimeSec >= 0)
    ? currentTimeSec
    : Math.max(0, (Date.now() - jhAudioStartedAtMs) / 1000);

  const leadPad = effDur > 1.2 ? 0.06 : 0;
  const spanDur = Math.max(0.4, effDur - (effDur > 1.2 ? 0.22 : 0));
  const progress = Math.max(0, Math.min(0.9999, (curSec - leadPad) / spanDur));
  const targetWeight = progress * totalWeight;

  let lo = 0;
  let hi = words.length - 1;
  let foundIdx = 0;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    const w = words[mid];
    if (targetWeight < w.startWeight) {
      hi = mid - 1;
    } else if (targetWeight >= w.endWeight) {
      foundIdx = mid;
      lo = mid + 1;
    } else {
      foundIdx = mid;
      break;
    }
  }

  if (foundIdx === jhActiveWordIdx) return foundIdx;

  const prevIdx = jhActiveWordIdx;
  if (prevIdx >= 0 && foundIdx === prevIdx + 1) {
    const prevEl = document.getElementById(prefix + '_' + prevIdx);
    if (prevEl && prevEl.classList) {
      prevEl.classList.remove('jh-word-active');
      prevEl.classList.add('jh-word-spoken');
    }
    const nextEl = document.getElementById(prefix + '_' + foundIdx);
    if (nextEl && nextEl.classList) {
      nextEl.classList.remove('jh-word-spoken');
      nextEl.classList.add('jh-word-active');
    }
  } else {
    for (let i = 0; i < words.length; i++) {
      const el = document.getElementById(prefix + '_' + i);
      if (el && el.classList) {
        el.classList.toggle('jh-word-active', i === foundIdx);
        el.classList.toggle('jh-word-spoken', i < foundIdx);
      }
    }
  }

  const prevWord = prevIdx >= 0 ? words[prevIdx] : null;
  const curWord = words[foundIdx];
  if (prevWord && prevWord.blockId && (!curWord || prevWord.blockId !== curWord.blockId)) {
    const prevBlock = document.getElementById(prevWord.blockId);
    if (prevBlock && prevBlock.classList) prevBlock.classList.remove('jh-block-active');
  }
  if (curWord && curWord.blockId) {
    const curBlock = document.getElementById(curWord.blockId);
    if (curBlock && curBlock.classList) curBlock.classList.add('jh-block-active');
  }

  if (!isLetter && curWord && curWord.inCuriosityA) {
    const card = jhFilteredReels[jhCurrentIdx];
    if (card && !jhRevealedMap[card.id]) {
      jhRevealedMap[card.id] = true;
      const box = document.getElementById('jhCurBox_' + jhCurrentIdx);
      if (box && box.classList) {
        box.classList.add('revealed');
        const hint = box.querySelector ? box.querySelector('.jh-curiosity-tap-hint') : null;
        if (hint) hint.textContent = '✨ খোলা হয়েছে';
      }
    }
  }

  const activeEl = document.getElementById(prefix + '_' + foundIdx);
  if (activeEl && typeof activeEl.scrollIntoView === 'function') {
    try {
      activeEl.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    } catch (e) {}
  }

  jhActiveWordIdx = foundIdx;
  return foundIdx;
}

function startJhWordHighlightLoop(cutSec) {
  stopJhWordHighlightLoop();
  jhActiveCutSec = Number(cutSec) || 0;
  jhAudioStartedAtMs = Date.now();
  syncJhWordHighlightToTime(0, 0);
  jhWordHighlightTimer = setInterval(() => {
    if (!jhAudioPlaying) {
      stopJhWordHighlightLoop();
      return;
    }
    const aud = getJhAudioEl();
    const cur = aud && Number.isFinite(aud.currentTime) ? aud.currentTime : undefined;
    const dur = aud && Number.isFinite(aud.duration) && aud.duration > 0 ? aud.duration : 0;
    syncJhWordHighlightToTime(cur, dur);
  }, 55);
}

function stopJhAudio() {
  if (jhAutoAdvanceTimer) {
    clearTimeout(jhAutoAdvanceTimer);
    jhAutoAdvanceTimer = null;
  }
  const aud = getJhAudioEl();
  if (aud) {
    try { aud.pause(); } catch (e) {}
  }
  jhAudioPlaying = false;
  clearJhWordHighlight();
  updateActiveCardPlayBtns();
}

function spawnLotusBurst(x, y, symbols) {
  if (typeof document === 'undefined' || !document.body) return;
  const icons = symbols || ['❤️', '🌸', '✨', '💖'];
  for (let i = 0; i < 5; i++) {
    const el = document.createElement('div');
    el.className = 'jh-particle-burst';
    el.textContent = icons[i % icons.length];
    const dx = (Math.random() - 0.5) * 90;
    el.style.left = Math.max(20, Math.min(window.innerWidth - 40, (x || window.innerWidth * 0.8) + dx)) + 'px';
    el.style.top = Math.max(60, (y || window.innerHeight * 0.75) - i * 12) + 'px';
    document.body.appendChild(el);
    setTimeout(() => {
      if (el.parentNode) el.parentNode.removeChild(el);
    }, 1150);
  }
}

/* CATEGORY DROPDOWN (NO PAGE COUNTS ON TOP BAR) */
function toggleJhCategoryDropdown(ev) {
  if (ev && typeof ev.stopPropagation === 'function') ev.stopPropagation();
  jhCategoryDropdownOpen = !jhCategoryDropdownOpen;
  const menu = document.getElementById('jhCategoryDropdownMenu');
  if (menu) menu.classList.toggle('open', jhCategoryDropdownOpen);
  renderJhCategoryDropdownUI();
}

function closeJhCategoryDropdown() {
  jhCategoryDropdownOpen = false;
  const menu = document.getElementById('jhCategoryDropdownMenu');
  if (menu) menu.classList.remove('open');
}

function getSelectedCategorySummaryLabel() {
  if (jhSelectedChannels.has('all') || jhSelectedChannels.size === 0) {
    return '✨ সব ▾';
  }
  const selectedList = JHALAK_CATEGORIES.filter(c => jhSelectedChannels.has(c.id));
  if (selectedList.length === 1) {
    return `${selectedList[0].label_bn} ▾`;
  }
  return `📂 ${jhBnNum(selectedList.length)}টি বিভাগ ▾`;
}

function getActiveCategoryCounts() {
  const counts = { all: 0 };
  JHALAK_CATEGORIES.forEach(c => {
    if (c.id !== 'all') counts[c.id] = 0;
  });
  ALL_JHALAK_REELS.forEach(r => {
    if (!isReelDone(r.id)) {
      counts.all += 1;
      counts[r.vibe] = (counts[r.vibe] || 0) + 1;
    }
  });
  return counts;
}

function renderJhCategoryDropdownUI() {
  const triggerBtn = document.getElementById('btnJhCategoryDropdown');
  if (triggerBtn) {
    triggerBtn.textContent = getSelectedCategorySummaryLabel();
  }
  const menu = document.getElementById('jhCategoryDropdownMenu');
  if (!menu) return;

  const modeBadge = jhMultiSelectCategories
    ? '☑️ একসাথে একাধিক বিভাগ বেছে নাও (Multi-Select)'
    : '🔘 যেকোনো একটি বিভাগ বেছে নাও (Single-Select)';

  const itemsHtml = JHALAK_CATEGORIES.map(cat => {
    const isSel = jhSelectedChannels.has(cat.id);
    const indicator = jhMultiSelectCategories
      ? (isSel ? '☑️' : '⬜')
      : (isSel ? '🔘' : '⚪');
    return `
      <button type="button" class="jh-cat-option ${isSel ? 'active' : ''}" data-chan="${cat.id}" onclick="filterJhalakChannel('${cat.id}', event)">
        <span class="jh-cat-opt-left">${indicator} <span>${cat.label_bn}</span></span>
      </button>
    `;
  }).join('');

  menu.innerHTML = `
    <div class="jh-cat-menu-header">${modeBadge}</div>
    <div class="jh-cat-options-list">${itemsHtml}</div>
  `;
}

function renderJhCategoryStatsUI() {
  const statsBox = document.getElementById('jhCategoryStatsBox');
  if (!statsBox) return;

  const rowsHtml = JHALAK_CATEGORIES.map(cat => {
    let totalCount = 0;
    let doneCount = 0;
    let catLikes = 0;
    ALL_JHALAK_REELS.forEach(r => {
      if (cat.id === 'all' || r.vibe === cat.id) {
        totalCount += 1;
        if (isReelDone(r.id)) doneCount += 1;
        catLikes += getReelLikeCount(r.id);
      }
    });
    const activeCount = totalCount - doneCount;
    const likeBadge = jhShowLikeCount
      ? `<span class="jh-stat-likes">❤️ ${jhBnNum(catLikes)}</span>`
      : '';
    return `
      <div class="jh-stat-chip">
        <div class="jh-stat-chip-top">${cat.label_bn}</div>
        <div class="jh-stat-chip-sub"><strong>${jhBnNum(activeCount)}/${jhBnNum(totalCount)}টি পাতা</strong> · ✅ ${jhBnNum(doneCount)} ${likeBadge}</div>
      </div>
    `;
  }).join('');

  statsBox.innerHTML = rowsHtml;
  renderJhAdminItemsList();
}

function filterJhalakChannel(channelId, ev) {
  if (ev && typeof ev.stopPropagation === 'function') ev.stopPropagation();
  const ch = channelId || 'all';
  stopJhAudio();

  if (!jhMultiSelectCategories) {
    jhSelectedChannels = new Set([ch]);
    closeJhCategoryDropdown();
  } else {
    if (ch === 'all') {
      jhSelectedChannels = new Set(['all']);
    } else {
      jhSelectedChannels.delete('all');
      if (jhSelectedChannels.has(ch)) {
        jhSelectedChannels.delete(ch);
      } else {
        jhSelectedChannels.add(ch);
      }
      if (jhSelectedChannels.size === 0) {
        jhSelectedChannels.add('all');
      }
    }
  }

  rebuildJhFilteredPool();
  jhVisitedIds.clear();
  jhHistoryStack = [];
  jhHistoryPos = -1;
  jhCurrentIdx = jhFilteredReels.length > 0 ? Math.floor(Math.random() * jhFilteredReels.length) : 0;
  if (jhFilteredReels[jhCurrentIdx]) {
    jhVisitedIds.add(jhFilteredReels[jhCurrentIdx].id);
    jhHistoryStack.push(jhFilteredReels[jhCurrentIdx].id);
    jhHistoryPos = 0;
  }
  jhLastSlideDir = 'next';
  renderJhCategoryDropdownUI();
  renderJhalakReelStream();
}

/* RANDOMIZED PAGE TRANSITION WITH PROFESSIONAL SIDEWAYS ANIMATION */
function captureOutgoingCardSnapshot() {
  const vp = document.getElementById('jhReelsViewport');
  if (!vp || !vp.innerHTML) return;
  const m = vp.innerHTML.match(/<div class="jh-card-stage">[\s\S]*<\/article>/);
  if (m) {
    jhOutgoingCardHtml = m[0]
      .replace(/<\/article>\s*$/, '')
      .replace(/\sid="jh(?:Word|TitleBlock|SecBlock|CurBox|DoneBtn|StickyLikeBtn|StickyLikeCount)_[^"]*"/g, '')
      .replace(/\sid="jh(?:StickyLikeBtn|StickyLikeCount)"/g, '')
      .replace(/\b(?:jh-word-active|jh-word-spoken|jh-block-active)\b/g, '');
  }
}

function stepJhalakReel(delta, autoPlayAfter) {
  if (!jhFilteredReels.length) return;
  stopJhAudio();
  captureOutgoingCardSnapshot();

  if (delta < 0) {
    jhLastSlideDir = 'prev';
    if (jhHistoryPos > 0) {
      jhHistoryPos -= 1;
      const prevId = jhHistoryStack[jhHistoryPos];
      const foundIdx = jhFilteredReels.findIndex(r => r.id === prevId);
      if (foundIdx >= 0) {
        jhCurrentIdx = foundIdx;
      } else {
        jhCurrentIdx = pickRandomNextReelIndex();
      }
    } else {
      jhCurrentIdx = pickRandomNextReelIndex();
    }
  } else {
    jhLastSlideDir = 'next';
    if (jhHistoryPos >= 0 && jhHistoryPos + 1 < jhHistoryStack.length) {
      jhHistoryPos += 1;
      const nextId = jhHistoryStack[jhHistoryPos];
      const foundIdx = jhFilteredReels.findIndex(r => r.id === nextId);
      jhCurrentIdx = foundIdx >= 0 ? foundIdx : pickRandomNextReelIndex();
    } else {
      jhCurrentIdx = pickRandomNextReelIndex();
      if (jhFilteredReels[jhCurrentIdx]) {
        jhVisitedIds.add(jhFilteredReels[jhCurrentIdx].id);
        jhHistoryStack.push(jhFilteredReels[jhCurrentIdx].id);
        jhHistoryPos = jhHistoryStack.length - 1;
      }
    }
  }

  renderJhalakReelStream();
  const vp = document.getElementById('jhReelsViewport');
  if (vp) vp.scrollTop = 0;
  if (autoPlayAfter) {
    jhAutoAdvanceTimer = setTimeout(() => playReelAudioAtIndex(jhCurrentIdx), 240);
  }
}

/* MARK DONE BUTTON: EXCLUDES CONTENT FROM FUTURE REELS & ADVANCES TO RANDOM NEXT */
function markCurrentJhalakReelDone(ev) {
  if (ev && typeof ev.stopPropagation === 'function') ev.stopPropagation();
  const card = jhFilteredReels[jhCurrentIdx];
  if (!card) return;

  jhDoneMap[card.id] = (Number(jhDoneMap[card.id]) || 0) + 1;
  saveJhDoneAndLikes();

  if (ev) {
    spawnLotusBurst(ev.clientX, ev.clientY, ['✅', '🌸', '✨', '🎉']);
  }

  stopJhAudio();
  captureOutgoingCardSnapshot();
  rebuildJhFilteredPool();
  jhLastSlideDir = 'next';

  if (jhFilteredReels.length > 0) {
    jhCurrentIdx = Math.floor(Math.random() * jhFilteredReels.length);
    if (jhFilteredReels[jhCurrentIdx]) {
      jhVisitedIds.add(jhFilteredReels[jhCurrentIdx].id);
      jhHistoryStack.push(jhFilteredReels[jhCurrentIdx].id);
      jhHistoryPos = jhHistoryStack.length - 1;
    }
  } else {
    jhCurrentIdx = 0;
  }

  renderJhCategoryDropdownUI();
  renderJhCategoryStatsUI();
  renderJhalakReelStream();
  const vp = document.getElementById('jhReelsViewport');
  if (vp) vp.scrollTop = 0;
  if (jhAutoPlayVoices && jhFilteredReels.length > 0) {
    jhAutoAdvanceTimer = setTimeout(() => playReelAudioAtIndex(jhCurrentIdx), 260);
  }
}

/* TRANSLUCENT STICK-ON LIKE BUTTON (SAME CONTENT CAN BE LIKED MULTIPLE TIMES) */
function likeJhalakReelAtIndex(idx, ev) {
  if (ev && typeof ev.stopPropagation === 'function') ev.stopPropagation();
  const card = jhFilteredReels[idx !== undefined ? idx : jhCurrentIdx];
  if (!card) return;
  jhLikesMap[card.id] = (Number(jhLikesMap[card.id]) || 0) + 1;
  saveJhDoneAndLikes();

  if (ev) {
    spawnLotusBurst(ev.clientX, ev.clientY, ['❤️', '💖', '🌸', '✨']);
  }
  updateStickyLikeBtnUI();
  renderJhCategoryStatsUI();
}

function likeCurrentJhalakReel(ev) {
  likeJhalakReelAtIndex(jhCurrentIdx, ev);
}

function updateStickyLikeBtnUI() {
  const card = jhFilteredReels[jhCurrentIdx];
  const btn = document.getElementById('jhStickyLikeBtn');
  if (!btn) return;
  if (!card) {
    btn.style.display = 'none';
    return;
  }
  btn.style.display = 'inline-flex';
  const count = getReelLikeCount(card.id);
  btn.classList.toggle('has-likes', count > 0);
  if (jhShowLikeCount) {
    btn.innerHTML = `<span class="jh-like-heart">❤️</span> <span class="jh-like-label">ভালো লেগেছে</span> <span id="jhStickyLikeCount" class="jh-like-count-badge">${jhBnNum(count)}</span>`;
  } else {
    btn.innerHTML = `<span class="jh-like-heart">❤️</span> <span class="jh-like-label">ভালো লেগেছে</span>`;
  }
}

/* ADMIN SETTINGS: CATEGORY-LEVEL SELECTABLE DONE & LIKES CONTROLS (NO HUGE LIST) */
function setAdminCategoryFilter(catId) {
  jhAdminFilterCat = catId || 'gods';
  const catItems = ALL_JHALAK_REELS.filter(r =>
    jhAdminFilterCat === 'all' || r.vibe === jhAdminFilterCat
  );
  jhAdminSelectedItemId = catItems.length ? catItems[0].id : '';
  renderJhAdminItemsList();
}

function selectAdminItem(cardId) {
  jhAdminSelectedItemId = cardId || '';
  renderJhAdminItemsList();
}

function setCategoryDoneState(catId, doneVal) {
  const clean = Math.max(0, Number(doneVal) || 0);
  ALL_JHALAK_REELS.forEach(r => {
    if (catId === 'all' || r.vibe === catId) {
      if (clean === 0) delete jhDoneMap[r.id];
      else jhDoneMap[r.id] = clean;
    }
  });
  saveJhDoneAndLikes();
  rebuildJhFilteredPool();
  if (jhCurrentIdx >= jhFilteredReels.length) {
    jhCurrentIdx = Math.max(0, jhFilteredReels.length - 1);
  }
  renderJhCategoryDropdownUI();
  renderJhCategoryStatsUI();
  renderJhalakReelStream();
}

function adjustCategoryLikeCounts(catId, delta) {
  ALL_JHALAK_REELS.forEach(r => {
    if (catId === 'all' || r.vibe === catId) {
      const nextVal = Math.max(0, getReelLikeCount(r.id) + delta);
      if (nextVal === 0) delete jhLikesMap[r.id];
      else jhLikesMap[r.id] = nextVal;
    }
  });
  saveJhDoneAndLikes();
  updateStickyLikeBtnUI();
  renderJhCategoryStatsUI();
}

function resetCategoryLikeCounts(catId) {
  ALL_JHALAK_REELS.forEach(r => {
    if (catId === 'all' || r.vibe === catId) {
      delete jhLikesMap[r.id];
    }
  });
  saveJhDoneAndLikes();
  updateStickyLikeBtnUI();
  renderJhCategoryStatsUI();
}

function adjustReelDoneCount(cardId, delta) {
  const cur = getReelDoneCount(cardId);
  const nextVal = Math.max(0, cur + delta);
  if (nextVal === 0) delete jhDoneMap[cardId];
  else jhDoneMap[cardId] = nextVal;
  saveJhDoneAndLikes();
  rebuildJhFilteredPool();
  if (jhCurrentIdx >= jhFilteredReels.length) {
    jhCurrentIdx = Math.max(0, jhFilteredReels.length - 1);
  }
  renderJhCategoryDropdownUI();
  renderJhCategoryStatsUI();
  renderJhalakReelStream();
}

function setReelDoneCount(cardId, val) {
  const clean = Math.max(0, Number(val) || 0);
  if (clean === 0) delete jhDoneMap[cardId];
  else jhDoneMap[cardId] = clean;
  saveJhDoneAndLikes();
  rebuildJhFilteredPool();
  if (jhCurrentIdx >= jhFilteredReels.length) {
    jhCurrentIdx = Math.max(0, jhFilteredReels.length - 1);
  }
  renderJhCategoryDropdownUI();
  renderJhCategoryStatsUI();
  renderJhalakReelStream();
}

function adjustReelLikeCount(cardId, delta) {
  const cur = getReelLikeCount(cardId);
  const nextVal = Math.max(0, cur + delta);
  if (nextVal === 0) delete jhLikesMap[cardId];
  else jhLikesMap[cardId] = nextVal;
  saveJhDoneAndLikes();
  updateStickyLikeBtnUI();
  renderJhCategoryStatsUI();
}

function setReelLikeCount(cardId, val) {
  const clean = Math.max(0, Number(val) || 0);
  if (clean === 0) delete jhLikesMap[cardId];
  else jhLikesMap[cardId] = clean;
  saveJhDoneAndLikes();
  updateStickyLikeBtnUI();
  renderJhCategoryStatsUI();
}

function resetAllJhDoneCounts() {
  jhDoneMap = {};
  saveJhDoneAndLikes();
  rebuildJhFilteredPool();
  jhCurrentIdx = 0;
  renderJhCategoryDropdownUI();
  renderJhCategoryStatsUI();
  renderJhalakReelStream();
}

function resetAllJhLikeCounts() {
  jhLikesMap = {};
  saveJhDoneAndLikes();
  updateStickyLikeBtnUI();
  renderJhCategoryStatsUI();
}

function renderJhAdminItemsList() {
  const listEl = document.getElementById('jhAdminItemsList');
  if (!listEl) return;

  const contentCats = JHALAK_CATEGORIES.filter(c => c.id !== 'all');
  if (!jhAdminFilterCat || !JHALAK_CATEGORIES.some(c => c.id === jhAdminFilterCat)) {
    jhAdminFilterCat = 'gods';
  }

  const catOptionsHtml = JHALAK_CATEGORIES.map(c => {
    let total = 0;
    let done = 0;
    let likes = 0;
    ALL_JHALAK_REELS.forEach(r => {
      if (c.id === 'all' || r.vibe === c.id) {
        total += 1;
        if (isReelDone(r.id)) done += 1;
        likes += getReelLikeCount(r.id);
      }
    });
    const selAttr = c.id === jhAdminFilterCat ? 'selected' : '';
    return `<option value="${c.id}" ${selAttr}>${c.label_bn} — ডান: ${jhBnNum(done)}/${jhBnNum(total)} · ❤️ ${jhBnNum(likes)}</option>`;
  }).join('');

  const items = ALL_JHALAK_REELS.filter(r =>
    jhAdminFilterCat === 'all' || r.vibe === jhAdminFilterCat
  );

  if (!jhAdminSelectedItemId || !items.some(r => r.id === jhAdminSelectedItemId)) {
    jhAdminSelectedItemId = items.length ? items[0].id : '';
  }

  let catTotal = items.length;
  let catDone = 0;
  let catLikes = 0;
  items.forEach(r => {
    if (isReelDone(r.id)) catDone += 1;
    catLikes += getReelLikeCount(r.id);
  });

  const activeCatObj = JHALAK_CATEGORIES.find(c => c.id === jhAdminFilterCat) || contentCats[0];
  const selectedItem = items.find(r => r.id === jhAdminSelectedItemId) || items[0];

  const itemOptionsHtml = items.map((r, idx) => {
    const dCount = getReelDoneCount(r.id);
    const lCount = getReelLikeCount(r.id);
    const selAttr = selectedItem && r.id === selectedItem.id ? 'selected' : '';
    const statusTag = dCount > 0 ? '✅' : '📖';
    return `<option value="${r.id}" ${selAttr}>${jhBnNum(idx + 1)}. ${statusTag} ${r.title_bn} (ডান:${jhBnNum(dCount)} · ❤️${jhBnNum(lCount)})</option>`;
  }).join('');

  const selectedRowHtml = selectedItem ? (() => {
    const dCount = getReelDoneCount(selectedItem.id);
    const lCount = getReelLikeCount(selectedItem.id);
    return `
      <div class="jh-admin-row ${dCount > 0 ? 'is-done' : ''}">
        <div class="jh-admin-row-title">
          <span class="jh-admin-badge">${selectedItem.badge_bn}</span>
          <span>${selectedItem.title_bn}</span>
        </div>
        <div class="jh-admin-row-controls">
          <div class="jh-admin-stepper">
            <span>✅ ডান:</span>
            <button type="button" class="jh-step-mini" onclick="adjustReelDoneCount('${selectedItem.id}', -1)">−</button>
            <strong id="adminDoneVal_${selectedItem.id}">${jhBnNum(dCount)}</strong>
            <button type="button" class="jh-step-mini" onclick="adjustReelDoneCount('${selectedItem.id}', 1)">+</button>
          </div>
          <div class="jh-admin-stepper">
            <span>❤️ লাইক:</span>
            <button type="button" class="jh-step-mini" onclick="adjustReelLikeCount('${selectedItem.id}', -1)">−</button>
            <strong id="adminLikeVal_${selectedItem.id}">${jhBnNum(lCount)}</strong>
            <button type="button" class="jh-step-mini" onclick="adjustReelLikeCount('${selectedItem.id}', 1)">+</button>
          </div>
        </div>
      </div>
    `;
  })() : '';

  listEl.innerHTML = `
    <div class="jh-admin-field-group">
      <label class="jh-admin-label" for="jhAdminCatSelect">১. বিভাগ বেছে নাও (Category):</label>
      <select id="jhAdminCatSelect" class="jh-admin-select" onchange="setAdminCategoryFilter(this.value)">
        ${catOptionsHtml}
      </select>
    </div>

    <div class="jh-admin-cat-card">
      <div class="jh-admin-cat-summary">
        <span>${activeCatObj.label_bn} বিভাগ</span>
        <span>✅ ডান: ${jhBnNum(catDone)}/${jhBnNum(catTotal)} · ❤️ লাইক: ${jhBnNum(catLikes)}</span>
      </div>
      <div class="jh-admin-cat-actions">
        <button type="button" class="jh-admin-mini-btn" onclick="setCategoryDoneState('${jhAdminFilterCat}', 0)">🔄 বিভাগের ডান রিসেট</button>
        <button type="button" class="jh-admin-mini-btn" onclick="setCategoryDoneState('${jhAdminFilterCat}', 1)">✅ বিভাগের সব ডান</button>
        <button type="button" class="jh-admin-mini-btn" onclick="resetCategoryLikeCounts('${jhAdminFilterCat}')">🔄 বিভাগের লাইক রিসেট</button>
        <button type="button" class="jh-admin-mini-btn" onclick="adjustCategoryLikeCounts('${jhAdminFilterCat}', 1)">❤️ বিভাগের সব পাতায় +১ লাইক</button>
      </div>
    </div>

    <div class="jh-admin-field-group">
      <label class="jh-admin-label" for="jhAdminItemSelect">২. এই বিভাগের নির্দিষ্ট পাতা বেছে নাও (${jhBnNum(items.length)}টি):</label>
      <select id="jhAdminItemSelect" class="jh-admin-select" onchange="selectAdminItem(this.value)">
        ${itemOptionsHtml}
      </select>
    </div>

    ${selectedRowHtml}
  `;
}

/* SETTINGS GEAR: AUTO-REELS, AUTO-VOICE, SINGLE/MULTI CATEGORY & LIKE COUNT TOGGLES */
function syncJhSettingsButtonsUI() {
  const flowBtn = document.getElementById('btnJhAutoFlow');
  if (flowBtn) {
    flowBtn.classList.toggle('active-flow', jhAutoFlow);
    flowBtn.textContent = jhAutoFlow ? '🔄 অটো-রিলস (পরের পাতা): চালু' : '🔄 অটো-রিলস (পরের পাতা): বন্ধ';
  }
  const voiceBtn = document.getElementById('btnJhAutoVoice');
  if (voiceBtn) {
    voiceBtn.classList.toggle('active-flow', jhAutoPlayVoices);
    voiceBtn.textContent = jhAutoPlayVoices ? '🔊 অটো-ভয়েস: চালু' : '🔊 অটো-ভয়েস: বন্ধ';
  }
  const catModeBtn = document.getElementById('btnJhCatSelectMode');
  if (catModeBtn) {
    catModeBtn.classList.toggle('active-flow', jhMultiSelectCategories);
    catModeBtn.textContent = jhMultiSelectCategories
      ? '📂 বিভাগ নির্বাচন: অনেকগুলো (Multi-Select)'
      : '📂 বিভাগ নির্বাচন: একটাই (Single-Select)';
  }
  const showLikesBtn = document.getElementById('btnJhShowLikeCount');
  if (showLikesBtn) {
    showLikesBtn.classList.toggle('active-flow', jhShowLikeCount);
    showLikesBtn.textContent = jhShowLikeCount
      ? '❤️ লাইকের সংখ্যা দেখাও: চালু'
      : '❤️ লাইকের সংখ্যা দেখাও: বন্ধ';
  }
  renderJhCategoryDropdownUI();
  renderJhCategoryStatsUI();
  updateStickyLikeBtnUI();
}

function toggleJhAutoFlow() {
  jhAutoFlow = !jhAutoFlow;
  try { localStorage.setItem('ma_jhalak_auto_flow_v1', jhAutoFlow ? '1' : '0'); } catch (e) {}
  syncJhSettingsButtonsUI();
}

function toggleJhAutoVoice() {
  jhAutoPlayVoices = !jhAutoPlayVoices;
  try { localStorage.setItem('ma_jhalak_auto_voice_v1', jhAutoPlayVoices ? '1' : '0'); } catch (e) {}
  if (!jhAutoPlayVoices) stopJhAudio();
  syncJhSettingsButtonsUI();
}

function toggleJhCategorySelectMode() {
  jhMultiSelectCategories = !jhMultiSelectCategories;
  try { localStorage.setItem('ma_jhalak_cat_multiselect_v1', jhMultiSelectCategories ? '1' : '0'); } catch (e) {}
  if (!jhMultiSelectCategories && jhSelectedChannels.size > 1) {
    const first = Array.from(jhSelectedChannels)[0] || 'all';
    filterJhalakChannel(first);
  }
  syncJhSettingsButtonsUI();
}

function toggleJhShowLikeCount() {
  jhShowLikeCount = !jhShowLikeCount;
  try { localStorage.setItem('ma_jhalak_show_likes_v1', jhShowLikeCount ? '1' : '0'); } catch (e) {}
  syncJhSettingsButtonsUI();
}

function openJhalakSettingsDrawer() {
  closeJhCategoryDropdown();
  syncJhSettingsButtonsUI();
  const modal = document.getElementById('jhSettingsDrawer');
  if (modal) modal.classList.add('open');
}

function closeJhalakSettingsDrawer() {
  const modal = document.getElementById('jhSettingsDrawer');
  if (modal) modal.classList.remove('open');
}

function toggleJhalakCuriosityBox(idx, ev) {
  const card = jhFilteredReels[idx !== undefined ? idx : jhCurrentIdx];
  if (!card) return;
  jhRevealedMap[card.id] = !jhRevealedMap[card.id];
  const box = document.getElementById('jhCurBox_' + (idx !== undefined ? idx : jhCurrentIdx));
  if (box) {
    box.classList.toggle('revealed', !!jhRevealedMap[card.id]);
    const hint = box.querySelector('.jh-curiosity-tap-hint');
    if (hint) hint.textContent = jhRevealedMap[card.id] ? '✨ খোলা হয়েছে' : '👆 ছুঁয়ে দেখো';
  }
  if (jhRevealedMap[card.id] && ev) {
    spawnLotusBurst(ev.clientX, ev.clientY, ['🔮', '✨', '🌸']);
  }
}

function updateActiveCardPlayBtns() {
  const isReelPlaying = jhAudioPlaying && jhAudioMode === 'reel';
  const headerBtn = document.getElementById('btnJhHeaderListen');
  if (headerBtn) {
    headerBtn.classList.toggle('playing', isReelPlaying);
    headerBtn.textContent = isReelPlaying ? '⏹️ থামাও' : '🔊 শোনো';
  }
  const isLetterPlaying = jhAudioPlaying && jhAudioMode === 'letter';
  const letterBtn = document.getElementById('btnJhLetterPlay');
  if (letterBtn) {
    letterBtn.classList.toggle('playing', isLetterPlaying);
    letterBtn.textContent = isLetterPlaying ? '⏹️ থামাও' : '🔊 শোনো';
  }
}

function playReelAudioAtIndex(idx) {
  const targetIdx = idx !== undefined ? idx : jhCurrentIdx;
  const card = jhFilteredReels[targetIdx];
  if (!card) return;
  const aud = getJhAudioEl();
  if (!aud) return;

  if (jhAudioPlaying && jhAudioMode === 'reel' && jhCurrentIdx === targetIdx) {
    stopJhAudio();
    return;
  }

  stopJhAudio();
  jhCurrentIdx = targetIdx;
  if (!card.audio_url) return;

  jhAudioMode = 'reel';
  aud.src = card.audio_url;
  const cutSec = Number(card.story_end) || 0;

  aud.ontimeupdate = function () {
    const dur = Number.isFinite(aud.duration) && aud.duration > 0 ? aud.duration : 0;
    syncJhWordHighlightToTime(aud.currentTime, dur);
    if (cutSec > 2 && aud.currentTime >= cutSec) {
      aud.pause();
      handleReelAudioEnded(targetIdx);
    }
  };
  aud.onended = function () {
    handleReelAudioEnded(targetIdx);
  };

  jhAudioPlaying = true;
  updateActiveCardPlayBtns();
  startJhWordHighlightLoop(cutSec);
  const playPromise = typeof aud.play === 'function' ? aud.play() : null;
  if (playPromise && typeof playPromise.catch === 'function') {
    playPromise.catch(() => {
      jhAudioPlaying = false;
      clearJhWordHighlight();
      updateActiveCardPlayBtns();
    });
  }
}

function handleReelAudioEnded(idx) {
  jhAudioPlaying = false;
  clearJhWordHighlight();
  updateActiveCardPlayBtns();
  if (jhAutoFlow && idx === jhCurrentIdx && jhFilteredReels.length > 1) {
    jhAutoAdvanceTimer = setTimeout(() => {
      stepJhalakReel(1, jhAutoPlayVoices);
    }, 1500);
  }
}

/* RENDER ACTIVE LONG-FORM SCROLLABLE PAGE (SLIDE ANIMATION + WORD HIGHLIGHTING + DONE BUTTON) */
function renderJhalakReelStream() {
  const vp = document.getElementById('jhReelsViewport');
  if (!vp) return;

  if (!jhFilteredReels.length) {
    jhCurrentWordTimings = [];
    jhCurrentTotalWeight = 0;
    jhActiveWordIdx = -1;
    vp.innerHTML = `
      <article class="jh-reel-slide jh-slide-anim-next">
        <div class="jh-card-stage" style="text-align:center;padding:36px 22px;">
          <h2 class="jh-hook-title">🎉 এই বিভাগের সব পাতা পড়া হয়ে গেছে মা!</h2>
          <p style="font-size:1.05rem;color:#5C4938;margin-bottom:18px;">
            তুমি চাইলে অন্য কোনো বিভাগ বেছে নিতে পারো অথবা সেটিংস (⚙️) থেকে পাতাগুলো আবার রিসেট করে নিতে পারো।
          </p>
          <button type="button" class="jh-top-listen-btn" onclick="resetAllJhDoneCounts()">
            🔄 সব পাতা আবার চালু করো
          </button>
        </div>
      </article>
    `;
    updateStickyLikeBtnUI();
    return;
  }

  const idx = Math.max(0, Math.min(jhFilteredReels.length - 1, jhCurrentIdx));
  jhCurrentIdx = idx;
  const card = jhFilteredReels[idx];
  const isRev = !!jhRevealedMap[card.id];
  const hasYt = Boolean(card.yt_query && String(card.yt_query).trim());
  const ytUrl = hasYt
    ? 'https://www.youtube.com/results?search_query=' + encodeURIComponent(card.yt_query)
    : '';
  const ytHtml = hasYt
    ? `<a class="jh-yt-link" href="${ytUrl}" target="_blank" rel="noopener noreferrer">▶️ ইউটিউবে দেখো: ${card.yt_label_bn || card.title_bn} ↗</a>`
    : '';

  const ttsState = { words: [], totalWeight: 0, prefix: 'jhWord' };
  const titleBlockId = 'jhTitleBlock_' + idx;
  const wrappedTitleHtml = wrapTextWithJhTtsWords(card.title_bn, ttsState, {
    blockId: titleBlockId,
    addHeadingPause: true
  });

  const sectionsList = Array.isArray(card.sections) && card.sections.length
    ? card.sections
    : [
        { heading_bn: '📖 সম্পূর্ণ গল্প ও কথা', body_bn: card.hook_bn || '', tone: 'story' },
        { heading_bn: card.hitch_label_bn || '🦋 মনের কথা', body_bn: card.hitch_bn || '', tone: 'hitch' }
      ];

  const sectionsHtml = sectionsList.map((sec, secIdx) => {
    const secBlockId = `jhSecBlock_${idx}_${secIdx}`;
    const wrappedHeadingHtml = wrapTextWithJhTtsWords(sec.heading_bn, ttsState, {
      blockId: secBlockId,
      addHeadingPause: true
    });
    const paragraphs = String(sec.body_bn || '')
      .split(/\n+/)
      .filter(Boolean)
      .map(p => {
        const wrappedP = wrapTextWithJhTtsWords(p, ttsState, {
          blockId: secBlockId,
          addHeadingPause: false
        });
        return `<p class="jh-sec-para">${wrappedP}</p>`;
      })
      .join('');
    const toneClass = sec.tone === 'hitch' ? 'jh-sec-hitch' : (sec.tone === 'extra' ? 'jh-sec-extra' : 'jh-sec-story');
    return `
      <section id="${secBlockId}" class="jh-content-section ${toneClass}">
        <h3 class="jh-sec-heading">${wrappedHeadingHtml}</h3>
        <div class="jh-sec-body">${paragraphs}</div>
      </section>
    `;
  }).join('');

  const curBlockId = `jhCurBox_${idx}`;
  const wrappedCurQHtml = wrapTextWithJhTtsWords(card.curiosity_q_bn, ttsState, {
    blockId: curBlockId,
    addHeadingPause: true
  });
  const wrappedCurAHtml = wrapTextWithJhTtsWords(card.curiosity_a_bn, ttsState, {
    blockId: curBlockId,
    inCuriosityA: true,
    addHeadingPause: false
  });

  jhCurrentWordTimings = ttsState.words;
  jhCurrentTotalWeight = ttsState.totalWeight;
  jhActiveWordIdx = -1;

  const animClass = jhLastSlideDir === 'prev' ? 'jh-slide-anim-prev' : 'jh-slide-anim-next';
  const ghostDirClass = jhLastSlideDir === 'prev' ? 'out-right' : 'out-left';
  const ghostHtml = jhOutgoingCardHtml
    ? `<div class="jh-outgoing-ghost ${ghostDirClass}" aria-hidden="true">${jhOutgoingCardHtml}</div>`
    : '';
  jhOutgoingCardHtml = '';

  const likeCount = getReelLikeCount(card.id);
  const likeInnerHtml = jhShowLikeCount
    ? `<span class="jh-like-heart">❤️</span> <span class="jh-like-label">ভালো লেগেছে</span> <span id="jhStickyLikeCount" class="jh-like-count-badge">${jhBnNum(likeCount)}</span>`
    : `<span class="jh-like-heart">❤️</span> <span class="jh-like-label">ভালো লেগেছে</span>`;

  vp.innerHTML = `
    ${ghostHtml}
    <article id="jhSlide_${idx}" class="jh-reel-slide ${animClass}" data-idx="${idx}" data-vibe="${card.vibe}">
      <div class="jh-card-stage">
        <div class="jh-card-top">
          <span class="jh-vibe-badge">${card.badge_bn}</span>
        </div>

        <h2 id="${titleBlockId}" class="jh-hook-title">${wrappedTitleHtml}</h2>

        ${sectionsHtml}

        <div id="${curBlockId}" class="jh-curiosity-box ${isRev ? 'revealed' : ''}" onclick="toggleJhalakCuriosityBox(${idx}, event)">
          <div class="jh-curiosity-q">
            <span>${wrappedCurQHtml}</span>
            <span class="jh-curiosity-tap-hint">${isRev ? '✨ খোলা হয়েছে' : '👆 ছুঁয়ে দেখো'}</span>
          </div>
          <div class="jh-curiosity-a">${wrappedCurAHtml}</div>
        </div>

        ${ytHtml}

        <div class="jh-page-bottom-actions">
          <button id="jhStickyLikeBtn" type="button" class="jh-sticky-like-btn ${likeCount > 0 ? 'has-likes' : ''}" onclick="likeCurrentJhalakReel(event)">
            ${likeInnerHtml}
          </button>
          <button id="jhDoneBtn_${idx}" type="button" class="jh-done-btn" onclick="markCurrentJhalakReelDone(event)">
            ✅ হয়ে গেছে
          </button>
        </div>
      </div>
    </article>
  `;

  updateStickyLikeBtnUI();
  updateActiveCardPlayBtns();
}

/* KOUSHIK'S 8-SLIDE LETTER (CHITHI — OPENED FROM SETTINGS) */
function openJhalakLetterDrawer() {
  closeJhalakSettingsDrawer();
  stopJhAudio();
  renderJhalakLetterSlide();
  const modal = document.getElementById('jhLetterDrawer');
  if (modal) modal.classList.add('open');
}

function closeJhalakLetterDrawer() {
  stopJhAudio();
  const modal = document.getElementById('jhLetterDrawer');
  if (modal) modal.classList.remove('open');
}

function renderJhalakLetterSlide() {
  const s = SLIDES[jhSlideLetterIdx] || SLIDES[0];
  if (!s) return;
  const imgEl = document.getElementById('jhLetterImg');
  const titleEl = document.getElementById('jhLetterTitle');
  const bodyEl = document.getElementById('jhLetterBody');
  if (imgEl) imgEl.src = s.img_b64 || '';

  const letterState = { words: [], totalWeight: 0, prefix: 'jhLetterWord' };
  const wrappedTitle = wrapTextWithJhTtsWords(s.title_bn, letterState, {
    blockId: 'jhLetterTitle',
    addHeadingPause: true
  });
  const wrappedHighlight = s.highlight_bn
    ? wrapTextWithJhTtsWords(s.highlight_bn, letterState, {
        blockId: 'jhLetterBody',
        addHeadingPause: true
      })
    : '';
  const wrappedBody = wrapTextWithJhTtsWords(s.text_bn, letterState, {
    blockId: 'jhLetterBody',
    addHeadingPause: false
  });

  jhLetterWordTimings = letterState.words;
  jhLetterTotalWeight = letterState.totalWeight;
  jhActiveWordIdx = -1;

  if (titleEl) titleEl.innerHTML = wrappedTitle;
  if (bodyEl) {
    bodyEl.innerHTML = (wrappedHighlight
      ? `<strong style="display:block;color:#7C2D12;margin-bottom:6px;">${wrappedHighlight}</strong>`
      : '') + `<span>${wrappedBody}</span>`;
  }
}

function stepJhalakLetterSlide(delta) {
  stopJhAudio();
  jhSlideLetterIdx = (jhSlideLetterIdx + delta + SLIDES.length) % SLIDES.length;
  renderJhalakLetterSlide();
}

function playJhalakLetterAudio() {
  const s = SLIDES[jhSlideLetterIdx] || SLIDES[0];
  const aud = getJhAudioEl();
  if (!aud || !s || !s.audio_url) return;

  if (jhAudioPlaying && jhAudioMode === 'letter') {
    stopJhAudio();
    return;
  }

  stopJhAudio();
  jhAudioMode = 'letter';
  aud.src = s.audio_url;

  aud.ontimeupdate = function () {
    const dur = Number.isFinite(aud.duration) && aud.duration > 0 ? aud.duration : 0;
    syncJhWordHighlightToTime(aud.currentTime, dur);
  };
  aud.onended = function () {
    jhAudioPlaying = false;
    clearJhWordHighlight();
    updateActiveCardPlayBtns();
  };

  jhAudioPlaying = true;
  updateActiveCardPlayBtns();
  startJhWordHighlightLoop(0);
  const playPromise = typeof aud.play === 'function' ? aud.play() : null;
  if (playPromise && typeof playPromise.catch === 'function') {
    playPromise.catch(() => {
      jhAudioPlaying = false;
      clearJhWordHighlight();
      updateActiveCardPlayBtns();
    });
  }
}

window.addEventListener('DOMContentLoaded', () => {
  if (jhFilteredReels.length > 0) {
    jhCurrentIdx = Math.floor(Math.random() * jhFilteredReels.length);
    jhVisitedIds.add(jhFilteredReels[jhCurrentIdx].id);
    jhHistoryStack.push(jhFilteredReels[jhCurrentIdx].id);
    jhHistoryPos = 0;
  }
  syncJhSettingsButtonsUI();
  renderJhalakReelStream();

  document.addEventListener('click', () => {
    if (jhCategoryDropdownOpen) closeJhCategoryDropdown();
  });

  window.addEventListener('keydown', ev => {
    if (ev.key === 'ArrowLeft') stepJhalakReel(-1, jhAutoPlayVoices);
    else if (ev.key === 'ArrowRight') stepJhalakReel(1, jhAutoPlayVoices);
  });

  const vp = document.getElementById('jhReelsViewport');
  if (vp && typeof vp.addEventListener === 'function') {
    vp.addEventListener('touchstart', ev => {
      if (ev.touches && ev.touches[0]) {
        jhTouchStartX = ev.touches[0].clientX;
        jhTouchStartY = ev.touches[0].clientY;
      }
    }, { passive: true });
    vp.addEventListener('touchend', ev => {
      if (ev.changedTouches && ev.changedTouches[0]) {
        const dx = ev.changedTouches[0].clientX - jhTouchStartX;
        const dy = ev.changedTouches[0].clientY - jhTouchStartY;
        if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.4) {
          stepJhalakReel(dx < 0 ? 1 : -1, jhAutoPlayVoices);
        }
      }
    }, { passive: true });
    vp.addEventListener('mousedown', ev => {
      jhMouseDownX = ev.clientX;
      jhMouseDownY = ev.clientY;
    });
    vp.addEventListener('mouseup', ev => {
      if (jhMouseDownX === null) return;
      const dx = ev.clientX - jhMouseDownX;
      const dy = ev.clientY - jhMouseDownY;
      jhMouseDownX = null;
      jhMouseDownY = null;
      if (Math.abs(dx) > 75 && Math.abs(dx) > Math.abs(dy) * 1.6) {
        stepJhalakReel(dx < 0 ? 1 : -1, jhAutoPlayVoices);
      }
    });
    vp.addEventListener('wheel', ev => {
      if (jhWheelLock) return;
      if (Math.abs(ev.deltaX) > 48 && Math.abs(ev.deltaX) > Math.abs(ev.deltaY) * 1.5) {
        jhWheelLock = true;
        stepJhalakReel(ev.deltaX > 0 ? 1 : -1, jhAutoPlayVoices);
        setTimeout(() => { jhWheelLock = false; }, 480);
      }
    }, { passive: true });
  }
});
