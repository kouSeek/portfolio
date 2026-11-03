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
  function apply() {
    try {
      if (!document.head || typeof document.createElement !== 'function') return;
      const el = document.getElementById('pageFavicon');
      if (!el || !el.getAttribute) return;
      const emoji = el.getAttribute('data-emoji') || '';
      const b64 = el.getAttribute('data-png-b64') || '';
      const httpsPng = el.getAttribute('data-https-png') || b64;
      const httpsIco = el.getAttribute('data-https-ico') || httpsPng;
      const useHttps = (typeof location !== 'undefined' && /^https?:$/i.test(location.protocol) && (typeof navigator === 'undefined' || navigator.onLine !== false));
      const pngHref = useHttps ? httpsPng : (b64 || httpsPng);
      const icoHref = useHttps ? httpsIco : (b64 || httpsIco);
      document.querySelectorAll('link[rel*="icon"]').forEach(n => { if (n.parentNode) n.parentNode.removeChild(n); });
      const l1 = document.createElement('link');
      l1.id = 'pageFavicon';
      l1.setAttribute('data-emoji', emoji);
      l1.setAttribute('data-png-b64', b64);
      l1.setAttribute('data-https-png', httpsPng);
      l1.setAttribute('data-https-ico', httpsIco);
      l1.rel = 'icon'; l1.type = 'image/png'; l1.sizes = '64x64'; l1.href = pngHref;
      document.head.appendChild(l1);
      const l2 = document.createElement('link');
      l2.rel = 'shortcut icon'; l2.type = useHttps ? 'image/x-icon' : 'image/png'; l2.href = icoHref;
      document.head.appendChild(l2);
      const l3 = document.createElement('link');
      l3.rel = 'apple-touch-icon'; l3.sizes = '64x64'; l3.href = b64 || pngHref;
      document.head.appendChild(l3);
    } catch (e) {}
  }
  apply();
  if (typeof setTimeout === 'function') setTimeout(apply, 90);
})();

initMorningQuoteAndAlarm();
findInitialCurrentDay();
renderSlide();
renderPlanView();
scrollActiveDayChipIntoView();
engageProactiveWelcomeAudio();
