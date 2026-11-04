/* ============================================================================
   MODULE 3: DAILY 6-GAME VIEW CONTROLLER, SEQUENTIAL LOCK & CALENDAR GRIDS
   (🎓 আজকের খেলা — src/js/plan-view.js)
   ============================================================================ */
function togglePrimaryCalendarGrid() {
  primaryCalOpen = !primaryCalOpen;
  renderPlanView();
}

function selectDay(dayNum, autoPlayAudio) {
  if (!isDayUnlocked(dayNum)) {
    const frontier = getHighestUnlockedDay();
    showCelebrationToast('🔒 মা, আগে ‘দিন ' + toBnDigits(frontier) + '’-এর সবকটা খেলায় টিক (✅) দাও—তাহলেই নতুন দিনের চমক খুলে যাবে!');
    return false;
  }
  curDayNum = dayNum;
  curGameIdx = getNextOpenGameIdx(dayNum);
  primaryCalOpen = false;
  stopAllAudio();
  renderPlanView();
  scrollActiveDayChipIntoView();
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if (autoPlayAudio) toggleDayOverviewAudio();
  return true;
}

function selectGame(gIdx, autoPlayAudio) {
  const d = findDayObj(curDayNum);
  const maxIdx = (d && d.agendas) ? d.agendas.length - 1 : 0;
  curGameIdx = Math.max(0, Math.min(maxIdx, gIdx));
  stopAllAudio();
  renderPlanView();
  if (autoPlayAudio !== false) {
    const btnEl = document.getElementById('btnAgPlay_' + curDayNum + '_' + curGameIdx);
    playAgendaByIdx(curDayNum, curGameIdx, btnEl);
  }
}

function toggleShowAllGames() {
  showAllGamesInDay = !showAllGamesInDay;
  renderPlanView();
}

function toggleRadioMode() {
  radioAutoPlay = !radioAutoPlay;
  renderPlanView();
}

function toggleStoryOnlyAudio() {
  storyOnlyAudio = !storyOnlyAudio;
  renderPlanView();
}

function extractSongSearchUrl(ag) {
  const src = (ag.prompt_bn || '') + ' ' + (ag.title_bn || '');
  const m = src.match(/[‘'“"]([^’'”"]{3,60})[’'”"]/);
  const query = (m && m[1]) ? (m[1] + ' বাংলা গান') : ((ag.title_bn || 'বাংলা পুরনো দিনের গান') + ' বাংলা গান');
  return 'https://www.youtube.com/results?search_query=' + encodeURIComponent(query);
}

