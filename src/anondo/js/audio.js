/* ============================================================================
   ANONDO MODULE 1: STATE & PROACTIVE AUDIO ENGINE (`src/anondo/js/audio.js`)
   ============================================================================ */
const audioEl = new Audio();
audioEl.preload = "auto";
let activeAudioBtnId = null;
let activeAudioKey = null;
let activeAudioTitle = "";

let curTab = "play";
let curDay = 1;
let curGame = 0;
let curSlide = 0;
let curQuote = 0;
let curPillar = 0;
let autoAdvanceSlides = true;
let autoWelcomeSucceeded = false;
let autoWelcomeFallbackArmed = false;
let sosInterval = null;

const STORAGE_KEY = "anondo_koushik_en_done_v1";
let doneMap = {};
try {
  doneMap = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
} catch (e) { doneMap = {}; }

function formatAudioSeconds(sec) {
  if (!sec || !isFinite(sec) || sec < 0) return "0:00";
  const s = Math.floor(sec);
  const mins = Math.floor(s / 60);
  const rem = s % 60;
  return mins + ":" + (rem < 10 ? "0" + rem : rem);
}

function updateNowPlayingBar(showBar) {
  const bar = document.getElementById("nowPlayingBar");
  if (!bar) return;
  if (!showBar) {
    bar.classList.remove("visible");
    return;
  }
  bar.classList.add("visible");
  const titleEl = document.getElementById("npTitle");
  const fillEl = document.getElementById("npFill");
  const timeEl = document.getElementById("npTime");
  if (titleEl) titleEl.textContent = activeAudioTitle || "Playing...";
  const dur = audioEl.duration || 0;
  const cur = audioEl.currentTime || 0;
  if (fillEl) {
    const pct = dur > 0 ? Math.min(100, Math.max(0, (cur / dur) * 100)) : 0;
    fillEl.style.width = pct.toFixed(1) + "%";
  }
  if (timeEl) {
    timeEl.textContent = dur > 0
      ? (formatAudioSeconds(cur) + " / " + formatAudioSeconds(dur))
      : formatAudioSeconds(cur);
  }
}

function seekAudioFromTrack(ev) {
  const track = document.getElementById("npTrack");
  if (!track || !audioEl.duration || !isFinite(audioEl.duration)) return;
  const rect = track.getBoundingClientRect();
  if (!rect.width) return;
  const ratio = Math.min(1, Math.max(0, (ev.clientX - rect.left) / rect.width));
  audioEl.currentTime = ratio * audioEl.duration;
  updateNowPlayingBar(true);
}

function syncAllAudioButtonsUI(isPlaying) {
  document.querySelectorAll("[data-default-label]").forEach(btn => {
    const matchesActive = (btn.id === activeAudioBtnId) ||
      (btn.getAttribute("data-audio-key") && btn.getAttribute("data-audio-key") === activeAudioKey);
    if (matchesActive && isPlaying) {
      btn.classList.add("playing");
      btn.innerHTML = "⏸️ Pause";
    } else {
      btn.classList.remove("playing");
      btn.innerHTML = btn.getAttribute("data-default-label");
    }
  });
  const topBtn = document.getElementById("topPlayBtn");
  if (topBtn) {
    if (isPlaying) {
      topBtn.classList.add("playing");
      topBtn.innerHTML = "⏸️ Pause";
    } else {
      topBtn.classList.remove("playing");
      topBtn.innerHTML = "🔊 Listen";
    }
  }
  updateNowPlayingBar(isPlaying);
}

function stopAllAudio() {
  audioEl.pause();
  activeAudioBtnId = null;
  activeAudioKey = null;
  syncAllAudioButtonsUI(false);
}

function playOrToggleAudio(btnId, audioKey, srcUrl, titleText, onBlockedCallback) {
  if (!srcUrl) return;
  if (activeAudioKey === audioKey && !audioEl.paused) {
    audioEl.pause();
    syncAllAudioButtonsUI(false);
    return;
  }
  if (activeAudioKey === audioKey && audioEl.paused && audioEl.currentTime > 0 && !audioEl.ended) {
    activeAudioBtnId = btnId;
    syncAllAudioButtonsUI(true);
    audioEl.play().catch(() => syncAllAudioButtonsUI(false));
    return;
  }
  audioEl.pause();
  activeAudioBtnId = btnId;
  activeAudioKey = audioKey;
  activeAudioTitle = titleText || "";
  audioEl.src = srcUrl;
  audioEl.currentTime = 0;
  syncAllAudioButtonsUI(true);
  const p = audioEl.play();
  if (p && p.then) {
    p.then(() => {
      autoWelcomeSucceeded = true;
      detachAutoWelcomeGestureFallback();
    }).catch(() => {
      stopAllAudio();
      if (typeof onBlockedCallback === "function") onBlockedCallback();
    });
  }
}

function onFirstGestureWelcomeUnlock(ev) {
  detachAutoWelcomeGestureFallback();
  if (autoWelcomeSucceeded || !audioEl.paused || activeAudioKey) return;
  const explicitTarget = (ev && ev.target && typeof ev.target.closest === "function")
    ? ev.target.closest("#topPlayBtn, #btnDayMainPlay, .ag-btn, .game-tile, .day-chip, .day-nav-btn, .tab-btn, .slide-dot, .big-voice-btn")
    : null;
  if (explicitTarget) return;
  autoWelcomeSucceeded = true;
  if (curTab === "letter") toggleSlideAudio();
  else if (curTab === "pillars") togglePillarVoice(curPillar);
  else toggleDayVoice();
}

