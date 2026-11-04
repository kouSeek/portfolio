/* ============================================================================
   MODULE 2: UNIFIED AOEDE AUDIO ENGINE, PROACTIVE WELCOME & NOTIFICATIONS
   (src/js/audio.js)
   ============================================================================ */
const audioEl = document.getElementById('audioPlayer');
const topPlayBtn = document.getElementById('topPlayBtn');
let activeAudioBtnId = null;
let activeAudioKey = null;
let activeStoryEndSec = 0;
let autoWelcomeSucceeded = false;
let autoWelcomeFallbackArmed = false;

function getEffectiveAudioDuration() {
  const rawDur = audioEl.duration || 0;
  if (storyOnlyAudio && activeStoryEndSec > 4 && (!rawDur || activeStoryEndSec < rawDur)) {
    return activeStoryEndSec;
  }
  return rawDur;
}

function formatAudioSecondsBn(sec) {
  if (!sec || !isFinite(sec) || sec < 0) return '০:০০';
  const s = Math.floor(sec);
  const mins = Math.floor(s / 60);
  const rem = s % 60;
  return toBnDigits(mins) + ':' + toBnDigits(rem < 10 ? '0' + rem : rem);
}

function updateNowPlayingBar(showBar) {
  const bar = document.getElementById('nowPlayingBar');
  if (!bar) return;
  if (!showBar) {
    bar.classList.remove('visible');
    return;
  }
  bar.classList.add('visible');
  const fill = document.getElementById('npFill');
  const timeEl = document.getElementById('npTime');
  const dur = getEffectiveAudioDuration();
  const cur = Math.min(dur || (audioEl.currentTime || 0), audioEl.currentTime || 0);
  if (fill) {
    const pct = dur > 0 ? Math.min(100, Math.max(0, (cur / dur) * 100)) : 0;
    fill.style.width = pct.toFixed(1) + '%';
  }
  if (timeEl) {
    timeEl.textContent = dur > 0
      ? (formatAudioSecondsBn(cur) + ' / ' + formatAudioSecondsBn(dur))
      : formatAudioSecondsBn(cur);
  }
}

function seekAudioFromTrack(ev) {
  const track = document.getElementById('npTrack');
  const effDur = getEffectiveAudioDuration();
  if (!track || !effDur || !isFinite(effDur) || !track.getBoundingClientRect) return;
  const rect = track.getBoundingClientRect();
  if (!rect.width) return;
  const ratio = Math.min(1, Math.max(0, (ev.clientX - rect.left) / rect.width));
  audioEl.currentTime = ratio * effDur;
  updateNowPlayingBar(true);
}

function syncAllAudioButtonsUI(isPlaying) {
  document.querySelectorAll('[data-default-label]').forEach(btn => {
    if (btn.id === activeAudioBtnId && isPlaying) {
      btn.classList.add('playing');
      btn.innerHTML = '⏸️ থামাও';
    } else {
      btn.classList.remove('playing');
      btn.innerHTML = btn.getAttribute('data-default-label');
    }
  });
  if (topPlayBtn) {
    if (isPlaying) {
      topPlayBtn.classList.add('playing');
      topPlayBtn.innerHTML = '⏸️ থামাও';
    } else {
      topPlayBtn.classList.remove('playing');
      topPlayBtn.innerHTML = '🔊 শোনো';
    }
  }
  updateNowPlayingBar(isPlaying);
}

function stopAllAudio() {
  audioEl.pause();
  activeAudioBtnId = null;
  activeAudioKey = null;
  activeStoryEndSec = 0;
  syncAllAudioButtonsUI(false);
}