function toggleAgendaDone(dayNum, agIdx) {
  const key = dayNum + '_' + agIdx;
  const newlyDone = !doneMap[key];
  doneMap[key] = newlyDone;
  saveDoneMap();

  if (newlyDone) {
    if (isDayFullyDone(dayNum)) {
      if (dayNum < ALL_DAYS.length) {
        showCelebrationToast('🎉 দারুণ মা! দিন ' + toBnDigits(dayNum) + ' শেষ হয়েছে—দিন ' + toBnDigits(dayNum + 1) + '-এর নতুন চমক খুলে গেল!');
      } else {
        showCelebrationToast('🎉 অসাধারণ মা! আজকের সব খেলা খুব সুন্দরভাবে শেষ হয়েছে!');
      }

      if (dayNum < ALL_DAYS.length) {
        const nextDay = dayNum + 1;
        curDayNum = nextDay;
        curGameIdx = getNextOpenGameIdx(nextDay);
        stopAllAudio();
        renderPlanView();
        scrollActiveDayChipIntoView();
        toggleDayOverviewAudio();
        return;
      }
    } else {
      showCelebrationToast('🌸 সাবাশ মা! খেলাটা খুব সুন্দরভাবে শেষ করলে!');
      if (!showAllGamesInDay) {
        curGameIdx = getNextOpenGameIdx(dayNum);
        stopAllAudio();
        renderPlanView();
        const nextBtnEl = document.getElementById('btnAgPlay_' + dayNum + '_' + curGameIdx);
        playAgendaByIdx(dayNum, curGameIdx, nextBtnEl);
        return;
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

function buildWalkieTalkieStudioHtml(d, ag, idx) {
  const cardKey = d.day + '_' + idx;
  const turns = kalyaniThreads[cardKey] || [];
  const isRecHere = vnRecordingState.active && vnRecordingState.dayNum === d.day && vnRecordingState.agIdx === idx;
  const isSendingHere = vnRecordingState.sending && vnRecordingState.dayNum === d.day && vnRecordingState.agIdx === idx;
  const pendingPhoto = vnPendingPhotos[cardKey] || null;
  const hasApiKey = !!getGeminiApiKey();
  const showKeyBox = (vnShowKeyInputForCard === cardKey);

  const threadHtml = turns.map((t, tIdx) => `
    <div class="vn-turn-block">
      <div class="vn-user-bubble">
        <div class="vn-bubble-eyebrow">🗣️ মায়ের অডিও মেসেজ ${t.has_photo ? '📷' : ''}:</div>
        <div class="vn-bubble-text">“${t.heard_bn}”</div>
      </div>
      <div class="vn-ai-bubble">
        <div class="vn-bubble-eyebrow">🌸 কল্যাণীর ভয়েস মেসেজ উত্তর:</div>
        <div class="vn-bubble-text">${t.reply_bn}</div>
        <button id="btnVnReplyPlay_${d.day}_${idx}_${tIdx}" class="ag-btn listen vn-reply-play-btn" data-default-label="🔊 কল্যাণীর উত্তর শোনো" onclick="playVoiceNoteReplyAudio(${d.day}, ${idx}, ${tIdx})">
          🔊 কল্যাণীর উত্তর শোনো
        </button>
      </div>
    </div>
  `).join('');

  const photoPreviewHtml = pendingPhoto ? `
    <div class="vn-photo-badge">📷 ছবি যুক্ত হয়েছে — ভয়েস মেসেজের সাথে কল্যাণী ছবিটাও দেখবে!</div>
  ` : '';

  const keyBoxHtml = showKeyBox ? `
    <div class="vn-key-setup-box">
      <div class="vn-key-label">🔑 গুগল জেমিনি এআই চাবি (API Key — একবার দিলেই ফোনে সেভ থাকবে):</div>
      <div class="vn-key-row">
        <input id="vnKeyInput_${d.day}_${idx}" type="password" class="vn-key-input" placeholder="AIza..." value="${getGeminiApiKey()}" />
        <button class="ag-btn check checked" onclick="saveCardGeminiKeyFromInput(${d.day}, ${idx})">সেভ করো</button>
      </div>
    </div>
  ` : '';

  let controlsHtml = '';
  if (isRecHere) {
    controlsHtml = `
      <div class="vn-recording-panel">
        <div class="vn-rec-status">
          🔴 মা, তোমার ভয়েস মেসেজ রেকর্ড হচ্ছে... (<span id="vnTimer_${d.day}_${idx}">${formatAudioSecondsBn(vnRecordingState.seconds)}</span>)
        </div>
        <div class="vn-rec-hint">
          ধীরেসুস্থে যতক্ষণ খুশি থেমে থেমে বলো — কেউ মাঝখানে কথা বলবে না! বলা শেষ হলে নিচের সবুজ বোতামটা ছোঁও:
        </div>
        <div id="vnLivePreview_${d.day}_${idx}" class="vn-live-preview">
          ${vnRecordingState.liveTranscript ? ('🗣️ “' + vnRecordingState.liveTranscript + '”') : '🎙️ মায়ের গলার আওয়াজ শোনা হচ্ছে...'}
        </div>
        <div class="vn-rec-actions">
          <button id="btnVnSend_${d.day}_${idx}" class="vn-send-btn" onclick="finishAndSendVoiceNote(${d.day}, ${idx})">
            ✅ বলা শেষ — কল্যাণীকে পাঠাও ▶️
          </button>
          <button id="btnVnCancel_${d.day}_${idx}" class="ag-btn" onclick="cancelVoiceNoteRecording()">
            ❌ বাতিল করো
          </button>
        </div>
      </div>
    `;
  } else if (isSendingHere) {
    controlsHtml = `
      <div class="vn-sending-panel">
        ⏳ কল্যাণী মনোযোগ দিয়ে তোমার ভয়েস মেসেজ শুনছে এবং অডিও উত্তর তৈরি করছে...
      </div>
    `;
  } else {
    const recBtnLabel = turns.length > 0
      ? '🎙️ পরের ভয়েস মেসেজ রেকর্ড করো (উত্তর দাও)'
      : '🎙️ এখানে ছুঁয়ে ভয়েস মেসেজ রেকর্ড করো (অ্যাপ পাল্টাতে হবে না)';
    controlsHtml = `
      <div class="vn-idle-controls">
        <button id="btnVnRecord_${d.day}_${idx}" class="vn-record-btn" onclick="startVoiceNoteRecording(${d.day}, ${idx})">
          ${recBtnLabel}
        </button>
        <div class="vn-secondary-row">
          <input id="vnPhotoInput_${d.day}_${idx}" type="file" accept="image/*" capture="environment" style="display:none;" onchange="handleCardPhotoSelected(${d.day}, ${idx}, this)" />
          <button class="ag-btn vn-photo-btn" onclick="triggerCardPhotoUpload(${d.day}, ${idx})">
            📷 ছবি তুলে দেখাও
          </button>
          <button class="ag-btn vn-key-btn" onclick="toggleCardKeySetup(${d.day}, ${idx})">
            ${hasApiKey ? '🔑 এআই যুক্ত ✅' : '🔑 এআই চাবি'}
          </button>
        </div>
      </div>
    `;
  }

  return `
    <div id="vnStudio_${d.day}_${idx}" class="walkie-talkie-studio">
      <div class="vn-studio-header">
        <span>🎙️ কল্যাণীর সাথে ভয়েস মেসেজে কথা বলো (অন্য অ্যাপে যেতে হবে না):</span>
      </div>
      ${threadHtml}
      ${photoPreviewHtml}
      ${controlsHtml}
      ${keyBoxHtml}
    </div>
  `;
}

function buildAgendaCardHtml(d, ag, idx) {
  const isDone = !!doneMap[d.day + '_' + idx];
  const btnId = `btnAgPlay_${d.day}_${idx}`;
  const accent = ag.accent || GAME_ACCENTS[idx] || 'terra';
  const catStr = (ag.category || '') + ' ' + (ag.short_bn || '');
  const isSongGame = (ag.category || '').includes('🎵') || (ag.prompt_bn || '').includes('ইউটিউব মিউজিক');

  let stepHeading = '✨ মা, আজ কী করবো দেখো:';
  if (isSongGame) {
    stepHeading = '🎵 মা, আজকের গান ও মনের টান:';
  } else if (catStr.includes('💬') || catStr.includes('স্মৃতির ঝাঁপি') || catStr.includes('মনের গভীর কথা')) {
    stepHeading = '💬 মা, আজকের মনের গভীর কথা ও স্মৃতির ঝাঁপি:';
  } else if (catStr.includes('📖') || catStr.includes('গল্প')) {
    stepHeading = '📖 মা, আজকের গল্প ও মনের কথা:';
  } else if (catStr.includes('🌿') || catStr.includes('মনের আরাম') || catStr.includes('মনের আনন্দ')) {
    stepHeading = '🌿 মা, আজকের মনের আরাম ও ভাবনা:';
  } else if (catStr.includes('🗣️') || catStr.includes('হিন্দি')) {
    stepHeading = '🗣️ মা, আজকের সহজ ও আত্মবিশ্বাসী হিন্দি খেলা:';
  } else if (catStr.includes('🌍') || catStr.includes('জানাশোনা') || catStr.includes('বিস্ময়') || catStr.includes('🌟')) {
    stepHeading = '🌍 মা, আজকের অবাক করা জানাশোনা:';
  } else if (catStr.includes('🔤') || catStr.includes('ইংরেজি')) {
    stepHeading = '🔤 মা, আজকের সহজ ইংরেজি খেলা:';
  } else if (catStr.includes('🎨') || catStr.includes('আঁকা') || catStr.includes('সৃষ্টি')) {
    stepHeading = '🎨 মা, আজকের নিজের খুশির সৃষ্টি:';
  }

  const ytMusicGuideHtml = isSongGame ? `
      <div class="agenda-prompt-box yt-music-box">
        <div class="agenda-prompt-label">🎵 ইউটিউবে সরাসরি গানটা শোনো বা ভয়েস মেসেজে কল্যাণীকে বলো!</div>
        <div class="agenda-detail" style="font-size:1.01rem;">মা, উপরের কমলা বোতামটায় ছুঁলেই সরাসরি ইউটিউবে গানটা বেজে উঠবে! আর গানটা শোনা হয়ে গেলে নিচে ভয়েস মেসেজ রেকর্ড করে কল্যাণীর সাথে গানের কথা আর মনের ভাবনা নিয়ে গল্প করো।</div>
      </div>` : '';

  const followupLabel = isSongGame
    ? '💬 গানটা শোনা হয়ে গেলে এর মানে আর গল্পটা জানতে জেমিনিকে বলো:'
    : '💬 জেমিনির উত্তরটা শোনার পর গল্পটা আরও জমাতে দ্বিতীয় কথায় বলো:';

  const followupHtml = ag.followup_prompt_bn ? `
      <div class="agenda-prompt-box">
        <div class="agenda-prompt-label">${followupLabel}</div>
        <div class="agenda-prompt-speech">“${ag.followup_prompt_bn}”</div>
      </div>` : '';

  const promptLabel = isSongGame
    ? '🎙️ এই গানটা নিয়ে ভয়েস মেসেজে কী বলবে তার ক্লু:'
    : '🎙️ ভয়েস মেসেজে কল্যাণীকে কী বলবে তার ক্লু (নিজের মতো ধীরেসুস্থে বলো):';

  const ytDirectBtnHtml = isSongGame ? `
      <a class="yt-direct-btn" href="${extractSongSearchUrl(ag)}" target="_blank" rel="noopener noreferrer" onclick="stopAllAudio()">
        🎵 ইউটিউবে এই গানটা সরাসরি চালাও ▶️
      </a>` : '';

  return `
    <article class="agenda-card ${isDone ? 'done-card' : ''}" data-accent="${accent}" id="agendaCard_${d.day}_${idx}">
      <div class="agenda-card-header">
        <div class="agenda-cat">${ag.category}</div>
      </div>
      <div class="agenda-title">${ag.title_bn}</div>
      <div class="step-section">
        <div class="agenda-step-heading">${stepHeading}</div>
        <div class="agenda-detail">${ag.detail_bn}</div>
      </div>${ytDirectBtnHtml}
      <div class="agenda-prompt-box">
        <div class="agenda-prompt-label">${promptLabel}</div>
        <div class="agenda-prompt-speech">“${ag.prompt_bn}”</div>
        <div class="agenda-prompt-howto">💡 (নিজের মতো সহজ বাংলায় থেমে থেমে বললেই হবে—নিচের সবুজ বোতামটা ছুঁয়ে রেকর্ড করো!)</div>
      </div>
      ${buildWalkieTalkieStudioHtml(d, ag, idx)}
      <div class="agenda-actions">
        <button id="${btnId}" class="ag-btn listen" data-default-label="🔊 গল্পটা শোনো" onclick="playAgendaByIdx(${d.day}, ${idx}, this)">🔊 গল্পটা শোনো</button>
        <button class="ag-btn check ${isDone ? 'checked' : ''}" onclick="toggleAgendaDone(${d.day}, ${idx})">
          ${isDone ? '✅ ভালো লেগেছে' : '❤️ ভালো লাগলো'}
        </button>
      </div>
      <details class="optional-prompt-drawer">
        <summary class="optional-prompt-summary">💬 দ্বিতীয় কথার ক্লু ও পুরো অডিও দেখো ▾</summary>
        <div class="optional-prompt-body">${ytMusicGuideHtml}${followupHtml}
          <button class="ag-btn full-prompt-audio-btn" onclick="playAgendaByIdx(${d.day}, ${idx}, null, true)">🔊 ক্লু-সহ পুরো কথা শোনো</button>
        </div>
      </details>
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

  const d = findDayObj(curDayNum);
  curDayNum = d.day;
  if (curGameIdx < 0 || curGameIdx >= d.agendas.length) curGameIdx = 0;
  const stage = document.getElementById('activeDayStage');

  let tilesHtml = '';
  d.agendas.forEach((ag, idx) => {
    const isDone = !!doneMap[d.day + '_' + idx];
    const isAct = (!showAllGamesInDay && idx === curGameIdx);
    const shortLbl = ag.short_bn || GAME_SHORT_LABELS[idx] || ag.category;
    const accent = ag.accent || GAME_ACCENTS[idx] || 'terra';
    tilesHtml += `
      <button id="gameTile_${d.day}_${idx}" data-accent="${accent}" class="game-tile ${isAct ? 'active' : ''} ${isDone ? 'done-tile' : ''}" onclick="selectGame(${idx}, true)">
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
        <button id="prevGameBtn" class="ag-btn" ${curGameIdx <= 0 ? 'disabled' : ''} onclick="selectGame(${curGameIdx - 1}, true)">⬅️ আগের খেলা</button>
        <button id="nextGameBtn" class="ag-btn" ${curGameIdx >= d.agendas.length - 1 ? 'disabled' : ''} onclick="selectGame(${curGameIdx + 1}, true)">পরের খেলা ➡️</button>
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
      <div class="radio-mode-banner">
        <div class="radio-mode-text">📻 <strong>রেডিও মোড:</strong> শুধু আরাম করে গল্প শোনো — কিছু বলতে বা করতে হবে না!</div>
        <button id="btnToggleRadioMode" class="radio-toggle-pill ${radioAutoPlay ? 'on' : ''}" onclick="toggleRadioMode()">
          ${radioAutoPlay ? '📻 পরপর গল্প: চালু' : '⏸️ পরপর গল্প: বন্ধ'}
        </button>
      </div>
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
      <div class="game-grid-6" data-count="${d.agendas.length}">${tilesHtml}</div>
    </div>

    <div class="agenda-stack">${agendasHtml}</div>
  `;
  syncAllAudioButtonsUI(!audioEl.paused);
}

const TV_HUB_CHANNELS = [
  {
    icon: '🎬',
    title_bn: 'উত্তম-সুচিত্রার চিরকালের বাংলা ছবি',
    desc_bn: 'হারানো সুর, সপ্তপদী, পথে হলো দেরী ও পুরনো দিনের সেরা বাংলা সিনেমা',
    query: 'Uttam Suchitra classic Bengali full movie',
    accent: 'terra'
  },
  {
    icon: '😂',
    title_bn: 'ভানু বন্দ্যোপাধ্যায় ও জহর রায়ের হাসির ছবি',
    desc_bn: 'যমালয়ে জীবন্ত মানুষ, সাড়ে চুয়াত্তর ও ভানু-জহরের পেট ফাটা হাসির দৃশ্য',
    query: 'Bhanu Bandyopadhyay Jahar Roy Bengali comedy scenes movie',
    accent: 'amber'
  },
  {
    icon: '🎵',
    title_bn: 'হেমন্ত মুখোপাধ্যায় ও সন্ধ্যা মুখোপাধ্যায়ের গান',
    desc_bn: 'দুপুর বা বিকেলের শান্ত সময়ে শোনার মতো চিরসবুজ বাংলা আধুনিক গান',
    query: 'Hemanta Mukherjee Sandhya Mukherjee Bengali evergreen songs jukebox',
    accent: 'emerald'
  },
  {
    icon: '🎶',
    title_bn: 'মান্না দে ও রবীন্দ্রসঙ্গীতের শান্ত আসর',
    desc_bn: 'কফি হাউসের সেই আড্ডাটা ও মন ভালো করা রবীন্দ্রসঙ্গীতের ডালি',
    query: 'Manna Dey Rabindra Sangeet Bengali songs jukebox',
    accent: 'indigo'
  },
  {
    icon: '🎧',
    title_bn: 'বাংলা অডিও গল্প (রবীন্দ্রনাথ ও শরৎচন্দ্র)',
    desc_bn: 'চোখ বুজে শুয়ে শুয়ে শোনার মতো ছোটগল্প ও শ্রুতিনাটক',
    query: 'Rabindranath Tagore Sarat Chandra Bengali audio story Golpo',
    accent: 'plum'
  },
  {
    icon: '🛕',
    title_bn: 'দক্ষিণেশ্বর, বেলুড় মঠ ও মা সারদা জয়রামবাটী',
    desc_bn: 'মা সারদার জীবনকথা, দক্ষিণেশ্বরের আরতি ও ভক্তিমূলক কথা ও গান',
    query: 'Maa Sarada Jayrambati Dakshineswar Belur Math Bengali',
    accent: 'rose'
  },
  {
    icon: '🍲',
    title_bn: 'বাংলার ঘরোয়া রান্না ও গ্রামের সকাল',
    desc_bn: 'সাবেকি বাঙালি রান্না, ঠাকুরবাড়ির পদ ও শান্ত গ্রামের ভিডিও',
    query: 'traditional Bengali recipe cooking village vlog',
    accent: 'emerald'
  },
  {
    icon: '📺',
    title_bn: 'দাদাগিরি ও দিদি নাম্বার ১-এর মজার পর্ব',
    desc_bn: 'সৌরভ গাঙ্গুলী ও রচনা ব্যানার্জীর সাথে হাসি-গল্পের ঘরোয়া আসর',
    query: 'Didi No 1 Dadagiri Bengali episode',
    accent: 'terra'
  }
];

function renderTvView() {
  const stage = document.getElementById('tvHubStage');
  if (!stage) return;
  const cardsHtml = TV_HUB_CHANNELS.map((ch, idx) => {
    const url = 'https://www.youtube.com/results?search_query=' + encodeURIComponent(ch.query);
    return `
      <a id="tvCard_${idx}" class="tv-channel-card" data-accent="${ch.accent}" href="${url}" target="_blank" rel="noopener noreferrer" onclick="stopAllAudio()">
        <div class="tv-card-icon">${ch.icon}</div>
        <div class="tv-card-body">
          <div class="tv-card-title">${ch.title_bn}</div>
          <div class="tv-card-desc">${ch.desc_bn}</div>
          <div class="tv-card-cta">▶️ এক ছোঁয়ায় ইউটিউবে দেখো</div>
        </div>
      </a>
    `;
  }).join('');

  stage.innerHTML = `
    <div class="day-hero-card">
      <div class="day-hero-badge">📺 মায়ের নিজের টিভি ও গানের ঘর</div>
      <div class="day-hero-title">শুধু একটা বোতামে ছুঁয়ে দেখো বা শোনো</div>
      <div class="day-hero-summary" style="margin-bottom:0;">
        মা, এখানে কিছু টাইপ করতে বা মুখে বলতে হবে না। যেটা দেখতে বা শুনতে ইচ্ছে করছে, শুধু সেই কার্ডটায় একবার ছুঁলেই সরাসরি ইউটিউবে খুলে যাবে!
      </div>
    </div>
    <div class="tv-hub-grid">${cardsHtml}</div>
  `;
}
