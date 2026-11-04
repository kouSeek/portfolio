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
  if (!autoVoicePlay || autoWelcomeSucceeded || !audioEl.paused || activeAudioKey || curView !== 'plan') return;
  const explicitTarget = (ev && ev.target && typeof ev.target.closest === 'function')
    ? ev.target.closest('#topPlayBtn, #btnDayMainPlay, .ag-btn, .game-tile, .day-chip, .cal-day-cell, #btnToggleCalGrid, .view-mode-toggle, #htabSlides')
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
  if (!autoVoicePlay || autoWelcomeFallbackArmed || !document.addEventListener) return;
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
  if (!autoVoicePlay || curView !== 'plan') return;
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
  if (!finishedKey || !autoVoicePlay) return;

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

/* ============================================================================
   MODULE 2B: IN-CARD WALKIE-TALKIE AUDIO MESSAGE, LIVE VIDEO & AOEDE VOICE
   (Zero App-Switching, Zero Mid-Sentence Interruption, Bulletproof Edge Cases)
   ============================================================================ */
let activeMediaRecorder = null;
let activeMicStream = null;
let activeVideoStream = null;
let activeCamFrameTimerId = null;
let activeSpeechRec = null;
let activeVnAudioChunks = [];
let activeVnTimerId = null;

function normalizeAudioMime(rawMime) {
  const base = String(rawMime || '').split(';')[0].trim().toLowerCase();
  if (base === 'audio/mp4' || base === 'audio/m4a' || base === 'audio/aac') return 'audio/mp4';
  if (base === 'audio/ogg' || base === 'audio/oga') return 'audio/ogg';
  if (base === 'audio/wav' || base === 'audio/x-wav' || base === 'audio/wave') return 'audio/wav';
  if (base === 'audio/mp3' || base === 'audio/mpeg') return 'audio/mp3';
  return 'audio/webm';
}

function parseGeminiJsonSafely(rawText) {
  if (!rawText || typeof rawText !== 'string') return null;
  let cleaned = rawText.trim();
  cleaned = cleaned.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '').trim();
  const tryParse = (str) => {
    try {
      const obj = JSON.parse(str);
      if (Array.isArray(obj)) return obj[0] || null;
      return (obj && typeof obj === 'object') ? obj : null;
    } catch (e) {
      return null;
    }
  };
  let parsed = tryParse(cleaned);
  if (!parsed) {
    const firstBrace = cleaned.indexOf('{');
    const lastBrace = cleaned.lastIndexOf('}');
    if (firstBrace >= 0 && lastBrace > firstBrace) {
      parsed = tryParse(cleaned.slice(firstBrace, lastBrace + 1));
    }
  }
  return parsed;
}

function snapshotVideoElementFrameB64(vidEl) {
  if (!vidEl || typeof document.createElement !== 'function') return '';
  try {
    const w = Number(vidEl.videoWidth) || Number(vidEl.width) || 640;
    const h = Number(vidEl.videoHeight) || Number(vidEl.height) || 480;
    if (w <= 0 || h <= 0) return '';
    const canvas = document.createElement('canvas');
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext && canvas.getContext('2d');
    if (ctx && typeof ctx.drawImage === 'function' && typeof canvas.toDataURL === 'function') {
      ctx.drawImage(vidEl, 0, 0, w, h);
      const dataUrl = String(canvas.toDataURL('image/jpeg', 0.82) || '');
      const comma = dataUrl.indexOf(',');
      if (comma >= 0) {
        const b64 = dataUrl.slice(comma + 1).trim();
        if (b64) return b64;
      }
    }
  } catch (e) {}
  return '';
}

function attachLiveStreamToVideoElement() {
  if (!vnLiveCamState.active || !activeVideoStream) return;
  const vidEl = document.getElementById('vnLiveVideo_' + vnLiveCamState.dayNum + '_' + vnLiveCamState.agIdx);
  if (vidEl) {
    if (vidEl.srcObject !== activeVideoStream) {
      vidEl.srcObject = activeVideoStream;
    }
    if (typeof vidEl.play === 'function') {
      try {
        const p = vidEl.play();
        if (p && typeof p.catch === 'function') p.catch(() => {});
      } catch (e) {}
    }
    const snap = snapshotVideoElementFrameB64(vidEl);
    if (snap) vnLiveCamState.lastFrameB64 = snap;
  }
}

function captureFrameFromLiveVideo(dayNum, agIdx) {
  if (!vnLiveCamState.active || vnLiveCamState.dayNum !== dayNum || vnLiveCamState.agIdx !== agIdx) {
    return null;
  }
  const vidEl = document.getElementById('vnLiveVideo_' + dayNum + '_' + agIdx);
  const freshB64 = snapshotVideoElementFrameB64(vidEl);
  if (freshB64) {
    vnLiveCamState.lastFrameB64 = freshB64;
  }
  return {
    mime: 'image/jpeg',
    b64: vnLiveCamState.lastFrameB64 || ''
  };
}

