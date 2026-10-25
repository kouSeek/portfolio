/* ============================================================================
   MODULE 3: DAILY 6-GAME VIEW CONTROLLER, SEQUENTIAL LOCK & CALENDAR GRIDS
   (🎓 আজকের খেলা — src/js/plan-view.js)
   ============================================================================ */
function togglePrimaryCalendarGrid() {
  primaryCalOpen = !primaryCalOpen;
  renderPlanView();
}

function toggleExtendedCalendarGrid() {
  extCalOpen = !extCalOpen;
  renderPlanView();
}

function selectDay(dayNum, autoPlayAudio) {
  if (!isDayUnlocked(dayNum)) {
    const frontier = getHighestUnlockedDay();
    showCelebrationToast('🔒 মা, আগে ‘দিন ' + toBnDigits(frontier) + '’-এর সবকটা খেলায় টিক (✅) দাও—তাহলেই নতুন দিনের চমক খুলে যাবে!');
    return false;
  }
  curDayNum = dayNum;
  curGameIdx = getFirstIncompleteGameIdx(dayNum);
  primaryCalOpen = false;
  stopAllAudio();
  renderPlanView();
  scrollActiveDayChipIntoView();
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if (autoPlayAudio) toggleDayOverviewAudio();
  return true;
}

function selectGame(gIdx) {
  const d = findDayObj(curDayNum);
  const maxIdx = (d && d.agendas) ? d.agendas.length - 1 : 5;
  curGameIdx = Math.max(0, Math.min(maxIdx, gIdx));
  stopAllAudio();
  renderPlanView();
}

function toggleShowAllGames() {
  showAllGamesInDay = !showAllGamesInDay;
  renderPlanView();
}

function toggleAgendaDone(dayNum, agIdx) {
  const key = dayNum + '_' + agIdx;
  const newlyDone = !doneMap[key];
  doneMap[key] = newlyDone;
  saveDoneMap();

  if (newlyDone) {
    if (isDayFullyDone(dayNum)) {
      if (dayNum === 21) {
        extCalOpen = true;
        showCelebrationToast('🎉 অসাধারণ মা! ২১ দিনের সব খেলা শেষ—এবার নতুন ৩০ দিনের ক্যালেন্ডার খুলে গেছে!');
      } else if (dayNum < ALL_DAYS.length) {
        showCelebrationToast('🎉 দারুণ মা! দিন ' + toBnDigits(dayNum) + ' শেষ হয়েছে—দিন ' + toBnDigits(dayNum + 1) + '-এর নতুন চমক খুলে গেল!');
      } else {
        showCelebrationToast('🎉 অসাধারণ মা! আজকের সব খেলা খুব সুন্দরভাবে শেষ হয়েছে!');
      }

      if (dayNum < ALL_DAYS.length) {
        const nextDay = dayNum + 1;
        curDayNum = nextDay;
        curGameIdx = getFirstIncompleteGameIdx(nextDay);
        stopAllAudio();
        renderPlanView();
        scrollActiveDayChipIntoView();
        toggleDayOverviewAudio();
        return;
      }
    } else {
      showCelebrationToast('🌸 সাবাশ মা! খেলাটা খুব সুন্দরভাবে শেষ করলে!');
      if (!showAllGamesInDay) {
        curGameIdx = getFirstIncompleteGameIdx(dayNum);
      }
    }
  }
  renderPlanView();
}

function buildCalendarGridCellsHtml(daysArray, idPrefix) {
  return daysArray.map(item => {
    const done = isDayFullyDone(item.day);
    const unlocked = isDayUnlocked(item.day);
    const isAct = (item.day === curDayNum);
    const stateCls = (isAct ? ' active' : '') + (done ? ' done' : '') + (!unlocked ? ' locked' : '');
    const icon = done ? '✅ ' : (!unlocked ? '🔒 ' : '');
    return `<button id="${idPrefix}_${item.day}" class="cal-day-cell${stateCls}" onclick="selectDay(${item.day}, true)">${icon}দিন ${toBnDigits(item.day)}</button>`;
  }).join('');
}

