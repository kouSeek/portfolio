/* ============================================================================
   MODULE 1: STATE, PERSISTENCE & SEQUENTIAL PROGRESSION ENGINE (src/js/state.js)
   ============================================================================ */
const ALL_DAYS = DAYS_21;

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
let autoAdvance = true;
let autoVoicePlay = true;
try {
  const savedAutoVoice = localStorage.getItem('ma_kalyani_auto_voice_v1');
  if (savedAutoVoice === 'false') autoVoicePlay = false;
  else if (savedAutoVoice === 'true') autoVoicePlay = true;
} catch (e) {}

function saveAutoVoicePlay() {
  try { localStorage.setItem('ma_kalyani_auto_voice_v1', autoVoicePlay ? 'true' : 'false'); } catch (e) {}
}

let radioAutoPlay = true;
let storyOnlyAudio = true;
let unlockAllDaysMode = true;
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

let kalyaniThreads = {};
try {
  const parsedThreads = JSON.parse(localStorage.getItem('ma_kalyani_threads_v1') || '{}');
  if (parsedThreads && typeof parsedThreads === 'object') kalyaniThreads = parsedThreads;
} catch (e) {
  kalyaniThreads = {};
}

function saveKalyaniThreads() {
  try { localStorage.setItem('ma_kalyani_threads_v1', JSON.stringify(kalyaniThreads)); } catch (e) {}
}

let kalyaniMemoryNotes = [];
try {
  const parsedMem = JSON.parse(localStorage.getItem('ma_kalyani_memory_v1') || '[]');
  if (Array.isArray(parsedMem)) kalyaniMemoryNotes = parsedMem;
} catch (e) {
  kalyaniMemoryNotes = [];
}

function addKalyaniMemoryNote(note) {
  if (!note || typeof note !== 'string') return;
  const trimmed = note.trim();
  if (!trimmed || kalyaniMemoryNotes.includes(trimmed)) return;
  kalyaniMemoryNotes.push(trimmed);
  if (kalyaniMemoryNotes.length > 60) kalyaniMemoryNotes = kalyaniMemoryNotes.slice(-60);
  try { localStorage.setItem('ma_kalyani_memory_v1', JSON.stringify(kalyaniMemoryNotes)); } catch (e) {}
  appendMaWikiEntry('agent_pattern_log', trimmed, '');
}

