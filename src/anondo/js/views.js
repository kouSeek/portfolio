/* ============================================================================
   ANONDO MODULE 2: VIEW RENDERERS & BOOTSTRAP (`src/anondo/js/views.js`)
   ============================================================================ */
function showToast(msg) {
  const el = document.getElementById("toastEl");
  el.textContent = msg;
  el.style.display = "block";
  clearTimeout(window._tTimer);
  window._tTimer = setTimeout(() => { el.style.display = "none"; }, 3200);
}

function switchTab(tab) {
  curTab = tab;
  stopAllAudio();
  ["play", "letter", "pillars"].forEach(t => {
    document.getElementById("view" + t.charAt(0).toUpperCase() + t.slice(1)).classList.toggle("active", t === tab);
    document.getElementById("tab" + t.charAt(0).toUpperCase() + t.slice(1)).classList.toggle("active", t === tab);
  });
  if (tab === "play") {
    renderPlayView();
    toggleDayVoice();
  } else if (tab === "letter") {
    curQuote = (curQuote + 1) % ANONDO_DATA.quotes.length;
    renderLetterView();
    toggleSlideAudio();
  } else if (tab === "pillars") {
    renderPillarsView();
    togglePillarVoice(curPillar);
  }
}

function toggleOffDutyMode() {
  const btn = document.getElementById("offDutyBtn");
  btn.textContent = "✅ Caretaker Shift Off (100% Free)";
  showToast("🌿 Caretaker coat hung up—this evening belongs strictly to play, music & rest!");
}

