/* ============================================================================
   MODULE 3: DAILY 6-GAME VIEW CONTROLLER, SEQUENTIAL LOCK & CALENDAR GRIDS
   (🎓 আজকের খেলা — src/js/plan-view.js)
   ============================================================================ */
function togglePrimaryCalendarGrid() {
  primaryCalOpen = !primaryCalOpen;
  renderPlanView();
}

function selectDay(dayNum, autoPlayAudio) {
  if (!isDayUnlocked(dayNum)) {
    const frontier = getHighestUnlockedDay();
    showCelebrationToast('🔒 মা, আগে ‘দিন ' + toBnDigits(frontier) + '’-এর সবকটা খেলায় টিক (✅) দাও—তাহলেই নতুন দিনের চমক খুলে যাবে!');
    return false;
  }
  if (typeof stopActiveVoiceAndVideoCapture === 'function') stopActiveVoiceAndVideoCapture();
  curDayNum = dayNum;
  curGameIdx = getNextOpenGameIdx(dayNum);
  primaryCalOpen = false;
  stopAllAudio();
  renderPlanView();
  scrollActiveDayChipIntoView();
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if (autoPlayAudio && autoVoicePlay) toggleDayOverviewAudio();
  return true;
}

function selectGame(gIdx, autoPlayAudio) {
  if (typeof stopActiveVoiceAndVideoCapture === 'function') stopActiveVoiceAndVideoCapture();
  const d = findDayObj(curDayNum);
  const maxIdx = (d && d.agendas) ? d.agendas.length - 1 : 0;
  curGameIdx = Math.max(0, Math.min(maxIdx, gIdx));
  stopAllAudio();
  renderPlanView();
  if (autoPlayAudio !== false && autoVoicePlay) {
    const btnEl = document.getElementById('btnAgPlay_' + curDayNum + '_' + curGameIdx);
    playAgendaByIdx(curDayNum, curGameIdx, btnEl);
  }
}

function toggleShowAllGames() {
  showAllGamesInDay = !showAllGamesInDay;
  renderPlanView();
}

function toggleAutoVoicePlay() {
  autoVoicePlay = !autoVoicePlay;
  saveAutoVoicePlay();
  if (!autoVoicePlay) stopAllAudio();
  renderPlanView();
  if (typeof renderKoushikAdminPanel === 'function') renderKoushikAdminPanel();
}

function toggleRadioMode() {
  radioAutoPlay = !radioAutoPlay;
  renderPlanView();
  if (typeof renderKoushikAdminPanel === 'function') renderKoushikAdminPanel();
}

function toggleStoryOnlyAudio() {
  storyOnlyAudio = !storyOnlyAudio;
  renderPlanView();
  if (typeof renderKoushikAdminPanel === 'function') renderKoushikAdminPanel();
}

function toggleUnlockAllDaysMode() {
  unlockAllDaysMode = !unlockAllDaysMode;
  renderPlanView();
  if (typeof renderKoushikAdminPanel === 'function') renderKoushikAdminPanel();
}