const DEFAULT_MA_WIKI_PAGES = [
  {
    id: 'mind_and_mood',
    title_bn: 'মন ও মেজাজের ধরণ',
    icon: '🌸',
    tags: ['#মন', '#আরাম', '#রেডিও-মোড'],
    entries: [
      'মা কোনো নির্দেশ বা পরীক্ষার চাপ ছাড়া একদম নিজের ছন্দে [[রেডিও মোড]]-এ গল্প ও গান শুনতে ভালোবাসেন।',
      'হঠাৎ “এটা চাও না ওটা চাও?” জিজ্ঞেস করলে মা ধাঁধায় পড়ে যান; তাই কল্যাণী নিজে থেকেই মায়ের জন্য সবচেয়ে ভালো ও আরামের প্রস্তাবটি এগিয়ে দেয়।',
      'বিছানায় শুয়ে বা বসে বিনা চেষ্টায় [[হাসি, ভগবান ও প্রিয় গল্প]] শুনলে মায়ের মন নিমেষে শান্ত ও প্রফুল্ল হয়ে ওঠে।'
    ]
  },
  {
    id: 'joy_gods_and_stories',
    title_bn: 'হাসি, ভগবান ও প্রিয় গল্প',
    icon: '🪷',
    tags: ['#হাসি', '#ভগবান', '#রাজা', '#পশুপাখি'],
    entries: [
      'মা নিষ্পাপ ও শিশুর মতো নির্মল হাসির গল্প যেমন [[গোপাল ভাঁড় ও রাজা কৃষ্ণচন্দ্র]], বীরবল এবং তেনালি রামের মজার কাহিনী ভীষণ ভালোবাসেন।',
      'ভগবানের মিষ্টি ও স্নেহময় লীলা—বিশেষ করে [[ননীচোরা বালগোপাল]], কৈলাসে [[ভোলানাথ ও গণেশ]], [[পুরীর জগন্নাথদেব]] ও [[মা সারদা ও ঠাকুর]]-এর ঘরোয়া অমৃতকথা মায়ের খুব প্রিয়।',
      'মা যুদ্ধ, মারামারি বা রক্তপাত একদম পছন্দ করেন না—তাই রামায়ণ বা মহাভারতের যুদ্ধের গল্প মায়ের ভালো লাগে না।',
      'আদুরে পশুপাখি যেমন ছোট্ট হাতির ছানা, সমুদ্রের ভোঁদড় ছানা, কাঠবিড়ালি, গাইগরু-বাছুর ও পোষা টিয়াপাখির মিষ্টি গল্পে মা খুব আনন্দ পান।'
    ]
  },
  {
    id: 'food_and_preferences',
    title_bn: 'খাবার ও নিজের পছন্দ',
    icon: '🍲',
    tags: ['#খাবার', '#স্বাধীনতা', '#পছন্দ'],
    entries: [
      'মা ডিম, সয়াবিন ও মাশরুম একদম পছন্দ করেন না এবং ডাল বা পনির খেতেও বিশেষ ভালোবাসেন না।',
      'তাজা ফল, ভালো মাছের পদ, ছানার রান্না ও মিষ্টি ঘরোয়া বাঙালি খাবার মায়ের প্রিয়।',
      'কে কী ভাববে সেই দ্বিধা ছেড়ে মা যাতে নিজের খাবারের পছন্দ ও প্রয়োজনের কথা [[কথাবার্তা ও ভাষা]]-য় খোলাখুলি বলেন, কল্যাণী সবসময় সেই সাহস জোগায়।'
    ]
  },
  {
    id: 'ranaghat_and_memories',
    title_bn: 'রানাঘাট ও সোনালী স্মৃতি',
    icon: '🏡',
    tags: ['#রানাঘাট', '#পরিবার', '#স্মৃতি'],
    entries: [
      'নদিয়া জেলার রানাঘাটের শৈশব, স্কুলজীবনের বান্ধবী এবং শরতের দুর্গাপুজোর সকাল মায়ের মনের সোনালী আশ্রয়।',
      'কৌশিক ও দিদিকে (কঙ্কনা) স্নেহে মানুষ করার গর্ব এবং আয়ুষ ও ঐশীর মিষ্টি মুখ মায়ের প্রাণের আনন্দ।',
      '২০১৬ সালের পর বাবার অভাব ও মনের জমে থাকা কথাগুলো হালকা করে মা এখন শান্ত ও রাজকীয় সম্মানে জীবন উপভোগ করছেন।'
    ]
  },
  {
    id: 'language_and_voice',
    title_bn: 'কথাবার্তা ও ভাষা',
    icon: '🗣️',
    tags: ['#ইংরেজি', '#হিন্দি-আড্ডা', '#স্পষ্ট-বাংলা'],
    entries: [
      'রোজকার সহজ ইংরেজি শব্দ (Comfortable, Peaceful, Actually, Prefer, Choice, Definitely, Relax, Manage) খেলার ছলে নিজের মতো শোনা ও বলা।',
      'হায়দরাবাদে বা বাইরে প্রতিবেশীদের সাথে মিষ্টি ঘরোয়া হিন্দিতে গল্পগুজব (গপশপ) করার আনন্দ।',
      'অভিমান না করে নিজের বিশ্রাম, খাবার বা মনের ইচ্ছে সোজাসুজি স্পষ্ট বাংলায় প্রকাশ করা।'
    ]
  },
  {
    id: 'comfort_and_wellbeing',
    title_bn: 'শরীর ও আরাম',
    icon: '🌿',
    tags: ['#আরাম', '#বিশ্রাম', '#স্বাস্থ্য'],
    entries: [
      'হাঁটাচলার আরামের জন্য কৌশিক মায়ের পায়ের আর্চ-সাপোর্ট (Skechers Arch Support) জুতো এনে দিয়েছে এবং ঘরে ২৫–২৬ ডিগ্রি আরামদায়ক তাপমাত্রা বজায় থাকে।',
      'সামান্য দু-টাকার তলানি বা লেবুর তিতো খোসা নিংড়ানোর খাটনি ছেড়ে মায়ের শরীরের আরাম ও বিশ্রামই সবার আগে।'
    ]
  },
  {
    id: 'agent_pattern_log',
    title_bn: 'আজকের এজেন্ট ডায়েরি ও প্যাটার্ন',
    icon: '🧠',
    tags: ['#এজেন্ট-লার্নিং', '#প্যাটার্ন'],
    entries: [
      'কল্যাণী এজেন্ট মায়ের প্রতিটি ভালো লাগা, গল্প শোনা ও ভয়েস মেসেজ থেকে নিজে থেকেই শিখে মায়ের মনের মতো নতুন গল্প সাজিয়ে দেয়।'
    ]
  }
];

let kalyaniWikiVault = {
  activePageId: 'joy_gods_and_stories',
  patternScores: { comedy: 5, gods: 5, animals: 5, music: 4, reminiscence: 4 },
  dynamicCards: {},
  pages: JSON.parse(JSON.stringify(DEFAULT_MA_WIKI_PAGES))
};

try {
  const savedWiki = JSON.parse(localStorage.getItem('ma_kalyani_wiki_vault_v1') || 'null');
  if (savedWiki && typeof savedWiki === 'object' && Array.isArray(savedWiki.pages) && savedWiki.pages.length > 0) {
    kalyaniWikiVault = Object.assign(kalyaniWikiVault, savedWiki);
  }
} catch (e) {}