function buildAgendaCardHtml(d, ag, idx) {
  const isDone = !!doneMap[d.day + '_' + idx];
  const btnId = `btnAgPlay_${d.day}_${idx}`;
  const accent = GAME_ACCENTS[idx] || 'terra';
  const isSongGame = (ag.category || '').includes('গান') || (ag.detail_bn || '').includes('ইউটিউব মিউজিক');

  const ytMusicGuideHtml = isSongGame ? `
      <div class="agenda-prompt-box yt-music-box">
        <div class="agenda-prompt-label">🎵 ফোনের জেমিনি নিজে থেকেই ইউটিউব মিউজিকে (YouTube Music) গান বাজাতে পারে!</div>
        <div class="agenda-detail" style="font-size:1.01rem;">মা, ফোনের জেমিনির ইউটিউব মিউজিকের সাথে সরাসরি যোগ আছে। যেকোনো গান শুনতে ইচ্ছে করলেই শুধু মাইক 🎙️ ছুঁয়ে মুখে বলবে:<br><strong>“জেমিনি, ইউটিউব মিউজিকে ‘[গানের নাম বা যেকোনো লাইন]’ গানটা চালিয়ে দাও।”</strong><br>গানের পুরো নাম মনে না থাকলেও চলবে—গানের যেকোনো একটা লাইন বলে এইটুকু বললেই ও নিজে থেকে ইউটিউব মিউজিক খুলে গানটা বাজিয়ে দেবে!</div>
      </div>` : '';

  const followupHtml = ag.followup_prompt_bn ? `
      <div class="agenda-prompt-box">
        <div class="agenda-prompt-label">💬 গানটা শোনা হয়ে গেলে এর মানে আর গল্পটা জানতে জেমিনিকে বলো:</div>
        <div class="agenda-prompt-speech">“${ag.followup_prompt_bn}”</div>
      </div>` : '';

  const promptLabel = isSongGame
    ? '🎙️ ইউটিউব মিউজিকে আজকের গানটা চালাতে ফোনে জেমিনি (Gemini) খুলে মাইক ছুঁয়ে বলো:'
    : '🎙️ এবার ফোনে জেমিনি (Gemini) খুলে মাইক ছুঁয়ে মুখে বলো:';

  return `
    <article class="agenda-card ${isDone ? 'done-card' : ''}" data-accent="${accent}" id="agendaCard_${d.day}_${idx}">
      <div class="agenda-card-header">
        <div class="agenda-cat">${ag.category}</div>
      </div>
      <div class="agenda-title">${ag.title_bn}</div>
      <div class="step-section">
        <div class="agenda-step-heading">✨ মা, আজ কী করবো দেখো:</div>
        <div class="agenda-detail">${ag.detail_bn}</div>
      </div>${ytMusicGuideHtml}
      <div class="agenda-prompt-box">
        <div class="agenda-prompt-label">${promptLabel}</div>
        <div class="agenda-prompt-speech">“${ag.prompt_bn}”</div>
        <div class="agenda-prompt-howto">💡 (নিজের মতো সহজ বাংলায় বললেই হবে, ভুল হওয়ার কোনো ভয় নেই—বলো আর শোনো ও কী করে!)</div>
      </div>${followupHtml}
      <div class="agenda-actions">
        <button id="${btnId}" class="ag-btn listen" data-default-label="🔊 শোনো" onclick="playAgendaByIdx(${d.day}, ${idx}, this)">🔊 শোনো</button>
        <button class="ag-btn check ${isDone ? 'checked' : ''}" onclick="toggleAgendaDone(${d.day}, ${idx})">
          ${isDone ? '✅ করা হয়েছে' : '⬜ আমি এটা করেছি'}
        </button>
      </div>
    </article>
  `;
}