const DELIGHT_STORIES_21 = [
  {
    day: 1,
    topic: 'gods',
    badge_bn: '🦜 মা সারদা ও ঠাকুরের মিষ্টি হাসির ঝাঁপি (যুদ্ধহীন শান্তির গল্প)',
    title_bn: 'মা সারদার পোষা টিয়াপাখি ‘গঙ্গারাম’ ও ঠাকুরের গরম জিলিপির আনন্দ',
    story_bn: 'জয়রামবাটীতে মা সারদার একটি খুব আদরের পোষা টিয়াপাখি ছিল, তার নাম ছিল ‘গঙ্গারাম’! সকাল হলেই গঙ্গারাম খাঁচা থেকে মা সারদাকে ডেকে বলতো— “মা, হরে কৃষ্ণ বলো! মা, গঙ্গারামকে একটু ছোলা-গুড় দাও!” আর দক্ষিণেশ্বরে ঠাকুর শ্রীরামকৃষ্ণ ছিলেন ঠিক ছোট্ট শিশুর মতো সরল—গরম জিলিপি বা সন্দেশ দেখলে তিনি শিশুর মতো হাততালি দিয়ে হেসে উঠতেন। ভগবান তো এমনই নিষ্পাপ আনন্দ আর হাসির মধ্যে থাকেন মা!',
    yt_query: 'Maa Sarada Jayrambati Gangaram parrot Sri Ramakrishna funny sweet story Bengali'
  },
  {
    day: 2,
    topic: 'gods',
    badge_bn: '🧈 ননীচোরা বালগোপালের আদুরে লীলা',
    title_bn: 'ননীচোরা বালগোপালের মাখন চুরি ও ছোট্ট বাছুরের পেছনে লুকানো',
    story_bn: 'বৃন্দাবনে ছোট্ট বালগোপাল একদিন শিকের ওপর থেকে মাখন পেড়ে নিজেও খেলেন আর ছোট্ট বাঁদর ছানাদেরও খাওয়ালেন। যেই মা যশোদা লাঠি হাতে এসে বললেন— “কানাই, মাখন কে খেয়েছে?” অমনি গোপাল তাঁর সারা মুখে মাখন মাখা অবস্থায় পুটপুট করে বললেন— “মা, আমি তো একফোঁটাও খাইনি, এই দুষ্টু বাছুরটা আর বাঁদরগুলো আমার মুখে মাখন মাখিয়ে দিয়েছে!” ছোট্ট গোপালের এই মিষ্টি বাহানা শুনে মা যশোদা রাগ ভুলে হেসে তাঁকে কোলে তুলে নিলেন।',
    yt_query: 'Bala Gopala makhan churi sweet Bengali story song'
  },
  {
    day: 3,
    topic: 'comedy',
    badge_bn: '😂 নদিয়ার রাজা কৃষ্ণচন্দ্র ও গোপাল ভাঁড়ের হাসির গল্প',
    title_bn: 'মহারাজ কৃষ্ণচন্দ্র ও গোপাল ভাঁড়ের ‘মাটির সমান মিষ্টি’র পেট ফাটা হাসি',
    story_bn: 'তোমার নিজের নদিয়া জেলার মহারাজ কৃষ্ণচন্দ্র একদিন সভায় জিজ্ঞেস করলেন— “বলো তো গোপাল, পৃথিবীর সবচেয়ে মিষ্টি জিনিস কী?” সভার পণ্ডিতেরা কেউ বললেন রসগোল্লা, কেউ বললেন মধু। কিন্তু গোপাল ভাঁড় গম্ভীর মুখে বলল— “মহারাজ, সবচেয়ে মিষ্টি হলো আমাদের নদিয়ার মাটির কুঁজোর ঠান্ডা জল আর গাছের ছায়ায় দুপুরের ভাতঘুম!” রাজামশাই হেসে বললেন, “সত্যিই তো গোপাল, আরামের চেয়ে মিষ্টি আর কিছু নেই!”',
    yt_query: 'Gopal Bhar Maharaj Krishnachandra Bengali funny story'
  },
  {
    day: 4,
    topic: 'animals',
    badge_bn: '🐘 আদুরে পশুপাখির মজার কীর্তি',
    title_bn: 'ছোট্ট হাতির ছানার নিজের শুঁড় চোষা ও মায়ের আঁচলের পেছনে লুকানো',
    story_bn: 'তুমি কি জানো মা, মানুষের ছোট্ট বাচ্চারা যেমন নিজের বুড়ো আঙুল মুখে দিয়ে চুষতে থাকে, ছোট্ট হাতির ছানারাও ঠিক তেমনই নিজের লম্বা শুঁড়ের ডগাটা মুখে পুরে চুষতে ভালোবাসে! জন্মের পর প্রথম কয়েক মাস তারা নিজের শুঁড়টা কীভাবে সামলাবে বুঝতেই পারে না—হাঁটতে গিয়ে নিজের শুঁড়েই পা দিয়ে গড়িয়ে পড়ে আর মা হাতি শুঁড় দিয়ে আদর করে তাকে তুলে দেয়।',
    yt_query: 'cute baby elephant playing with trunk mother elephant video'
  },
  {
    day: 5,
    topic: 'gods',
    badge_bn: '🐭 কৈলাসে ভোলানাথ, মা পার্বতী ও ছোট্ট গণেশের মিষ্টি গল্প',
    title_bn: 'ইঁদুর বাহনে ছোট্ট গণেশের বিশ্বভ্রমণ — ‘বাবা-মা-ই তো আমার গোটা জগৎ!’',
    story_bn: 'একদিন কৈলাসে মা পার্বতী একটি সুস্বাদু মিষ্টি মোদক হাতে নিয়ে বললেন, যে সবার আগে ত্রিভুবন ঘুরে আসবে সে-ই এই মোদকটি পাবে। কার্তিক তো ময়ূরে চড়ে সাঁই করে আকাশে উড়ে গেলেন! কিন্তু আমাদের নাদুসনুদুস ছোট্ট গণেশ তাঁর ছোট্ট ইঁদুর বাহনে চড়ে ধীরেসুস্থে বাবা মহাদেব ও মা পার্বতীর চারপাশে সাতবার ঘুরে এসে হাত জোড় করে বললেন— “মা, বাবা আর মায়ের চরণেই তো গোটা বিশ্বব্রহ্মাণ্ড!” মা পার্বতী খুশিতে গদগদ হয়ে গণেশকেই মোদকটি খাওয়ালেন।',
    yt_query: 'Ganesh circling Shiva Parvati modak sweet Bengali story'
  },
  {
    day: 6,
    topic: 'animals',
    badge_bn: '🦦 আদুরে পশুপাখির নিষ্পাপ ভালোবাসা',
    title_bn: 'সমুদ্রের ভোঁদড় ছানাদের হাত ধরাধরি করে জলের ওপর ঘুমানো',
    story_bn: 'সমুদ্রের নীল জলে যে ছোট্ট লোমশ ভোঁদড় ছানারা (Sea Otters) থাকে, তারা জলের ওপর চিত হয়ে ভাসতে ভাসতে ঘুমায়। কিন্তু জলের ঢেউয়ে যাতে ঘুমের মধ্যে মা বা বন্ধুর কাছ থেকে ভেসে দূরে চলে না যায়, তাই তারা ঘুমানোর সময় একে অপরের ছোট্ট হাত দুটো শক্ত করে ধরে রাখে! কী মিষ্টি তাদের এই ভালোবাসা, তাই না মা?',
    yt_query: 'sea otters holding hands sleeping cute animal video'
  },
  {
    day: 7,
    topic: 'gods',
    badge_bn: '🛕 পুরীর জগন্নাথদেবের মিষ্টি মানভঞ্জন (যুদ্ধহীন ভক্তির গল্প)',
    title_bn: 'পুরীর জগন্নাথদেবের রসগোল্লা দিয়ে মা লক্ষ্মীর অভিমান ভাঙানো!',
    story_bn: 'রথযাত্রায় জগন্নাথদেব যখন মা লক্ষ্মীকে মন্দিরে রেখে ভাই-বোন বলরাম ও সুভদ্রাকে নিয়ে মাসির বাড়ি গুণ্ডিচা মন্দিরে বেড়াতে যান, মা লক্ষ্মী তখন অভিমান করে মন্দিরের সদর দরজা বন্ধ করে দেন! ফিরে এসে জগন্নাথদেব দরজার বাইরে দাঁড়িয়ে মা লক্ষ্মীর রাগ ভাঙানোর জন্য এক হাঁড়ি রসগোল্লা উপহার দেন। ভগবানের সংসারেও এমন মিষ্টি খুনসুটি আর রসগোল্লার আদর চলে মা!',
    yt_query: 'Puri Jagannath Rasagolla Niladri Bije Maa Lakshmi sweet Bengali story'
  },
  {
    day: 8,
    topic: 'comedy',
    badge_bn: '👑 রাজা-মহারাজা ও বীরবল-গোপালের মজার বুদ্ধি',
    title_bn: 'রাজ্যে মোট ক’টা কাক আছে? গোপাল ভাঁড়ের চটজলদি মজার উত্তর!',
    story_bn: 'একদিন মহারাজ কৃষ্ণচন্দ্র গোপাল ভাঁড়কে জব্দ করার জন্য জিজ্ঞেস করলেন— “গোপাল, আমাদের নদিয়া রাজ্যে ঠিক ক’টা কাক আছে বলো তো?” গোপাল একটুও না ঘাবড়ে আঙুল গুনে বলল— “মহারাজ, নিরানব্বই হাজার নয়শো নিরানব্বইটা! বিশ্বাস না হলে গুনে দেখুন—যদি দেখেন কয়েকটা কম আছে তবে জানবেন তারা পাশের রাজ্যে মামাবাড়ি বেড়াতে গেছে, আর বেশি থাকলে জানবেন তাদের আত্মীয়রা আমাদের রাজ্যে বেড়াতে এসেছে!”',
    yt_query: 'Gopal Bhar counting crows funny Bengali comedy'
  },
  {
    day: 9,
    topic: 'animals',
    badge_bn: '🐿️ আদুরে কাঠবিড়ালির মজার কীর্তি',
    title_bn: 'ভুলোমনা কাঠবিড়ালির লুকানো বাদাম থেকে আস্ত ফলের বাগান!',
    story_bn: 'গাছের ডালে যে ছোট্ট ডোরাকাটা কাঠবিড়ালিরা (Squirrels) তিড়িং-বিড়িং করে লাফায়, তারা শীতকালে খাওয়ার জন্য মাটির নিচে প্রচুর ফল আর বাদাম লুকিয়ে রাখে। কিন্তু মজার ব্যাপার হলো, তারা এতটাই ভুলোমনা যে অর্ধেক বাদাম কোথায় লুকিয়েছে তা বেমালুম ভুলে যায়! আর সেই ভুলে যাওয়া বীজগুলো থেকেই বৃষ্টির জলে শত শত নতুন ফলের গাছ জন্মায়—অর্থাৎ ভুলে যাওয়াটাও প্রকৃতির কী দারুণ আশীর্বাদ!',
    yt_query: 'cute squirrel hiding nuts funny animal video'
  },
  {
    day: 10,
    topic: 'gods',
    badge_bn: '🍲 কাশীর মা অন্নপূর্ণা ও ভোলানাথের মিষ্টি কথা',
    title_bn: 'মা অন্নপূর্ণার সোনার হাতা ও ভোলা মহেশ্বরের পরম তৃপ্তি',
    story_bn: 'কাশীধামে মা অন্নপূর্ণা যখন নিজের হাতে সোনার হাতা দিয়ে অন্ন পরিবেশন করেন, স্বয়ং ভোলা মহেশ্বরও বাটি হাতে মায়ের সামনে এসে দাঁড়ান। মা অন্নপূর্ণা হাসিমুখে বলেন— “সংসারের সব মানুষ আর পশুপাখি পেট ভরে শান্তিতে খেলেই আমার সবচেয়ে বড় পূজা হয়।” ঠিক যেমন তুমি সারাজীবন সবাইকে ভালোবেসে খাইয়েছো মা!',
    yt_query: 'Maa Annapurna Kashi Shiva sweet Bengali devotional story'
  },
  {
    day: 11,
    topic: 'comedy',
    badge_bn: '🐱 তেনালি রামের মজার হাসির গল্প',
    title_bn: 'তেনালি রামের পোষা বিড়াল ও দুধের বাটির হাসির কাণ্ড',
    story_bn: 'বিজয়নগরের রাজা একবার তেনালি রামকে একটি বিড়াল আর একটি গাইগরু দিয়েছিলেন যাতে বিড়ালটি রোজ দুধ খেয়ে মোটা হয়। তেনালি রাম নিজেই রোজ মালাই দেওয়া দুধটুকু খেয়ে নিতেন, আর বিড়ালকে একবার গরম দুধ দিয়েছিলেন যাতে বিড়ালটার জিভে ছ্যাঁকা লাগে! এরপর রাজার সামনে যখনই ঠান্ডা দুধের বাটি রাখা হলো, বিড়ালটা গরম দুধের ভয়ে এক লাফে পালিয়ে গেল!',
    yt_query: 'Tenali Raman cat and hot milk Bengali funny story'
  },
  {
    day: 12,
    topic: 'animals',
    badge_bn: '🐄 গাইগরু ও ছোট্ট বাছুরের প্রাণের বন্ধুত্ব',
    title_bn: 'গাইগরুদেরও মানুষের মতো ‘সবচেয়ে প্রিয় বন্ধু’ থাকে!',
    story_bn: 'তুমি কি জানো মা, মাঠে বা গোয়ালে যে শান্ত গাইগরু ও বাছুরেরা থাকে, তাদেরও ঠিক আমাদের মতো একজন করে ‘সবচেয়ে প্রিয় বান্ধবী’ (Best Friend) থাকে! বিজ্ঞানীরা দেখেছেন, প্রিয় বান্ধবী গরুটির পাশে দাঁড়িয়ে ঘাস চিবোলে তাদের মন একদম শান্ত ও খুশি থাকে, আর একে অপরকে জিভ দিয়ে আদর করে দেয়।',
    yt_query: 'cute cow and calf best friends heartwarming video'
  },
  {
    day: 13,
    topic: 'animals',
    badge_bn: '🦚 বৃন্দাবনের ময়ূর ও বর্ষার মেঘের আনন্দ',
    title_bn: 'আকাশে কালো মেঘ দেখলেই ময়ূর কেন পেখম তুলে নাচে?',
    story_bn: 'গরমের পর আকাশে যখন প্রথম ঠান্ডা মেঘ জমে আর মাটির সোঁদা গন্ধ ওঠে, মনের আনন্দে ময়ূর তার হাজার রঙের পেখম মেলে নাচতে শুরু করে। বৃন্দাবনের কুঞ্জবনে বালগোপালের বাঁশির সুর শুনলেও ময়ূরেরা মেঘের ডাক ভেবে পেখম তুলে নাচতো!',
    yt_query: 'peacock dancing in rain Vrindavan cute video'
  },
  {
    day: 14,
    topic: 'gods',
    badge_bn: '🍬 দক্ষিণেশ্বরে ঠাকুর শ্রীরামকৃষ্ণের নির্মল হাসির কথা',
    title_bn: 'ঠাকুর শ্রীরামকৃষ্ণের ছোট্ট ছেলের মতো সন্দেশের হাঁড়ি খোঁজা',
    story_bn: 'দক্ষিণেশ্বরে মা ভবতারিণীর ভোগের পর ঠাকুর শ্রীরামকৃষ্ণ কখনো কখনো ছোট্ট বালকের মতো ঘরে ঝুলিয়ে রাখা সন্দেশের হাঁড়ি থেকে নিজের হাতে একটুখানি সন্দেশ ভেঙে খেতেন আর মিটিমিটি হাসতেন। মা সারদা তা দেখে স্নেহের হাসি হেসে তাঁর জন্য আলাদা বাটিতে নরম ছানার মিষ্টি ঢেকে রাখতেন।',
    yt_query: 'Sri Ramakrishna Dakshineswar sweet sandesh Maa Sarada story Bengali'
  },
  {
    day: 15,
    topic: 'animals',
    badge_bn: '🐧 পেঙ্গুইন পাখির মিষ্টি উপহারের গল্প',
    title_bn: 'বরফের দেশে পেঙ্গুইন পাখি কীভাবে সবচেয়ে মসৃণ নুড়ি পাথর খুঁজে উপহার দেয়!',
    story_bn: 'বরফের দেশে যে ছোট্ট পেঙ্গুইন পাখিরা কোট-পরা মানুষের মতো হেলেদুলে হাঁটে, তারা নিজের সঙ্গীকে খুশি করার জন্য সমুদ্রের পাড় জুড়ে খুঁজে খুঁজে সবচেয়ে গোল ও মসৃণ নুড়ি পাথরটি (Pebble) মুখে করে এনে উপহার দেয়! সেই পাথরটি দিয়েই তারা দুজনে মিলে নিজেদের বাসা সাজায়।',
    yt_query: 'cute penguin gifting pebble funny walking video'
  },
  {
    day: 16,
    topic: 'comedy',
    badge_bn: '😂 গোপাল ভাঁড়ের নির্মল হাসির আড্ডা',
    title_bn: 'গোপাল ভাঁড়ের ‘স্বপ্নে পাওয়া একশো মোহর’ ও রাজামশাইয়ের হাসি',
    story_bn: 'একদিন গোপাল ভাঁড় রাজসভায় এসে বলল— “মহারাজ, কাল রাতে স্বপ্নে দেখলাম আপনি আমাকে একশোটা সোনার মোহর দিচ্ছেন, কিন্তু নব্বইটা দেওয়ার পরই ঘুমটা ভেঙে গেল—বাকি দশটা মোহর আজ দিয়ে দিন!” মহারাজ কৃষ্ণচন্দ্র হেসে বললেন— “বেশ তো গোপাল, আজ রাতে আবার ঘুমিয়ে বাকি দশটা মোহর স্বপ্নেই নিয়ে নিও!”',
    yt_query: 'Gopal Bhar gold coins dream funny Bengali story'
  },
  {
    day: 17,
    topic: 'gods',
    badge_bn: '🌸 জয়রামবাটীতে মা সারদা ও বিড়ালছানার গল্প',
    title_bn: 'মা সারদার কোলের বিড়ালছানা ও ‘সবাই আমার সন্তান’',
    story_bn: 'জয়রামবাটীর বাড়িতে একটি ছোট্ট বিড়ালছানা রোজ মা সারদার পায়ের কাছে এসে মিউমিউ করতো। কেউ বিড়ালটিকে তাড়াতে গেলে মা সারদা বাধা দিয়ে বলতেন— “ওকে মারিস নে, ও-ও তো আমারই সন্তান! ওকে একটু দুধ-ভাত মেখে দে।” মা সারদার কাছে মানুষ থেকে ছোট্ট পশুপাখি—সবার জন্যই ছিল সমান আদর।',
    yt_query: 'Maa Sarada cat story Jayrambati Bengali'
  },
  {
    day: 18,
    topic: 'gods',
    badge_bn: '🪈 বৃন্দাবনে বালগোপালের বাঁশি ও হরিণছানার মায়া',
    title_bn: 'বালগোপালের বাঁশির সুরে যমুনার তীরে হরিণছানা ও পাখিদের শান্ত আসর',
    story_bn: 'বিকেলবেলা যমুনার ধারে কদম গাছের ছায়ায় বসে ছোট্ট গোপাল যখন বাঁশিতে মিষ্টি সুর তুলতেন, তখন বনের ছোট্ট হরিণছানারা আর গাইগরুরা ঘাস খাওয়া ভুলে কান খাড়া করে তাঁর পাশে এসে চুপটি করে বসে থাকতো। শান্ত সুর আর ভালোবাসা পশুপাখিরাও কত সহজে বোঝে!',
    yt_query: 'Krishna flute deer calf Vrindavan peaceful bhajan Bengali'
  },
  {
    day: 19,
    topic: 'comedy',
    badge_bn: '👑 সম্রাট আকবর ও বীরবলের হাসির গল্প',
    title_bn: 'বীরবলের ‘সবচেয়ে বড় রেখাটিকে না ছুঁয়ে ছোট করে দেওয়া’র বুদ্ধি!',
    story_bn: 'একদিন সম্রাট আকবর মেঝেতে খড়ি দিয়ে একটি দাগ টেনে বললেন— “বীরবল, এই দাগটাতে হাত না লাগিয়ে বা না মুছে এটাকে ছোট করে দেখাও তো!” বীরবল হাসিমুখে ঠিক তার নিচে আরেকটি লম্বা দাগ টেনে দিলেন—অমনি উপরের দাগটা আপনাআপনি ছোট হয়ে গেল! ঝগড়া বা লড়াই না করেও বুদ্ধি আর হাসিমুখে সব সমস্যার সমাধান হয়।',
    yt_query: 'Akbar Birbal line puzzle Bengali funny story'
  },
  {
    day: 20,
    topic: 'animals',
    badge_bn: '🐦 বাড়ির বারান্দার চড়ুই ও শালিক পাখির সংসার',
    title_bn: 'চড়ুই পাখির ধুলো-স্নান ও শালিক পাখির সকালবেলার বৈঠক',
    story_bn: 'বারান্দায় বা উঠোনে ছোট্ট চড়ুই পাখিদের ফুড়ুৎ-ফুড়ুৎ করে লাফানো আর ডানা ঝাপটে মাটির ধুলো বা জলের বাটিতে স্নান করা দেখতে কী মজার লাগে! তারা সামান্য দুটো চালের দানা পেলেই কিচিরমিচির করে গোটা বাড়ি আনন্দে মাতিয়ে রাখে।',
    yt_query: 'cute sparrow bird bath balcony funny video'
  },
  {
    day: 21,
    topic: 'gods',
    badge_bn: '🌺 ভগবানের রাজ্যে শিশুর মতো নির্মল আনন্দের আশীর্বাদ',
    title_bn: 'নিজের মনটাকে শিশুর মতো খুশি ও হালকা রাখাই ভগবানের সবচেয়ে প্রিয় পূজা',
    story_bn: 'ঠাকুর শ্রীরামকৃষ্ণ বলতেন— “যার মন ছোট্ট শিশুর মতো সরল, যে অল্পেই হাসে আর কারো ওপর রাগ পুষে রাখে না, ভগবান তার হৃদয়েই আনন্দে বাস করেন।” মা, তুমি ঠিক তেমনই সরল ও নরম মনের মানুষ—তাই কৌশিক চায় তুমি প্রতিদিন এমনই হাসিমুখে, বিনা চিন্তায় রাজরানীর মতো আনন্দে থাকো!',
    yt_query: 'Sri Ramakrishna Maa Sarada peaceful bhajan story Bengali'
  }
];