function escapeSingleQuotes(s) {
  return String(s || "").replace(/\\/g, "\\\\").replace(/'/g, "\\'");
}

function renderPlayView() {
  const strip = document.getElementById("dayStrip");
  strip.innerHTML = ANONDO_DATA.days.map(d => {
    const allDone = d.games.every((_, idx) => doneMap[d.day + "_" + idx]);
    const cls = "day-chip" + (d.day === curDay ? " active" : "") + (allDone ? " done" : "");
    return `<button class="${cls}" onclick="selectDay(${d.day}, true)">${allDone ? "✅ " : ""}Day ${d.day}</button>`;
  }).join("");

  const dObj = ANONDO_DATA.days[curDay - 1];
  document.getElementById("heroPhasePill").textContent = `✨ ${dObj.phase || 'House-Money Era'} • As the day, so is the day`;
  document.getElementById("heroDayTitle").textContent = `Day ${dObj.day} • ${dObj.title}`;
  document.getElementById("heroDaySub").textContent = dObj.sub;
  document.getElementById("prevDayBtn").disabled = (curDay <= 1);
  document.getElementById("nextDayBtn").disabled = (curDay >= ANONDO_DATA.days.length);

  const grid = document.getElementById("gameGrid");
  grid.innerHTML = dObj.games.map((g, idx) => {
    const isDone = !!doneMap[curDay + "_" + idx];
    const cls = "game-tile" + (idx === curGame ? " active" : "") + (isDone ? " done" : "");
    return `<button class="${cls}" onclick="selectGame(${idx}, true)">${isDone ? "✅ " : ""}${g.short}</button>`;
  }).join("");

  const ag = dObj.games[curGame] || dObj.games[0];
  const isDone = !!doneMap[curDay + "_" + curGame];
  const agAudioKey = `ag_${curDay}_${curGame}`;
  const btnId = `btnAgPlay_${curDay}_${curGame}`;
  const topBtnId = `btnAgPlayTop_${curDay}_${curGame}`;
  const isSong = (ag.pillar === "music") || (ag.category || "").includes("🎵");

  const ytGuideHtml = isSong ? `
    <div class="prompt-box yt-box">
      <div class="prompt-lbl">🎵 Eyes-Closed Pass-1 Listening (@YouTube Music + 3-Pass Bhaavna):</div>
      <div style="font-size:0.92rem;color:var(--ink-2);">Ask Gemini to launch the track on YouTube Music, close your eyes on Pass 1 with zero note-grading, picture the visual movie scene, and then unpack the lyric philosophy in Turn 2.</div>
    </div>` : "";

  const followupHtml = ag.followup_prompt ? `
    <div class="prompt-box followup-box">
      <div class="prompt-lbl-row">
        <span class="prompt-lbl">💬 Turn 2 — Deepen, Steelman or Test Your Ear:</span>
        <button class="ag-btn" style="padding:4px 10px;font-size:0.8rem;" onclick="copyPrompt('${escapeSingleQuotes(ag.followup_prompt)}')">📋 Copy Turn 2</button>
      </div>
      <div class="prompt-txt">“${ag.followup_prompt}”</div>
    </div>` : "";

  document.getElementById("activeGameStage").innerHTML = `
    <article class="card">
      <div class="card-top-bar">
        <span class="card-badge">${ag.category}</span>
        <div class="card-inline-controls">
          <button id="${topBtnId}" class="ag-btn listen" data-default-label="🔊 Listen" data-audio-key="${agAudioKey}" onclick="toggleGameVoice(${curDay}, ${curGame})">🔊 Listen</button>
          <button class="ag-btn check ${isDone ? 'checked' : ''}" onclick="toggleDone(${curDay}, ${curGame})">
            ${isDone ? '✅ Done' : '⬜ Mark Done'}
          </button>
          <button class="ag-btn" ${curGame <= 0 ? "disabled" : ""} onclick="selectGame(${curGame - 1}, true)" title="Previous">⬅️</button>
          <button class="ag-btn" ${curGame >= dObj.games.length - 1 ? "disabled" : ""} onclick="selectGame(${curGame + 1}, true)" title="Next">➡️</button>
        </div>
      </div>

      <h2 class="card-title">${ag.title}</h2>
      <p class="card-story">${ag.detail}</p>
      ${ytGuideHtml}

      <div class="prompt-box">
        <div class="prompt-lbl-row">
          <span class="prompt-lbl">🎙️ Turn 1 — Speak or Paste into Gemini Live:</span>
          <button class="ag-btn" style="padding:4px 10px;font-size:0.8rem;" onclick="copyPrompt('${escapeSingleQuotes(ag.prompt)}')">📋 Copy Turn 1</button>
        </div>
        <div class="prompt-txt">“${ag.prompt}”</div>
      </div>
      ${followupHtml}

      <div class="agenda-actions">
        <button id="${btnId}" class="ag-btn listen" data-default-label="🔊 Listen" data-audio-key="${agAudioKey}" onclick="toggleGameVoice(${curDay}, ${curGame})">🔊 Listen</button>
        <button class="ag-btn check ${isDone ? 'checked' : ''}" onclick="toggleDone(${curDay}, ${curGame})">
          ${isDone ? '✅ Enjoyed & Completed' : '⬜ I Enjoyed This'}
        </button>
      </div>
      <div class="game-stepper-row">
        <button class="ag-btn" ${curGame <= 0 ? "disabled" : ""} onclick="selectGame(${curGame - 1}, true)">⬅️ Previous Exploration</button>
        <button class="ag-btn" ${curGame >= dObj.games.length - 1 ? "disabled" : ""} onclick="selectGame(${curGame + 1}, true)">Next Exploration ➡️</button>
      </div>
    </article>
  `;
  syncAllAudioButtonsUI(!audioEl.paused);
}

function getFirstOpenGameForDay(dNum) {
  const dObj = ANONDO_DATA.days[dNum - 1];
  if (!dObj || !dObj.games) return 0;
  for (let i = 0; i < dObj.games.length; i++) {
    if (!doneMap[dNum + "_" + i]) return i;
  }
  return 0;
}

function findInitialCurrentDay() {
  for (let i = 0; i < ANONDO_DATA.days.length; i++) {
    const d = ANONDO_DATA.days[i];
    const allDone = d.games.every((_, idx) => doneMap[d.day + "_" + idx]);
    if (!allDone) {
      curDay = d.day;
      curGame = getFirstOpenGameForDay(curDay);
      return;
    }
  }
  curDay = 1;
  curGame = 0;
}

function selectDay(d, autoPlay) {
  if (d < 1 || d > ANONDO_DATA.days.length) return;
  curDay = d;
  curGame = getFirstOpenGameForDay(d);
  stopAllAudio();
  renderPlayView();
  if (autoPlay !== false) toggleDayVoice();
}

function selectGame(idx, autoPlay) {
  const dObj = ANONDO_DATA.days[curDay - 1];
  curGame = Math.max(0, Math.min(dObj.games.length - 1, idx));
  stopAllAudio();
  renderPlayView();
  if (autoPlay !== false) toggleGameVoice(curDay, curGame);
}

function toggleDone(d, idx) {
  const k = d + "_" + idx;
  doneMap[k] = !doneMap[k];
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(doneMap)); } catch (e) {}
  if (doneMap[k]) {
    showToast("🌻 Nice flow, Koushik!");
    const dObj = ANONDO_DATA.days[d - 1];
    if (idx + 1 < dObj.games.length) {
      curGame = idx + 1;
      stopAllAudio();
      renderPlayView();
      toggleGameVoice(d, curGame);
      return;
    } else if (d < ANONDO_DATA.days.length) {
      curDay = d + 1;
      curGame = getFirstOpenGameForDay(curDay);
      stopAllAudio();
      renderPlayView();
      toggleDayVoice();
      return;
    }
  }
  renderPlayView();
}

