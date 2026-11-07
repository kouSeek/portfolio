/* ============================================================================
   ⚡ ZORBA — MODULE 2: RANDOMIZED REELS ENGINE, ELASTIC OVERSCROLL PULL-TO-TURN,
   ACOUSTIC KARAOKE WORD HIGHLIGHTING, PLAY/PAUSE/RESUME/STOP, AND ADMIN SETTINGS
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
let jhAudioPaused = false;
let jhAutoAdvanceTimer = null;
let jhSlideLetterIdx = 0;
let jhRevealedMap = {};
let jhLikesMap = {};
let jhDoneMap = {};
let jhAdminFilterCat = 'cbt';
let jhAdminSelectedItemId = '';
let jhOutgoingCardHtml = '';
let jhCurrentWordTimings = [];
let jhCurrentTotalWeight = 0;
let jhCurrentTimelineDur = 0;
let jhLetterWordTimings = [];
let jhLetterTotalWeight = 0;
let jhLetterTimelineDur = 0;
let jhAudioMode = 'reel';
let jhActiveWordIdx = -1;
let jhWordHighlightTimer = null;
let jhAudioStartedAtMs = 0;
let jhActiveCutSec = 0;
let jhTouchStartX = 0;
let jhTouchStartY = 0;
let jhTouchStartScrollTop = 0;
let jhTouchStartAtTop = true;
let jhTouchStartAtBottom = true;
let jhPullAnchorY = null;
let jhPullDirection = '';
let jhPullDistance = 0;
let jhPullThresholdReached = false;
let jhMouseDownX = null;
let jhMouseDownY = null;
let jhWheelLock = false;
let jhWheelOverscrollAccum = 0;
let jhWheelOverscrollDir = '';
let jhWheelDecayTimer = null;

const JH_NEXT_PULL_THRESHOLD = 105;
const JH_PREV_PULL_THRESHOLD = 90;

try {
  const savedFlow = localStorage.getItem('koushik_zorba_auto_flow_v1');
  if (savedFlow === '0') jhAutoFlow = false;
  const savedVoice = localStorage.getItem('koushik_zorba_auto_voice_v1');
  if (savedVoice === '0') jhAutoPlayVoices = false;
  const savedMulti = localStorage.getItem('koushik_zorba_cat_multiselect_v1');
  if (savedMulti === '1') jhMultiSelectCategories = true;
  const savedShowLikes = localStorage.getItem('koushik_zorba_show_likes_v1');
  if (savedShowLikes === '0') jhShowLikeCount = false;
  const savedLikes = localStorage.getItem('koushik_zorba_likes_v1');
  if (savedLikes) {
    const parsedL = JSON.parse(savedLikes);
    if (parsedL && typeof parsedL === 'object') jhLikesMap = parsedL;
  }
  const savedDone = localStorage.getItem('koushik_zorba_done_v1');
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
    localStorage.setItem('koushik_zorba_likes_v1', JSON.stringify(jhLikesMap));
    localStorage.setItem('koushik_zorba_done_v1', JSON.stringify(jhDoneMap));
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
   (Calibrated Multi-Feature Word & Pause Regression + Closed-Loop Silence Sync)
   ============================================================================ */