function getDelightStoryForDay(dayNum) {
  return DELIGHT_STORIES_21.find(s => s.day === dayNum) || DELIGHT_STORIES_21[(Math.max(1, dayNum) - 1) % DELIGHT_STORIES_21.length];
}

function toggleDelightLiked(dayNum) {
  const key = String(dayNum);
  const nextVal = !delightLikedMap[key];
  delightLikedMap[key] = nextVal;
  saveDelightLikedMap();
  const s = getDelightStoryForDay(dayNum);
  if (nextVal && s) {
    recordMaBehaviorSignal('delight_like', 'মা দিন ' + toBnDigits(dayNum) + '-এর “' + s.title_bn + '” গল্পটি খুব পছন্দ করেছেন (❤️)।', s.topic);
    showCelebrationToast('🌸 মা, তোমার ভালো লাগার কথাটি কল্যাণীর স্মৃতি-উইকিতে যত্ন করে রাখা হলো!');
  }
  renderPlanView();
  if (typeof renderKoushikAdminPanel === 'function') renderKoushikAdminPanel();
}

function buildProactiveAgentCardHtml(d) {
  const dynCard = (kalyaniWikiVault.dynamicCards || {})[String(d.day)] || null;
  const dynBtnId = 'btnDynAgentPlay_' + d.day;
  const isOpen = !!(agentGeneratingState || dynCard);

  let dynCardHtml = '';
  if (agentGeneratingState) {
    dynCardHtml = `
      <div class="vn-sending-panel" style="margin-top:10px;">
        ✨ নতুন গল্প তৈরি হচ্ছে...
      </div>
    `;
  } else if (dynCard) {
    dynCardHtml = `
      <div id="dynamicAgentStoryCard_${d.day}" class="agent-dynamic-story-box">
        <div class="agenda-cat">${dynCard.badge_bn}</div>
        <div class="agenda-title" style="margin-top:4px;">${dynCard.title_bn}</div>
        <div class="agenda-detail">${dynCard.story_bn}</div>
        <div class="agenda-actions" style="margin-top:8px;">
          <button id="${dynBtnId}" class="ag-btn listen" data-default-label="🔊 শোনো" onclick="playDynamicAgentCardAudio(${d.day})">
            🔊 শোনো
          </button>
        </div>
      </div>
    `;
  }

  return `
    <details id="kalyaniAgentCard" class="agent-companion-card minimal-section-drawer"${isOpen ? ' open' : ''} ontoggle="if(this.open && typeof prefetchStoryByDrawer==='function') prefetchStoryByDrawer('agent', ${d.day})">
      <summary class="minimal-drawer-summary">✨ নতুন গল্প ও মনের কথা (ঐচ্ছিক) ▾</summary>
      <div class="minimal-drawer-body">
        <div class="agent-flow-pills">
          <button id="btnAgentFlowComedy_${d.day}" class="agent-flow-btn" onclick="generateDynamicAgentStory(${d.day}, 'comedy')">
            😂 হাসির গল্প
          </button>
          <button id="btnAgentFlowGods_${d.day}" class="agent-flow-btn" onclick="generateDynamicAgentStory(${d.day}, 'gods')">
            🪷 ঠাকুরের গল্প
          </button>
          <button id="btnAgentFlowAnimals_${d.day}" class="agent-flow-btn" onclick="generateDynamicAgentStory(${d.day}, 'animals')">
            🐘 পশুপাখি
          </button>
          <button id="btnAgentFlowSpeak_${d.day}" class="agent-flow-btn speak" onclick="generateDynamicAgentStory(${d.day}, 'speak_mind')">
            💬 মনের কথা
          </button>
        </div>
        ${dynCardHtml}
      </div>
    </details>
  `;
}

