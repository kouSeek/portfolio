/* ============================================================================
   MODULE 3: DAILY 6-GAME VIEW CONTROLLER (🎓 আজকের খেলা — src/js/plan-view.js)
   ============================================================================ */
function switchCoursePart(partNum) {
  curPart = partNum;
  document.getElementById('segPart1').className = 'part-seg-btn' + (partNum === 1 ? ' active' : '');
  document.getElementById('segPart2').className = 'part-seg-btn' + (partNum === 2 ? ' active' : '');
  const list = partNum === 2 ? DAYS_PART2_30 : DAYS_21;
  const firstInc = list.find(d => !isDayFullyDone(d.day));
  curDayNum = firstInc ? firstInc.day : list[0].day;
  curGameIdx = getFirstIncompleteGameIdx(curDayNum);
  stopAllAudio();
  renderPlanView();
  scrollActiveDayChipIntoView();
}

function selectDay(dayNum, autoPlayAudio) {
  curDayNum = dayNum;
  curPart = dayNum > 21 ? 2 : 1;
  document.getElementById('segPart1').className = 'part-seg-btn' + (curPart === 1 ? ' active' : '');
  document.getElementById('segPart2').className = 'part-seg-btn' + (curPart === 2 ? ' active' : '');
  curGameIdx = getFirstIncompleteGameIdx(dayNum);
  stopAllAudio();
  renderPlanView();
  scrollActiveDayChipIntoView();
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if (autoPlayAudio) toggleDayOverviewAudio();
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
      const doneDayObj = findDayObj(dayNum);
      const dispDone = doneDayObj.part === 2 ? toBnDigits(doneDayObj.part_day) : toBnDigits(dayNum);
      showCelebrationToast('🎉 দারুণ মা! দিন ' + dispDone + '-এর সব খেলা সম্পূর্ণ হয়েছে!');
      if (dayNum < 51) {
        const nextDay = dayNum + 1;
        curDayNum = nextDay;
        curPart = nextDay > 21 ? 2 : 1;
        document.getElementById('segPart1').className = 'part-seg-btn' + (curPart === 1 ? ' active' : '');
        document.getElementById('segPart2').className = 'part-seg-btn' + (curPart === 2 ? ' active' : '');
        curGameIdx = getFirstIncompleteGameIdx(nextDay);
        stopAllAudio();
        renderPlanView();
        scrollActiveDayChipIntoView();
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
        <div class="agenda-prompt-label">🗣️ ধাপ ৩ — গানটা শোনা হয়ে গেলে এর মানে আর গল্পটা জানতে জেমিনিকে বলো:</div>
        <div class="agenda-prompt-speech">“${ag.followup_prompt_bn}”</div>
      </div>` : '';

  const step2Label = isSongGame
    ? '🎙️ ধাপ ২ — ইউটিউব মিউজিকে আজকের গানটা চালাতে ফোনে জেমিনি (Gemini) খুলে মাইক ছুঁয়ে বলো:'
    : '🎙️ ধাপ ২ — এবার ফোনে জেমিনি (Gemini) খুলে মাইক ছুঁয়ে মুখে বলো:';

  return `
    <article class="agenda-card ${isDone ? 'done-card' : ''}" data-accent="${accent}" id="agendaCard_${d.day}_${idx}">
      <div class="agenda-card-header">
        <div class="agenda-cat">${ag.category}</div>
        <span class="agenda-slot-pill">খেলা ${idx + 1} / ${d.agendas.length}</span>
      </div>
      <div class="agenda-title">${ag.title_bn}</div>
      <div class="step-section">
        <div class="agenda-step-heading">📋 ধাপ ১ — মা, আজ কী করবো দেখো:</div>
        <div class="agenda-detail">${ag.detail_bn}</div>
      </div>${ytMusicGuideHtml}
      <div class="agenda-prompt-box">
        <div class="agenda-prompt-label">${step2Label}</div>
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
  updateProgressPill();
  const activeList = getActiveCourseDays();
  const strip = document.getElementById('dayStrip');
  strip.innerHTML = '';

  activeList.forEach(d => {
    const btn = document.createElement('button');
    const done = isDayFullyDone(d.day);
    const dispDay = d.part === 2 ? ('দিন ' + toBnDigits(d.part_day)) : ('দিন ' + toBnDigits(d.day));
    btn.id = 'dayChip_' + d.day;
    btn.className = 'day-chip' + (d.day === curDayNum ? ' active' : '') + (done ? ' done' : '');
    btn.innerHTML = (done ? '✅ ' : '') + dispDay;
    btn.onclick = () => selectDay(d.day, false);
    strip.appendChild(btn);
  });

  const d = activeList.find(x => x.day === curDayNum) || activeList[0];
  curDayNum = d.day;
  if (curGameIdx < 0 || curGameIdx >= d.agendas.length) curGameIdx = 0;
  const stage = document.getElementById('activeDayStage');

  let dayDoneCount = 0;
  let tilesHtml = '';
  d.agendas.forEach((ag, idx) => {
    const isDone = !!doneMap[d.day + '_' + idx];
    if (isDone) dayDoneCount++;
    const isAct = (!showAllGamesInDay && idx === curGameIdx);
    const shortLbl = GAME_SHORT_LABELS[idx] || ('খেলা ' + (idx + 1));
    const accent = GAME_ACCENTS[idx] || 'terra';
    tilesHtml += `
      <button id="gameTile_${d.day}_${idx}" data-accent="${accent}" class="game-tile ${isAct ? 'active' : ''} ${isDone ? 'done-tile' : ''}" onclick="selectGame(${idx})">
        <span class="game-tile-num">${isDone ? '✅ ' : ''}খেলা ${toBnDigits(idx + 1)}</span>
        <span class="game-tile-lbl">${shortLbl}</span>
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
        <button id="prevGameBtn" class="ag-btn" ${curGameIdx <= 0 ? 'disabled' : ''} onclick="selectGame(${curGameIdx - 1})">⬅️ আগের খেলা (${toBnDigits(curGameIdx)}/${toBnDigits(d.agendas.length)})</button>
        <button id="nextGameBtn" class="ag-btn" ${curGameIdx >= d.agendas.length - 1 ? 'disabled' : ''} onclick="selectGame(${curGameIdx + 1})">পরের খেলা (${toBnDigits(curGameIdx + 2)}/${toBnDigits(d.agendas.length)}) ➡️</button>
      </div>
    `;
  }

  const minDay = activeList[0].day;
  const maxDay = activeList[activeList.length - 1].day;
  const dispDayLabel = d.part === 2 ? ('পার্ট ২ • দিন ' + toBnDigits(d.part_day)) : ('পার্ট ১ • দিন ' + toBnDigits(d.day));

  stage.innerHTML = `
    <div class="day-hero-card">
      <div class="day-hero-top">
        <div class="day-hero-badge">${dispDayLabel} • ${d.phase}</div>
        <span class="day-hero-prog">আজকের অগ্রগতি: ${toBnDigits(dayDoneCount)} / ${toBnDigits(d.agendas.length)}</span>
      </div>
      <div class="day-hero-title">${d.title_bn}</div>
      <div class="day-hero-summary">${d.summary_bn}</div>
      <button id="btnDayMainPlay" class="big-voice-btn" data-default-label="🔊 আজকের কথাগুলো শোনো" onclick="toggleDayOverviewAudio()">
        🔊 আজকের কথাগুলো শোনো
      </button>
      <div class="day-prev-next-row">
        <button class="ag-btn" style="flex:1;" ${d.day <= minDay ? 'disabled' : ''} onclick="selectDay(${d.day - 1}, false)">⬅️ আগের দিন</button>
        <button class="ag-btn" style="flex:1;" ${d.day >= maxDay ? 'disabled' : ''} onclick="selectDay(${d.day + 1}, false)">পরের দিন ➡️</button>
      </div>
    </div>

    <div class="game-nav-card">
      <div class="game-nav-header">
        <span class="game-nav-title">🎯 আজকের ${toBnDigits(d.agendas.length)}টি খেলা (যেকোনো খেলায় ছুঁয়ে সরাসরি খোলো):</span>
        <button id="toggleAllGamesBtn" class="view-mode-toggle" onclick="toggleShowAllGames()">
          ${showAllGamesInDay ? '🎯 ১টি করে দেখো' : `📜 সব ${toBnDigits(d.agendas.length)}টি একসাথে`}
        </button>
      </div>
      <div class="game-grid-6">${tilesHtml}</div>
    </div>

    <div class="agenda-stack">${agendasHtml}</div>
  `;
  syncAllAudioButtonsUI(!audioEl.paused);
}
