/* ============================================================================
   MODULE 4: HEIRLOOM LETTER & MORNING INSPIRATION (💌 চিঠি — src/js/letter-view.js)
   ============================================================================ */
function pickNewRandomQuote(autoPlayAudio) {
  if (MORNING_QUOTES.length > 1) {
    let nextIdx = curQuoteIdx;
    for (let tries = 0; tries < 10 && nextIdx === curQuoteIdx; tries++) {
      nextIdx = Math.floor(Math.random() * MORNING_QUOTES.length);
    }
    if (nextIdx === curQuoteIdx) {
      nextIdx = (curQuoteIdx + 1) % MORNING_QUOTES.length;
    }
    curQuoteIdx = nextIdx;
  }
  const qEl = document.getElementById('dailyQuoteText');
  if (qEl) qEl.textContent = MORNING_QUOTES[curQuoteIdx];
  if (autoPlayAudio) {
    stopAllAudio();
    toggleMorningQuoteAudio();
  }
  return curQuoteIdx;
}

function renderSlideDots() {
  const dotsRow = document.getElementById('slideDotsRow');
  if (!dotsRow) return;
  dotsRow.innerHTML = '';
  SLIDES.forEach((s, idx) => {
    const dot = document.createElement('button');
    dot.className = 'slide-dot' + (idx === curSlideIdx ? ' active' : '');
    dot.textContent = toBnDigits(idx + 1);
    dot.setAttribute('aria-label', 'চিঠির পাতা ' + (idx + 1));
    dot.onclick = () => goToSlide(idx, false);
    dotsRow.appendChild(dot);
  });
}

function renderSlide() {
  const s = SLIDES[curSlideIdx];
  const vLink = document.getElementById('btnWatchMovieLetter');
  if (vLink && typeof LETTER_VIDEO_URL === 'string') vLink.href = LETTER_VIDEO_URL;
  const imgEl = document.getElementById('slideImg');
  if (imgEl) imgEl.src = s.img_b64;
  document.getElementById('slideBadge').textContent = s.badge;
  document.getElementById('slideTitleBn').textContent = s.title_bn;
  document.getElementById('slideHighlight').textContent = s.highlight_bn;
  document.getElementById('slideBodyBn').textContent = s.text_bn;
  document.getElementById('prevBtn').disabled = (curSlideIdx === 0);
  document.getElementById('nextBtn').disabled = (curSlideIdx === SLIDES.length - 1);
  renderSlideDots();
  syncAllAudioButtonsUI(!audioEl.paused);
}

function goToSlide(idx, autoPlay) {
  curSlideIdx = Math.max(0, Math.min(SLIDES.length - 1, idx));
  stopAllAudio();
  renderSlide();
  if (autoPlay) toggleSlideAudio();
}

function prevSlide() {
  if (curSlideIdx > 0) goToSlide(curSlideIdx - 1, true);
}

function nextSlide() {
  if (curSlideIdx < SLIDES.length - 1) goToSlide(curSlideIdx + 1, true);
}

function toggleAutoPlayAll() {
  autoAdvance = !autoAdvance;
  document.getElementById('autoAdvanceBtn').textContent = autoAdvance ? '🔁 পরপর: চালু' : '🔁 পরপর: বন্ধ';
}

/* Gentle Touch Swipe Support on Letter Card */
(function attachLetterSwipe() {
  const card = document.getElementById('letterSlideCard');
  if (!card || !card.addEventListener) return;
  let touchStartX = 0;
  let touchStartY = 0;
  card.addEventListener('touchstart', ev => {
    if (!ev.touches || !ev.touches.length) return;
    touchStartX = ev.touches[0].clientX;
    touchStartY = ev.touches[0].clientY;
  }, { passive: true });
  card.addEventListener('touchend', ev => {
    if (!ev.changedTouches || !ev.changedTouches.length) return;
    const dx = ev.changedTouches[0].clientX - touchStartX;
    const dy = ev.changedTouches[0].clientY - touchStartY;
    if (Math.abs(dx) > 56 && Math.abs(dx) > Math.abs(dy) * 1.4) {
      if (dx < 0) nextSlide();
      else prevSlide();
    }
  }, { passive: true });
})();