function renderPlanView() {
  if (!isDayUnlocked(curDayNum)) {
    curDayNum = getHighestUnlockedDay();
    curGameIdx = getFirstIncompleteGameIdx(curDayNum);
  }

  const strip = document.getElementById('dayStrip');
  strip.innerHTML = '';

  DAYS_21.forEach(item => {
    const btn = document.createElement('button');
    const done = isDayFullyDone(item.day);
    const unlocked = isDayUnlocked(item.day);
    const icon = done ? '✅ ' : (!unlocked ? '🔒 ' : '');
    btn.id = 'dayChip_' + item.day;
    btn.className = 'day-chip'
      + (item.day === curDayNum ? ' active' : '')
      + (done ? ' done' : '')
      + (!unlocked ? ' locked' : '');
    btn.innerHTML = icon + 'দিন ' + toBnDigits(item.day);
    btn.onclick = () => selectDay(item.day, true);
    strip.appendChild(btn);
  });

  const calBtn = document.getElementById('btnToggleCalGrid');
  if (calBtn) {
    calBtn.innerHTML = primaryCalOpen ? '🗓️ বন্ধ করো' : '🗓️ ক্যালেন্ডার';
  }

  const primaryCalEl = document.getElementById('primaryCalGridWrap');
  if (primaryCalEl) {
    if (primaryCalOpen) {
      primaryCalEl.style.display = 'block';
      primaryCalEl.innerHTML = `
        <div class="cal-grid-subtitle">মা, এক-একটা দিনের সব খেলায় টিক (✅) দিলে পরের দিনটা আপনিই খুলে যাবে:</div>
        <div id="primaryCalendarGrid" class="calendar-grid">${buildCalendarGridCellsHtml(DAYS_21, 'p1CalCell')}</div>
      `;
    } else {
      primaryCalEl.style.display = 'none';
      primaryCalEl.innerHTML = '';
    }
  }

  const extCalWrap = document.getElementById('extendedPart2CalWrap');
  if (extCalWrap) {
    if (areFirst21DaysComplete()) {
      extCalWrap.style.display = 'block';
      const extBodyHtml = extCalOpen ? `
        <div class="cal-grid-subtitle">মা, প্রথম ২১ দিনের সব খেলা শেষ করে তুমি এই নতুন ক্যালেন্ডারটা খুলেছো! নিজের আনন্দে এক-একটা দিন খেলো:</div>
        <div id="extCalendarGrid" class="calendar-grid">${buildCalendarGridCellsHtml(DAYS_PART2_30, 'calCell')}</div>
      ` : '';
      extCalWrap.innerHTML = `
        <button id="btnToggleExtCal" class="ext-cal-header-btn" onclick="toggleExtendedCalendarGrid()">
          <span>🌿 নতুন ৩০ দিনের ক্যালেন্ডার (দিন ২২ – ৫১)</span>
          <span>${extCalOpen ? '▴ গুটিয়ে রাখো' : '▾ খুলে দেখো'}</span>
        </button>${extBodyHtml}
      `;
    } else {
      extCalWrap.style.display = 'none';
      extCalWrap.innerHTML = '';
    }
  }

  const d = findDayObj(curDayNum);
  curDayNum = d.day;
  if (curGameIdx < 0 || curGameIdx >= d.agendas.length) curGameIdx = 0;
  const stage = document.getElementById('activeDayStage');

  let tilesHtml = '';
  d.agendas.forEach((ag, idx) => {
    const isDone = !!doneMap[d.day + '_' + idx];
    const isAct = (!showAllGamesInDay && idx === curGameIdx);
    const shortLbl = GAME_SHORT_LABELS[idx] || ag.category;
    const accent = GAME_ACCENTS[idx] || 'terra';
    tilesHtml += `
      <button id="gameTile_${d.day}_${idx}" data-accent="${accent}" class="game-tile ${isAct ? 'active' : ''} ${isDone ? 'done-tile' : ''}" onclick="selectGame(${idx})">
        <span class="game-tile-lbl">${isDone ? '✅ ' : ''}${shortLbl}</span>
      </button>
    `;
  });

  let agendasHtml = '';
  if (showAllGamesInDay) {
    d.agendas.forEach((ag, idx) => {
      agendasHtml += buildAgendaCardHtml(d, ag, idx);
    });
  } else {
    const activeAg = d.agendas[curGameIdx] || d.agendas[0];
    agendasHtml = buildAgendaCardHtml(d, activeAg, curGameIdx) + `
      <div class="game-stepper-row">
        <button id="prevGameBtn" class="ag-btn" ${curGameIdx <= 0 ? 'disabled' : ''} onclick="selectGame(${curGameIdx - 1})">⬅️ আগের খেলা</button>
        <button id="nextGameBtn" class="ag-btn" ${curGameIdx >= d.agendas.length - 1 ? 'disabled' : ''} onclick="selectGame(${curGameIdx + 1})">পরের খেলা ➡️</button>
      </div>
    `;
  }

  const atFirstDay = d.day <= 1;
  const atLastDay = d.day >= ALL_DAYS.length;
  const nextUnlocked = !atLastDay && isDayUnlocked(d.day + 1);
  const nextBtnCls = (!atLastDay && !nextUnlocked) ? 'ag-btn locked-btn' : 'ag-btn';
  const nextBtnLabel = atLastDay ? 'পরের দিন ➡️' : (nextUnlocked ? 'পরের দিন ➡️' : '🔒 পরের দিন');

  stage.innerHTML = `
    <div class="day-hero-card">
      <div class="day-hero-top">
        <div class="day-hero-badge">দিন ${toBnDigits(d.day)} • ${d.phase}</div>
      </div>
      <div class="day-hero-title">${d.title_bn}</div>
      <div class="day-hero-summary">${d.summary_bn}</div>
      <button id="btnDayMainPlay" class="big-voice-btn" data-default-label="🔊 আজকের কথাগুলো শোনো" onclick="toggleDayOverviewAudio()">
        🔊 আজকের কথাগুলো শোনো
      </button>
      <div class="day-prev-next-row">
        <button id="prevDayBtn" class="ag-btn" style="flex:1;" ${atFirstDay ? 'disabled' : ''} onclick="selectDay(${d.day - 1}, true)">⬅️ আগের দিন</button>
        <button id="nextDayBtn" class="${nextBtnCls}" style="flex:1;" ${atLastDay ? 'disabled' : ''} onclick="selectDay(${d.day + 1}, true)">${nextBtnLabel}</button>
      </div>
    </div>

    <div class="game-nav-card">
      <div class="game-nav-header">
        <span class="game-nav-title">🎯 আজকের খেলাগুলো (যেকোনোটায় ছুঁয়ে খোলো):</span>
        <button id="toggleAllGamesBtn" class="view-mode-toggle" onclick="toggleShowAllGames()">
          ${showAllGamesInDay ? '🎯 ১টি করে দেখো' : '📜 সব খেলা একসাথে'}
        </button>
      </div>
      <div class="game-grid-6">${tilesHtml}</div>
    </div>

    <div class="agenda-stack">${agendasHtml}</div>
  `;
  syncAllAudioButtonsUI(!audioEl.paused);
}
