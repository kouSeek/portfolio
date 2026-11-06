/* ============================================================================
   ✨ ঝলক (JHALAK) — MODULE 2: FULL-SCREEN REELS PLAYER, MULTI-SELECT CATEGORIES,
   TOP LISTEN BUTTON, RELEVANT YOUTUBE LINKS, TV TAB & SETTINGS (AUTO-REELS,
   AUTO-PLAY VOICES & CHITHI)
   ============================================================================ */

let jhActiveTab = 'reels';
let jhSelectedChannels = new Set(['all']);
let jhFilteredReels = ALL_JHALAK_REELS.slice();
let jhCurrentIdx = 0;
let jhAutoFlow = true;
let jhAutoPlayVoices = true;
let jhAudioPlaying = false;
let jhAutoAdvanceTimer = null;
let jhSlideLetterIdx = 0;
let jhObserver = null;
let jhRevealedMap = {};

try {
  const savedFlow = localStorage.getItem('ma_jhalak_auto_flow_v1');
  if (savedFlow === '0') jhAutoFlow = false;
  const savedVoice = localStorage.getItem('ma_jhalak_auto_voice_v1');
  if (savedVoice === '0') jhAutoPlayVoices = false;
} catch (e) {}

function getJhAudioEl() {
  return document.getElementById('jhAudioPlayer');
}

function stopJhAudio() {
  if (jhAutoAdvanceTimer) {
    clearTimeout(jhAutoAdvanceTimer);
    jhAutoAdvanceTimer = null;
  }
  const aud = getJhAudioEl();
  if (aud) {
    try { aud.pause(); } catch (e) {}
  }
  jhAudioPlaying = false;
  updateActiveCardPlayBtns();
}

function spawnLotusBurst(x, y, symbols) {
  if (typeof document === 'undefined' || !document.body) return;
  const icons = symbols || ['🌸', '✨', '💖', '🪷'];
  for (let i = 0; i < 5; i++) {
    const el = document.createElement('div');
    el.className = 'jh-particle-burst';
    el.textContent = icons[i % icons.length];
    const dx = (Math.random() - 0.5) * 90;
    el.style.left = Math.max(20, Math.min(window.innerWidth - 40, (x || window.innerWidth / 2) + dx)) + 'px';
    el.style.top = Math.max(60, (y || window.innerHeight * 0.65) - i * 12) + 'px';
    document.body.appendChild(el);
    setTimeout(() => {
      if (el.parentNode) el.parentNode.removeChild(el);
    }, 1150);
  }
}

/* HEADER TABS: JHALAK REELS vs TV */
function switchJhalakMainTab(tabName) {
  jhActiveTab = tabName === 'tv' ? 'tv' : 'reels';
  stopJhAudio();

  const tabReels = document.getElementById('tabJhReels');
  const tabTv = document.getElementById('tabJhTv');
  const chanStrip = document.getElementById('jhChannelStrip');
  const reelsVp = document.getElementById('jhReelsViewport');
  const tvVp = document.getElementById('jhTvViewport');

  if (tabReels) tabReels.classList.toggle('active', jhActiveTab === 'reels');
  if (tabTv) tabTv.classList.toggle('active', jhActiveTab === 'tv');
  if (chanStrip) chanStrip.style.display = jhActiveTab === 'reels' ? 'flex' : 'none';
  if (reelsVp) reelsVp.style.display = jhActiveTab === 'reels' ? 'block' : 'none';
  if (tvVp) tvVp.style.display = jhActiveTab === 'tv' ? 'block' : 'none';
}

/* MULTI-SELECT CATEGORY FILTERING */
function filterJhalakChannel(channelId) {
  const ch = channelId || 'all';
  stopJhAudio();

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

  document.querySelectorAll('.jh-chan-chip').forEach(btn => {
    const cAttr = btn.getAttribute('data-chan');
    btn.classList.toggle('active', jhSelectedChannels.has(cAttr));
  });

  if (jhSelectedChannels.has('all')) {
    jhFilteredReels = ALL_JHALAK_REELS.slice();
  } else {
    jhFilteredReels = ALL_JHALAK_REELS.filter(r =>
      jhSelectedChannels.has(r.vibe) || (jhSelectedChannels.has('music') && r.is_music)
    );
  }

  jhCurrentIdx = 0;
  renderJhalakReelStream();
  const vp = document.getElementById('jhReelsViewport');
  if (vp) vp.scrollTop = 0;
}