function saveKalyaniWikiVault() {
  try { localStorage.setItem('ma_kalyani_wiki_vault_v1', JSON.stringify(kalyaniWikiVault)); } catch (e) {}
}

function appendMaWikiEntry(pageId, entryBn, boostTopic) {
  if (!entryBn || typeof entryBn !== 'string') return;
  const clean = entryBn.replace(/[*#`]/g, '').trim();
  if (!clean) return;
  const targetId = pageId || 'agent_pattern_log';
  let page = (kalyaniWikiVault.pages || []).find(p => p.id === targetId);
  if (!page) {
    page = kalyaniWikiVault.pages[kalyaniWikiVault.pages.length - 1];
  }
  if (page && Array.isArray(page.entries) && !page.entries.includes(clean)) {
    page.entries.unshift(clean);
    if (page.entries.length > 25) page.entries = page.entries.slice(0, 25);
  }
  if (boostTopic && kalyaniWikiVault.patternScores && typeof kalyaniWikiVault.patternScores[boostTopic] === 'number') {
    kalyaniWikiVault.patternScores[boostTopic] += 1;
  }
  saveKalyaniWikiVault();
}

function recordMaBehaviorSignal(signalType, detailBn, boostTopic) {
  if (boostTopic && kalyaniWikiVault.patternScores && typeof kalyaniWikiVault.patternScores[boostTopic] === 'number') {
    kalyaniWikiVault.patternScores[boostTopic] += 1;
  }
  if (detailBn) {
    appendMaWikiEntry('agent_pattern_log', detailBn, '');
  } else {
    saveKalyaniWikiVault();
  }
}

function buildMaWikiContextMarkdown() {
  const scores = kalyaniWikiVault.patternScores || {};
  const lines = [
    '=== MA\'S LIVING OBSIDIAN-STYLE LLM WIKI (KALYANI CONNECTOME) ===',
    'Pattern Affinity Scores: ' + JSON.stringify(scores)
  ];
  (kalyaniWikiVault.pages || []).forEach(p => {
    lines.push('## [[' + p.title_bn + ']] (' + p.id + ')');
    (p.entries || []).slice(0, 6).forEach(e => {
      lines.push('- ' + e);
    });
  });
  return lines.join('\n');
}

function getTopMaInterestTheme() {
  const sc = kalyaniWikiVault.patternScores || { comedy: 5, gods: 5, animals: 5 };
  let bestKey = 'comedy';
  let bestVal = -1;
  ['comedy', 'gods', 'animals', 'music', 'reminiscence'].forEach(k => {
    if ((sc[k] || 0) > bestVal) {
      bestVal = sc[k] || 0;
      bestKey = k;
    }
  });
  return bestKey;
}

const vnAudioCache = {};
let vnLiveCamState = {
  active: false,
  dayNum: 0,
  agIdx: -1,
  facingMode: 'environment',
  lastFrameB64: ''
};
let vnRecordingState = {
  active: false,
  sending: false,
  dayNum: 0,
  agIdx: -1,
  seconds: 0,
  liveTranscript: '',
  errorMsg: ''
};

let delightLikedMap = {};
try {
  const parsedDelight = JSON.parse(localStorage.getItem('ma_kalyani_delight_liked_v1') || '{}');
  if (parsedDelight && typeof parsedDelight === 'object') delightLikedMap = parsedDelight;
} catch (e) {
  delightLikedMap = {};
}

function saveDelightLikedMap() {
  try { localStorage.setItem('ma_kalyani_delight_liked_v1', JSON.stringify(delightLikedMap)); } catch (e) {}
}

function getGeminiApiKey() {
  try { return (localStorage.getItem('ma_kalyani_gemini_key_v1') || '').trim(); } catch (e) { return ''; }
}

function saveGeminiApiKey(rawKey) {
  const clean = String(rawKey || '').trim();
  try {
    if (clean) localStorage.setItem('ma_kalyani_gemini_key_v1', clean);
  } catch (e) {}
  return clean;
}

function clearGeminiApiKey() {
  try {
    if (typeof localStorage.removeItem === 'function') {
      localStorage.removeItem('ma_kalyani_gemini_key_v1');
    } else {
      localStorage.setItem('ma_kalyani_gemini_key_v1', '');
    }
  } catch (e) {}
}

function hydrateGeminiKeyFromUrl() {
  try {
    if (typeof window === 'undefined' || !window.location) return;
    const href = String(window.location.href || '');
    const m = href.match(/[?#&](?:key|gemini_key)=([A-Za-z0-9_-]{20,})/);
    if (m && m[1]) {
      saveGeminiApiKey(m[1]);
    }
  } catch (e) {}
}
hydrateGeminiKeyFromUrl();

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
  if (unlockAllDaysMode) return true;
  if (dayNum <= 1) return true;
  for (let k = 1; k < dayNum; k++) {
    if (!isDayFullyDone(k)) return false;
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
