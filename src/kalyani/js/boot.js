/* ============================================================================
   MODULE 5: NAVIGATION ROUTER & PROACTIVE APPLICATION BOOTSTRAP (src/js/boot.js)
   ============================================================================ */
function switchView(mode) {
  curView = mode;
  stopAllAudio();
  if (typeof stopActiveVoiceAndVideoCapture === 'function') stopActiveVoiceAndVideoCapture();
  document.getElementById('viewPlan').className = 'view-sec' + (mode === 'plan' ? ' active' : '');
  document.getElementById('viewSlides').className = 'view-sec' + (mode === 'slides' ? ' active' : '');
  const tvSec = document.getElementById('viewTv');
  if (tvSec) tvSec.className = 'view-sec' + (mode === 'tv' ? ' active' : '');
  document.getElementById('htabPlan').className = 'htab-btn' + (mode === 'plan' ? ' active' : '');
  document.getElementById('htabSlides').className = 'htab-btn' + (mode === 'slides' ? ' active' : '');
  const htabTv = document.getElementById('htabTv');
  if (htabTv) htabTv.className = 'htab-btn' + (mode === 'tv' ? ' active' : '');

  if (mode === 'plan') {
    renderPlanView();
    if (autoVoicePlay) toggleDayOverviewAudio();
  } else if (mode === 'slides') {
    pickNewRandomQuote(false);
    renderSlide();
    if (autoVoicePlay) toggleSlideAudio();
  } else if (mode === 'tv' && typeof renderTvView === 'function') {
    renderTvView();
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function initMorningQuote() {
  const qEl = document.getElementById('dailyQuoteText');
  if (qEl) qEl.textContent = MORNING_QUOTES[curQuoteIdx];
}

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('kalyani-sw.js').catch(() => {});
}

let _screenWakeLock = null;
let _screenWakeLockPending = false;

async function requestScreenWakeLock() {
  try {
    if (typeof navigator === 'undefined' || !navigator.wakeLock || typeof navigator.wakeLock.request !== 'function') {
      return null;
    }
    if (typeof document !== 'undefined' && document.visibilityState === 'hidden') {
      return null;
    }
    if (_screenWakeLock && !_screenWakeLock.released) {
      return _screenWakeLock;
    }
    if (_screenWakeLockPending) {
      return _screenWakeLock;
    }
    _screenWakeLockPending = true;
    const sentinel = await navigator.wakeLock.request('screen');
    _screenWakeLock = sentinel || { released: false };
    _screenWakeLockPending = false;
    if (typeof window !== 'undefined') {
      window._screenWakeLock = _screenWakeLock;
    }
    if (sentinel && typeof sentinel.addEventListener === 'function') {
      sentinel.addEventListener('release', () => {
        if (_screenWakeLock === sentinel) {
          _screenWakeLock = null;
        }
      });
    }
    return _screenWakeLock;
  } catch (e) {
    _screenWakeLockPending = false;
    return null;
  }
}

(function initScreenWakeLock() {
  requestScreenWakeLock();
  if (typeof document !== 'undefined' && typeof document.addEventListener === 'function') {
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState !== 'hidden') {
        requestScreenWakeLock();
      }
    });
    ['touchstart', 'pointerdown', 'click', 'keydown'].forEach(evName => {
      document.addEventListener(evName, () => {
        if (!_screenWakeLock || _screenWakeLock.released) {
          requestScreenWakeLock();
        }
      }, { passive: true });
    });
  }
  if (typeof window !== 'undefined' && typeof window.addEventListener === 'function') {
    window.addEventListener('focus', () => requestScreenWakeLock());
    window.addEventListener('pageshow', () => requestScreenWakeLock());
  }
  if (typeof setInterval === 'function') {
    const _wlTimer = setInterval(() => {
      if (typeof document === 'undefined' || document.visibilityState !== 'hidden') {
        if (!_screenWakeLock || _screenWakeLock.released) {
          requestScreenWakeLock();
        }
      }
    }, 25000);
    if (_wlTimer && typeof _wlTimer.unref === 'function') _wlTimer.unref();
  }
})();

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

initMorningQuote();
findInitialCurrentDay();
renderSlide();
if (typeof renderKoushikAdminPanel === 'function') renderKoushikAdminPanel();
if (typeof renderTvView === 'function') renderTvView();
renderPlanView();
scrollActiveDayChipIntoView();
engageProactiveWelcomeAudio();