function playOrToggleAudio(btnId, audioKey, srcUrl, fallbackB64, onBlockedFallback, storyEndSec) {
  if (activeAudioKey === audioKey && !audioEl.paused) {
    audioEl.pause();
    syncAllAudioButtonsUI(false);
    return;
  }
  if (activeAudioKey === audioKey && audioEl.paused && audioEl.currentTime > 0 && !audioEl.ended) {
    if (!storyOnlyAudio || !activeStoryEndSec || audioEl.currentTime < activeStoryEndSec - 0.3) {
      activeAudioBtnId = btnId;
      syncAllAudioButtonsUI(true);
      audioEl.play().catch(() => syncAllAudioButtonsUI(false));
      return;
    }
  }
  audioEl.pause();
  activeAudioBtnId = btnId;
  activeAudioKey = audioKey;
  activeStoryEndSec = (storyEndSec && storyEndSec > 4) ? Number(storyEndSec) : 0;
  audioEl.src = srcUrl || fallbackB64 || '';
  audioEl.currentTime = 0;
  syncAllAudioButtonsUI(true);

  const playPromise = audioEl.play();
  if (playPromise && typeof playPromise.then === 'function') {
    playPromise.then(() => {
      autoWelcomeSucceeded = true;
      detachAutoWelcomeGestureFallback();
    }).catch(() => {
      if (fallbackB64 && audioEl.src !== fallbackB64) {
        audioEl.src = fallbackB64;
        audioEl.play().then(() => {
          autoWelcomeSucceeded = true;
          detachAutoWelcomeGestureFallback();
        }).catch(() => {
          stopAllAudio();
          if (typeof onBlockedFallback === 'function') onBlockedFallback();
        });
      } else {
        stopAllAudio();
        if (typeof onBlockedFallback === 'function') onBlockedFallback();
      }
    });
  }
}

function onFirstGestureWelcomeUnlock(ev) {
  detachAutoWelcomeGestureFallback();
  if (autoWelcomeSucceeded || !audioEl.paused || activeAudioKey || curView !== 'plan') return;
  const explicitTarget = (ev && ev.target && typeof ev.target.closest === 'function')
    ? ev.target.closest('#topPlayBtn, #btnDayMainPlay, .ag-btn, .game-tile, .day-chip, .cal-day-cell, #btnToggleCalGrid, #btnToggleExtCal, .view-mode-toggle, #htabSlides, .perm-btn-primary')
    : null;
  if (explicitTarget) return;
  autoWelcomeSucceeded = true;
  toggleDayOverviewAudio();
}

function preloadOpenGameAudio(dayObj, gameIdx) {
  try {
    if (!dayObj || !dayObj.agendas || !dayObj.agendas[gameIdx] || typeof Audio !== 'function') return;
    const url = dayObj.agendas[gameIdx].audio_url;
    if (!url) return;
    const pre = new Audio();
    pre.preload = 'auto';
    pre.src = url;
  } catch (e) {}
}

function attachAutoWelcomeGestureFallback() {
  if (autoWelcomeFallbackArmed || !document.addEventListener) return;
  autoWelcomeFallbackArmed = true;
  document.addEventListener('pointerdown', onFirstGestureWelcomeUnlock, true);
  document.addEventListener('touchstart', onFirstGestureWelcomeUnlock, true);
  document.addEventListener('keydown', onFirstGestureWelcomeUnlock, true);
}

function detachAutoWelcomeGestureFallback() {
  if (!autoWelcomeFallbackArmed || !document.removeEventListener) return;
  autoWelcomeFallbackArmed = false;
  document.removeEventListener('pointerdown', onFirstGestureWelcomeUnlock, true);
  document.removeEventListener('touchstart', onFirstGestureWelcomeUnlock, true);
  document.removeEventListener('keydown', onFirstGestureWelcomeUnlock, true);
}

function engageProactiveWelcomeAudio() {
  if (curView !== 'plan') return;
  const d = findDayObj(curDayNum);
  const refDay = d.audio_ref_day || d.day || 1;
  const refObj = DAYS_21.find(x => x.day === refDay) || d;
  preloadOpenGameAudio(d, curGameIdx);
  playOrToggleAudio(
    'btnDayMainPlay',
    'day_main_' + d.day,
    d.audio_url || refObj.audio_url,
    d.audio_b64 || refObj.audio_b64,
    attachAutoWelcomeGestureFallback
  );
}