function buildDailyDelightCardHtml(d) {
  const s = getDelightStoryForDay(d.day);
  const liked = !!delightLikedMap[String(d.day)];
  const playBtnId = 'btnDelightPlay_' + d.day;
  const ytUrl = 'https://www.youtube.com/results?search_query=' + encodeURIComponent(s.yt_query);

  return `
    <details id="dailyDelightCard" class="agenda-card delight-hero-card minimal-section-drawer" data-accent="amber" ontoggle="if(this.open && typeof prefetchStoryByDrawer==='function') prefetchStoryByDrawer('delight', ${d.day})">
      <summary class="minimal-drawer-summary">😄 আজকের ছোট গল্প: ${s.title_bn} (ঐচ্ছিক) ▾</summary>
      <div class="minimal-drawer-body">
        <div class="agenda-detail">${s.story_bn}</div>
        <div class="agenda-actions" style="margin-top:10px;">
          <button id="${playBtnId}" class="ag-btn listen" data-default-label="🔊 শোনো" onclick="playDelightStoryAudio(${d.day})">🔊 শোনো</button>
          <button id="btnDelightLike_${d.day}" class="ag-btn check ${liked ? 'checked' : ''}" onclick="toggleDelightLiked(${d.day})">
            ${liked ? '✅ ভালো লেগেছে' : '❤️ ভালো লাগলো'}
          </button>
          <a class="ag-btn" href="${ytUrl}" target="_blank" rel="noopener noreferrer" onclick="stopAllAudio()" style="text-decoration:none;">
            ▶️ ইউটিউব
          </a>
        </div>
      </div>
    </details>
  `;
}

