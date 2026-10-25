/* ============================================================================
   MODULE 5: NAVIGATION ROUTER & PROACTIVE APPLICATION BOOTSTRAP (src/js/boot.js)
   ============================================================================ */
function switchView(mode) {
  curView = mode;
  stopAllAudio();
  document.getElementById('viewPlan').className = 'view-sec' + (mode === 'plan' ? ' active' : '');
  document.getElementById('viewSlides').className = 'view-sec' + (mode === 'slides' ? ' active' : '');
  document.getElementById('htabPlan').className = 'htab-btn' + (mode === 'plan' ? ' active' : '');
  document.getElementById('htabSlides').className = 'htab-btn' + (mode === 'slides' ? ' active' : '');

  if (mode === 'plan') {
    renderPlanView();
  } else if (mode === 'slides') {
    pickNewRandomQuote(false);
    renderSlide();
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function initMorningQuoteAndAlarm() {
  const qEl = document.getElementById('dailyQuoteText');
  if (qEl) qEl.textContent = MORNING_QUOTES[curQuoteIdx];

  const notifGranted = ('Notification' in window) && Notification.permission === 'granted';
  const permBanner = document.getElementById('permBanner');
  if (permBanner) {
    permBanner.style.display = (maProfile.permsGranted && notifGranted) ? 'none' : 'flex';
  }

  checkAndFireDailyMorningNotification();
  setInterval(checkAndFireDailyMorningNotification, 45000);
}

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('ma-sw.js').catch(() => {});
}

initMorningQuoteAndAlarm();
findInitialCurrentDay();
renderSlide();
renderPlanView();
scrollActiveDayChipIntoView();
engageProactiveWelcomeAudio();
