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
    toggleDayOverviewAudio();
  } else if (mode === 'slides') {
    pickNewRandomQuote(false);
    renderSlide();
    toggleSlideAudio();
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
  navigator.serviceWorker.register('kalyani-sw.js').catch(() => {});
}

(function hydratePageFavicon() {
  try {
    if (!document.head || typeof document.createElement !== 'function') return;
    const el = document.getElementById('pageFavicon');
    if (!el) return;
    const emoji = el.getAttribute && el.getAttribute('data-emoji');
    let uri = el.getAttribute ? el.getAttribute('href') : el.href;
    let mime = 'image/svg+xml';
    if (emoji) {
      const c = document.createElement('canvas');
      c.width = 64; c.height = 64;
      const ctx = c.getContext && c.getContext('2d');
      if (ctx) {
        ctx.font = '54px "Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(emoji, 32, 35);
        uri = c.toDataURL('image/png');
        mime = 'image/png';
      }
    }
    if (!uri) return;
    document.querySelectorAll('link[rel*="icon"]').forEach(n => { if (n.parentNode) n.parentNode.removeChild(n); });
    ['icon', 'shortcut icon', 'apple-touch-icon'].forEach(rel => {
      const lk = document.createElement('link');
      if (rel === 'icon') { lk.id = 'pageFavicon'; if (emoji) lk.setAttribute('data-emoji', emoji); }
      lk.rel = rel;
      if (rel !== 'apple-touch-icon') lk.type = mime;
      lk.href = uri;
      document.head.appendChild(lk);
    });
  } catch (e) {}
})();

initMorningQuoteAndAlarm();
findInitialCurrentDay();
renderSlide();
renderPlanView();
scrollActiveDayChipIntoView();
engageProactiveWelcomeAudio();