/* SETTINGS GEAR: AUTO-REELS, AUTO-PLAY VOICES & CHITHI */
function syncJhSettingsButtonsUI() {
  const flowBtn = document.getElementById('btnJhAutoFlow');
  if (flowBtn) {
    flowBtn.classList.toggle('active-flow', jhAutoFlow);
    flowBtn.textContent = jhAutoFlow ? '🔄 অটো-রিলস: চালু' : '🔄 অটো-রিলস: বন্ধ';
  }
  const voiceBtn = document.getElementById('btnJhAutoVoice');
  if (voiceBtn) {
    voiceBtn.classList.toggle('active-flow', jhAutoPlayVoices);
    voiceBtn.textContent = jhAutoPlayVoices ? '🔊 অটো-ভয়েস: চালু' : '🔊 অটো-ভয়েস: বন্ধ';
  }
}

function toggleJhAutoFlow() {
  jhAutoFlow = !jhAutoFlow;
  try { localStorage.setItem('ma_jhalak_auto_flow_v1', jhAutoFlow ? '1' : '0'); } catch (e) {}
  syncJhSettingsButtonsUI();
}

function toggleJhAutoVoice() {
  jhAutoPlayVoices = !jhAutoPlayVoices;
  try { localStorage.setItem('ma_jhalak_auto_voice_v1', jhAutoPlayVoices ? '1' : '0'); } catch (e) {}
  if (!jhAutoPlayVoices) stopJhAudio();
  syncJhSettingsButtonsUI();
}

function openJhalakSettingsDrawer() {
  syncJhSettingsButtonsUI();
  const modal = document.getElementById('jhSettingsDrawer');
  if (modal) modal.classList.add('open');
}

function closeJhalakSettingsDrawer() {
  const modal = document.getElementById('jhSettingsDrawer');
  if (modal) modal.classList.remove('open');
}

function toggleJhalakCuriosityBox(idx, ev) {
  const card = jhFilteredReels[idx];
  if (!card) return;
  jhRevealedMap[card.id] = !jhRevealedMap[card.id];
  const box = document.getElementById('jhCurBox_' + idx);
  if (box) {
    box.classList.toggle('revealed', !!jhRevealedMap[card.id]);
    const hint = box.querySelector('.jh-curiosity-tap-hint');
    if (hint) hint.textContent = jhRevealedMap[card.id] ? '✨ খোলা হয়েছে' : '👆 ছুঁয়ে দেখো';
  }
  if (jhRevealedMap[card.id] && ev) {
    spawnLotusBurst(ev.clientX, ev.clientY, ['🔮', '✨', '🌸']);
  }
}

function updateActiveCardPlayBtns() {
  jhFilteredReels.forEach((c, idx) => {
    const mainBtn = document.getElementById('jhMainPlay_' + idx);
    const isThisPlaying = jhAudioPlaying && idx === jhCurrentIdx;
    if (mainBtn) {
      mainBtn.classList.toggle('playing', isThisPlaying);
      mainBtn.textContent = isThisPlaying ? '⏹️ থামাও' : '🔊 শোনো';
    }
  });
}

function playReelAudioAtIndex(idx) {
  const card = jhFilteredReels[idx];
  if (!card) return;
  const aud = getJhAudioEl();
  if (!aud) return;

  if (jhAudioPlaying && jhCurrentIdx === idx) {
    stopJhAudio();
    return;
  }

  stopJhAudio();
  jhCurrentIdx = idx;
  if (!card.audio_url) return;

  aud.src = card.audio_url;
  const cutSec = Number(card.story_end) || 0;

  aud.ontimeupdate = function () {
    if (cutSec > 2 && aud.currentTime >= cutSec) {
      aud.pause();
      handleReelAudioEnded(idx);
    }
  };
  aud.onended = function () {
    handleReelAudioEnded(idx);
  };

  jhAudioPlaying = true;
  updateActiveCardPlayBtns();
  const playPromise = aud.play();
  if (playPromise && typeof playPromise.catch === 'function') {
    playPromise.catch(() => {
      jhAudioPlaying = false;
      updateActiveCardPlayBtns();
    });
  }
}

function handleReelAudioEnded(idx) {
  jhAudioPlaying = false;
  updateActiveCardPlayBtns();
  if (jhAutoFlow && idx === jhCurrentIdx && idx + 1 < jhFilteredReels.length) {
    jhAutoAdvanceTimer = setTimeout(() => {
      scrollToReelIndex(idx + 1, jhAutoPlayVoices);
    }, 1600);
  }
}

