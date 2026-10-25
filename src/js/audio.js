/* ============================================================================
   MODULE 2: UNIFIED AOEDE AUDIO ENGINE, PROGRESS BAR & NOTIFICATIONS (src/js/audio.js)
   ============================================================================ */
const audioEl = document.getElementById('audioPlayer');
const topPlayBtn = document.getElementById('topPlayBtn');
let activeAudioBtnId = null;
let activeAudioKey = null;

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
  const dur = audioEl.duration || 0;
  const cur = audioEl.currentTime || 0;
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
  if (!track || !audioEl.duration || !isFinite(audioEl.duration) || !track.getBoundingClientRect) return;
  const rect = track.getBoundingClientRect();
  if (!rect.width) return;
  const ratio = Math.min(1, Math.max(0, (ev.clientX - rect.left) / rect.width));
  audioEl.currentTime = ratio * audioEl.duration;
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
  syncAllAudioButtonsUI(false);
}

function playOrToggleAudio(btnId, audioKey, srcUrl, fallbackB64) {
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
  audioEl.src = srcUrl || fallbackB64 || '';
  audioEl.currentTime = 0;
  syncAllAudioButtonsUI(true);
  audioEl.play().catch(() => {
    if (fallbackB64 && audioEl.src !== fallbackB64) {
      audioEl.src = fallbackB64;
      audioEl.play().catch(() => stopAllAudio());
    } else {
      stopAllAudio();
    }
  });
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
  else playAgendaByIdx(curDayNum, curGameIdx, document.getElementById('btnAgPlay_' + curDayNum + '_' + curGameIdx));
}

async function playAgendaByIdx(dayNum, agIdx, btnEl) {
  const btnId = btnEl ? btnEl.id : ('btnAgPlay_' + dayNum + '_' + agIdx);
  const audioKey = 'ag_' + dayNum + '_' + agIdx;

  if (activeAudioKey === audioKey && !audioEl.paused) {
    audioEl.pause();
    syncAllAudioButtonsUI(false);
    return;
  }
  if (activeAudioKey === audioKey && audioEl.paused && audioEl.currentTime > 0 && !audioEl.ended) {
    activeAudioBtnId = btnId;
    syncAllAudioButtonsUI(true);
    audioEl.play().catch(() => stopAllAudio());
    return;
  }

  const d = findDayObj(dayNum);
  const ag = (d && d.agendas && d.agendas[agIdx]) ? d.agendas[agIdx] : null;
  if (!ag) return;

  const fallbackB64 = (dayNum === 1 && DAY1_AG_MAP[agIdx]) ? DAY1_AG_MAP[agIdx].b64 : (d.audio_b64 || '');
  playOrToggleAudio(btnId, audioKey, ag.audio_url, fallbackB64);
}

audioEl.addEventListener('timeupdate', () => {
  if (!audioEl.paused) updateNowPlayingBar(true);
});

audioEl.addEventListener('ended', () => {
  const finishedKey = activeAudioKey;
  stopAllAudio();
  if (curView === 'slides' && autoAdvance && finishedKey && finishedKey.startsWith('slide_') && curSlideIdx < SLIDES.length - 1) {
    setTimeout(() => goToSlide(curSlideIdx + 1, true), 900);
  } else if (curView === 'plan' && finishedKey && finishedKey.startsWith('day_main_')) {
    const btnEl = document.getElementById('btnAgPlay_' + curDayNum + '_' + curGameIdx);
    playAgendaByIdx(curDayNum, curGameIdx, btnEl);
  }
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
  if ('Notification' in window && Notification.permission === 'granted') {
    if (navigator.serviceWorker && navigator.serviceWorker.ready) {
      navigator.serviceWorker.ready.then(reg => {
        reg.showNotification(title, {
          body: quote,
          icon: 'favicon.svg',
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
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.getTracks().forEach(t => t.stop());
    }
    maProfile.permsGranted = true;
    saveMaProfile();
    const permBanner = document.getElementById('permBanner');
    if (permBanner) permBanner.style.display = 'none';
    fireMorningMotivationNotification(true);
  } catch (err) {
    alert('মা, ব্রাউজারের পপ-আপে "Allow" (অনুমতি দিন) বোতামটি ছোঁও।');
  }
}
