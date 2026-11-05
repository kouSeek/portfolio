/* ============================================================================
   ✨ ঝলক (JHALAK) — MODULE 2: FULL-SCREEN REELS PLAYER, AUTO-FLOW BIOSCOPE,
   1-TAP CURIOSITY FLIP, WALKIE-TALKIE GEMINI STUDIO & LETTER/TV DRAWER
   ============================================================================ */

let jhActiveChannel = 'all';
let jhFilteredReels = ALL_JHALAK_REELS.slice();
let jhCurrentIdx = 0;
let jhAutoFlow = true;
let jhAudioPlaying = false;
let jhAutoAdvanceTimer = null;
let jhSlideLetterIdx = 0;
let jhObserver = null;
let jhMediaRecorder = null;
let jhRecordedChunks = [];

let jhLikedMap = {};
try {
  jhLikedMap = JSON.parse(localStorage.getItem('ma_jhalak_liked_v1') || '{}') || {};
} catch (e) {
  jhLikedMap = {};
}

let jhRevealedMap = {};

function saveJhLikedMap() {
  try { localStorage.setItem('ma_jhalak_liked_v1', JSON.stringify(jhLikedMap)); } catch (e) {}
}

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

function filterJhalakChannel(channelId) {
  jhActiveChannel = channelId || 'all';
  stopJhAudio();
  document.querySelectorAll('.jh-chan-chip').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-chan') === jhActiveChannel);
  });
  if (jhActiveChannel === 'all') {
    jhFilteredReels = ALL_JHALAK_REELS.slice();
  } else {
    jhFilteredReels = ALL_JHALAK_REELS.filter(r => r.vibe === jhActiveChannel);
  }
  jhCurrentIdx = 0;
  renderJhalakReelStream();
  const vp = document.getElementById('jhReelsViewport');
  if (vp) vp.scrollTop = 0;
}

function shuffleJhalakFeed(ev) {
  if (ev) spawnLotusBurst(ev.clientX, ev.clientY, ['🎲', '✨', '🌸']);
  stopJhAudio();
  const copy = jhFilteredReels.slice();
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const tmp = copy[i];
    copy[i] = copy[j];
    copy[j] = tmp;
  }
  jhFilteredReels = copy;
  jhCurrentIdx = 0;
  renderJhalakReelStream();
  const vp = document.getElementById('jhReelsViewport');
  if (vp) vp.scrollTop = 0;
  setTimeout(() => playReelAudioAtIndex(0), 120);
}

function toggleJhAutoFlow() {
  jhAutoFlow = !jhAutoFlow;
  const btn = document.getElementById('btnJhAutoFlow');
  if (btn) {
    btn.classList.toggle('active-flow', jhAutoFlow);
    btn.textContent = jhAutoFlow ? '🎧 অটো-রিলস: চালু' : '🎧 অটো-রিলস: বন্ধ';
  }
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

function toggleJhalakLike(idx, ev) {
  const card = jhFilteredReels[idx];
  if (!card) return;
  jhLikedMap[card.id] = !jhLikedMap[card.id];
  saveJhLikedMap();
  const btn = document.getElementById('jhLikeBtn_' + idx);
  if (btn) {
    btn.classList.toggle('liked', !!jhLikedMap[card.id]);
    const ic = btn.querySelector('.ic');
    if (ic) ic.textContent = jhLikedMap[card.id] ? '❤️' : '🤍';
  }
  if (jhLikedMap[card.id] && ev) {
    spawnLotusBurst(ev.clientX, ev.clientY, ['❤️', '🌸', '🪷', '✨']);
  }
}

function updateActiveCardPlayBtns() {
  jhFilteredReels.forEach((c, idx) => {
    const mainBtn = document.getElementById('jhMainPlay_' + idx);
    const railBtn = document.getElementById('jhRailPlay_' + idx);
    const isThisPlaying = jhAudioPlaying && idx === jhCurrentIdx;
    if (mainBtn) {
      mainBtn.classList.toggle('playing', isThisPlaying);
      mainBtn.textContent = isThisPlaying ? '⏹️ কণ্ঠ থামাও' : '🔊 এই ঝলকটি শোনো';
    }
    if (railBtn) {
      const ic = railBtn.querySelector('.ic');
      const lbl = railBtn.querySelector('.lbl');
      if (ic) ic.textContent = isThisPlaying ? '⏹️' : '🔊';
      if (lbl) lbl.textContent = isThisPlaying ? 'থামাও' : 'শোনো';
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
      scrollToReelIndex(idx + 1, true);
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

  const total = jhFilteredReels.length;
  const html = jhFilteredReels.map((card, idx) => {
    const isLiked = !!jhLikedMap[card.id];
    const isRev = !!jhRevealedMap[card.id];
    const ytUrl = 'https://www.youtube.com/results?search_query=' + encodeURIComponent(card.yt_query || card.title_bn);
    return `
      <article id="jhSlide_${idx}" class="jh-reel-slide" data-idx="${idx}" data-vibe="${card.vibe}">
        <div class="jh-card-stage">
          <div>
            <div class="jh-card-top">
              <span class="jh-vibe-badge">${card.badge_bn}</span>
              <span class="jh-card-num">ঝলক ${jhBnNum(idx + 1)} / ${jhBnNum(total)}</span>
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
          </div>

          <div class="jh-audio-strip">
            <button id="jhMainPlay_${idx}" class="jh-main-listen-btn" onclick="playReelAudioAtIndex(${idx})">
              🔊 এই ঝলকটি শোনো
            </button>
            <button class="jh-next-inline-btn" onclick="scrollToReelIndex(${idx + 1}, true)">
              পরের ঝলক ⬇️
            </button>
          </div>

          <aside class="jh-right-rail" aria-label="ঝলক অ্যাকশন">
            <button id="jhRailPlay_${idx}" class="jh-rail-btn" onclick="playReelAudioAtIndex(${idx})">
              <span class="ic">🔊</span>
              <span class="lbl">শোনো</span>
            </button>
            <button id="jhLikeBtn_${idx}" class="jh-rail-btn ${isLiked ? 'liked' : ''}" onclick="toggleJhalakLike(${idx}, event)">
              <span class="ic">${isLiked ? '❤️' : '🤍'}</span>
              <span class="lbl">ভালো</span>
            </button>
            <a class="jh-rail-btn" href="${ytUrl}" target="_blank" rel="noopener noreferrer" onclick="stopJhAudio()">
              <span class="ic">🎬</span>
              <span class="lbl">ভিডিও</span>
            </a>
            <button class="jh-rail-btn" onclick="openJhalakVoiceDrawer(${idx})">
              <span class="ic">🎤</span>
              <span class="lbl">কল্যাণী</span>
            </button>
            <button class="jh-rail-btn" onclick="scrollToReelIndex(${idx + 1}, true)">
              <span class="ic">⬇️</span>
              <span class="lbl">পরের</span>
            </button>
          </aside>
        </div>
      </article>
    `;
  }).join('');

  vp.innerHTML = html;
  setupJhalakIntersectionObserver();
}

function setupJhalakIntersectionObserver() {
  if (typeof IntersectionObserver === 'undefined') return;
  if (jhObserver) jhObserver.disconnect();
  const vp = document.getElementById('jhReelsViewport');
  jhObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting && entry.intersectionRatio >= 0.65) {
        const idx = Number(entry.target.getAttribute('data-idx')) || 0;
        if (idx !== jhCurrentIdx) {
          stopJhAudio();
          jhCurrentIdx = idx;
          if (jhAutoFlow) {
            playReelAudioAtIndex(idx);
          }
        }
      }
    });
  }, { root: vp, threshold: [0.68] });

  document.querySelectorAll('.jh-reel-slide').forEach(el => jhObserver.observe(el));
}

