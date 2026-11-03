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

(function hydratePageFavicon() {
  try {
    if (!document.head || typeof document.createElement !== "function") return;
    const el = document.getElementById("pageFavicon");
    if (!el) return;
    const emoji = el.getAttribute && el.getAttribute("data-emoji");
    let uri = el.getAttribute ? el.getAttribute("href") : el.href;
    let mime = "image/svg+xml";
    if (emoji) {
      const c = document.createElement("canvas");
      c.width = 64; c.height = 64;
      const ctx = c.getContext && c.getContext("2d");
      if (ctx) {
        ctx.font = '54px "Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif';
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(emoji, 32, 35);
        uri = c.toDataURL("image/png");
        mime = "image/png";
      }
    }
    if (!uri) return;
    document.querySelectorAll('link[rel*="icon"]').forEach(n => { if (n.parentNode) n.parentNode.removeChild(n); });
    ["icon", "shortcut icon", "apple-touch-icon"].forEach(rel => {
      const lk = document.createElement("link");
      if (rel === "icon") { lk.id = "pageFavicon"; if (emoji) lk.setAttribute("data-emoji", emoji); }
      lk.rel = rel;
      if (rel !== "apple-touch-icon") lk.type = mime;
      lk.href = uri;
      document.head.appendChild(lk);
    });
  } catch (e) {}
})();

findInitialCurrentDay();
renderPlayView();
renderLetterView();
renderPillarsView();
engageProactiveWelcomeAudio();