function copyPrompt(txt) {
  if (navigator.clipboard) navigator.clipboard.writeText(txt);
  showToast("📋 Copied—open Gemini Live to speak or paste!");
}

function nextQuote(autoPlay) {
  curQuote = (curQuote + 1) % ANONDO_DATA.quotes.length;
  document.getElementById("quoteBox").textContent = "“" + ANONDO_DATA.quotes[curQuote].text + "”";
  stopAllAudio();
  if (autoPlay !== false) toggleQuoteAudio();
}

function renderLetterView() {
  document.getElementById("quoteBox").textContent = "“" + ANONDO_DATA.quotes[curQuote].text + "”";
  const s = ANONDO_DATA.slides[curSlide];
  const slideAudioKey = "slide_" + s.id;
  const dotsHtml = ANONDO_DATA.slides.map((item, idx) =>
    `<button class="slide-dot ${idx === curSlide ? 'active' : ''}" onclick="goToSlide(${idx}, true)">${idx + 1}</button>`
  ).join("");
  const imgHtml = s.img_b64 ? `
    <div class="slide-img-wrap">
      <img class="slide-img" src="${s.img_b64}" alt="${s.title}" />
    </div>` : "";

  document.getElementById("letterStage").innerHTML = `
    <div class="card-top-bar">
      <span class="card-badge">${s.badge}</span>
      <div class="card-inline-controls">
        <button id="btnSlideTopPlay" class="ag-btn listen" data-default-label="🔊 Listen to Slide" data-audio-key="${slideAudioKey}" onclick="toggleSlideAudio()">🔊 Listen to Slide</button>
        <button class="ag-btn" ${curSlide <= 0 ? "disabled" : ""} onclick="changeSlide(-1, true)">⬅️ Prev</button>
        <button class="ag-btn" ${curSlide >= ANONDO_DATA.slides.length - 1 ? "disabled" : ""} onclick="changeSlide(1, true)">Next ➡️</button>
      </div>
    </div>
    ${imgHtml}
    <div class="slide-dots">${dotsHtml}</div>
    <h2 class="card-title">${s.title}</h2>
    <div class="reframe-box" style="font-weight:700;">✨ ${s.highlight}</div>
    <p class="card-story">${s.text}</p>
    <button id="btnSlideMainPlay" class="big-voice-btn" data-default-label="🔊 Listen to Slide" data-audio-key="${slideAudioKey}" onclick="toggleSlideAudio()" style="margin-bottom:10px;">
      🔊 Listen to Slide
    </button>
    <div class="game-stepper-row">
      <button class="ag-btn" ${curSlide <= 0 ? "disabled" : ""} onclick="changeSlide(-1, true)">⬅️ Previous</button>
      <button class="ag-btn" onclick="toggleAutoAdvanceSlides()">${autoAdvanceSlides ? "🔁 Auto-Advance: ON" : "🔁 Auto-Advance: OFF"}</button>
      <button class="ag-btn" ${curSlide >= ANONDO_DATA.slides.length - 1 ? "disabled" : ""} onclick="changeSlide(1, true)">Next ➡️</button>
    </div>
  `;
  syncAllAudioButtonsUI(!audioEl.paused);
}

function toggleAutoAdvanceSlides() {
  autoAdvanceSlides = !autoAdvanceSlides;
  renderLetterView();
}

function goToSlide(idx, autoPlay) {
  curSlide = Math.max(0, Math.min(ANONDO_DATA.slides.length - 1, idx));
  stopAllAudio();
  renderLetterView();
  if (autoPlay !== false) toggleSlideAudio();
}

function changeSlide(delta, autoPlay) {
  goToSlide(curSlide + delta, autoPlay !== false);
}

function renderPillarsView() {
  document.getElementById("pillarsContainer").innerHTML = PILLARS_DATA.map((p, idx) => `
    <div class="prompt-box" style="margin-bottom:0;">
      <div class="prompt-lbl-row">
        <div class="prompt-lbl">${p.badge} — ${p.title}</div>
        <button id="btnPillarPlay_${idx}" class="ag-btn listen" style="padding:5px 11px;font-size:0.82rem;" data-default-label="🔊 Listen" data-audio-key="pillar_${idx}" onclick="togglePillarVoice(${idx})">🔊 Listen</button>
      </div>
      <p style="font-size:0.94rem;color:var(--ink-2);">${p.detail}</p>
    </div>
  `).join("");
  syncAllAudioButtonsUI(!audioEl.paused);
}

function openSosModal() {
  document.getElementById("sosModal").classList.add("open");
}