function toggleMorningQuoteAudio() {
  const qIdx = curQuoteIdx;
  const qa = QUOTES_AUDIO[qIdx] || QUOTES_AUDIO[0];
  playOrToggleAudio('btnQuotePlay', 'quote_' + qIdx, qa.url, qa.b64);
}

function toggleDayOverviewAudio() {
  const d = findDayObj(curDayNum);
  const refDay = d.audio_ref_day || d.day || 1;
  const refObj = DAYS_21.find(x => x.day === refDay) || d;
  preloadOpenGameAudio(d, curGameIdx);
  playOrToggleAudio(
    'btnDayMainPlay',
    'day_main_' + d.day,
    d.audio_url || refObj.audio_url,
    d.audio_b64 || refObj.audio_b64
  );
}

function toggleSlideAudio() {
  const s = SLIDES[curSlideIdx];
  playOrToggleAudio('btnSlideMainPlay', 'slide_' + s.id, s.audio_url, s.audio_b64);
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
  if (curView === 'slides') toggleSlideAudio();
  else if (!autoWelcomeSucceeded && !activeAudioKey) toggleDayOverviewAudio();
  else playAgendaByIdx(curDayNum, curGameIdx, document.getElementById('btnAgPlay_' + curDayNum + '_' + curGameIdx));
}

async function playAgendaByIdx(dayNum, agIdx, btnEl, playFullWithPrompt) {
  const btnId = btnEl ? btnEl.id : ('btnAgPlay_' + dayNum + '_' + agIdx);
  const audioKey = 'ag_' + dayNum + '_' + agIdx + (playFullWithPrompt ? '_full' : '');

  const d = findDayObj(dayNum);
  const ag = (d && d.agendas && d.agendas[agIdx]) ? d.agendas[agIdx] : null;
  if (!ag) return;

  const cutSec = (!playFullWithPrompt && storyOnlyAudio && ag.story_end) ? Number(ag.story_end) : 0;
  const fallbackB64 = (dayNum === 1 && DAY1_AG_MAP[agIdx]) ? DAY1_AG_MAP[agIdx].b64 : (d.audio_b64 || '');
  playOrToggleAudio(btnId, audioKey, ag.audio_url, fallbackB64, null, cutSec);
}

function handleAudioTrackCompleted() {
  const finishedKey = activeAudioKey;
  stopAllAudio();
  if (!finishedKey) return;

  if (curView === 'slides' && autoAdvance && finishedKey.startsWith('slide_') && curSlideIdx < SLIDES.length - 1) {
    setTimeout(() => goToSlide(curSlideIdx + 1, true), 900);
  } else if (curView === 'plan' && finishedKey.startsWith('day_main_')) {
    const btnEl = document.getElementById('btnAgPlay_' + curDayNum + '_' + curGameIdx);
    playAgendaByIdx(curDayNum, curGameIdx, btnEl);
  } else if (curView === 'plan' && radioAutoPlay && finishedKey.startsWith('ag_')) {
    const parts = finishedKey.split('_');
    const dayNum = parseInt(parts[1] || String(curDayNum), 10);
    const agIdx = parseInt(parts[2] || String(curGameIdx), 10);
    const d = findDayObj(dayNum);
    const totalInDay = (d && d.agendas) ? d.agendas.length : 6;
    if (agIdx + 1 < totalInDay) {
      selectGame(agIdx + 1, true);
    } else if (dayNum < ALL_DAYS.length && isDayUnlocked(dayNum + 1)) {
      selectDay(dayNum + 1, true);
    }
  }
}

audioEl.addEventListener('timeupdate', () => {
  if (audioEl.paused) return;
  if (storyOnlyAudio && activeStoryEndSec > 4 && audioEl.currentTime >= activeStoryEndSec) {
    handleAudioTrackCompleted();
    return;
  }
  updateNowPlayingBar(true);
});

audioEl.addEventListener('ended', () => {
  handleAudioTrackCompleted();
});