const JH_PRONOUNCEABLE_CAPS = new Set([
  'KORTEX', 'ZORBA', 'ANONDO', 'KALYANI', 'JHALAK', 'ONE', 'TWO', 'NOT',
  'AND', 'THE', 'FOR', 'ALL', 'CASE', 'CLOSED', 'BAIL', 'PAID', 'FULL', 'NEXT'
]);
const JH_ABBREV_RE = /^(?:(?:[A-Za-z]\.)+|(?:Dr|Mr|Mrs|Ms|Prof|Sr|Jr|St|Fig|No|Vol|Ch|Sec)\.|(?:vs|etc|e\.g|i\.e)\.)["'”’)\]]*$/;
const JH_SPOKEN_UNIT_EXTRA_MS = {
  ms: 540,
  hz: 220,
  khz: 450,
  mhz: 450,
  db: 380,
  cr: 260,
  vs: 260,
  etc: 460
};

function isSpokenWordToken(token) {
  if (!token) return false;
  const cleaned = String(token)
    .replace(/[\u{10000}-\u{10FFFF}\u2600-\u27BF\uFE0F]/gu, '')
    .replace(/[•*#_`~↗"'“”‘’()\[\]{}]/g, '');
  return /[\u0980-\u09FF\u0900-\u097FA-Za-z0-9&+=]/.test(cleaned);
}

function computeCalibratedWordTimingWeights(rawWord, nextWord, isTitleOrHeading, isHeadingEnd) {
  const w = String(rawWord || '');
  const nw = String(nextWord || '');
  const clean = w
    .replace(/[\u{10000}-\u{10FFFF}\u2600-\u27BF\uFE0F]/gu, '')
    .replace(/[•*#_`~↗"'“”‘’()\[\]{}]/g, '');

  const hasInternalEmdash = /[A-Za-z\u0980-\u09FF][—–][A-Za-z\u0980-\u09FF]/.test(clean) ? 1 : 0;
  const subparts = clean.split(/[-—–/]+/).filter(Boolean);
  const nExtraSubwords = Math.max(0, subparts.length - 1);

  const digitMatches = clean.match(/[0-9\u09E6-\u09EF]/g);
  const digits = digitMatches ? digitMatches.length : 0;
  const hasNumRange = /[0-9\u09E6-\u09EF]\s*[—–\-/:]\s*[0-9\u09E6-\u09EF]/.test(w) ? 1 : 0;
  const hasDecimal = /[0-9\u09E6-\u09EF]\.[0-9\u09E6-\u09EF]/.test(w) ? 1 : 0;
  const symMatches = w.match(/[₹$%°+=×∝&]/g);
  const symWords = symMatches ? symMatches.length : 0;

  let acronymCaps = 0;
  let unitExtraMs = 0;
  for (let i = 0; i < subparts.length; i++) {
    const sp = subparts[i];
    const alphaOnly = sp.replace(/[^A-Za-z]/g, '');
    const lowAlpha = alphaOnly.toLowerCase();
    if (Object.prototype.hasOwnProperty.call(JH_SPOKEN_UNIT_EXTRA_MS, lowAlpha)) {
      unitExtraMs += JH_SPOKEN_UNIT_EXTRA_MS[lowAlpha];
    } else if (alphaOnly.length >= 2 && alphaOnly === alphaOnly.toUpperCase() && !JH_PRONOUNCEABLE_CAPS.has(alphaOnly)) {
      acronymCaps += alphaOnly.length;
    } else if (/^(?:[0-9]+[A-Za-z]|[A-Za-z][0-9]+)$/.test(sp)) {
      acronymCaps += 1;
    }
  }

  const alphaStr = clean.replace(/[^A-Za-z\u0980-\u09FF\u0900-\u097F]/g, '');
  const charCount = alphaStr.length;
  const enVowelMatches = alphaStr.match(/[aeiouyAEIOUY]+/g);
  let enVowelClusters = enVowelMatches ? enVowelMatches.length : 0;
  for (let i = 0; i < subparts.length; i++) {
    const spA = subparts[i].replace(/[^A-Za-z]/g, '').toLowerCase();
    if (
      spA.length > 3 &&
      spA.endsWith('e') &&
      !spA.endsWith('le') &&
      !spA.endsWith('ee') &&
      !spA.endsWith('ie') &&
      !spA.endsWith('ye') &&
      !spA.endsWith('oe')
    ) {
      enVowelClusters = Math.max(1, enVowelClusters - 1);
    }
  }
  const indicVowelMatches = alphaStr.match(/[\u09BE-\u09CC\u09D7\u0985-\u0994\u0981-\u0983\u093E-\u094C\u0905-\u0914\u0901-\u0903]/g);
  const indicVowels = indicVowelMatches ? indicVowelMatches.length : 0;
  const syllables = charCount > 0 ? Math.max(1, enVowelClusters + indicVowels) : 0;

  let alphaMs =
    17.0 +
    159.0 * syllables +
    10.4 * charCount +
    125.0 * acronymCaps +
    118.0 * hasInternalEmdash +
    7.0 * nExtraSubwords +
    unitExtraMs;
  if (isTitleOrHeading) {
    alphaMs *= 1.15;
  }

  const numSymMs =
    215.0 * digits +
    360.0 * hasNumRange +
    325.0 * hasDecimal +
    274.0 * symWords;
  const syllableWeight = Math.round(Math.max(85, alphaMs + numSymMs));

  let pauseTier = 0;
  if (isHeadingEnd) {
    pauseTier = 3;
  } else if (/[।.?!]["'”’)\]]*$/.test(w) && !JH_ABBREV_RE.test(clean)) {
    pauseTier = 3;
  } else if (/[:;—–-]["'”’)\]]*$/.test(w)) {
    pauseTier = 2;
  } else if (/[,،]["'”’)\]]*$/.test(w)) {
    pauseTier = 1;
  } else if (/["'”’)\]]+$/.test(w) || /^["'“‘(\[]+/.test(nw)) {
    pauseTier = 1;
  }

  const pauseWeight = pauseTier === 3 ? 390 : (pauseTier === 2 ? 200 : (pauseTier === 1 ? 190 : 0));
  return { syllableWeight, pauseTier, pauseWeight };
}

function wrapTextWithJhTtsWords(text, state, opts) {
  const raw = String(text || '');
  if (!raw) return '';
  const parts = raw.split(/(\s+)/);
  const spokenPartIndices = [];
  for (let i = 0; i < parts.length; i++) {
    if (isSpokenWordToken(parts[i])) {
      spokenPartIndices.push(i);
    }
  }
  const lastSpokenPartIdx = spokenPartIndices.length ? spokenPartIndices[spokenPartIndices.length - 1] : -1;
  const prefix = (state && state.prefix) || 'jhWord';
  const blockId = (opts && opts.blockId) || '';
  const inCuriosityA = Boolean(opts && opts.inCuriosityA);
  const addHeadingPause = Boolean(opts && opts.addHeadingPause);

  let spokenCursor = 0;
  return parts.map((part, pIdx) => {
    if (!isSpokenWordToken(part)) return part;

    const nextSpokenIdx = (spokenCursor + 1 < spokenPartIndices.length)
      ? spokenPartIndices[spokenCursor + 1]
      : -1;
    const nextSpokenWord = nextSpokenIdx >= 0 ? parts[nextSpokenIdx] : '';
    spokenCursor += 1;

    const isHeadingEnd = addHeadingPause && pIdx === lastSpokenPartIdx;
    const { syllableWeight, pauseTier, pauseWeight } = computeCalibratedWordTimingWeights(
      part,
      nextSpokenWord,
      addHeadingPause,
      isHeadingEnd
    );
    const weight = syllableWeight + pauseWeight;

    const wIdx = state.words.length;
    const startWeight = state.totalWeight;
    const wordEndWeight = startWeight + syllableWeight;
    const endWeight = startWeight + weight;
    state.totalWeight = endWeight;
    state.words.push({
      idx: wIdx,
      word: part,
      syllableWeight: syllableWeight,
      pauseWeight: pauseWeight,
      pauseTier: pauseTier,
      weight: weight,
      startWeight: startWeight,
      wordEndWeight: wordEndWeight,
      endWeight: endWeight,
      startSec: 0,
      endSec: 0,
      blockId: blockId,
      inCuriosityA: inCuriosityA
    });

    const curAttr = inCuriosityA ? ' data-curiosity-a="1"' : '';
    return `<span id="${prefix}_${wIdx}" class="jh-tts-word" data-widx="${wIdx}"${curAttr}>${part}</span>`;
  }).join('');
}

/* ACOUSTIC SILENCE-MAP & CLOSED-LOOP REGRESSION WORD TIMELINE BUILDER */
function buildAcousticWordTimeline(words, totalWeight, audioMeta) {
  if (!words || !words.length || totalWeight <= 0) return 0;

  const totalDur = (audioMeta && Number(audioMeta.dur) > 0.5)
    ? Number(audioMeta.dur)
    : Math.max(2.0, totalWeight / 1000);

  if (audioMeta && Array.isArray(audioMeta.word_starts) && audioMeta.word_starts.length === words.length) {
    for (let i = 0; i < words.length; i++) {
      const s = Math.max(0, Number(audioMeta.word_starts[i]) || 0);
      const nextS = (i + 1 < words.length) ? Math.max(s + 0.04, Number(audioMeta.word_starts[i + 1]) || 0) : totalDur;
      words[i].startSec = i === 0 ? 0 : s;
      words[i].endSec = nextS;
    }
    return totalDur;
  }

  const rawSilences = (audioMeta && Array.isArray(audioMeta.silences)) ? audioMeta.silences : [];
  const silences = [];
  for (let i = 0; i < rawSilences.length; i++) {
    const pair = rawSilences[i];
    if (Array.isArray(pair) && pair.length >= 2) {
      const s = Math.max(0, Number(pair[0]) || 0);
      const e = Math.min(totalDur, Number(pair[1]) || 0);
      if (e - s >= 0.12) silences.push([s, e]);
    }
  }

  if (!silences.length) {
    const lead = totalDur > 1.2 ? 0.18 : 0;
    const span = Math.max(0.4, totalDur - (totalDur > 1.2 ? 0.34 : 0));
    for (let i = 0; i < words.length; i++) {
      words[i].startSec = i === 0 ? 0 : (lead + (words[i].startWeight / totalWeight) * span);
      words[i].endSec = lead + (words[i].endWeight / totalWeight) * span;
    }
    return totalDur;
  }

  const speechStart = (silences[0][0] <= 0.08)
    ? Math.min(totalDur * 0.15, silences[0][1])
    : (totalDur > 1.2 ? 0.18 : 0.04);
  const lastSil = silences[silences.length - 1];
  const speechEnd = (lastSil[1] >= totalDur - 0.14)
    ? Math.max(speechStart + 0.4, lastSil[0])
    : Math.max(speechStart + 0.4, totalDur - 0.12);

  const innerSils = [];
  for (let i = 0; i < silences.length; i++) {
    const s = silences[i][0];
    const e = silences[i][1];
    if (s > speechStart + 0.10 && e < speechEnd - 0.10) {
      innerSils.push([s, e]);
    }
  }

  const sortedSilDurs = innerSils.map(pair => pair[1] - pair[0]).sort((a, b) => a - b);
  const medSilDur = sortedSilDurs.length ? sortedSilDurs[Math.floor(sortedSilDurs.length / 2)] : 0.22;
  const tier3MinDur = medSilDur <= 0.30 ? 0.25 : 0.34;
  const tier12MaxDur = medSilDur <= 0.30 ? 0.32 : 0.45;

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
    let lo = 0;
    let hi = totalDur;
    for (let iter = 0; iter < 26; iter++) {
      const mid = (lo + hi) * 0.5;
      if (voicedTimeAt(mid) < targetV) lo = mid;
      else hi = mid;
    }
    return (lo + hi) * 0.5;
  }

  function snapOutOfSilence(t) {
    for (let i = 0; i < silences.length; i++) {
      const s = silences[i][0];
      const e = silences[i][1];
      if (t > s + 0.01 && t < e - 0.01) return e;
    }
    return t;
  }

  const anchors = [];
  let lastTEnd = speechStart;
  let lastWEnd = 0;
  let lastSilIdx = -1;

  for (let i = 0; i < words.length - 1; i++) {
    const w = words[i];
    const tier = w.pauseTier || 0;
    if (tier === 0) continue;

    const remW = Math.max(1.0, totalWeight - lastWEnd);
    const remT = Math.max(0.1, speechEnd - lastTEnd);
    const wordEndW = w.wordEndWeight !== undefined ? w.wordEndWeight : (w.startWeight + (w.syllableWeight || 140));
    const predT = lastTEnd + ((wordEndW - lastWEnd) / remW) * remT;
    const maxTol = tier === 3 ? 1.35 : 0.95;

    let bestK = -1;
    let bestCost = 999.0;
    for (let sIdx = lastSilIdx + 1; sIdx < innerSils.length; sIdx++) {
      const sStart = innerSils[sIdx][0];
      const sEnd = innerSils[sIdx][1];
      if (sStart <= lastTEnd + 0.08) continue;
      if (sStart - predT > maxTol) break;

      const sDur = sEnd - sStart;
      if (tier === 3 && sDur < tier3MinDur && !/^\d+\.$/.test(w.word)) continue;
      if ((tier === 1 || tier === 2) && sDur > tier12MaxDur) continue;

      const dist = Math.abs(sStart - predT);
      if (dist <= maxTol) {
        const expP = (w.pauseWeight || (tier === 3 ? 390 : 195)) / 1000.0;
        const cost = dist + 0.6 * Math.abs(sDur - expP);
        if (cost < bestCost) {
          bestCost = cost;
          bestK = sIdx;
        }
      }
    }

    if (bestK >= 0) {
      const sStart = innerSils[bestK][0];
      const sEnd = innerSils[bestK][1];
      anchors.push({
        endWordIdx: i,
        endSec: sStart,
        nextStartSec: sEnd
      });
      lastTEnd = sEnd;
      lastWEnd = w.endWeight;
      lastSilIdx = bestK;
    }
  }

  anchors.push({
    endWordIdx: words.length - 1,
    endSec: speechEnd,
    nextStartSec: totalDur
  });

  let segStartWordIdx = 0;
  let segStartSec = speechStart;
  for (let sIdx = 0; sIdx < anchors.length; sIdx++) {
    const seg = anchors[sIdx];
    const vStart = voicedTimeAt(segStartSec);
    const vEnd = Math.max(vStart + 0.02, voicedTimeAt(seg.endSec));
    const segWeights = [];
    let cumW = 0;

    for (let j = segStartWordIdx; j <= seg.endWordIdx; j++) {
      const sMs = words[j].syllableWeight || 140;
      const pMs = words[j].pauseWeight !== undefined
        ? words[j].pauseWeight
        : (words[j].pauseTier === 3 ? 390 : (words[j].pauseTier >= 1 ? 195 : 0));
      const wEff = (j === seg.endWordIdx) ? sMs : (sMs + pMs * 0.35);
      segWeights.push([cumW, cumW + wEff]);
      cumW += wEff;
    }

    const totalSegW = Math.max(1.0, cumW);
    for (let offset = 0; offset < segWeights.length; offset++) {
      const j = segStartWordIdx + offset;
      const f0 = segWeights[offset][0] / totalSegW;
      const f1 = segWeights[offset][1] / totalSegW;
      const rawStart = (j === segStartWordIdx) ? segStartSec : invVoicedTime(vStart + f0 * (vEnd - vStart));
      const rawEnd = (j === seg.endWordIdx) ? seg.nextStartSec : invVoicedTime(vStart + f1 * (vEnd - vStart));
      words[j].startSec = j === 0 ? 0 : snapOutOfSilence(rawStart);
      words[j].endSec = Math.max(words[j].startSec + 0.02, rawEnd);
      if (j > segStartWordIdx && words[j].startSec > words[j - 1].endSec) {
        words[j - 1].endSec = words[j].startSec;
      }
    }

    segStartWordIdx = seg.endWordIdx + 1;
    segStartSec = seg.nextStartSec;
  }

  return totalDur;
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
  const timelineDur = isLetter ? jhLetterTimelineDur : jhCurrentTimelineDur;
  const prefix = isLetter ? 'jhLetterWord' : 'jhWord';

  if (!words || !words.length || totalWeight <= 0) return -1;

  const baseDur = timelineDur > 0.5 ? timelineDur : Math.max(1.5, totalWeight / 1000);
  let effDur = (Number.isFinite(durationSec) && durationSec > 0.5) ? durationSec : baseDur;
  if (!isLetter && jhActiveCutSec > 2 && effDur > jhActiveCutSec) {
    effDur = jhActiveCutSec;
  }

  const aud = getJhAudioEl();
  const rawCurSec = (Number.isFinite(currentTimeSec) && currentTimeSec >= 0)
    ? currentTimeSec
    : (aud && Number.isFinite(aud.currentTime) && aud.currentTime >= 0 ? aud.currentTime : 0);

  const scaleFactor = (Math.abs(effDur - baseDur) > 1.0 && effDur > 0.5)
    ? (baseDur / effDur)
    : 1.0;
  const targetSec = Math.max(0, Math.min(baseDur - 0.001, rawCurSec * scaleFactor));

  let lo = 0;
  let hi = words.length - 1;
  let foundIdx = 0;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    const w = words[mid];
    if (targetSec < w.startSec) {
      hi = mid - 1;
    } else if (targetSec >= w.endSec) {
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
        if (hint) hint.textContent = '✨ Revealed';
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

function startJhWordHighlightLoop(cutSec, keepCurrentPos) {
  stopJhWordHighlightLoop();
  jhActiveCutSec = Number(cutSec) || 0;
  jhAudioStartedAtMs = Date.now();
  if (!keepCurrentPos) {
    syncJhWordHighlightToTime(0, 0);
  }
  jhWordHighlightTimer = setInterval(() => {
    if (!jhAudioPlaying) {
      stopJhWordHighlightLoop();
      return;
    }
    const aud = getJhAudioEl();
    if (!aud || aud.paused || aud.seeking) return;
    if (Number.isFinite(aud.currentTime)) {
      const dur = Number.isFinite(aud.duration) && aud.duration > 0 ? aud.duration : 0;
      syncJhWordHighlightToTime(aud.currentTime, dur);
    }
  }, 35);
}

function pauseJhAudio() {
  if (!jhAudioPlaying) return;
  stopJhWordHighlightLoop();
  const aud = getJhAudioEl();
  if (aud) {
    try { aud.pause(); } catch (e) {}
  }
  jhAudioPlaying = false;
  jhAudioPaused = true;
  updateActiveCardPlayBtns();
}

function resumeJhAudio() {
  if (!jhAudioPaused) return;
  const aud = getJhAudioEl();
  if (!aud) return;
  jhAudioPlaying = true;
  jhAudioPaused = false;
  updateActiveCardPlayBtns();
  startJhWordHighlightLoop(jhActiveCutSec, true);
  const playPromise = typeof aud.play === 'function' ? aud.play() : null;
  if (playPromise && typeof playPromise.catch === 'function') {
    playPromise.catch(() => {
      jhAudioPlaying = false;
      jhAudioPaused = true;
      stopJhWordHighlightLoop();
      updateActiveCardPlayBtns();
    });
  }
}

function stopJhAudio() {
  if (jhAutoAdvanceTimer) {
    clearTimeout(jhAutoAdvanceTimer);
    jhAutoAdvanceTimer = null;
  }
  const aud = getJhAudioEl();
  if (aud) {
    try {
      aud.pause();
      aud.currentTime = 0;
    } catch (e) {}
  }
  jhAudioPlaying = false;
  jhAudioPaused = false;
  clearJhWordHighlight();
  updateActiveCardPlayBtns();
}

function spawnLotusBurst(x, y, symbols) {
  if (typeof document === 'undefined' || !document.body) return;
  const icons = symbols || ['❤️', '⚡', '✨', '🦁'];
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
    return '✨ All ▾';
  }
  const selectedList = JHALAK_CATEGORIES.filter(c => jhSelectedChannels.has(c.id));
  if (selectedList.length === 1) {
    return `${selectedList[0].label_bn} ▾`;
  }
  return `📂 ${selectedList.length} Categories ▾`;
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
    ? '☑️ Select multiple categories (Multi-Select)'
    : '🔘 Select a category (Single-Select)';

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
    const likeBadge = jhShowLikeCount
      ? `<span class="jh-stat-likes">❤️ ${catLikes}</span>`
      : '';
    return `
      <div class="jh-stat-chip">
        <div class="jh-stat-chip-top">${cat.label_bn}</div>
        <div class="jh-stat-chip-sub"><strong>${totalCount} Pages</strong> · ✅ ${doneCount} ${likeBadge}</div>
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

/* RANDOMIZED PAGE TRANSITION WITH 3D CURTAIN-LIFT ANIMATION */
function captureOutgoingCardSnapshot() {
  const vp = document.getElementById('jhReelsViewport');
  if (!vp || !vp.innerHTML) return;
  const articleMatch = vp.innerHTML.match(/<article\b[^>]*>([\s\S]*?)<\/article>/);
  const sourceHtml = articleMatch ? articleMatch[1] : '';
  if (!sourceHtml) return;
  const m = sourceHtml.match(/<div class="jh-card-stage">[\s\S]*<\/div>/);
  if (m) {
    jhOutgoingCardHtml = m[0]
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
    spawnLotusBurst(ev.clientX, ev.clientY, ['✅', '⚡', '✨', '🎉']);
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
    spawnLotusBurst(ev.clientX, ev.clientY, ['❤️', '💖', '⚡', '✨']);
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
    btn.innerHTML = `<span class="jh-like-heart">❤️</span> <span class="jh-like-label">Like</span> <span id="jhStickyLikeCount" class="jh-like-count-badge">${count}</span>`;
  } else {
    btn.innerHTML = `<span class="jh-like-heart">❤️</span> <span class="jh-like-label">Like</span>`;
  }
}

/* ADMIN SETTINGS: CATEGORY-LEVEL SELECTABLE DONE & LIKES CONTROLS (NO HUGE LIST) */
function setAdminCategoryFilter(catId) {
  jhAdminFilterCat = catId || 'cbt';
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

  if (!jhAdminFilterCat || !JHALAK_CATEGORIES.some(c => c.id === jhAdminFilterCat)) {
    jhAdminFilterCat = 'cbt';
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
    return `<option value="${c.id}" ${selAttr}>${c.label_bn} — ${total} Pages · ✅ ${done} · ❤️ ${likes}</option>`;
  }).join('');

  const items = ALL_JHALAK_REELS.filter(r =>
    jhAdminFilterCat === 'all' || r.vibe === jhAdminFilterCat
  );

  if (!jhAdminSelectedItemId || !items.some(r => r.id === jhAdminSelectedItemId)) {
    jhAdminSelectedItemId = items.length ? items[0].id : '';
  }

  const selectedItem = items.find(r => r.id === jhAdminSelectedItemId) || items[0];

  const itemOptionsHtml = items.map((r, idx) => {
    const dCount = getReelDoneCount(r.id);
    const lCount = getReelLikeCount(r.id);
    const selAttr = selectedItem && r.id === selectedItem.id ? 'selected' : '';
    const statusTag = dCount > 0 ? '✅' : '📖';
    return `<option value="${r.id}" ${selAttr}>${idx + 1}. ${statusTag} ${r.title_bn} (Done:${dCount} · ❤️${lCount})</option>`;
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
            <span>✅ Done:</span>
            <button type="button" class="jh-step-mini" onclick="adjustReelDoneCount('${selectedItem.id}', -1)">−</button>
            <strong id="adminDoneVal_${selectedItem.id}">${dCount}</strong>
            <button type="button" class="jh-step-mini" onclick="adjustReelDoneCount('${selectedItem.id}', 1)">+</button>
          </div>
          <div class="jh-admin-stepper">
            <span>❤️ Likes:</span>
            <button type="button" class="jh-step-mini" onclick="adjustReelLikeCount('${selectedItem.id}', -1)">−</button>
            <strong id="adminLikeVal_${selectedItem.id}">${lCount}</strong>
            <button type="button" class="jh-step-mini" onclick="adjustReelLikeCount('${selectedItem.id}', 1)">+</button>
          </div>
        </div>
      </div>
    `;
  })() : '';

  listEl.innerHTML = `
    <div class="jh-admin-field-group">
      <label class="jh-admin-label" for="jhAdminCatSelect">1. Select Category:</label>
      <select id="jhAdminCatSelect" class="jh-admin-select" onchange="setAdminCategoryFilter(this.value)">
        ${catOptionsHtml}
      </select>
    </div>

    <div class="jh-admin-field-group">
      <label class="jh-admin-label" for="jhAdminItemSelect">2. Select Page in Category (${items.length}):</label>
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
    flowBtn.textContent = jhAutoFlow ? '🔄 Auto-Reels (Next Page): ON' : '🔄 Auto-Reels (Next Page): OFF';
  }
  const voiceBtn = document.getElementById('btnJhAutoVoice');
  if (voiceBtn) {
    voiceBtn.classList.toggle('active-flow', jhAutoPlayVoices);
    voiceBtn.textContent = jhAutoPlayVoices ? '🔊 Auto-Voice: ON' : '🔊 Auto-Voice: OFF';
  }
  const catModeBtn = document.getElementById('btnJhCatSelectMode');
  if (catModeBtn) {
    catModeBtn.classList.toggle('active-flow', jhMultiSelectCategories);
    catModeBtn.textContent = jhMultiSelectCategories
      ? '📂 Category Selection: Multi-Select'
      : '📂 Category Selection: Single-Select';
  }
  const showLikesBtn = document.getElementById('btnJhShowLikeCount');
  if (showLikesBtn) {
    showLikesBtn.classList.toggle('active-flow', jhShowLikeCount);
    showLikesBtn.textContent = jhShowLikeCount
      ? '❤️ Show Like Count: ON'
      : '❤️ Show Like Count: OFF';
  }
  renderJhCategoryDropdownUI();
  renderJhCategoryStatsUI();
  updateStickyLikeBtnUI();
}

function toggleJhAutoFlow() {
  jhAutoFlow = !jhAutoFlow;
  try { localStorage.setItem('koushik_zorba_auto_flow_v1', jhAutoFlow ? '1' : '0'); } catch (e) {}
  syncJhSettingsButtonsUI();
}

function toggleJhAutoVoice() {
  jhAutoPlayVoices = !jhAutoPlayVoices;
  try { localStorage.setItem('koushik_zorba_auto_voice_v1', jhAutoPlayVoices ? '1' : '0'); } catch (e) {}
  if (!jhAutoPlayVoices) stopJhAudio();
  syncJhSettingsButtonsUI();
}

function toggleJhCategorySelectMode() {
  jhMultiSelectCategories = !jhMultiSelectCategories;
  try { localStorage.setItem('koushik_zorba_cat_multiselect_v1', jhMultiSelectCategories ? '1' : '0'); } catch (e) {}
  if (!jhMultiSelectCategories && jhSelectedChannels.size > 1) {
    const first = Array.from(jhSelectedChannels)[0] || 'all';
    filterJhalakChannel(first);
  }
  syncJhSettingsButtonsUI();
}

function toggleJhShowLikeCount() {
  jhShowLikeCount = !jhShowLikeCount;
  try { localStorage.setItem('koushik_zorba_show_likes_v1', jhShowLikeCount ? '1' : '0'); } catch (e) {}
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
    if (hint) hint.textContent = jhRevealedMap[card.id] ? '✨ Revealed' : '👆 Tap to Reveal';
  }
  if (jhRevealedMap[card.id] && ev) {
    spawnLotusBurst(ev.clientX, ev.clientY, ['🔮', '✨', '⚡']);
  }
}

function updateActiveCardPlayBtns() {
  const isReelPlaying = jhAudioPlaying && jhAudioMode === 'reel';
  const isReelPaused = jhAudioPaused && jhAudioMode === 'reel';
  const headerBtn = document.getElementById('btnJhHeaderListen');
  if (headerBtn) {
    headerBtn.classList.toggle('playing', isReelPlaying);
    headerBtn.classList.toggle('paused', isReelPaused);
    headerBtn.textContent = isReelPlaying
      ? '⏸️ Pause'
      : (isReelPaused ? '▶️ Resume' : '🔊 Listen');
  }
  const headerStopBtn = document.getElementById('btnJhHeaderStop');
  if (headerStopBtn && headerStopBtn.style) {
    headerStopBtn.style.display = (isReelPlaying || isReelPaused) ? 'inline-flex' : 'none';
  }

  const isLetterPlaying = jhAudioPlaying && jhAudioMode === 'letter';
  const isLetterPaused = jhAudioPaused && jhAudioMode === 'letter';
  const letterBtn = document.getElementById('btnJhLetterPlay');
  if (letterBtn) {
    letterBtn.classList.toggle('playing', isLetterPlaying);
    letterBtn.classList.toggle('paused', isLetterPaused);
    letterBtn.textContent = isLetterPlaying
      ? '⏸️ Pause'
      : (isLetterPaused ? '▶️ Resume' : '🔊 Listen');
  }
  const letterStopBtn = document.getElementById('btnJhLetterStop');
  if (letterStopBtn && letterStopBtn.style) {
    letterStopBtn.style.display = (isLetterPlaying || isLetterPaused) ? 'inline-flex' : 'none';
  }
}

function playReelAudioAtIndex(idx) {
  const targetIdx = idx !== undefined ? idx : jhCurrentIdx;
  const card = jhFilteredReels[targetIdx];
  if (!card) return;
  const aud = getJhAudioEl();
  if (!aud) return;

  if (jhAudioMode === 'reel' && jhCurrentIdx === targetIdx) {
    if (jhAudioPlaying) {
      pauseJhAudio();
      return;
    }
    if (jhAudioPaused) {
      resumeJhAudio();
      return;
    }
  }

  stopJhAudio();
  jhCurrentIdx = targetIdx;
  if (!card.audio_url) return;

  jhAudioMode = 'reel';
  aud.src = card.audio_url;
  const cutSec = Number(card.story_end) || 0;

  const syncFromAudio = function () {
    const dur = Number.isFinite(aud.duration) && aud.duration > 0 ? aud.duration : 0;
    syncJhWordHighlightToTime(aud.currentTime, dur);
    if (cutSec > 2 && aud.currentTime >= cutSec) {
      aud.pause();
      handleReelAudioEnded(targetIdx);
    }
  };
  aud.ontimeupdate = syncFromAudio;
  aud.onplaying = syncFromAudio;
  aud.onseeked = syncFromAudio;
  aud.onended = function () {
    handleReelAudioEnded(targetIdx);
  };

  jhAudioPlaying = true;
  jhAudioPaused = false;
  updateActiveCardPlayBtns();
  startJhWordHighlightLoop(cutSec, false);
  const playPromise = typeof aud.play === 'function' ? aud.play() : null;
  if (playPromise && typeof playPromise.catch === 'function') {
    playPromise.catch(() => {
      jhAudioPlaying = false;
      jhAudioPaused = false;
      clearJhWordHighlight();
      updateActiveCardPlayBtns();
    });
  }
}

function handleReelAudioEnded(idx) {
  jhAudioPlaying = false;
  jhAudioPaused = false;
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
          <h2 class="jh-hook-title">🎉 Every Page in This Category Is Done!</h2>
          <p style="font-size:1.05rem;color:#94A3B8;margin-bottom:18px;">
            Switch to another category from the top menu or reset Done pages anytime from Settings (⚙️).
          </p>
          <button type="button" class="jh-top-listen-btn" onclick="resetAllJhDoneCounts()">
            🔄 Re-Enable All Pages
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
    ? `<a class="jh-yt-link" href="${ytUrl}" target="_blank" rel="noopener noreferrer">▶️ Watch on YouTube: ${card.yt_label_bn || card.title_bn} ↗</a>`
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
        { heading_bn: '📖 Deep Dive & Perspective', body_bn: card.hook_bn || '', tone: 'story' },
        { heading_bn: card.hitch_label_bn || '⚡ Micro-Experiment', body_bn: card.hitch_bn || '', tone: 'hitch' }
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

  const timingKey = card.id;
  const cardAudioMeta = (typeof JHALAK_AUDIO_TIMINGS !== 'undefined' && JHALAK_AUDIO_TIMINGS && (JHALAK_AUDIO_TIMINGS[card.id] || JHALAK_AUDIO_TIMINGS[card.audio_rel]))
    ? (JHALAK_AUDIO_TIMINGS[card.id] || JHALAK_AUDIO_TIMINGS[card.audio_rel])
    : null;
  jhCurrentTimelineDur = buildAcousticWordTimeline(ttsState.words, ttsState.totalWeight, cardAudioMeta);
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
    ? `<span class="jh-like-heart">❤️</span> <span class="jh-like-label">Like</span> <span id="jhStickyLikeCount" class="jh-like-count-badge">${likeCount}</span>`
    : `<span class="jh-like-heart">❤️</span> <span class="jh-like-label">Like</span>`;

  vp.innerHTML = `
    ${ghostHtml}
    <article id="jhSlide_${idx}" class="jh-reel-slide ${animClass}" data-idx="${idx}" data-vibe="${card.vibe}">
      <div class="jh-card-stage">
        <h2 id="${titleBlockId}" class="jh-hook-title"><span class="jh-vibe-badge">${card.badge_bn}</span> ${wrappedTitleHtml}</h2>

        ${sectionsHtml}

        <div id="${curBlockId}" class="jh-curiosity-box ${isRev ? 'revealed' : ''}" onclick="toggleJhalakCuriosityBox(${idx}, event)">
          <div class="jh-curiosity-q">
            <span>${wrappedCurQHtml}</span>
            <span class="jh-curiosity-tap-hint">${isRev ? '✨ Revealed' : '👆 Tap to Reveal'}</span>
          </div>
          <div class="jh-curiosity-a">${wrappedCurAHtml}</div>
        </div>

        ${ytHtml}

        <div class="jh-page-bottom-actions">
          <button id="jhStickyLikeBtn" type="button" class="jh-sticky-like-btn ${likeCount > 0 ? 'has-likes' : ''}" onclick="likeCurrentJhalakReel(event)">
            ${likeInnerHtml}
          </button>
          <button id="jhDoneBtn_${idx}" type="button" class="jh-done-btn" onclick="markCurrentJhalakReelDone(event)">
            ✅ Done
          </button>
        </div>

        <div class="jh-bottom-pull-cue">
          ⬆️ At the bottom, pull up a bit more for next page • ⬇️ At the top, pull down for previous page
        </div>
      </div>
    </article>
  `;

  resetJhOverscrollPullUI(false);
  updateStickyLikeBtnUI();
  updateActiveCardPlayBtns();
}

/* ============================================================================
   ELASTIC OVERSCROLL PULL-TO-TURN & 3D CURTAIN-LIFT ENGINE
   (Top Pull -> Smooth Top of Previous Page | Bottom Long Pull -> Top of Next Page)
   ============================================================================ */
function hideJhPullIndicators() {
  const topInd = document.getElementById('jhPullIndicatorTop');
  const botInd = document.getElementById('jhPullIndicatorBottom');
  if (topInd && topInd.classList) {
    topInd.classList.remove('visible');
    topInd.classList.remove('ready');
  }
  if (botInd && botInd.classList) {
    botInd.classList.remove('visible');
    botInd.classList.remove('ready');
  }
  const topFill = document.getElementById('jhPullTopFill');
  const botFill = document.getElementById('jhPullBottomFill');
  if (topFill && topFill.style) topFill.style.width = '0%';
  if (botFill && botFill.style) botFill.style.width = '0%';
}

function updateJhOverscrollPullUI(dir, rawPullPx) {
  const cleanPull = Math.max(0, Number(rawPullPx) || 0);
  jhPullDirection = dir;
  jhPullDistance = cleanPull;

  const threshold = dir === 'next' ? JH_NEXT_PULL_THRESHOLD : JH_PREV_PULL_THRESHOLD;
  const progress = Math.max(0, Math.min(1, cleanPull / threshold));
  const isReady = progress >= 1;

  if (isReady && !jhPullThresholdReached) {
    jhPullThresholdReached = true;
    try {
      if (typeof navigator !== 'undefined' && typeof navigator.vibrate === 'function') {
        navigator.vibrate(16);
      }
    } catch (e) {}
  } else if (!isReady && jhPullThresholdReached) {
    jhPullThresholdReached = false;
  }

  const dampedPx = Math.min(92, Math.round(Math.pow(cleanPull, 0.8) * 1.35));
  const scaleVal = (1 - progress * 0.025).toFixed(4);
  const slideEl = document.getElementById('jhSlide_' + jhCurrentIdx);
  if (slideEl && slideEl.style) {
    if (slideEl.classList) slideEl.classList.remove('jh-pull-springback');
    const signedY = dir === 'next' ? -dampedPx : dampedPx;
    slideEl.style.transform = `translate3d(0, ${signedY}px, 0) scale(${scaleVal})`;
  }

  const topInd = document.getElementById('jhPullIndicatorTop');
  const botInd = document.getElementById('jhPullIndicatorBottom');
  if (dir === 'next') {
    if (topInd && topInd.classList) {
      topInd.classList.remove('visible');
      topInd.classList.remove('ready');
    }
    if (botInd && botInd.classList) {
      botInd.classList.toggle('visible', cleanPull > 8);
      botInd.classList.toggle('ready', isReady);
    }
    const botArrow = document.getElementById('jhPullBottomArrow');
    const botText = document.getElementById('jhPullBottomText');
    const botFill = document.getElementById('jhPullBottomFill');
    if (botArrow) botArrow.textContent = isReady ? '✨' : '⬆️';
    if (botText) {
      botText.textContent = isReady
        ? 'Release — jumping to top of next page!'
        : 'Pull up a bit more for next page...';
    }
    if (botFill && botFill.style) botFill.style.width = Math.round(progress * 100) + '%';
  } else if (dir === 'prev') {
    if (botInd && botInd.classList) {
      botInd.classList.remove('visible');
      botInd.classList.remove('ready');
    }
    if (topInd && topInd.classList) {
      topInd.classList.toggle('visible', cleanPull > 8);
      topInd.classList.toggle('ready', isReady);
    }
    const topArrow = document.getElementById('jhPullTopArrow');
    const topText = document.getElementById('jhPullTopText');
    const topFill = document.getElementById('jhPullTopFill');
    if (topArrow) topArrow.textContent = isReady ? '✨' : '⬇️';
    if (topText) {
      topText.textContent = isReady
        ? 'Release — jumping to top of previous page!'
        : 'Pull down a bit more for previous page...';
    }
    if (topFill && topFill.style) topFill.style.width = Math.round(progress * 100) + '%';
  }
}

function resetJhOverscrollPullUI(animateSpring) {
  jhPullAnchorY = null;
  jhPullDirection = '';
  jhPullDistance = 0;
  jhPullThresholdReached = false;
  hideJhPullIndicators();

  const slideEl = document.getElementById('jhSlide_' + jhCurrentIdx);
  if (slideEl && slideEl.style) {
    if (animateSpring && slideEl.classList) {
      slideEl.classList.add('jh-pull-springback');
    }
    slideEl.style.transform = '';
  }
}

function commitOrResetJhOverscrollPull() {
  const dir = jhPullDirection;
  const dist = jhPullDistance;
  if (dir === 'next' && dist >= JH_NEXT_PULL_THRESHOLD) {
    resetJhOverscrollPullUI(false);
    stepJhalakReel(1, jhAutoPlayVoices);
    return true;
  }
  if (dir === 'prev' && dist >= JH_PREV_PULL_THRESHOLD) {
    resetJhOverscrollPullUI(false);
    stepJhalakReel(-1, jhAutoPlayVoices);
    return true;
  }
  resetJhOverscrollPullUI(true);
  return false;
}

/* KOUSHIK'S 8-SLIDE PERSONAL LETTER (OPENED FROM SETTINGS) */
function getZorbaSlides() {
  if (typeof ANONDO_DATA !== 'undefined' && ANONDO_DATA && Array.isArray(ANONDO_DATA.slides)) {
    return ANONDO_DATA.slides;
  }
  if (typeof SLIDES !== 'undefined' && Array.isArray(SLIDES)) {
    return SLIDES;
  }
  return [];
}

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
  const slidesList = getZorbaSlides();
  const s = slidesList[jhSlideLetterIdx] || slidesList[0];
  if (!s) return;
  const imgEl = document.getElementById('jhLetterImg');
  const titleEl = document.getElementById('jhLetterTitle');
  const bodyEl = document.getElementById('jhLetterBody');
  if (imgEl) imgEl.src = s.img_b64 || '';

  const slideTitle = s.title || s.title_bn || '';
  const slideHighlight = s.highlight || s.highlight_bn || '';
  const slideText = s.text || s.text_bn || '';

  const letterState = { words: [], totalWeight: 0, prefix: 'jhLetterWord' };
  const wrappedTitle = wrapTextWithJhTtsWords(slideTitle, letterState, {
    blockId: 'jhLetterTitle',
    addHeadingPause: true
  });
  const wrappedHighlight = slideHighlight
    ? wrapTextWithJhTtsWords(slideHighlight, letterState, {
        blockId: 'jhLetterBody',
        addHeadingPause: true
      })
    : '';
  const wrappedBody = wrapTextWithJhTtsWords(slideText, letterState, {
    blockId: 'jhLetterBody',
    addHeadingPause: false
  });

  const slideAudioMeta = s.audio_meta || (
    typeof JHALAK_AUDIO_TIMINGS !== 'undefined' &&
    JHALAK_AUDIO_TIMINGS &&
    JHALAK_AUDIO_TIMINGS['slides/slide_' + s.id + '.mp3']
  ) || null;
  jhLetterTimelineDur = buildAcousticWordTimeline(letterState.words, letterState.totalWeight, slideAudioMeta);
  jhLetterWordTimings = letterState.words;
  jhLetterTotalWeight = letterState.totalWeight;
  jhActiveWordIdx = -1;

  if (titleEl) titleEl.innerHTML = wrappedTitle;
  if (bodyEl) {
    bodyEl.innerHTML = (wrappedHighlight
      ? `<strong style="display:block;color:#FCD34D;margin-bottom:6px;">${wrappedHighlight}</strong>`
      : '') + `<span>${wrappedBody}</span>`;
  }
}

function stepJhalakLetterSlide(delta) {
  stopJhAudio();
  const slidesList = getZorbaSlides();
  if (!slidesList.length) return;
  jhSlideLetterIdx = (jhSlideLetterIdx + delta + slidesList.length) % slidesList.length;
  renderJhalakLetterSlide();
}

function playJhalakLetterAudio() {
  const slidesList = getZorbaSlides();
  const s = slidesList[jhSlideLetterIdx] || slidesList[0];
  const aud = getJhAudioEl();
  if (!aud || !s || !s.audio_url) return;

  if (jhAudioMode === 'letter') {
    if (jhAudioPlaying) {
      pauseJhAudio();
      return;
    }
    if (jhAudioPaused) {
      resumeJhAudio();
      return;
    }
  }

  stopJhAudio();
  jhAudioMode = 'letter';
  aud.src = s.audio_url;

  const syncLetterAudio = function () {
    const dur = Number.isFinite(aud.duration) && aud.duration > 0 ? aud.duration : 0;
    syncJhWordHighlightToTime(aud.currentTime, dur);
  };
  aud.ontimeupdate = syncLetterAudio;
  aud.onplaying = syncLetterAudio;
  aud.onseeked = syncLetterAudio;
  aud.onended = function () {
    jhAudioPlaying = false;
    jhAudioPaused = false;
    clearJhWordHighlight();
    updateActiveCardPlayBtns();
  };

  jhAudioPlaying = true;
  jhAudioPaused = false;
  updateActiveCardPlayBtns();
  startJhWordHighlightLoop(0, false);
  const playPromise = typeof aud.play === 'function' ? aud.play() : null;
  if (playPromise && typeof playPromise.catch === 'function') {
    playPromise.catch(() => {
      jhAudioPlaying = false;
      jhAudioPaused = false;
      clearJhWordHighlight();
      updateActiveCardPlayBtns();
    });
  }
}

/* PWA SERVICE WORKER REGISTRATION, SCREEN WAKE LOCK & FAVICON HYDRATION */
if (typeof navigator !== 'undefined' && 'serviceWorker' in navigator) {
  navigator.serviceWorker.register('kalyani-sw.js').catch(() => {});
}

let _screenWakeLock = null;
let _screenWakeLockPending = false;

async function requestScreenWakeLock() {
  try {
    if (typeof navigator === 'undefined' || !navigator.wakeLock || typeof navigator.wakeLock.request !== 'function') {
      return null;
    }
    if (typeof document !== 'undefined' && document.visibilityState === 'hidden') {
      return null;
    }
    if (_screenWakeLock && !_screenWakeLock.released) {
      return _screenWakeLock;
    }
    if (_screenWakeLockPending) {
      return _screenWakeLock;
    }
    _screenWakeLockPending = true;
    const sentinel = await navigator.wakeLock.request('screen');
    _screenWakeLock = sentinel || { released: false };
    _screenWakeLockPending = false;
    if (typeof window !== 'undefined') {
      window._screenWakeLock = _screenWakeLock;
    }
    if (sentinel && typeof sentinel.addEventListener === 'function') {
      sentinel.addEventListener('release', () => {
        if (_screenWakeLock === sentinel) {
          _screenWakeLock = null;
        }
      });
    }
    return _screenWakeLock;
  } catch (e) {
    _screenWakeLockPending = false;
    return null;
  }
}

(function initScreenWakeLock() {
  requestScreenWakeLock();
  if (typeof document !== 'undefined' && typeof document.addEventListener === 'function') {
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState !== 'hidden') {
        requestScreenWakeLock();
      }
    });
    ['touchstart', 'pointerdown', 'click', 'keydown'].forEach(evName => {
      document.addEventListener(evName, () => {
        if (!_screenWakeLock || _screenWakeLock.released) {
          requestScreenWakeLock();
        }
      }, { passive: true });
    });
  }
  if (typeof window !== 'undefined' && typeof window.addEventListener === 'function') {
    window.addEventListener('focus', () => requestScreenWakeLock());
    window.addEventListener('pageshow', () => requestScreenWakeLock());
  }
  if (typeof setInterval === 'function') {
    const _wlTimer = setInterval(() => {
      if (typeof document === 'undefined' || document.visibilityState !== 'hidden') {
        if (!_screenWakeLock || _screenWakeLock.released) {
          requestScreenWakeLock();
        }
      }
    }, 25000);
    if (_wlTimer && typeof _wlTimer.unref === 'function') _wlTimer.unref();
  }
})();

(function hydratePageFavicon() {
  function apply() {
    try {
      if (typeof document === 'undefined' || !document.head || typeof document.createElement !== 'function') return;
      const el = document.getElementById('pageFavicon');
      if (!el || !el.getAttribute) return;
      const emoji = el.getAttribute('data-emoji') || '';
      const b64 = el.getAttribute('data-png-b64') || '';
      const httpsPng = el.getAttribute('data-https-png') || b64;
      const httpsIco = el.getAttribute('data-https-ico') || httpsPng;
      const useHttps = (typeof location !== 'undefined' && /^https?:$/i.test(location.protocol) && (typeof navigator === 'undefined' || navigator.onLine !== false));
      const pngHref = useHttps ? httpsPng : (b64 || httpsPng);
      const icoHref = useHttps ? httpsIco : (b64 || httpsIco);
      if (typeof document.querySelectorAll === 'function') {
        document.querySelectorAll('link[rel*="icon"]').forEach(n => {
          if (n.parentNode) n.parentNode.removeChild(n);
        });
      }
      const l1 = document.createElement('link');
      l1.id = 'pageFavicon';
      l1.setAttribute('data-emoji', emoji);
      l1.setAttribute('data-png-b64', b64);
      l1.setAttribute('data-https-png', httpsPng);
      l1.setAttribute('data-https-ico', httpsIco);
      l1.rel = 'icon';
      l1.type = 'image/png';
      l1.sizes = '64x64';
      l1.href = pngHref;
      document.head.appendChild(l1);
      const l2 = document.createElement('link');
      l2.rel = 'shortcut icon';
      l2.type = useHttps ? 'image/x-icon' : 'image/png';
      l2.href = icoHref;
      document.head.appendChild(l2);
      const l3 = document.createElement('link');
      l3.rel = 'apple-touch-icon';
      l3.sizes = '64x64';
      l3.href = b64 || pngHref;
      document.head.appendChild(l3);
    } catch (e) {}
  }
  apply();
  if (typeof setTimeout === 'function') setTimeout(apply, 90);
})();

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
    if (ev.key === 'ArrowDown' || ev.key === 'PageDown' || ev.key === 'ArrowRight') {
      stepJhalakReel(1, jhAutoPlayVoices);
    } else if (ev.key === 'ArrowUp' || ev.key === 'PageUp' || ev.key === 'ArrowLeft') {
      stepJhalakReel(-1, jhAutoPlayVoices);
    }
  });

  const vp = document.getElementById('jhReelsViewport');
  if (vp && typeof vp.addEventListener === 'function') {
    vp.addEventListener('touchstart', ev => {
      if (ev.touches && ev.touches[0]) {
        jhTouchStartX = ev.touches[0].clientX;
        jhTouchStartY = ev.touches[0].clientY;
        const curScroll = vp.scrollTop || 0;
        const maxScroll = Math.max(0, (vp.scrollHeight || 0) - (vp.clientHeight || 0));
        jhTouchStartScrollTop = curScroll;
        jhTouchStartAtTop = maxScroll <= 12 || curScroll <= 10;
        jhTouchStartAtBottom = maxScroll <= 12 || curScroll >= maxScroll - 14;
        jhPullAnchorY = null;
        jhPullDirection = '';
        jhPullDistance = 0;
        jhPullThresholdReached = false;
      }
    }, { passive: true });

    vp.addEventListener('touchmove', ev => {
      if (!ev.touches || !ev.touches[0]) return;
      const curX = ev.touches[0].clientX;
      const curY = ev.touches[0].clientY;
      const totalDx = curX - jhTouchStartX;
      const totalDy = curY - jhTouchStartY;
      if (Math.abs(totalDx) > Math.abs(totalDy) * 1.2) return;

      const curScroll = vp.scrollTop || 0;
      const maxScroll = Math.max(0, (vp.scrollHeight || 0) - (vp.clientHeight || 0));
      const atTop = maxScroll <= 12 || curScroll <= 8;
      const atBottom = maxScroll <= 12 || curScroll >= maxScroll - 10;

      if (atBottom && totalDy < -12) {
        if (jhPullDirection !== 'next') {
          jhPullDirection = 'next';
          jhPullAnchorY = curY;
        }
        const rawPull = Math.max(0, jhPullAnchorY - curY);
        updateJhOverscrollPullUI('next', rawPull);
      } else if (atTop && totalDy > 12) {
        if (jhPullDirection !== 'prev') {
          jhPullDirection = 'prev';
          jhPullAnchorY = curY;
        }
        const rawPull = Math.max(0, curY - jhPullAnchorY);
        updateJhOverscrollPullUI('prev', rawPull);
      } else if (jhPullDirection) {
        resetJhOverscrollPullUI(false);
      }
    }, { passive: true });

    vp.addEventListener('touchend', ev => {
      if (jhPullDirection) {
        commitOrResetJhOverscrollPull();
        return;
      }
      if (ev.changedTouches && ev.changedTouches[0]) {
        const dx = ev.changedTouches[0].clientX - jhTouchStartX;
        const dy = ev.changedTouches[0].clientY - jhTouchStartY;
        const curScroll = vp.scrollTop || 0;
        const maxScroll = Math.max(0, (vp.scrollHeight || 0) - (vp.clientHeight || 0));
        const nowAtTop = maxScroll <= 12 || curScroll <= 8;
        const nowAtBottom = maxScroll <= 12 || curScroll >= maxScroll - 10;
        if (Math.abs(dy) >= JH_NEXT_PULL_THRESHOLD && Math.abs(dy) > Math.abs(dx) * 1.2) {
          if (dy < 0 && jhTouchStartAtBottom && nowAtBottom) {
            stepJhalakReel(1, jhAutoPlayVoices);
          } else if (dy > 0 && jhTouchStartAtTop && nowAtTop) {
            stepJhalakReel(-1, jhAutoPlayVoices);
          }
        }
      }
    }, { passive: true });

    vp.addEventListener('touchcancel', () => {
      resetJhOverscrollPullUI(true);
    }, { passive: true });

    vp.addEventListener('mousedown', ev => {
      jhMouseDownX = ev.clientX;
      jhMouseDownY = ev.clientY;
      jhPullAnchorY = null;
      jhPullDirection = '';
      jhPullDistance = 0;
    });

    vp.addEventListener('mousemove', ev => {
      if (jhMouseDownY === null) return;
      const totalDx = ev.clientX - jhMouseDownX;
      const totalDy = ev.clientY - jhMouseDownY;
      if (Math.abs(totalDx) > Math.abs(totalDy) * 1.2) return;
      const curScroll = vp.scrollTop || 0;
      const maxScroll = Math.max(0, (vp.scrollHeight || 0) - (vp.clientHeight || 0));
      const atTop = maxScroll <= 12 || curScroll <= 8;
      const atBottom = maxScroll <= 12 || curScroll >= maxScroll - 10;

      if (atBottom && totalDy < -12) {
        if (jhPullDirection !== 'next') {
          jhPullDirection = 'next';
          jhPullAnchorY = ev.clientY;
        }
        updateJhOverscrollPullUI('next', Math.max(0, jhPullAnchorY - ev.clientY));
      } else if (atTop && totalDy > 12) {
        if (jhPullDirection !== 'prev') {
          jhPullDirection = 'prev';
          jhPullAnchorY = ev.clientY;
        }
        updateJhOverscrollPullUI('prev', Math.max(0, ev.clientY - jhPullAnchorY));
      }
    });

    vp.addEventListener('mouseup', () => {
      jhMouseDownX = null;
      jhMouseDownY = null;
      if (jhPullDirection) {
        commitOrResetJhOverscrollPull();
      }
    });

    vp.addEventListener('wheel', ev => {
      if (jhWheelLock) return;
      const curScroll = vp.scrollTop || 0;
      const maxScroll = Math.max(0, (vp.scrollHeight || 0) - (vp.clientHeight || 0));
      const atTop = maxScroll <= 12 || curScroll <= 8;
      const atBottom = maxScroll <= 12 || curScroll >= maxScroll - 10;

      if (atBottom && ev.deltaY > 4 && Math.abs(ev.deltaY) >= Math.abs(ev.deltaX)) {
        if (jhWheelOverscrollDir !== 'next') {
          jhWheelOverscrollDir = 'next';
          jhWheelOverscrollAccum = 0;
        }
        jhWheelOverscrollAccum += ev.deltaY * 0.65;
        updateJhOverscrollPullUI('next', jhWheelOverscrollAccum);
        if (jhWheelDecayTimer) clearTimeout(jhWheelDecayTimer);
        if (jhPullDistance >= JH_NEXT_PULL_THRESHOLD) {
          jhWheelLock = true;
          jhWheelOverscrollAccum = 0;
          jhWheelOverscrollDir = '';
          commitOrResetJhOverscrollPull();
          setTimeout(() => { jhWheelLock = false; }, 650);
        } else {
          jhWheelDecayTimer = setTimeout(() => {
            jhWheelOverscrollAccum = 0;
            jhWheelOverscrollDir = '';
            resetJhOverscrollPullUI(true);
          }, 240);
        }
      } else if (atTop && ev.deltaY < -4 && Math.abs(ev.deltaY) >= Math.abs(ev.deltaX)) {
        if (jhWheelOverscrollDir !== 'prev') {
          jhWheelOverscrollDir = 'prev';
          jhWheelOverscrollAccum = 0;
        }
        jhWheelOverscrollAccum += Math.abs(ev.deltaY) * 0.65;
        updateJhOverscrollPullUI('prev', jhWheelOverscrollAccum);
        if (jhWheelDecayTimer) clearTimeout(jhWheelDecayTimer);
        if (jhPullDistance >= JH_PREV_PULL_THRESHOLD) {
          jhWheelLock = true;
          jhWheelOverscrollAccum = 0;
          jhWheelOverscrollDir = '';
          commitOrResetJhOverscrollPull();
          setTimeout(() => { jhWheelLock = false; }, 650);
        } else {
          jhWheelDecayTimer = setTimeout(() => {
            jhWheelOverscrollAccum = 0;
            jhWheelOverscrollDir = '';
            resetJhOverscrollPullUI(true);
          }, 240);
        }
      } else if (jhWheelOverscrollAccum > 0) {
        jhWheelOverscrollAccum = 0;
        jhWheelOverscrollDir = '';
        resetJhOverscrollPullUI(false);
      }
    }, { passive: true });
  }
});