function attachAutoWelcomeGestureFallback() {
  if (autoWelcomeFallbackArmed || !document.addEventListener) return;
  autoWelcomeFallbackArmed = true;
  document.addEventListener("pointerdown", onFirstGestureWelcomeUnlock, true);
  document.addEventListener("touchstart", onFirstGestureWelcomeUnlock, true);
  document.addEventListener("keydown", onFirstGestureWelcomeUnlock, true);
}

function detachAutoWelcomeGestureFallback() {
  if (!autoWelcomeFallbackArmed || !document.removeEventListener) return;
  autoWelcomeFallbackArmed = false;
  document.removeEventListener("pointerdown", onFirstGestureWelcomeUnlock, true);
  document.removeEventListener("touchstart", onFirstGestureWelcomeUnlock, true);
  document.removeEventListener("keydown", onFirstGestureWelcomeUnlock, true);
}

function preloadGameAudio(dNum, gIdx) {
  try {
    const dObj = ANONDO_DATA.days[dNum - 1];
    if (!dObj || !dObj.games[gIdx] || typeof Audio !== "function") return;
    const pre = new Audio();
    pre.preload = "auto";
    pre.src = dObj.games[gIdx].audio_url;
  } catch (e) {}
}

function engageProactiveWelcomeAudio() {
  const dObj = ANONDO_DATA.days[curDay - 1];
  if (!dObj) return;
  preloadGameAudio(curDay, curGame);
  playOrToggleAudio(
    "btnDayMainPlay",
    "day_main_" + curDay,
    dObj.audio_url,
    "Day " + curDay + ": Overview",
    attachAutoWelcomeGestureFallback
  );
}

audioEl.addEventListener("timeupdate", () => {
  if (!audioEl.paused) updateNowPlayingBar(true);
});

audioEl.addEventListener("ended", () => {
  const finishedKey = activeAudioKey;
  stopAllAudio();
  if (curTab === "letter" && autoAdvanceSlides && finishedKey && finishedKey.startsWith("slide_") && curSlide < ANONDO_DATA.slides.length - 1) {
    setTimeout(() => goToSlide(curSlide + 1, true), 800);
  } else if (curTab === "play" && finishedKey && finishedKey.startsWith("day_main_")) {
    toggleGameVoice(curDay, curGame);
  } else if (curTab === "pillars" && finishedKey && finishedKey.startsWith("pillar_") && curPillar < PILLARS_DATA.length - 1) {
    curPillar++;
    renderPillarsView();
    setTimeout(() => togglePillarVoice(curPillar), 700);
  }
});

function toggleDayVoice() {
  const dObj = ANONDO_DATA.days[curDay - 1];
  if (!dObj) return;
  preloadGameAudio(curDay, curGame);
  playOrToggleAudio("btnDayMainPlay", "day_main_" + curDay, dObj.audio_url, "Day " + curDay + ": Overview", attachAutoWelcomeGestureFallback);
}

function toggleGameVoice(dNum, gIdx) {
  const dObj = ANONDO_DATA.days[dNum - 1];
  if (!dObj || !dObj.games[gIdx]) return;
  const g = dObj.games[gIdx];
  const key = "ag_" + dNum + "_" + gIdx;
  playOrToggleAudio("btnAgPlay_" + dNum + "_" + gIdx, key, g.audio_url, g.short, attachAutoWelcomeGestureFallback);
}

function toggleQuoteAudio() {
  const q = ANONDO_DATA.quotes[curQuote];
  if (!q) return;
  playOrToggleAudio("btnQuotePlay", "quote_" + curQuote, q.audio_url, "Daily Anchor", attachAutoWelcomeGestureFallback);
}

function toggleSlideAudio() {
  const s = ANONDO_DATA.slides[curSlide];
  if (!s) return;
  playOrToggleAudio("btnSlideMainPlay", "slide_" + s.id, s.audio_url, s.badge, attachAutoWelcomeGestureFallback);
}

function togglePillarVoice(pIdx) {
  curPillar = Math.max(0, Math.min(PILLARS_DATA.length - 1, pIdx));
  const p = PILLARS_DATA[curPillar];
  const q = ANONDO_DATA.quotes[curPillar % ANONDO_DATA.quotes.length];
  if (!p || !q) return;
  playOrToggleAudio("btnPillarPlay_" + curPillar, "pillar_" + curPillar, p.audio_url || q.audio_url, p.badge, attachAutoWelcomeGestureFallback);
}

function toggleMasterAudio() {
  if (!audioEl.paused) {
    audioEl.pause();
    syncAllAudioButtonsUI(false);
    return;
  }
  if (activeAudioKey && audioEl.paused && audioEl.currentTime > 0 && !audioEl.ended) {
    syncAllAudioButtonsUI(true);
    audioEl.play().catch(() => stopAllAudio());
    return;
  }
  if (curTab === "letter") toggleSlideAudio();
  else if (curTab === "pillars") togglePillarVoice(curPillar);
  else if (!autoWelcomeSucceeded && !activeAudioKey) toggleDayVoice();
  else toggleGameVoice(curDay, curGame);
}