/* Pleasant Morning Bell Chime via Web Audio API */
function playMorningChimeSound() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const notes = [523.25, 659.25, 783.99, 1046.50];
    notes.forEach((freq, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, ctx.currentTime + i * 0.18);
      gain.gain.setValueAtTime(0.001, ctx.currentTime + i * 0.18);
      gain.gain.exponentialRampToValueAtTime(0.22, ctx.currentTime + i * 0.18 + 0.04);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + i * 0.18 + 1.1);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(ctx.currentTime + i * 0.18);
      osc.stop(ctx.currentTime + i * 0.18 + 1.15);
    });
  } catch (e) {}
}

function checkAndFireDailyMorningNotification() {
  const now = new Date();
  const todayStr = now.toISOString().slice(0, 10);
  if (maProfile.lastMorningNotifDate === todayStr) return;

  const parts = (maProfile.morningTime || '08:00').split(':');
  const targetH = parseInt(parts[0] || '8', 10);
  const targetM = parseInt(parts[1] || '0', 10);
  const nowMins = now.getHours() * 60 + now.getMinutes();
  const targetMins = targetH * 60 + targetM;

  if (nowMins >= targetMins && nowMins <= targetMins + 240) {
    maProfile.lastMorningNotifDate = todayStr;
    saveMaProfile();
    fireMorningMotivationNotification(false);
  }
}

function fireMorningMotivationNotification(isManualTest) {
  const quote = MORNING_QUOTES[curQuoteIdx];
  playMorningChimeSound();
  const title = '☀️ সুপ্রভাত মা! আজকের অনুপ্রেরণা';
  const favEl = document.getElementById('pageFavicon');
  const notifIcon = (favEl && favEl.getAttribute && favEl.getAttribute('href')) || 'favicon.svg';
  if ('Notification' in window && Notification.permission === 'granted') {
    if (navigator.serviceWorker && navigator.serviceWorker.ready) {
      navigator.serviceWorker.ready.then(reg => {
        reg.showNotification(title, {
          body: quote,
          icon: notifIcon,
          vibrate: [200, 100, 200],
          tag: 'ma-morning-motivation'
        });
      }).catch(() => {
        new Notification(title, { body: quote });
      });
    } else {
      new Notification(title, { body: quote });
    }
  }
  if (isManualTest) toggleMorningQuoteAudio();
}

async function requestMicAndNotificationPermission() {
  try {
    if ('Notification' in window) {
      await Notification.requestPermission();
    }
    maProfile.permsGranted = true;
    saveMaProfile();
    const permBanner = document.getElementById('permBanner');
    if (permBanner) permBanner.style.display = 'none';
    fireMorningMotivationNotification(true);
  } catch (err) {}
}

/* ============================================================================
   MODULE 2B: IN-CARD WALKIE-TALKIE AUDIO MESSAGE & AOEDE VOICE REPLY ENGINE
   (Zero App-Switching, Zero Mid-Sentence Interruption, 100% System Prompt Obedience)
   ============================================================================ */
let activeMediaRecorder = null;
let activeMicStream = null;
let activeSpeechRec = null;
let activeVnAudioChunks = [];
let activeVnTimerId = null;

function pcm24kBase64ToWavUrl(b64Pcm) {
  try {
    const rawStr = (typeof atob === 'function')
      ? atob(b64Pcm)
      : Buffer.from(b64Pcm, 'base64').toString('binary');
    const pcmLen = rawStr.length;
    const wavBytes = new Uint8Array(44 + pcmLen);
    const view = new DataView(wavBytes.buffer);
    const writeAscii = (off, str) => {
      for (let i = 0; i < str.length; i++) wavBytes[off + i] = str.charCodeAt(i);
    };
    writeAscii(0, 'RIFF');
    view.setUint32(4, 36 + pcmLen, true);
    writeAscii(8, 'WAVE');
    writeAscii(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, 1, true);
    view.setUint32(24, 24000, true);
    view.setUint32(28, 48000, true);
    view.setUint16(32, 2, true);
    view.setUint16(34, 16, true);
    writeAscii(36, 'data');
    view.setUint32(40, pcmLen, true);
    for (let i = 0; i < pcmLen; i++) {
      wavBytes[44 + i] = rawStr.charCodeAt(i);
    }
    let bin = '';
    for (let i = 0; i < wavBytes.length; i++) {
      bin += String.fromCharCode(wavBytes[i]);
    }
    const wavB64 = (typeof btoa === 'function')
      ? btoa(bin)
      : Buffer.from(bin, 'binary').toString('base64');
    return 'data:audio/wav;base64,' + wavB64;
  } catch (e) {
    return '';
  }
}