function extractSongSearchUrl(ag) {
  const src = (ag.prompt_bn || '') + ' ' + (ag.title_bn || '');
  const m = src.match(/[‘'“"]([^’'”"]{3,60})[’'”"]/);
  const query = (m && m[1]) ? (m[1] + ' বাংলা গান') : ((ag.title_bn || 'বাংলা পুরনো দিনের গান') + ' বাংলা গান');
  return 'https://www.youtube.com/results?search_query=' + encodeURIComponent(query);
}

function toggleAgendaDone(dayNum, agIdx) {
  const key = dayNum + '_' + agIdx;
  const newlyDone = !doneMap[key];
  doneMap[key] = newlyDone;
  saveDoneMap();

  if (newlyDone) {
    if (isDayFullyDone(dayNum)) {
      if (dayNum < ALL_DAYS.length) {
        showCelebrationToast('🎉 দারুণ মা! দিন ' + toBnDigits(dayNum) + ' শেষ হয়েছে—দিন ' + toBnDigits(dayNum + 1) + '-এর নতুন চমক খুলে গেল!');
      } else {
        showCelebrationToast('🎉 অসাধারণ মা! আজকের সব খেলা খুব সুন্দরভাবে শেষ হয়েছে!');
      }

      if (dayNum < ALL_DAYS.length) {
        const nextDay = dayNum + 1;
        curDayNum = nextDay;
        curGameIdx = getNextOpenGameIdx(nextDay);
        stopAllAudio();
        renderPlanView();
        scrollActiveDayChipIntoView();
        if (autoVoicePlay) toggleDayOverviewAudio();
        return;
      }
    } else {
      showCelebrationToast('🌸 সাবাশ মা! খেলাটা খুব সুন্দরভাবে শেষ করলে!');
      if (!showAllGamesInDay) {
        curGameIdx = getNextOpenGameIdx(dayNum);
        stopAllAudio();
        renderPlanView();
        if (autoVoicePlay) {
          const nextBtnEl = document.getElementById('btnAgPlay_' + dayNum + '_' + curGameIdx);
          playAgendaByIdx(dayNum, curGameIdx, nextBtnEl);
        }
        return;
      }
    }
  }
  renderPlanView();
}

function buildCalendarGridCellsHtml(daysArray, idPrefix) {
  return daysArray.map(item => {
    const done = isDayFullyDone(item.day);
    const unlocked = isDayUnlocked(item.day);
    const isAct = (item.day === curDayNum);
    const stateCls = (isAct ? ' active' : '') + (done ? ' done' : '') + (!unlocked ? ' locked' : '');
    const icon = done ? '✅ ' : (!unlocked ? '🔒 ' : '');
    return `<button id="${idPrefix}_${item.day}" class="cal-day-cell${stateCls}" onclick="selectDay(${item.day}, true)">${icon}দিন ${toBnDigits(item.day)}</button>`;
  }).join('');
}

function buildWalkieTalkieStudioHtml(d, ag, idx) {
  const cardKey = d.day + '_' + idx;
  const turns = kalyaniThreads[cardKey] || [];
  const isRecHere = vnRecordingState.active && vnRecordingState.dayNum === d.day && vnRecordingState.agIdx === idx;
  const isSendingHere = vnRecordingState.sending && vnRecordingState.dayNum === d.day && vnRecordingState.agIdx === idx;
  const isCamHere = vnLiveCamState.active && vnLiveCamState.dayNum === d.day && vnLiveCamState.agIdx === idx;

  const threadHtml = turns.map((t, tIdx) => `
    <div class="vn-turn-block">
      <div class="vn-user-bubble">
        <div class="vn-bubble-eyebrow">🗣️ মা যা পাঠিয়েছো ${t.has_live_video ? '📹' : '🎙️'}:</div>
        <div class="vn-bubble-text">“${t.heard_bn}”</div>
      </div>
      <div class="vn-ai-bubble">
        <div class="vn-gemini-badge">✨ জেমিনি (কল্যাণীর ভয়েস মেসেজ উত্তর):</div>
        <div class="vn-bubble-text">${t.reply_bn}</div>
        <button id="btnVnReplyPlay_${d.day}_${idx}_${tIdx}" class="ag-btn listen vn-reply-play-btn" data-default-label="🔊 জেমিনির উত্তর শোনো" onclick="playVoiceNoteReplyAudio(${d.day}, ${idx}, ${tIdx})">
          🔊 জেমিনির উত্তর শোনো
        </button>
      </div>
    </div>
  `).join('');

  const errHtml = vnRecordingState.errorMsg ? `<div class="vn-error-msg">${vnRecordingState.errorMsg}</div>` : '';

  const liveCamPanelHtml = isCamHere ? `
    <div id="vnLiveCamWrap_${d.day}_${idx}" class="vn-live-cam-stage">
      <div class="vn-live-cam-badge">📹 ভিডিও ক্যামেরা চালু</div>
      <video id="vnLiveVideo_${d.day}_${idx}" class="vn-live-video" autoplay playsinline muted></video>
      <div class="vn-secondary-row" style="margin-top:6px;">
        <button id="btnVnSwitchCam_${d.day}_${idx}" class="ag-btn" onclick="switchCardLiveCamera(${d.day}, ${idx})">🔄 ক্যামেরা ঘোরাও</button>
        <button id="btnVnStopCam_${d.day}_${idx}" class="ag-btn" onclick="toggleCardLiveVideo(${d.day}, ${idx})">⏹️ ক্যামেরা বন্ধ</button>
      </div>
    </div>
  ` : '';

  let controlsHtml = '';
  if (isSendingHere) {
    controlsHtml = `
      <div class="vn-sending-panel">
        <div class="vn-rec-status">✨ জেমিনি তোমার কথা শুনে উত্তর তৈরি করছে...</div>
        <div id="vnListenProgress_${d.day}_${idx}" class="vn-listen-progressbar sending" role="progressbar" aria-label="জেমিনি উত্তর তৈরি করছে">
          <div class="vn-listen-bar-fill"></div>
        </div>
      </div>
    `;
  } else if (isRecHere || isCamHere) {
    const pct = Math.min(100, Math.max(12, (vnRecordingState.seconds % 20) * 5 + 15));
    controlsHtml = `
      <div class="vn-recording-panel">
        <div class="vn-rec-status">
          🟢 জেমিনি এখন মন দিয়ে তোমার কথা শুনছে... (<span id="vnTimer_${d.day}_${idx}">${formatAudioSecondsBn(vnRecordingState.seconds)}</span>)
        </div>
        <div id="vnListenProgress_${d.day}_${idx}" class="vn-listen-progressbar listening" role="progressbar" aria-label="জেমিনি এখন শুনছে">
          <div id="vnListenFill_${d.day}_${idx}" class="vn-listen-bar-fill" style="width:${pct}%"></div>
        </div>
        <div id="vnLivePreview_${d.day}_${idx}" class="vn-live-preview">
          ${vnRecordingState.liveTranscript ? ('🗣️ “' + vnRecordingState.liveTranscript + '”') : '🎙️ মা, নিজের মতো ধীরেসুস্থে বলো...'}
        </div>
        <div class="vn-rec-actions">
          <button id="btnVnSend_${d.day}_${idx}" class="vn-send-btn" onclick="finishAndSendVoiceNote(${d.day}, ${idx})">
            ✅ বলা শেষ — কল্যাণীকে পাঠাও ▶️
          </button>
          <button id="btnVnCancel_${d.day}_${idx}" class="ag-btn" onclick="cancelVoiceNoteRecording()">
            ❌ বাতিল
          </button>
        </div>
      </div>
    `;
  } else {
    controlsHtml = `
      <div class="vn-idle-controls">
        <div class="vn-secondary-row">
          <button id="btnVnRecord_${d.day}_${idx}" class="vn-record-btn" style="flex:1;" onclick="startVoiceNoteRecording(${d.day}, ${idx}, false)">
            🎙️ ভয়েস পাঠাও
          </button>
          <button id="btnVnLiveCam_${d.day}_${idx}" class="ag-btn vn-livecam-btn" style="flex:1;" onclick="toggleCardLiveVideo(${d.day}, ${idx})">
            📹 ভিডিও পাঠাও
          </button>
        </div>
      </div>
    `;
  }

  return `
    <div id="vnStudio_${d.day}_${idx}" class="walkie-talkie-studio">
      <div class="vn-studio-header">কল্যাণীকে ভয়েস মেসেজ বা ভিডিও তুলে পাঠাও:</div>
      ${errHtml}
      ${threadHtml}
      ${liveCamPanelHtml}
      ${controlsHtml}
    </div>
  `;
}