/* WALKIE-TALKIE VOICE/VIDEO DRAWER */
function openJhalakVoiceDrawer(idx) {
  stopJhAudio();
  const card = jhFilteredReels[idx] || jhFilteredReels[jhCurrentIdx];
  const modal = document.getElementById('jhVoiceDrawer');
  const ctxTitle = document.getElementById('jhVoiceCardTitle');
  if (ctxTitle && card) ctxTitle.textContent = card.title_bn;
  if (modal) modal.classList.add('open');
}

function closeJhalakVoiceDrawer() {
  const modal = document.getElementById('jhVoiceDrawer');
  if (modal) modal.classList.remove('open');
}

async function sendQuickGreetingToKalyani() {
  const statusEl = document.getElementById('jhWtReplyBox');
  const card = jhFilteredReels[jhCurrentIdx] || ALL_JHALAK_REELS[0];
  if (!statusEl) return;
  const apiKey = (typeof localStorage !== 'undefined' && localStorage.getItem('ma_kalyani_gemini_key_v1')) || '';
  if (!apiKey) {
    statusEl.innerHTML = '🌸 <strong>কল্যাণী:</strong> মা, তোমার কথা শুনে আমার মনটা আনন্দে ভরে গেল! এই গল্পটা সত্যিই খুব মিষ্টি—তুমি একদম নিজের আনন্দে থাকো মা, আমি সবসময় তোমার পাশে আছি।';
    return;
  }
  statusEl.innerHTML = '🔴 <strong>কল্যাণী (জেমিনি) তোমার জন্য উত্তর সাজাচ্ছে...</strong>';
  try {
    const resp = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=' + encodeURIComponent(apiKey), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{
          role: 'user',
          parts: [{
            text: KALYANI_SYSTEM_PROMPT + '\n\nমা এখন এই রিলস কার্ডটি দেখছেন: ' + card.title_bn + ' — ' + card.hook_bn + '\nমাকে ৩-৪টি অত্যন্ত স্নেহময়, সহজ ঘরোয়া বাংলা বাক্যে আনন্দ ও উৎসাহ দাও।'
          }]
        }]
      })
    });
    const data = await resp.json();
    const reply = (((data.candidates || [])[0] || {}).content || {}).parts?.[0]?.text || 'মা, তুমি সবসময় আনন্দে আর আরামে থাকো!';
    statusEl.innerHTML = '✨ <strong>জেমিনি (কল্যাণী) বলছে:</strong><br>' + reply;
  } catch (e) {
    statusEl.innerHTML = '🌸 <strong>কল্যাণী:</strong> মা, আজকের এই গল্পটা ভীষণ সুন্দর—তুমি আরাম করে বসে উপভোগ করো!';
  }
}

/* KOUSHIK'S 8-SLIDE LETTER & TV DRAWER */
function openJhalakLetterDrawer() {
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
  renderJhalakReelStream();
});