async function synthesizeKalyaniAoedeAudio(textBn, apiKey) {
  if (!apiKey || !textBn) return '';
  try {
    const endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key=' + encodeURIComponent(apiKey);
    const resp = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{
          parts: [{
            text: 'Speak in a warm, affectionate, unhurried, soothing West Bengal Bengali voice (never rush):\n\n' + textBn
          }]
        }],
        generationConfig: {
          responseModalities: ['AUDIO'],
          speechConfig: {
            voiceConfig: {
              prebuiltVoiceConfig: { voiceName: 'Aoede' }
            }
          }
        }
      })
    });
    if (!resp.ok) return '';
    const data = await resp.json();
    const parts = (data && data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts) || [];
    for (let i = 0; i < parts.length; i++) {
      if (parts[i].inlineData && parts[i].inlineData.data) {
        return pcm24kBase64ToWavUrl(parts[i].inlineData.data);
      }
    }
  } catch (e) {}
  return '';
}

function buildWarmFallbackReply(ag, turnCount, heardText) {
  const cleanHeard = (heardText || '').trim() || 'মায়ের নিজের মনের কথা (ভয়েস মেসেজ)';
  const follow = (ag && ag.followup_prompt_bn) ? ag.followup_prompt_bn : '';
  if (turnCount === 0 && follow) {
    return {
      heard_bn: cleanHeard,
      reply_bn: 'মা, তোমার গলার আওয়াজ আর মনের কথাটা শুনে আমার মনটা একদম ভরে গেল! তুমি কী সুন্দর নিজের মতো করে কথাটা বললে। আচ্ছা মা, এবার একটু ভেবে বলো তো—' + follow,
      memory_note: ''
    };
  }
  return {
    heard_bn: cleanHeard,
    reply_bn: 'মা, তোমার প্রতিটি কথা এত সুন্দর আর আন্তরিক! তোমার সাথে এভাবে ধীরেসুস্থে গল্প করতে আমার ভীষণ ভালো লাগে। আজকের এই খেলাটা তুমি দারুণভাবে সম্পূর্ণ করলে!',
    memory_note: ''
  };
}