function buildAgendaCardHtml(d, ag, idx) {
  const isDone = !!doneMap[d.day + '_' + idx];
  const btnId = `btnAgPlay_${d.day}_${idx}`;
  const accent = ag.accent || GAME_ACCENTS[idx] || 'terra';
  const catStr = (ag.category || '') + ' ' + (ag.short_bn || '');
  const isSongGame = (ag.category || '').includes('🎵') || (ag.prompt_bn || '').includes('ইউটিউব মিউজিক');

  const cardKey = d.day + '_' + idx;
  const turns = kalyaniThreads[cardKey] || [];
  const isRecHere = vnRecordingState.active && vnRecordingState.dayNum === d.day && vnRecordingState.agIdx === idx;
  const isSendingHere = vnRecordingState.sending && vnRecordingState.dayNum === d.day && vnRecordingState.agIdx === idx;
  const isCamHere = vnLiveCamState.active && vnLiveCamState.dayNum === d.day && vnLiveCamState.agIdx === idx;
  const keepDrawerOpen = isRecHere || isSendingHere || isCamHere || turns.length > 0;

  let stepHeading = '✨ মা, আজ কী করবো দেখো:';
  if (isSongGame) {
    stepHeading = '🎵 মা, আজকের গান ও মনের টান:';
  } else if (catStr.includes('💬') || catStr.includes('স্মৃতির ঝাঁপি') || catStr.includes('মনের গভীর কথা')) {
    stepHeading = '💬 মা, আজকের মনের গভীর কথা ও স্মৃতির ঝাঁপি:';
  } else if (catStr.includes('📖') || catStr.includes('গল্প')) {
    stepHeading = '📖 মা, আজকের গল্প ও মনের কথা:';
  } else if (catStr.includes('🌿') || catStr.includes('মনের আরাম') || catStr.includes('মনের আনন্দ')) {
    stepHeading = '🌿 মা, আজকের মনের আরাম ও ভাবনা:';
  } else if (catStr.includes('🗣️') || catStr.includes('হিন্দি')) {
    stepHeading = '🗣️ মা, আজকের সহজ ও আত্মবিশ্বাসী হিন্দি খেলা:';
  } else if (catStr.includes('🌍') || catStr.includes('জানাশোনা') || catStr.includes('বিস্ময়') || catStr.includes('🌟')) {
    stepHeading = '🌍 মা, আজকের অবাক করা জানাশোনা:';
  } else if (catStr.includes('🔤') || catStr.includes('ইংরেজি')) {
    stepHeading = '🔤 মা, আজকের সহজ ইংরেজি খেলা:';
  } else if (catStr.includes('🎨') || catStr.includes('আঁকা') || catStr.includes('সৃষ্টি')) {
    stepHeading = '🎨 মা, আজকের নিজের খুশির সৃষ্টি:';
  }

  const ytMusicGuideHtml = isSongGame ? `
      <div class="agenda-prompt-box yt-music-box">
        <div class="agenda-prompt-label">🎵 ইউটিউবে সরাসরি গানটা শোনো বা ভয়েস মেসেজে কল্যাণীকে বলো!</div>
        <div class="agenda-detail" style="font-size:1.01rem;">মা, উপরের কমলা বোতামটায় ছুঁলেই সরাসরি ইউটিউবে গানটা বেজে উঠবে!</div>
      </div>` : '';

  const followupLabel = isSongGame
    ? '💬 গানটা শোনা হয়ে গেলে এর মানে আর গল্পটা জানতে জেমিনিকে বলো:'
    : '💬 জেমিনির উত্তরটা শোনার পর গল্পটা আরও জমাতে দ্বিতীয় কথায় বলো:';

  const followupHtml = ag.followup_prompt_bn ? `
      <div class="agenda-prompt-box">
        <div class="agenda-prompt-label">${followupLabel}</div>
        <div class="agenda-prompt-speech">“${ag.followup_prompt_bn}”</div>
      </div>` : '';

  const promptLabel = isSongGame
    ? '🎙️ গানের ক্লু:'
    : '🎙️ কী বলবে তার ক্লু:';

  const ytDirectBtnHtml = isSongGame ? `
      <a class="yt-direct-btn" href="${extractSongSearchUrl(ag)}" target="_blank" rel="noopener noreferrer" onclick="stopAllAudio()">
        🎵 ইউটিউবে এই গানটা সরাসরি চালাও ▶️
      </a>` : '';

  return `
    <article class="agenda-card ${isDone ? 'done-card' : ''}" data-accent="${accent}" id="agendaCard_${d.day}_${idx}">
      <div class="agenda-card-header">
        <div class="agenda-cat">${ag.category}</div>
      </div>
      <div class="agenda-title">${ag.title_bn}</div>
      ${ytDirectBtnHtml}
      <div class="agenda-actions">
        <button id="${btnId}" class="ag-btn listen" data-default-label="🔊 শোনো" onclick="playAgendaByIdx(${d.day}, ${idx}, this)">🔊 শোনো</button>
        <button id="btnAgDone_${d.day}_${idx}" class="ag-btn check ${isDone ? 'checked' : ''}" onclick="toggleAgendaDone(${d.day}, ${idx})">
          ${isDone ? '✅ হয়ে গেছে' : '⬜ হয়ে গেছে'}
        </button>
      </div>

      <details class="game-sub-drawer">
        <summary class="game-sub-summary">📖 গল্পটা পড়ো (ঐচ্ছিক) ▾</summary>
        <div class="step-section">
          <div class="agenda-step-heading">${stepHeading}</div>
          <div class="agenda-detail">${ag.detail_bn}</div>
        </div>
      </details>

      <details class="optional-prompt-drawer"${keepDrawerOpen ? ' open' : ''}>
        <summary class="optional-prompt-summary">🎙️ কথা বলো বা ভিডিও (ঐচ্ছিক) ▾</summary>
        <div class="optional-prompt-body">
          ${buildWalkieTalkieStudioHtml(d, ag, idx)}
          <details class="game-sub-drawer" style="margin-top:8px;">
            <summary class="game-sub-summary">💡 কী বলবে তার ক্লু (ঐচ্ছিক) ▾</summary>
            <div class="optional-prompt-body">
              <div class="agenda-prompt-box">
                <div class="agenda-prompt-label">${promptLabel}</div>
                <div class="agenda-prompt-speech">“${ag.prompt_bn}”</div>
              </div>${ytMusicGuideHtml}${followupHtml}
              <button class="ag-btn full-prompt-audio-btn" onclick="playAgendaByIdx(${d.day}, ${idx}, null, true)">🔊 ক্লু শোনো</button>
            </div>
          </details>
        </div>
      </details>
    </article>
  `;
}