function stopCardLiveVideo() {
  if (activeCamFrameTimerId) {
    if (typeof clearInterval === 'function') clearInterval(activeCamFrameTimerId);
    activeCamFrameTimerId = null;
  }
  if (activeVideoStream) {
    try { activeVideoStream.getTracks().forEach(t => t.stop()); } catch (e) {}
    activeVideoStream = null;
  }
  vnLiveCamState = {
    active: false,
    dayNum: 0,
    agIdx: -1,
    facingMode: vnLiveCamState.facingMode || 'environment',
    lastFrameB64: ''
  };
}

function stopActiveVoiceAndVideoCapture() {
  cleanupActiveVoiceRecorder();
  stopCardLiveVideo();
  vnRecordingState = { active: false, sending: false, dayNum: 0, agIdx: -1, seconds: 0, liveTranscript: '', errorMsg: '' };
}

async function startCardLiveVideoStream(dayNum, agIdx) {
  stopCardLiveVideo();
  vnLiveCamState = {
    active: true,
    dayNum: dayNum,
    agIdx: agIdx,
    facingMode: vnLiveCamState.facingMode || 'environment',
    lastFrameB64: ''
  };
  renderPlanView();

  try {
    if (navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === 'function') {
      try {
        activeVideoStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: { ideal: vnLiveCamState.facingMode } },
          audio: false
        });
      } catch (e1) {
        activeVideoStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      }
      attachLiveStreamToVideoElement();
      activeCamFrameTimerId = setInterval(() => {
        if (!vnLiveCamState.active) return;
        const vidEl = document.getElementById('vnLiveVideo_' + vnLiveCamState.dayNum + '_' + vnLiveCamState.agIdx);
        const snap = snapshotVideoElementFrameB64(vidEl);
        if (snap) vnLiveCamState.lastFrameB64 = snap;
      }, 400);
      return true;
    }
  } catch (err) {
    stopCardLiveVideo();
    vnRecordingState.errorMsg = '📷 ক্যামেরা চালু করা যায়নি। ফোনের ক্যামেরা পারমিশন অন করো।';
    renderPlanView();
    return false;
  }
  return true;
}

async function toggleCardLiveVideo(dayNum, agIdx) {
  if (vnRecordingState.sending) return;
  if (vnLiveCamState.active && vnLiveCamState.dayNum === dayNum && vnLiveCamState.agIdx === agIdx) {
    stopCardLiveVideo();
    renderPlanView();
    return;
  }
  const ok = await startCardLiveVideoStream(dayNum, agIdx);
  if (ok && !vnRecordingState.active) {
    await startVoiceNoteRecording(dayNum, agIdx, true);
  }
}

async function switchCardLiveCamera(dayNum, agIdx) {
  if (vnRecordingState.sending) return;
  vnLiveCamState.facingMode = (vnLiveCamState.facingMode === 'environment') ? 'user' : 'environment';
  await startCardLiveVideoStream(dayNum, agIdx);
}