async function callKalyaniGeminiAudioTurn(dayNum, agIdx, audioB64, audioMime, liveTranscript, photoObj) {
  const d = findDayObj(dayNum);
  const ag = (d && d.agendas && d.agendas[agIdx]) ? d.agendas[agIdx] : {};
  const cardKey = dayNum + '_' + agIdx;
  const history = kalyaniThreads[cardKey] || [];
  const apiKey = getGeminiApiKey();

  if (!apiKey) {
    return buildWarmFallbackReply(ag, history.length, liveTranscript);
  }

  const memBlock = kalyaniMemoryNotes.length
    ? ('\n\nREMEMBERED FACTS ABOUT MA FROM PREVIOUS CONVERSATIONS:\n- ' + kalyaniMemoryNotes.join('\n- '))
    : '';
  const turnGuidance = (history.length === 0 && ag.followup_prompt_bn)
    ? ('This is Turn 1 on this card. After warmly responding to Ma in 2–3 sentences, gently invite her into Turn 2 around this theme: "' + ag.followup_prompt_bn + '"')
    : 'This is a follow-up turn. Respond warmly in 3–4 simple West Bengal Bengali sentences, praising her openness and ending with a soothing thought or gentle question.';

  const sysInstruction = (typeof KALYANI_SYSTEM_PROMPT === 'string' ? KALYANI_SYSTEM_PROMPT : '')
    + memBlock
    + '\n\nACTIVE KALYANI APP CARD CONTEXT (Day ' + dayNum + ', Game ' + (agIdx + 1) + '):\n'
    + '- Category: ' + (ag.category || '') + '\n'
    + '- Title: ' + (ag.title_bn || '') + '\n'
    + '- Story/Context: ' + (ag.detail_bn || '') + '\n'
    + '- Suggested Prompt Ma Was Responding To: ' + (ag.prompt_bn || '') + '\n'
    + '- Turn Guidance: ' + turnGuidance + '\n\n'
    + 'OUTPUT FORMAT RULE: Return strictly valid JSON with keys:\n'
    + '{"heard_bn": "accurate Bengali transcript of what Ma just said in her audio message", "reply_bn": "your warm 3-4 sentence colloquial West Bengal Bengali reply to Ma (never rush, zero markdown symbols)", "memory_note": "short 1-line note of any new personal memory/preference Ma shared, or empty string"}';

  const contents = [];
  history.forEach(t => {
    contents.push({ role: 'user', parts: [{ text: t.heard_bn || 'মায়ের ভয়েস মেসেজ' }] });
    contents.push({ role: 'model', parts: [{ text: JSON.stringify({ heard_bn: t.heard_bn, reply_bn: t.reply_bn, memory_note: '' }) }] });
  });

  const userParts = [];
  if (photoObj && photoObj.b64) {
    userParts.push({ inlineData: { mimeType: photoObj.mime || 'image/jpeg', data: photoObj.b64 } });
  }
  if (audioB64) {
    userParts.push({ inlineData: { mimeType: audioMime || 'audio/webm', data: audioB64 } });
  }
  userParts.push({
    text: liveTranscript
      ? ('মা ভয়েস মেসেজে বললেন (সম্ভাব্য শ্রুতিলিপি: "' + liveTranscript + '")। অডিওটা মনোযোগ দিয়ে শুনে JSON উত্তর দাও।')
      : 'মা এইমাত্র এই ভয়েস মেসেজটি পাঠিয়েছেন। অডিওটা মনোযোগ দিয়ে শুনে JSON উত্তর দাও।'
  });
  contents.push({ role: 'user', parts: userParts });

  try {
    const endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=' + encodeURIComponent(apiKey);
    const resp = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        systemInstruction: { parts: [{ text: sysInstruction }] },
        contents: contents,
        generationConfig: {
          temperature: 0.7,
          responseMimeType: 'application/json'
        }
      })
    });
    if (!resp.ok) {
      return buildWarmFallbackReply(ag, history.length, liveTranscript);
    }
    const data = await resp.json();
    const rawText = (data && data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts[0] && data.candidates[0].content.parts[0].text) || '';
    const parsed = JSON.parse(rawText);
    if (parsed && parsed.reply_bn) {
      if (parsed.memory_note) addKalyaniMemoryNote(parsed.memory_note);
      return {
        heard_bn: parsed.heard_bn || liveTranscript || 'মায়ের ভয়েস মেসেজ',
        reply_bn: String(parsed.reply_bn).replace(/[*#`_]/g, '').trim(),
        memory_note: parsed.memory_note || ''
      };
    }
  } catch (e) {}
  return buildWarmFallbackReply(ag, history.length, liveTranscript);
}

function cleanupActiveVoiceRecorder() {
  if (activeVnTimerId) {
    if (typeof clearInterval === 'function') clearInterval(activeVnTimerId);
    activeVnTimerId = null;
  }
  if (activeSpeechRec) {
    try { activeSpeechRec.stop(); } catch (e) {}
    activeSpeechRec = null;
  }
  if (activeMicStream) {
    try { activeMicStream.getTracks().forEach(t => t.stop()); } catch (e) {}
    activeMicStream = null;
  }
  activeMediaRecorder = null;
}