function renderPlanView() {
  if (!isDayUnlocked(curDayNum)) {
    curDayNum = getHighestUnlockedDay();
    curGameIdx = getFirstIncompleteGameIdx(curDayNum);
  }

  const strip = document.getElementById('dayStrip');
  strip.innerHTML = '';

  DAYS_21.forEach(item => {
    const btn = document.createElement('button');
    const done = isDayFullyDone(item.day);
    const unlocked = isDayUnlocked(item.day);
    const icon = done ? '✅ ' : (!unlocked ? '🔒 ' : '');
    btn.id = 'dayChip_' + item.day;
    btn.className = 'day-chip'
      + (item.day === curDayNum ? ' active' : '')
      + (done ? ' done' : '')
      + (!unlocked ? ' locked' : '');
    btn.innerHTML = icon + 'দিন ' + toBnDigits(item.day);
    btn.onclick = () => selectDay(item.day, true);
    strip.appendChild(btn);
  });

  const calBtn = document.getElementById('btnToggleCalGrid');
  if (calBtn) {
    calBtn.innerHTML = primaryCalOpen ? '🗓️ বন্ধ' : '🗓️ ক্যালেন্ডার';
  }

  const primaryCalEl = document.getElementById('primaryCalGridWrap');
  if (primaryCalEl) {
    if (primaryCalOpen) {
      primaryCalEl.style.display = 'block';
      primaryCalEl.innerHTML = `
        <div class="cal-grid-subtitle">মা, যেকোনো দিন বেছে নাও:</div>
        <div id="primaryCalendarGrid" class="calendar-grid">${buildCalendarGridCellsHtml(DAYS_21, 'p1CalCell')}</div>
      `;
    } else {
      primaryCalEl.style.display = 'none';
      primaryCalEl.innerHTML = '';
    }
  }

  const d = findDayObj(curDayNum);
  curDayNum = d.day;
  if (curGameIdx < 0 || curGameIdx >= d.agendas.length) curGameIdx = 0;
  const stage = document.getElementById('activeDayStage');

  let tilesHtml = '';
  d.agendas.forEach((ag, idx) => {
    const isDone = !!doneMap[d.day + '_' + idx];
    const isAct = (!showAllGamesInDay && idx === curGameIdx);
    const shortLbl = ag.short_bn || GAME_SHORT_LABELS[idx] || ag.category;
    const accent = ag.accent || GAME_ACCENTS[idx] || 'terra';
    tilesHtml += `
      <button id="gameTile_${d.day}_${idx}" data-accent="${accent}" class="game-tile ${isAct ? 'active' : ''} ${isDone ? 'done-tile' : ''}" onclick="selectGame(${idx}, true)">
        <span class="game-tile-lbl">${isDone ? '✅ ' : ''}${shortLbl}</span>
      </button>
    `;
  });

  let agendasHtml = '';
  if (showAllGamesInDay) {
    d.agendas.forEach((ag, idx) => {
      agendasHtml += buildAgendaCardHtml(d, ag, idx);
    });
  } else {
    const activeAg = d.agendas[curGameIdx] || d.agendas[0];
    agendasHtml = buildAgendaCardHtml(d, activeAg, curGameIdx) + `
      <div class="game-stepper-row">
        <button id="prevGameBtn" class="ag-btn" ${curGameIdx <= 0 ? 'disabled' : ''} onclick="selectGame(${curGameIdx - 1}, true)">⬅️ আগের খেলা</button>
        <button id="nextGameBtn" class="ag-btn" ${curGameIdx >= d.agendas.length - 1 ? 'disabled' : ''} onclick="selectGame(${curGameIdx + 1}, true)">পরের খেলা ➡️</button>
      </div>
    `;
  }

  const atFirstDay = d.day <= 1;
  const atLastDay = d.day >= ALL_DAYS.length;
  const nextUnlocked = !atLastDay && isDayUnlocked(d.day + 1);
  const nextBtnCls = (!atLastDay && !nextUnlocked) ? 'ag-btn locked-btn' : 'ag-btn';
  const nextBtnLabel = atLastDay ? 'পরের দিন ➡️' : (nextUnlocked ? 'পরের দিন ➡️' : '🔒 পরের দিন');

  stage.innerHTML = `
    <div class="day-hero-card">
      <div class="day-hero-top">
        <div class="day-hero-badge">দিন ${toBnDigits(d.day)} • ${d.phase}</div>
      </div>
      <div class="day-hero-title">${d.title_bn}</div>
      <details class="game-sub-drawer" style="margin-bottom:10px;">
        <summary class="game-sub-summary">🌸 আজকের কথা পড়ো (ঐচ্ছিক) ▾</summary>
        <div class="day-hero-summary" style="margin-top:8px;">${d.summary_bn}</div>
      </details>
      <button id="btnDayMainPlay" class="big-voice-btn" data-default-label="🔊 আজকের কথা শোনো" onclick="toggleDayOverviewAudio()">
        🔊 আজকের কথা শোনো
      </button>
      <div class="day-prev-next-row">
        <button id="prevDayBtn" class="ag-btn" style="flex:1;" ${atFirstDay ? 'disabled' : ''} onclick="selectDay(${d.day - 1}, true)">⬅️ আগের দিন</button>
        <button id="nextDayBtn" class="${nextBtnCls}" style="flex:1;" ${atLastDay ? 'disabled' : ''} onclick="selectDay(${d.day + 1}, true)">${nextBtnLabel}</button>
      </div>
    </div>

    ${buildProactiveAgentCardHtml(d)}
    ${buildDailyDelightCardHtml(d)}

    <div class="game-nav-card">
      <div class="game-nav-header">
        <span class="game-nav-title">🎯 আজকের খেলা:</span>
        <button id="toggleAllGamesBtn" class="view-mode-toggle" onclick="toggleShowAllGames()">
          ${showAllGamesInDay ? '🎯 ১টি করে' : '📜 সবগুলো'}
        </button>
      </div>
      <div class="game-grid-6" data-count="${d.agendas.length}">${tilesHtml}</div>
    </div>

    <div class="agenda-stack">${agendasHtml}</div>
  `;
  attachLiveStreamToVideoElement();
  preloadOpenGameAudio(d, curGameIdx);
  syncAllAudioButtonsUI(!audioEl.paused);
}