function closeSosModal() {
  document.getElementById("sosModal").classList.remove("open");
  if (sosInterval) clearInterval(sosInterval);
}

function startSosTimer(sec) {
  if (sosInterval) clearInterval(sosInterval);
  let rem = sec;
  const el = document.getElementById("sosTimerDisplay");
  el.textContent = rem + "s";
  sosInterval = setInterval(() => {
    rem--;
    if (rem <= 0) {
      clearInterval(sosInterval);
      el.textContent = "✅ 20s complete! Exhale slowly.";
    } else {
      el.textContent = rem + "s";
    }
  }, 1000);
}

let _screenWakeLock = null;
let _screenWakeLockPending = false;

async function requestScreenWakeLock() {
  try {
    if (typeof navigator === "undefined" || !navigator.wakeLock || typeof navigator.wakeLock.request !== "function") {
      return null;
    }
    if (typeof document !== "undefined" && document.visibilityState === "hidden") {
      return null;
    }
    if (_screenWakeLock && !_screenWakeLock.released) {
      return _screenWakeLock;
    }
    if (_screenWakeLockPending) {
      return _screenWakeLock;
    }
    _screenWakeLockPending = true;
    const sentinel = await navigator.wakeLock.request("screen");
    _screenWakeLock = sentinel || { released: false };
    _screenWakeLockPending = false;
    if (typeof window !== "undefined") {
      window._screenWakeLock = _screenWakeLock;
    }
    if (sentinel && typeof sentinel.addEventListener === "function") {
      sentinel.addEventListener("release", () => {
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
  if (typeof document !== "undefined" && typeof document.addEventListener === "function") {
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState !== "hidden") {
        requestScreenWakeLock();
      }
    });
    ["touchstart", "pointerdown", "click", "keydown"].forEach(evName => {
      document.addEventListener(evName, () => {
        if (!_screenWakeLock || _screenWakeLock.released) {
          requestScreenWakeLock();
        }
      }, { passive: true });
    });
  }
  if (typeof window !== "undefined" && typeof window.addEventListener === "function") {
    window.addEventListener("focus", () => requestScreenWakeLock());
    window.addEventListener("pageshow", () => requestScreenWakeLock());
  }
  if (typeof setInterval === "function") {
    const _wlTimer = setInterval(() => {
      if (typeof document === "undefined" || document.visibilityState !== "hidden") {
        if (!_screenWakeLock || _screenWakeLock.released) {
          requestScreenWakeLock();
        }
      }
    }, 25000);
    if (_wlTimer && typeof _wlTimer.unref === "function") _wlTimer.unref();
  }
})();

(function hydratePageFavicon() {
  function apply() {
    try {
      if (!document.head || typeof document.createElement !== "function") return;
      const el = document.getElementById("pageFavicon");
      if (!el || !el.getAttribute) return;
      const emoji = el.getAttribute("data-emoji") || "";
      const b64 = el.getAttribute("data-png-b64") || "";
      const httpsPng = el.getAttribute("data-https-png") || b64;
      const httpsIco = el.getAttribute("data-https-ico") || httpsPng;
      const useHttps = (typeof location !== "undefined" && /^https?:$/i.test(location.protocol) && (typeof navigator === "undefined" || navigator.onLine !== false));
      const pngHref = useHttps ? httpsPng : (b64 || httpsPng);
      const icoHref = useHttps ? httpsIco : (b64 || httpsIco);
      document.querySelectorAll('link[rel*="icon"]').forEach(n => { if (n.parentNode) n.parentNode.removeChild(n); });
      const l1 = document.createElement("link");
      l1.id = "pageFavicon";
      l1.setAttribute("data-emoji", emoji);
      l1.setAttribute("data-png-b64", b64);
      l1.setAttribute("data-https-png", httpsPng);
      l1.setAttribute("data-https-ico", httpsIco);
      l1.rel = "icon"; l1.type = "image/png"; l1.sizes = "64x64"; l1.href = pngHref;
      document.head.appendChild(l1);
      const l2 = document.createElement("link");
      l2.rel = "shortcut icon"; l2.type = useHttps ? "image/x-icon" : "image/png"; l2.href = icoHref;
      document.head.appendChild(l2);
      const l3 = document.createElement("link");
      l3.rel = "apple-touch-icon"; l3.sizes = "64x64"; l3.href = b64 || pngHref;
      document.head.appendChild(l3);
    } catch (e) {}
  }
  apply();
  if (typeof setTimeout === "function") setTimeout(apply, 90);
})();

findInitialCurrentDay();
renderPlayView();
renderLetterView();
renderPillarsView();
engageProactiveWelcomeAudio();