function scrollToReelIndex(targetIdx, autoPlayAfter) {
  const clamped = Math.max(0, Math.min(jhFilteredReels.length - 1, targetIdx));
  jhCurrentIdx = clamped;
  const slideEl = document.getElementById('jhSlide_' + clamped);
  if (slideEl && typeof slideEl.scrollIntoView === 'function') {
    slideEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  if (autoPlayAfter) {
    setTimeout(() => playReelAudioAtIndex(clamped), 380);
  }
}

function renderJhalakReelStream() {
  const vp = document.getElementById('jhReelsViewport');
  if (!vp) return;

  const html = jhFilteredReels.map((card, idx) => {
    const isRev = !!jhRevealedMap[card.id];
    const hasYt = Boolean(card.yt_query && String(card.yt_query).trim());
    const ytUrl = hasYt
      ? 'https://www.youtube.com/results?search_query=' + encodeURIComponent(card.yt_query)
      : '';
    const ytHtml = hasYt
      ? `<a class="jh-yt-link" href="${ytUrl}" target="_blank" rel="noopener noreferrer">▶️ ইউটিউবে দেখো: ${card.yt_label_bn || card.title_bn} ↗</a>`
      : '';

    return `
      <article id="jhSlide_${idx}" class="jh-reel-slide" data-idx="${idx}" data-vibe="${card.vibe}">
        <div class="jh-card-stage">
          <div>
            <div class="jh-card-top">
              <span class="jh-vibe-badge">${card.badge_bn}</span>
              <button id="jhMainPlay_${idx}" class="jh-top-listen-btn" onclick="playReelAudioAtIndex(${idx})">
                🔊 শোনো
              </button>
            </div>
            <h2 class="jh-hook-title">${card.title_bn}</h2>
            <div class="jh-hook-story">${card.hook_bn}</div>
            <div class="jh-hitch-ribbon">
              <div class="jh-hitch-label">${card.hitch_label_bn}</div>
              <div class="jh-hitch-text">${card.hitch_bn}</div>
            </div>
            <div id="jhCurBox_${idx}" class="jh-curiosity-box ${isRev ? 'revealed' : ''}" onclick="toggleJhalakCuriosityBox(${idx}, event)">
              <div class="jh-curiosity-q">
                <span>${card.curiosity_q_bn}</span>
                <span class="jh-curiosity-tap-hint">${isRev ? '✨ খোলা হয়েছে' : '👆 ছুঁয়ে দেখো'}</span>
              </div>
              <div class="jh-curiosity-a">${card.curiosity_a_bn}</div>
            </div>
            ${ytHtml}
          </div>
        </div>
      </article>
    `;
  }).join('');

  vp.innerHTML = html;
  setupJhalakScrollObserver();
}

function setupJhalakScrollObserver() {
  if (typeof IntersectionObserver === 'undefined') return;
  if (jhObserver) {
    try { jhObserver.disconnect(); } catch (e) {}
  }
  const vp = document.getElementById('jhReelsViewport');
  jhObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting && entry.intersectionRatio >= 0.65) {
        const idx = Number(entry.target.getAttribute('data-idx')) || 0;
        if (idx !== jhCurrentIdx) {
          stopJhAudio();
          jhCurrentIdx = idx;
          if (jhAutoPlayVoices) {
            playReelAudioAtIndex(idx);
          }
        }
      }
    });
  }, { root: vp, threshold: [0.68] });

  document.querySelectorAll('.jh-reel-slide').forEach(el => jhObserver.observe(el));
}

/* KOUSHIK'S 8-SLIDE LETTER (CHITHI — OPENED FROM SETTINGS) */
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
  const s = SLIDES[jhSlideLetterIdx] || SLIDES[0];
  if (!s) return;
  const imgEl = document.getElementById('jhLetterImg');
  const titleEl = document.getElementById('jhLetterTitle');
  const bodyEl = document.getElementById('jhLetterBody');
  if (imgEl) imgEl.src = s.img_b64 || '';
  if (titleEl) titleEl.textContent = s.title_bn;
  if (bodyEl) bodyEl.textContent = s.text_bn;
}

function stepJhalakLetterSlide(delta) {
  jhSlideLetterIdx = (jhSlideLetterIdx + delta + SLIDES.length) % SLIDES.length;
  renderJhalakLetterSlide();
}

function playJhalakLetterAudio() {
  const s = SLIDES[jhSlideLetterIdx] || SLIDES[0];
  const aud = getJhAudioEl();
  if (!aud || !s || !s.audio_url) return;
  stopJhAudio();
  aud.src = s.audio_url;
  aud.play().catch(() => {});
}

window.addEventListener('DOMContentLoaded', () => {
  syncJhSettingsButtonsUI();
  renderJhalakReelStream();
});