const TV_HUB_CHANNELS = [
  {
    icon: '😂',
    title_bn: 'গোপাল ভাঁড় ও মহারাজ কৃষ্ণচন্দ্রের হাসির গল্প',
    desc_bn: 'নদিয়ার রাজা কৃষ্ণচন্দ্র ও গোপাল ভাঁড়ের নিষ্পাপ, পেট ফাটা হাসির কার্টুন ও গল্প',
    query: 'Gopal Bhar Bengali comedy episodes full',
    accent: 'amber'
  },
  {
    icon: '🪷',
    title_bn: 'ননীচোরা বালগোপাল, জগন্নাথদেব ও ভোলানাথের মিষ্টি লীলা',
    desc_bn: 'যুদ্ধ বা মারামারি ছাড়া ভগবানের আদুরে ঘরোয়া লীলা, পুরীর জগন্নাথ ও কৈলাসের গল্প',
    query: 'Bala Gopala makhan churi Puri Jagannath Shiva Parvati Ganesh sweet Bengali story',
    accent: 'rose'
  },
  {
    icon: '🐘',
    title_bn: 'আদুরে হাতির ছানা, বিড়ালছানা ও পশুপাখির মজার ভিডিও',
    desc_bn: 'ছোট্ট হাতির ছানা, বাছুর, বিড়ালছানা, টিয়াপাখি ও ভোঁদড় ছানাদের মিষ্টি দুষ্টুমি',
    query: 'cute baby elephant kitten calf parrot funny animal videos',
    accent: 'emerald'
  },
  {
    icon: '🎬',
    title_bn: 'উত্তম-সুচিত্রার চিরকালের বাংলা ছবি',
    desc_bn: 'হারানো সুর, সপ্তপদী, পথে হলো দেরী ও পুরনো দিনের সেরা বাংলা সিনেমা',
    query: 'Uttam Suchitra classic Bengali full movie',
    accent: 'terra'
  },
  {
    icon: '🤣',
    title_bn: 'ভানু বন্দ্যোপাধ্যায় ও জহর রায়ের হাসির ছবি',
    desc_bn: 'যমালয়ে জীবন্ত মানুষ, সাড়ে চুয়াত্তর ও ভানু-জহরের পেট ফাটা হাসির দৃশ্য',
    query: 'Bhanu Bandyopadhyay Jahar Roy Bengali comedy scenes movie',
    accent: 'amber'
  },
  {
    icon: '🎵',
    title_bn: 'হেমন্ত মুখোপাধ্যায় ও সন্ধ্যা মুখোপাধ্যায়ের গান',
    desc_bn: 'দুপুর বা বিকেলের শান্ত সময়ে শোনার মতো চিরসবুজ বাংলা আধুনিক গান',
    query: 'Hemanta Mukherjee Sandhya Mukherjee Bengali evergreen songs jukebox',
    accent: 'emerald'
  },
  {
    icon: '🎶',
    title_bn: 'মান্না দে ও রবীন্দ্রসঙ্গীতের শান্ত আসর',
    desc_bn: 'কফি হাউসের সেই আড্ডাটা ও মন ভালো করা রবীন্দ্রসঙ্গীতের ডালি',
    query: 'Manna Dey Rabindra Sangeet Bengali songs jukebox',
    accent: 'indigo'
  },
  {
    icon: '🎧',
    title_bn: 'বাংলা অডিও গল্প (রবীন্দ্রনাথ ও শরৎচন্দ্র)',
    desc_bn: 'চোখ বুজে শুয়ে শুয়ে শোনার মতো ছোটগল্প ও শ্রুতিনাটক',
    query: 'Rabindranath Tagore Sarat Chandra Bengali audio story Golpo',
    accent: 'plum'
  },
  {
    icon: '🛕',
    title_bn: 'দক্ষিণেশ্বর, বেলুড় মঠ ও মা সারদা জয়রামবাটী',
    desc_bn: 'মা সারদার জীবনকথা, দক্ষিণেশ্বরের আরতি ও ভক্তিমূলক কথা ও গান',
    query: 'Maa Sarada Jayrambati Dakshineswar Belur Math Bengali',
    accent: 'rose'
  },
  {
    icon: '🍲',
    title_bn: 'বাংলার ঘরোয়া রান্না ও গ্রামের সকাল',
    desc_bn: 'সাবেকি বাঙালি রান্না, ঠাকুরবাড়ির পদ ও শান্ত গ্রামের ভিডিও',
    query: 'traditional Bengali recipe cooking village vlog',
    accent: 'emerald'
  },
  {
    icon: '📺',
    title_bn: 'দাদাগিরি ও দিদি নাম্বার ১-এর মজার পর্ব',
    desc_bn: 'সৌরভ গাঙ্গুলী ও রচনা ব্যানার্জীর সাথে হাসি-গল্পের ঘরোয়া আসর',
    query: 'Didi No 1 Dadagiri Bengali episode',
    accent: 'terra'
  }
];

function renderTvView() {
  const stage = document.getElementById('tvHubStage');
  if (!stage) return;
  const cardsHtml = TV_HUB_CHANNELS.map((ch, idx) => {
    const url = 'https://www.youtube.com/results?search_query=' + encodeURIComponent(ch.query);
    return `
      <a id="tvCard_${idx}" class="tv-channel-card" data-accent="${ch.accent}" href="${url}" target="_blank" rel="noopener noreferrer" onclick="stopAllAudio()">
        <div class="tv-card-icon">${ch.icon}</div>
        <div class="tv-card-body">
          <div class="tv-card-title">${ch.title_bn}</div>
          <div class="tv-card-desc">${ch.desc_bn}</div>
          <div class="tv-card-cta">▶️ এক ছোঁয়ায় ইউটিউবে দেখো</div>
        </div>
      </a>
    `;
  }).join('');

  stage.innerHTML = `
    <div class="day-hero-card">
      <div class="day-hero-badge">📺 মায়ের নিজের টিভি ও গানের ঘর</div>
      <div class="day-hero-title">শুধু একটা বোতামে ছুঁয়ে দেখো বা শোনো</div>
      <div class="day-hero-summary" style="margin-bottom:0;">
        মা, এখানে কিছু টাইপ করতে বা মুখে বলতে হবে না। যেটা দেখতে বা শুনতে ইচ্ছে করছে, শুধু সেই কার্ডটায় একবার ছুঁলেই সরাসরি ইউটিউবে খুলে যাবে!
      </div>
    </div>
    <div class="tv-hub-grid">${cardsHtml}</div>
  `;
}
