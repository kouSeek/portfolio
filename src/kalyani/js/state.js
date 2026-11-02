/* ============================================================================
   MODULE 1: STATE, PERSISTENCE & SEQUENTIAL PROGRESSION ENGINE (src/js/state.js)
   ============================================================================ */
const ALL_DAYS = DAYS_21.concat(DAYS_PART2_30);

const GAME_SHORT_LABELS = GAME_META.map(m => m.short_bn);
const GAME_ACCENTS = GAME_META.map(m => m.accent);

const BN_NUM_MAP = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
function toBnDigits(val) {
  return String(val).replace(/\d/g, d => BN_NUM_MAP[Number(d)]);
}

let curView = 'plan';
let curSlideIdx = 0;
let curDayNum = 1;
let curGameIdx = 0;
let showAllGamesInDay = false;
let primaryCalOpen = false;
let extCalOpen = true;
let autoAdvance = true;
let curQuoteIdx = Math.floor(Date.now() / 86400000) % MORNING_QUOTES.length;
let toastTimer = null;

let doneMap = {};
try {
  const parsedDone = JSON.parse(localStorage.getItem('ma_21day_done_v2') || '{}');
  if (parsedDone && typeof parsedDone === 'object') doneMap = parsedDone;
} catch (e) {
  doneMap = {};
}

let maProfile = {
  morningTime: '08:00',
  lastMorningNotifDate: '',
  permsGranted: false
};
try {
  const savedProf = JSON.parse(localStorage.getItem('ma_kalyani_profile_v1') || 'null');
  if (savedProf && typeof savedProf === 'object') {
    maProfile = Object.assign(maProfile, savedProf);
  }
} catch (e) {}

function saveMaProfile() {
  try { localStorage.setItem('ma_kalyani_profile_v1', JSON.stringify(maProfile)); } catch (e) {}
}

function saveDoneMap() {
  try { localStorage.setItem('ma_21day_done_v2', JSON.stringify(doneMap)); } catch (e) {}
}

function showCelebrationToast(msg) {
  const toastEl = document.getElementById('celebrationToast');
  if (!toastEl) return;
  toastEl.textContent = msg;
  toastEl.classList.add('show');
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toastEl.classList.remove('show');
  }, 3000);
}

function findDayObj(dayNum) {
  return ALL_DAYS.find(x => x.day === dayNum) || DAYS_21[0];
}

function isDayFullyDone(dayNum) {
  const d = findDayObj(dayNum);
  const count = d ? d.agendas.length : 6;
  for (let i = 0; i < count; i++) {
    if (!doneMap[dayNum + '_' + i]) return false;
  }
  return true;
}

function isDayUnlocked(dayNum) {
  if (dayNum <= 1) return true;
  for (let k = 1; k < dayNum; k++) {
    if (!isDayFullyDone(k)) return false;
  }
  return true;
}

function areFirst21DaysComplete() {
  for (let i = 0; i < DAYS_21.length; i++) {
    if (!isDayFullyDone(DAYS_21[i].day)) return false;
  }
  return true;
}

function getHighestUnlockedDay() {
  for (let i = 0; i < ALL_DAYS.length; i++) {
    const d = ALL_DAYS[i];
    if (!isDayFullyDone(d.day)) return d.day;
  }
  return ALL_DAYS[ALL_DAYS.length - 1].day;
}

function getNextOpenGameIdx(dayNum) {
  const d = findDayObj(dayNum);
  const count = (d && d.agendas) ? d.agendas.length : 0;
  if (count <= 0) return 0;

  let latestDoneIdx = -1;
  for (let i = 0; i < count; i++) {
    if (doneMap[dayNum + '_' + i]) latestDoneIdx = i;
  }

  for (let i = latestDoneIdx + 1; i < count; i++) {
    if (!doneMap[dayNum + '_' + i]) return i;
  }

  for (let i = 0; i <= latestDoneIdx; i++) {
    if (!doneMap[dayNum + '_' + i]) return i;
  }

  return 0;
}

const getFirstIncompleteGameIdx = getNextOpenGameIdx;

function findInitialCurrentDay() {
  curDayNum = getHighestUnlockedDay();
  curGameIdx = getNextOpenGameIdx(curDayNum);
  showAllGamesInDay = false;
}

function scrollActiveDayChipIntoView() {
  const activeChip = document.getElementById('dayChip_' + curDayNum) || document.getElementById('calCell_' + curDayNum);
  if (activeChip && typeof activeChip.scrollIntoView === 'function') {
    activeChip.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
  }
}