async function startVoiceNoteRecording(dayNum, agIdx) {
  stopAllAudio();
  cleanupActiveVoiceRecorder();
  activeVnAudioChunks = [];
  vnRecordingState = {
    active: true,
    sending: false,
    dayNum: dayNum,
    agIdx: agIdx,
    seconds: 0,
    liveTranscript: '',
    errorMsg: ''
  };
  renderPlanView();

  activeVnTimerId = setInterval(() => {
    if (!vnRecordingState.active) return;
    vnRecordingState.seconds += 1;
    const timerEl = document.getElementById('vnTimer_' + dayNum + '_' + agIdx);
    if (timerEl) timerEl.textContent = formatAudioSecondsBn(vnRecordingState.seconds);
  }, 1000);

  try {
    const SpeechRec = (typeof window !== 'undefined') && (window.SpeechRecognition || window.webkitSpeechRecognition);
    if (SpeechRec) {
      activeSpeechRec = new SpeechRec();
      activeSpeechRec.lang = 'bn-IN';
      activeSpeechRec.continuous = true;
      activeSpeechRec.interimResults = true;
      activeSpeechRec.onresult = (ev) => {
        let txt = '';
        for (let i = 0; i < ev.results.length; i++) {
          txt += ev.results[i][0].transcript + ' ';
        }
        vnRecordingState.liveTranscript = txt.trim();
        const prevEl = document.getElementById('vnLivePreview_' + dayNum + '_' + agIdx);
        if (prevEl && vnRecordingState.liveTranscript) {
          prevEl.textContent = '🗣️ “' + vnRecordingState.liveTranscript + '”';
        }
      };
      try { activeSpeechRec.start(); } catch (e) {}
    }
  } catch (e) {}

  try {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      activeMicStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (typeof MediaRecorder !== 'undefined') {
        const mime = (typeof MediaRecorder.isTypeSupported === 'function' && MediaRecorder.isTypeSupported('audio/webm;codecs=opus'))
          ? 'audio/webm;codecs=opus'
          : ((typeof MediaRecorder.isTypeSupported === 'function' && MediaRecorder.isTypeSupported('audio/mp4')) ? 'audio/mp4' : '');
        activeMediaRecorder = mime ? new MediaRecorder(activeMicStream, { mimeType: mime }) : new MediaRecorder(activeMicStream);
        activeMediaRecorder.ondataavailable = (ev) => {
          if (ev.data && ev.data.size > 0) activeVnAudioChunks.push(ev.data);
        };
        activeMediaRecorder.start(250);
      }
    }
  } catch (err) {}
}

function cancelVoiceNoteRecording() {
  cleanupActiveVoiceRecorder();
  vnRecordingState = { active: false, sending: false, dayNum: 0, agIdx: -1, seconds: 0, liveTranscript: '', errorMsg: '' };
  renderPlanView();
}

function blobToBase64(blob) {
  return new Promise((resolve) => {
    if (!blob || typeof FileReader === 'undefined') {
      resolve('');
      return;
    }
    const reader = new FileReader();
    reader.onloadend = () => {
      const res = String(reader.result || '');
      const comma = res.indexOf(',');
      resolve(comma >= 0 ? res.slice(comma + 1) : '');
    };
    reader.onerror = () => resolve('');
    reader.readAsDataURL(blob);
  });
}