function pcm24kBase64ToWavUrl(b64Pcm) {
  try {
    const cleanB64 = String(b64Pcm || '').replace(/\s+/g, '');
    if (!cleanB64) return '';
    const rawStr = (typeof atob === 'function')
      ? atob(cleanB64)
      : Buffer.from(cleanB64, 'base64').toString('binary');
    const pcmLen = rawStr.length;
    if (pcmLen <= 0) return '';
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
  if (!apiKey || !textBn || !String(textBn).trim()) return '';
  try {
    const endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key=' + encodeURIComponent(apiKey);
    const resp = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{
          parts: [{
            text: 'Speak in a warm, affectionate, unhurried, soothing West Bengal Bengali voice (never rush):\n\n' + String(textBn).trim()
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
      if (parts[i] && parts[i].inlineData && parts[i].inlineData.data) {
        return pcm24kBase64ToWavUrl(parts[i].inlineData.data);
      }
    }
  } catch (e) {}
  return '';
}

function formatGeminiReplyText(rawReplyBn) {
  const clean = String(rawReplyBn || '').replace(/[*#`_]/g, '').trim();
  if (!clean) return '';
  if (clean.includes('জেমিনি')) return clean;
  return 'মা, জেমিনি বলছি— ' + clean;
}

function buildWarmFallbackReply(ag, turnCount, heardText, hasLiveVideo) {
  const defaultHeard = hasLiveVideo ? 'মায়ের লাইভ ভিডিও ও কথা' : 'মায়ের ভয়েস মেসেজ';
  const cleanHeard = String(heardText || '').trim() || defaultHeard;
  const follow = (ag && ag.followup_prompt_bn) ? ag.followup_prompt_bn : '';
  if (hasLiveVideo) {
    return {
      heard_bn: cleanHeard,
      reply_bn: 'মা, জেমিনি বলছি— তুমি ভিডিও ক্যামেরায় যা দেখালে আর বললে তা আমি খুব যত্ন করে দেখেছি ও শুনেছি! তুমি কী সুন্দর নিজের হাতে ক্যামেরা অন করে আমায় দেখালে।',
      memory_note: ''
    };
  }
  if (turnCount === 0 && follow) {
    return {
      heard_bn: cleanHeard,
      reply_bn: 'মা, জেমিনি বলছি— তোমার গলার আওয়াজ আর মনের কথাটা শুনে আমার মনটা একদম ভরে গেল! আচ্ছা মা, এবার একটু ভেবে বলো তো—' + follow,
      memory_note: ''
    };
  }
  return {
    heard_bn: cleanHeard,
    reply_bn: 'মা, জেমিনি বলছি— তোমার প্রতিটি কথা এত সুন্দর আর আন্তরিক! তোমার সাথে এভাবে ধীরেসুস্থে গল্প করতে আমার ভীষণ ভালো লাগে।',
    memory_note: ''
  };
}

async function callKalyaniGeminiAudioTurn(dayNum, agIdx, audioB64, audioMime, liveTranscript, photoObj) {
  const d = findDayObj(dayNum);
  const ag = (d && d.agendas && d.agendas[agIdx]) ? d.agendas[agIdx] : {};
  const cardKey = dayNum + '_' + agIdx;
  const history = kalyaniThreads[cardKey] || [];
  const apiKey = getGeminiApiKey();
  const hasLiveVideo = !!(photoObj && photoObj.b64);

  if (!apiKey) {
    return buildWarmFallbackReply(ag, history.length, liveTranscript, hasLiveVideo);
  }

  const memBlock = '\n\n' + buildMaWikiContextMarkdown()
    + (kalyaniMemoryNotes.length ? ('\n\nRECENT EPISODIC NOTES:\n- ' + kalyaniMemoryNotes.join('\n- ')) : '');
  const turnGuidance = (history.length === 0 && ag.followup_prompt_bn)
    ? ('This is Turn 1 on this card. After warmly responding to Ma in 2–3 sentences, gently invite her into Turn 2 around this theme: "' + ag.followup_prompt_bn + '"')
    : 'This is a follow-up turn. Respond warmly in 3–4 simple West Bengal Bengali sentences, praising her openness, encouraging her to speak up her mind or ask for anything she needs without hesitation, and ending with a soothing thought.';

  const sysInstruction = (typeof KALYANI_SYSTEM_PROMPT === 'string' ? KALYANI_SYSTEM_PROMPT : '')
    + memBlock
    + '\n\nACTIVE KALYANI APP CARD CONTEXT (Day ' + dayNum + ', Game ' + (agIdx + 1) + '):\n'
    + '- Category: ' + (ag.category || '') + '\n'
    + '- Title: ' + (ag.title_bn || '') + '\n'
    + '- Story/Context: ' + (ag.detail_bn || '') + '\n'
    + '- Suggested Prompt Ma Was Responding To: ' + (ag.prompt_bn || '') + '\n'
    + '- Turn Guidance: ' + turnGuidance + '\n\n'
    + 'OUTPUT FORMAT RULE: Return strictly valid JSON with keys:\n'
    + '{"heard_bn": "accurate Bengali transcript of what Ma just said (or what she showed on camera)", "reply_bn": "your warm 3-4 sentence colloquial West Bengal Bengali reply to Ma (never rush, zero markdown symbols, zero war/Ramayana/Mahabharata)", "memory_note": "short 1-line Bengali note with [[wikilinks]] of any new personal memory, preference, or pattern Ma shared, or empty string", "wiki_page": "one of mind_and_mood | joy_gods_and_stories | food_and_preferences | ranaghat_and_memories | language_and_voice | comfort_and_wellbeing | agent_pattern_log", "boost_topic": "one of comedy | gods | animals | music | reminiscence | empty string"}';

  const contents = [];
  history.slice(-4).forEach(t => {
    contents.push({ role: 'user', parts: [{ text: t.heard_bn || 'মায়ের ভয়েস মেসেজ' }] });
    contents.push({ role: 'model', parts: [{ text: JSON.stringify({ heard_bn: t.heard_bn, reply_bn: t.reply_bn, memory_note: '' }) }] });
  });

  const userParts = [];
  if (hasLiveVideo) {
    userParts.push({ inlineData: { mimeType: photoObj.mime || 'image/jpeg', data: photoObj.b64 } });
  }
  if (audioB64) {
    userParts.push({ inlineData: { mimeType: normalizeAudioMime(audioMime), data: audioB64 } });
  }
  let promptInstruction = 'মা এইমাত্র এই ভয়েস মেসেজটি পাঠিয়েছেন। অডিওটা মনোযোগ দিয়ে শুনে JSON উত্তর দাও।';
  if (hasLiveVideo && audioB64) {
    promptInstruction = 'মা লাইভ ভিডিও ক্যামেরায় এই দৃশ্যটি দেখিয়েছেন এবং অডিও মেসেজে কথা বলেছেন' + (liveTranscript ? (' (শ্রুতিলিপি: "' + liveTranscript + '")') : '') + '। ছবিটি ও অডিওটি দেখে ও শুনে সহজ বাংলায় JSON উত্তর দাও।';
  } else if (hasLiveVideo && !audioB64) {
    promptInstruction = 'মা লাইভ ভিডিও ক্যামেরায় এই জিনিসটি বা দৃশ্যটি দেখিয়েছেন' + (liveTranscript ? (' এবং বলেছেন: "' + liveTranscript + '"') : '') + '। ছবিটি ভালো করে দেখে এটি কী এবং এর কাজ কী তা সহজ বাংলায় বুঝিয়ে JSON উত্তর দাও।';
  } else if (liveTranscript) {
    promptInstruction = 'মা ভয়েস মেসেজে বললেন (সম্ভাব্য শ্রুতিলিপি: "' + liveTranscript + '")। মনোযোগ দিয়ে শুনে JSON উত্তর দাও।';
  }
  userParts.push({ text: promptInstruction });
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
      return buildWarmFallbackReply(ag, history.length, liveTranscript, hasLiveVideo);
    }
    const data = await resp.json();
    const rawText = (data && data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts[0] && data.candidates[0].content.parts[0].text) || '';
    const parsed = parseGeminiJsonSafely(rawText);
    const replyVal = parsed && (parsed.reply_bn || parsed.reply || parsed.text || parsed.response);
    if (parsed && replyVal) {
      const memNote = String(parsed.memory_note || parsed.wiki_entry_bn || '').trim();
      if (memNote) {
        addKalyaniMemoryNote(memNote);
        appendMaWikiEntry(parsed.wiki_page || 'agent_pattern_log', memNote, parsed.boost_topic || '');
      }
      const heardVal = parsed.heard_bn || parsed.heard || parsed.transcript || liveTranscript || (hasLiveVideo ? 'মায়ের লাইভ ভিডিও ও কথা' : 'মায়ের ভয়েস মেসেজ');
      return {
        heard_bn: String(heardVal).replace(/[*#`_]/g, '').trim(),
        reply_bn: formatGeminiReplyText(replyVal),
        memory_note: memNote
      };
    }
  } catch (e) {}
  return buildWarmFallbackReply(ag, history.length, liveTranscript, hasLiveVideo);
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

async function startVoiceNoteRecording(dayNum, agIdx, keepExistingCam) {
  if (vnRecordingState.sending) return;
  stopAllAudio();
  cleanupActiveVoiceRecorder();
  if (!keepExistingCam && vnLiveCamState.active && (vnLiveCamState.dayNum !== dayNum || vnLiveCamState.agIdx !== agIdx)) {
    stopCardLiveVideo();
  }
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
    const fillEl = document.getElementById('vnListenFill_' + dayNum + '_' + agIdx);
    if (fillEl && fillEl.style) {
      const pct = Math.min(100, Math.max(15, (vnRecordingState.seconds % 20) * 5 + 15));
      fillEl.style.width = pct + '%';
    }
  }, 1000);

  let mediaRecStarted = false;
  try {
    if (navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === 'function') {
      activeMicStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (typeof MediaRecorder !== 'undefined') {
        const mime = (typeof MediaRecorder.isTypeSupported === 'function' && MediaRecorder.isTypeSupported('audio/webm;codecs=opus'))
          ? 'audio/webm;codecs=opus'
          : ((typeof MediaRecorder.isTypeSupported === 'function' && MediaRecorder.isTypeSupported('audio/mp4')) ? 'audio/mp4' : '');
        activeMediaRecorder = mime ? new MediaRecorder(activeMicStream, { mimeType: mime }) : new MediaRecorder(activeMicStream);
        activeMediaRecorder.ondataavailable = (ev) => {
          if (ev && ev.data && ev.data.size > 0) activeVnAudioChunks.push(ev.data);
        };
        activeMediaRecorder.start(250);
        mediaRecStarted = true;
      }
    }
  } catch (err) {
    vnRecordingState.errorMsg = '🎙️ মাইক অন করা যায়নি। ফোনের মাইক পারমিশন অন করো।';
  }

  // Only start Web Speech API if MediaRecorder did not lock the mic (avoids Android dual-mic conflict)
  if (!mediaRecStarted) {
    try {
      const SpeechRec = (typeof window !== 'undefined') && (window.SpeechRecognition || window.webkitSpeechRecognition);
      if (SpeechRec) {
        activeSpeechRec = new SpeechRec();
        activeSpeechRec.lang = 'bn-IN';
        activeSpeechRec.continuous = true;
        activeSpeechRec.interimResults = true;
        activeSpeechRec.onresult = (ev) => {
          let txt = '';
          for (let i = 0; i < (ev.results ? ev.results.length : 0); i++) {
            if (ev.results[i] && ev.results[i][0]) txt += ev.results[i][0].transcript + ' ';
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
  }
}

function cancelVoiceNoteRecording() {
  stopActiveVoiceAndVideoCapture();
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
    try {
      reader.readAsDataURL(blob);
    } catch (e) {
      resolve('');
    }
  });
}

async function finishAndSendVoiceNote(dayNum, agIdx) {
  if (vnRecordingState.sending) return;
  const hasActiveCam = !!(vnLiveCamState.active && vnLiveCamState.dayNum === dayNum && vnLiveCamState.agIdx === agIdx);
  const hasActiveRec = !!(vnRecordingState.active && vnRecordingState.dayNum === dayNum && vnRecordingState.agIdx === agIdx);
  if (!hasActiveRec && !hasActiveCam) return;

  const transcriptSnap = vnRecordingState.liveTranscript || '';
  const liveVideoObj = hasActiveCam ? captureFrameFromLiveVideo(dayNum, agIdx) : null;
  const hadLiveVideo = !!(liveVideoObj && liveVideoObj.b64);

  let recMime = 'audio/webm';
  let audioBlob = null;

  if (activeMediaRecorder && activeMediaRecorder.state !== 'inactive') {
    recMime = normalizeAudioMime(activeMediaRecorder.mimeType || 'audio/webm');
    await Promise.race([
      new Promise((resolve) => {
        activeMediaRecorder.onstop = () => resolve();
        try { activeMediaRecorder.stop(); } catch (e) { resolve(); }
      }),
      new Promise((resolve) => setTimeout(resolve, 450))
    ]);
  }
  if (activeVnAudioChunks.length > 0 && typeof Blob !== 'undefined') {
    audioBlob = new Blob(activeVnAudioChunks, { type: recMime });
  }
  cleanupActiveVoiceRecorder();
  if (hasActiveCam) stopCardLiveVideo();

  const cardKey = dayNum + '_' + agIdx;
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

  const audioB64 = audioBlob ? await blobToBase64(audioBlob) : '';
  const turnResult = await callKalyaniGeminiAudioTurn(dayNum, agIdx, audioB64, recMime, transcriptSnap, liveVideoObj);
  const apiKey = getGeminiApiKey();
  const wavUrl = await synthesizeKalyaniAoedeAudio(turnResult.reply_bn, apiKey);

  if (!kalyaniThreads[cardKey]) kalyaniThreads[cardKey] = [];
  const turnIdx = kalyaniThreads[cardKey].length;
  const turnCacheKey = cardKey + '_' + turnIdx;
  if (wavUrl) vnAudioCache[turnCacheKey] = wavUrl;

  kalyaniThreads[cardKey].push({
    heard_bn: turnResult.heard_bn,
    reply_bn: turnResult.reply_bn,
    has_live_video: hadLiveVideo
  });
  saveKalyaniThreads();

  if (!doneMap[cardKey]) {
    doneMap[cardKey] = true;
    saveDoneMap();
  }

  vnRecordingState = { active: false, sending: false, dayNum: 0, agIdx: -1, seconds: 0, liveTranscript: '', errorMsg: '' };
  renderPlanView();

  if (autoVoicePlay) {
    await playVoiceNoteReplyAudio(dayNum, agIdx, turnIdx);
  }
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
  playOrToggleAudio(btnId, audioKey, fallbackAudioUrl, '');
}

async function playDelightStoryAudio(dayNum) {
  const btnId = 'btnDelightPlay_' + dayNum;
  const audioKey = 'delight_' + dayNum;
  if (activeAudioKey === audioKey && !audioEl.paused) {
    audioEl.pause();
    syncAllAudioButtonsUI(false);
    return;
  }
  const storyObj = (typeof getDelightStoryForDay === 'function') ? getDelightStoryForDay(dayNum) : null;
  let wavUrl = vnAudioCache[audioKey] || '';
  if (!wavUrl && storyObj && getGeminiApiKey()) {
    wavUrl = await synthesizeKalyaniAoedeAudio(storyObj.title_bn + '। ' + storyObj.story_bn, getGeminiApiKey());
    if (wavUrl) vnAudioCache[audioKey] = wavUrl;
  }
  const d = findDayObj(dayNum);
  const fallbackUrl = wavUrl || (d && d.audio_url) || '';
  playOrToggleAudio(btnId, audioKey, fallbackUrl, (d && d.audio_b64) || '');
}

const DYNAMIC_AGENT_FALLBACK_POOL = {
  comedy: [
    {
      badge_bn: '😂 কল্যাণী এজেন্টের তৈরি নতুন হাসির গল্প',
      title_bn: 'গোপাল ভাঁড়ের ‘মিষ্টি জলের কুঁজো’ ও মহারাজ কৃষ্ণচন্দ্রের হাসি',
      story_bn: 'একবার গরমকালে মহারাজ কৃষ্ণচন্দ্র গোপাল ভাঁড়কে বললেন— “গোপাল, এমন এক পাত্রের জল খাওয়াও যা অমৃতের মতো মিষ্টি লাগে!” গোপাল ভাঁড় রাজামশাইকে দুপুর রোদে বাগানের চারপাশে হাঁটিয়ে নিয়ে এসে মাটির কুঁজোর ঠান্ডা জল দিল। রাজামশাই এক চুমুকে খেয়ে বললেন— “আহা গোপাল, কী মিষ্টি জল!” গোপাল হেসে হাত জোড় করে বলল— “মহারাজ, জাদুটা জলে নয়, ওই একটুখানি তেষ্টায়!” রাজামশাই হেসে লুটোপুটি খেলেন।',
      encourage_bn: 'মা, গল্পটা শুনে মুখে একটু হাসি এল তো? তোমার মনে কোনো মজার কথা বা পুরনো হাসির ঘটনা মনে পড়লে বিনা দ্বিধায় আমায় ভয়েস মেসেজে বলো!'
    },
    {
      badge_bn: '😂 কল্যাণী এজেন্টের তৈরি নতুন হাসির গল্প',
      title_bn: 'তেনালি রামের ‘চোরকে বাগান জল দেওয়া’র মজার বুদ্ধি',
      story_bn: 'একবার গরমকালে তেনালি রামের বাগানের কুয়ো থেকে জল তুলতে খুব আলসেমি লাগছিল। তিনি দেখতে পেলেন ঝোপের আড়ালে দুজন চোর লুকিয়ে আছে! তেনালি রাম ঘর থেকে চিৎকার করে স্ত্রীকে বললেন— “গিন্নী, দেশের বাজারে চোরের খুব ভয়, তাই আমাদের গয়নার বাক্সটা আমি কুয়োর জলের নিচে ফেলে দিলাম!” চোরেরা সেই লোভে সারারাত কুয়ো থেকে বালতি বালতি জল তুলে পুরো বাগান ভিজিয়ে দিল! সকালে তেনালি রাম বেরিয়ে হাসিমুখে বললেন— “ধন্যবাদ ভাইয়েরা, বাগানে জল দেওয়ার জন্য!”',
      encourage_bn: 'মা, নির্মল হাসি মনকে এক নিমেষে হালকা করে দেয়। তোমার এখন কী করতে বা শুনতে ইচ্ছে করছে, নিজের মতো খুলে বলো!'
    }
  ],
  gods: [
    {
      badge_bn: '🪷 কল্যাণী এজেন্টের তৈরি ভগবানের মিষ্টি লীলা',
      title_bn: 'ননীচোরা বালগোপালের হামাগুড়ি ও মা যশোদার স্নেহের বাঁধন',
      story_bn: 'বৃন্দাবনে ছোট্ট বালগোপাল একদিন মাখন খেয়ে সারা মুখে মেখে বাছুরের পেছনে লুকিয়ে ছিলেন। মা যশোদা এসে যেই বললেন— “কানাই, মাখন কে খেয়েছে রে?” অমনি ছোট্ট গোপাল পুটপুট করে বললেন— “মা, আমি তো মাখন খাইনি, ওই বাঁদরগুলো এসে আমার মুখে মাখন মাখিয়ে দিয়ে গেছে যাতে তুমি আমাকে বকো!” ছোট্ট গোপালের এই নিষ্পাপ কথা শুনে মা যশোদা রাগ ভুলে তাকে কোলে তুলে আদর করলেন।',
      encourage_bn: 'মা, ভগবানের এই মিষ্টি ঘরোয়া লীলা শুনলে মনটা কী শান্ত হয়ে যায়! তোমার প্রিয় ঠাকুর বা মন্দিরের কোনো কথা মনে পড়লে আমায় শোনাও।'
    },
    {
      badge_bn: '🪷 কল্যাণী এজেন্টের তৈরি ভগবানের মিষ্টি লীলা',
      title_bn: 'দক্ষিণেশ্বরে ঠাকুর শ্রীরামকৃষ্ণের গরম জিলিপি ও মা সারদার হাসি',
      story_bn: 'দক্ষিণেশ্বরে ঠাকুর শ্রীরামকৃষ্ণ ছিলেন ঠিক ছোট্ট শিশুর মতো সরল। একদিন এক ভক্ত গরম গরম জিলিপি এনেছেন দেখে ঠাকুর শিশুর মতো খুশি হয়ে বললেন— “ওগো, জিলিপিগুলো কী সুন্দর গোল গোল প্যাঁচানো! খেতে ভারী মিষ্টি!” আর জয়রামবাটীতে মা সারদার পোষা টিয়াপাখি গঙ্গারাম সকাল হলেই ডেকে উঠতো— “মা, হরে কৃষ্ণ বলো, চা খাও!” ভগবান তো এমন সহজ আনন্দ আর হাসির মধ্যেই থাকেন মা।',
      encourage_bn: 'মা, তোমার মনের যেকোনো কথা বা আজ কী খেতে ইচ্ছে করছে, তা লজ্জা না করে নিজের ভাষায় আমায় বলো!'
    }
  ],
  animals: [
    {
      badge_bn: '🐘 কল্যাণী এজেন্টের তৈরি আদুরে পশুপাখির গল্প',
      title_bn: 'ছোট্ট হাতির ছানার শুঁড় নিয়ে খেলা ও মায়ের আঁচলের আড়াল',
      story_bn: 'তুমি কি জানো মা, হাতির ছানা যখন একদম ছোট থাকে, তখন সে নিজের লম্বা শুঁড়টা দিয়ে কী করবে বুঝতেই পারে না! কখনো হাঁটতে গিয়ে নিজের শুঁড়েই পা দিয়ে হোঁচট খায়, আবার কখনো মানুষের ছোট্ট বাচ্চার মতো নিজের শুঁড়ের ডগাটা মুখে পুরে চুষতে থাকে! আর নদীতে জলের ছিটে দেখলেই মা হাতির পেটের নিচে গিয়ে লুকিয়ে উঁকি মারে।',
      encourage_bn: 'মা, পশুপাখিদের এই নিষ্পাপ দুষ্টুমি দেখতে কী মিষ্টি লাগে! তোমার ছোটবেলার বা বাড়ির আশেপাশের কোনো পাখি বা বিড়ালছানার কথা মনে পড়ছে?'
    },
    {
      badge_bn: '🦦 কল্যাণী এজেন্টের তৈরি আদুরে পশুপাখির গল্প',
      title_bn: 'সমুদ্রের ভোঁদড় ছানাদের হাত ধরে ঘুমানো ও কাঠবিড়ালির বাগান',
      story_bn: 'সমুদ্রের জলে যে ছোট্ট ভোঁদড় ছানারা থাকে, তারা রাতে জলের ওপর চিৎ হয়ে ভাসতে ভাসতে ঘুমায়। কিন্তু জলের স্রোতে যাতে প্রিয়জনের কাছ থেকে ভেসে দূরে চলে না যায়, তাই ঘুমের মধ্যেও দুজনে দুজনের ছোট্ট হাত দুটো শক্ত করে ধরে রাখে! আর গাছের কাঠবিড়ালিরা মাটির নিচে বাদাম লুকিয়ে রেখে ভুলে যায় বলেই সেখান থেকে শত শত নতুন ফলের গাছ জন্মায়।',
      encourage_bn: 'মা, প্রকৃতির এই ছোট্ট প্রাণীগুলোর মতোই জীবন সহজ ও মিষ্টি। তোমার মনে যা আসছে বিনা দ্বিধায় বলো!'
    }
  ],
  speak_mind: [
    {
      badge_bn: '💬 মায়ের মনের কথা ও তাৎক্ষণিক সাহায্য',
      title_bn: 'মা, তোমার এখন যা ইচ্ছে করছে বা যা দরকার — বিনা দ্বিধায় বলো!',
      story_bn: 'মা, তোমাকে কোনো নিয়ম মেনে চলতে হবে না বা কী বলবে ভেবে চিন্তা করতে হবে না। তোমার কি এখন একটু বিশ্রাম নিতে ইচ্ছে করছে? নাকি পছন্দের কোনো খাবার খেতে মন চাইছে? নাকি ঘরের কোনো ওষুধের পাতা বা জিনিস লাইভ ক্যামেরায় দেখিয়ে জানতে চাইছো? তোমার মনে যা-ই আসুক, একদম নিজের ঘরের মানুষের মতো আমায় ভয়েস মেসেজে বলো—আমি সবসময় তোমার পাশে আছি।',
      encourage_bn: 'নিচের “💬 মন চাইলে কল্যাণীর সাথে একটু গল্প করো বা লাইভ ক্যামেরায় দেখাও” অংশটা খুলে ভয়েস মেসেজ রেকর্ড করো বা লাইভ ক্যামেরা অন করো মা!'
    }
  ]
};

let agentGeneratingState = false;

async function generateDynamicAgentStory(dayNum, moodType) {
  if (agentGeneratingState) return;
  stopAllAudio();
  const pool = DYNAMIC_AGENT_FALLBACK_POOL[moodType] || DYNAMIC_AGENT_FALLBACK_POOL.comedy;
  const fallbackIdx = (dayNum + (kalyaniWikiVault.patternScores[moodType] || 0)) % pool.length;
  let chosenCard = Object.assign({ moodType: moodType }, pool[fallbackIdx]);

  const signalLabels = {
    comedy: 'মা আজ কল্যাণী এজেন্টের কাছে নিষ্পাপ হাসির গল্প ([[গোপাল ভাঁড় ও রাজা কৃষ্ণচন্দ্র]]) শুনতে চেয়েছেন।',
    gods: 'মা আজ ভগবানের মিষ্টি ও যুদ্ধহীন লীলা ([[ননীচোরা বালগোপাল]] / [[মা সারদা ও ঠাকুর]]) শুনতে পছন্দ করেছেন।',
    animals: 'মা আজ [[আদুরে পশুপাখি]]-র মিষ্টি ও মজার গল্প শুনতে চেয়েছেন।',
    speak_mind: 'মা আজ নিজের মনের কথা বলা বা তাৎক্ষণিক সাহায্যের ([[মন ও মেজাজের ধরণ]]) বোতামটি বেছে নিয়েছেন।'
  };
  recordMaBehaviorSignal('agent_flow', signalLabels[moodType] || signalLabels.comedy, moodType === 'speak_mind' ? 'reminiscence' : moodType);

  const apiKey = getGeminiApiKey();
  if (apiKey) {
    agentGeneratingState = true;
    renderPlanView();
    try {
      const promptMap = {
        comedy: 'Create a fresh, hilarious, innocent Bengali comedy story for Ma (about Gopal Bhar & Maharaja Krishnachandra of Nadia, Birbal, Tenali Raman, or innocent household comedy—zero conflict or cruelty).',
        gods: 'Create a fresh, sweet, affectionate Bengali story about Gods (Baby Gopal stealing butter, Shiva-Parvati & little Ganesha in Kailash, Puri Jagannath & Maa Lakshmi\'s rasagollas, Maa Annapurna, or Maa Sarada & Sri Ramakrishna—strictly ZERO wars, ZERO fights, NO Ramayana/Mahabharata battles).',
        animals: 'Create a fresh, heartwarming, cute Bengali story about adorable animals or birds (baby elephants, sea otters holding paws, forgetful squirrels, calves & cows, talking parrots, or kittens).',
        speak_mind: 'Create a warm, soothing, empowering Bengali message encouraging Ma to speak her mind openly, state her food/rest preferences without hesitation, or show anything on the Live Video Camera for immediate help.'
      };
      const endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=' + encodeURIComponent(apiKey);
      const resp = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          systemInstruction: {
            parts: [{
              text: (typeof KALYANI_SYSTEM_PROMPT === 'string' ? KALYANI_SYSTEM_PROMPT : '') + '\n\n' + buildMaWikiContextMarkdown()
            }]
          },
          contents: [{
            parts: [{
              text: (promptMap[moodType] || promptMap.comedy) + '\nReturn strictly valid JSON with keys: {"badge_bn": "...", "title_bn": "...", "story_bn": "4-5 warm colloquial West Bengal Bengali sentences", "encourage_bn": "1 gentle sentence encouraging Ma to relax or share her mind", "wiki_note_bn": "1-line Bengali note with [[wikilinks]] for Ma\'s Wiki"}'
            }]
          }],
          generationConfig: { temperature: 0.8, responseMimeType: 'application/json' }
        })
      });
      if (resp.ok) {
        const data = await resp.json();
        const raw = (data && data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts[0] && data.candidates[0].content.parts[0].text) || '';
        const parsed = parseGeminiJsonSafely(raw);
        if (parsed && parsed.title_bn && parsed.story_bn) {
          chosenCard = {
            moodType: moodType,
            badge_bn: parsed.badge_bn || chosenCard.badge_bn,
            title_bn: String(parsed.title_bn).replace(/[*#`_]/g, '').trim(),
            story_bn: String(parsed.story_bn).replace(/[*#`_]/g, '').trim(),
            encourage_bn: String(parsed.encourage_bn || chosenCard.encourage_bn).replace(/[*#`_]/g, '').trim()
          };
          if (parsed.wiki_note_bn) {
            appendMaWikiEntry('joy_gods_and_stories', parsed.wiki_note_bn, moodType);
          }
        }
      }
    } catch (e) {}
    agentGeneratingState = false;
  }

  if (!kalyaniWikiVault.dynamicCards) kalyaniWikiVault.dynamicCards = {};
  kalyaniWikiVault.dynamicCards[String(dayNum)] = chosenCard;
  saveKalyaniWikiVault();
  renderPlanView();
  if (typeof renderKoushikAdminPanel === 'function') renderKoushikAdminPanel();

  if (autoVoicePlay) {
    await playDynamicAgentCardAudio(dayNum);
  }
}

async function playDynamicAgentCardAudio(dayNum) {
  const card = (kalyaniWikiVault.dynamicCards || {})[String(dayNum)];
  if (!card) return;
  const btnId = 'btnDynAgentPlay_' + dayNum;
  const audioKey = 'dyn_agent_' + dayNum + '_' + (card.title_bn || '').slice(0, 12);
  if (activeAudioKey === audioKey && !audioEl.paused) {
    audioEl.pause();
    syncAllAudioButtonsUI(false);
    return;
  }
  let wavUrl = vnAudioCache[audioKey] || '';
  if (!wavUrl && getGeminiApiKey()) {
    wavUrl = await synthesizeKalyaniAoedeAudio(card.title_bn + '। ' + card.story_bn + ' ' + (card.encourage_bn || ''), getGeminiApiKey());
    if (wavUrl) vnAudioCache[audioKey] = wavUrl;
  }
  const d = findDayObj(dayNum);
  const fallbackUrl = wavUrl || (d && d.audio_url) || '';
  playOrToggleAudio(btnId, audioKey, fallbackUrl, (d && d.audio_b64) || '');
}