async function finishAndSendVoiceNote(dayNum, agIdx) {
  const transcriptSnap = vnRecordingState.liveTranscript || '';
  let recMime = 'audio/webm';
  let audioBlob = null;

  if (activeMediaRecorder && activeMediaRecorder.state !== 'inactive') {
    recMime = activeMediaRecorder.mimeType || 'audio/webm';
    await new Promise((resolve) => {
      activeMediaRecorder.onstop = () => resolve();
      try { activeMediaRecorder.stop(); } catch (e) { resolve(); }
    });
  }
  if (activeVnAudioChunks.length > 0 && typeof Blob !== 'undefined') {
    audioBlob = new Blob(activeVnAudioChunks, { type: recMime });
  }
  cleanupActiveVoiceRecorder();

  vnRecordingState = {
    active: false,
    sending: true,
    dayNum: dayNum,
    agIdx: agIdx,
    seconds: 0,
    liveTranscript: transcriptSnap,
    errorMsg: ''
  };
  renderPlanView();

  const cardKey = dayNum + '_' + agIdx;
  const photoObj = vnPendingPhotos[cardKey] || null;
  delete vnPendingPhotos[cardKey];

  const audioB64 = audioBlob ? await blobToBase64(audioBlob) : '';
  const turnResult = await callKalyaniGeminiAudioTurn(dayNum, agIdx, audioB64, recMime, transcriptSnap, photoObj);
  const apiKey = getGeminiApiKey();
  const wavUrl = await synthesizeKalyaniAoedeAudio(turnResult.reply_bn, apiKey);

  if (!kalyaniThreads[cardKey]) kalyaniThreads[cardKey] = [];
  const turnIdx = kalyaniThreads[cardKey].length;
  const turnCacheKey = cardKey + '_' + turnIdx;
  if (wavUrl) vnAudioCache[turnCacheKey] = wavUrl;

  kalyaniThreads[cardKey].push({
    heard_bn: turnResult.heard_bn,
    reply_bn: turnResult.reply_bn,
    has_photo: !!(photoObj && photoObj.b64)
  });
  saveKalyaniThreads();

  if (!doneMap[cardKey]) {
    doneMap[cardKey] = true;
    saveDoneMap();
  }

  vnRecordingState = { active: false, sending: false, dayNum: 0, agIdx: -1, seconds: 0, liveTranscript: '', errorMsg: '' };
  renderPlanView();

  playVoiceNoteReplyAudio(dayNum, agIdx, turnIdx);
}

async function playVoiceNoteReplyAudio(dayNum, agIdx, turnIdx) {
  const cardKey = dayNum + '_' + agIdx;
  const turns = kalyaniThreads[cardKey] || [];
  const turn = turns[turnIdx];
  if (!turn) return;

  const turnCacheKey = cardKey + '_' + turnIdx;
  const btnId = 'btnVnReplyPlay_' + dayNum + '_' + agIdx + '_' + turnIdx;
  const audioKey = 'vn_reply_' + turnCacheKey;

  let wavUrl = vnAudioCache[turnCacheKey] || '';
  if (!wavUrl && getGeminiApiKey()) {
    wavUrl = await synthesizeKalyaniAoedeAudio(turn.reply_bn, getGeminiApiKey());
    if (wavUrl) vnAudioCache[turnCacheKey] = wavUrl;
  }

  const d = findDayObj(dayNum);
  const ag = (d && d.agendas && d.agendas[agIdx]) ? d.agendas[agIdx] : null;
  const fallbackAudioUrl = wavUrl || (ag && ag.audio_url) || (d && d.audio_url) || '';
  playMorningChimeSound();
  playOrToggleAudio(btnId, audioKey, fallbackAudioUrl, '');
}

function triggerCardPhotoUpload(dayNum, agIdx) {
  const inp = document.getElementById('vnPhotoInput_' + dayNum + '_' + agIdx);
  if (inp && typeof inp.click === 'function') inp.click();
}

function handleCardPhotoSelected(dayNum, agIdx, inputEl) {
  if (!inputEl || !inputEl.files || !inputEl.files[0] || typeof FileReader === 'undefined') return;
  const file = inputEl.files[0];
  const reader = new FileReader();
  reader.onloadend = () => {
    const res = String(reader.result || '');
    const comma = res.indexOf(',');
    if (comma >= 0) {
      vnPendingPhotos[dayNum + '_' + agIdx] = {
        mime: file.type || 'image/jpeg',
        b64: res.slice(comma + 1),
        previewUrl: res
      };
      renderPlanView();
    }
  };
  reader.readAsDataURL(file);
}

function toggleCardKeySetup(dayNum, agIdx) {
  const key = dayNum + '_' + agIdx;
  vnShowKeyInputForCard = (vnShowKeyInputForCard === key) ? null : key;
  renderPlanView();
}

function saveCardGeminiKeyFromInput(dayNum, agIdx) {
  const inp = document.getElementById('vnKeyInput_' + dayNum + '_' + agIdx);
  if (inp && inp.value) {
    saveGeminiApiKey(inp.value);
    vnShowKeyInputForCard = null;
    showCelebrationToast('🔑 কল্যাণীর ভয়েস মেসেজ এআই সংযোগ সফলভাবে চালু হয়েছে!');
    renderPlanView();
  }
}
