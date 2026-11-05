/* ============================================================================
   ✨ ঝলক (JHALAK) — MODULE 1: DOPAMINE-HITCHING REEL ENGINE & SMART DJ MIXER
   Interleaves Pure Delight (Comedy/Gods/Animals) -> Covert CBT Hitch -> Curiosity/Songs
   with 100% Zero Tasks, Zero Exams, and Pre-Generated Aoede Bengali Audio.
   ============================================================================ */

const JHALAK_BN_DIGITS = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
function jhBnNum(val) {
  return String(val).replace(/\d/g, d => JHALAK_BN_DIGITS[Number(d)]);
}

const JHALAK_DELIGHT_REELS = [
  {
    id: 'delight_1',
    vibe: 'laugh_gods',
    badge_bn: '🦜 মা সারদা ও ঠাকুরের হাসির ঝাঁপি',
    title_bn: 'মা সারদার পোষা টিয়াপাখি ‘গঙ্গারাম’ ও ঠাকুরের গরম জিলিপির আনন্দ',
    hook_bn: 'জয়রামবাটীতে মা সারদার একটি খুব আদরের পোষা টিয়াপাখি ছিল, তার নাম ছিল ‘গঙ্গারাম’! সকাল হলেই গঙ্গারাম খাঁচা থেকে মা সারদাকে ডেকে বলতো— “মা, হরে কৃষ্ণ বলো! মা, গঙ্গারামকে একটু ছোলা-গুড় দাও!” আর দক্ষিণেশ্বরে ঠাকুর শ্রীরামকৃষ্ণ গরম জিলিপি বা সন্দেশ দেখলে ছোট্ট শিশুর মতো হাততালি দিয়ে হেসে উঠতেন।',
    hitch_label_bn: '🦋 মনের জাদু (CBT Hitch): নিষ্পাপ আনন্দ',
    hitch_bn: 'ভগবান কোনো কঠোর নিয়ম বা ভয়ের মধ্যে থাকেন না মা—নিজের পছন্দের খাবার আনন্দে খাওয়া আর শিশুর মতো প্রাণখোলা হাসির মধ্যেই ঈশ্বর থাকেন!',
    curiosity_q_bn: '🔮 বলো তো মা, মা সারদা কেন পশুপাখিদেরও নিজের সন্তানের মতো খাওয়াতেন?',
    curiosity_a_bn: '🌸 মা সারদা বলতেন— “যাদের মুখে কথা নেই, তাদের আদর করলে ভগবান সবচেয়ে বেশি খুশি হন!” তাই গঙ্গারাম টিয়াপাখিও মাকে ‘মা’ বলে ডাকতো।',
    yt_query: 'Maa Sarada Jayrambati Gangaram parrot Sri Ramakrishna sweet story Bengali'
  },
  {
    id: 'delight_2',
    vibe: 'laugh_gods',
    badge_bn: '🧈 ননীচোরা বালগোপালের আদুরে লীলা',
    title_bn: 'ননীচোরা বালগোপালের মাখন চুরি ও ছোট্ট বাছুরের পেছনে লুকানো',
    hook_bn: 'বৃন্দাবনে ছোট্ট বালগোপাল একদিন শিকের ওপর থেকে তাজা মাখন পেড়ে নিজেও খেলেন আর ছোট্ট বাঁদর ছানাদেরও খাওয়ালেন। মা যশোদা এসে যেই বললেন— “কানাই, মাখন কে খেয়েছে?” অমনি গোপাল তাঁর সারা মুখে মাখন মাখা অবস্থায় বললেন— “মা, আমি তো একফোঁটাও খাইনি, এই দুষ্টু বাছুরটা আমার মুখে মাখন মাখিয়ে দিয়েছে!”',
    hitch_label_bn: '🦋 মনের জাদু (CBT Hitch): তাজা জিনিস আজই খাও',
    hitch_bn: 'দেখো মা, স্বয়ং বালগোপালও বাসি খাবারের বদলে একদম তাজা মাখন সবার আগে খেতেন! তুমিও ফলের ঝুড়ির সবচেয়ে তাজা ফলটা আজই আনন্দে খাবে।',
    curiosity_q_bn: '🔮 জানো কি মা, মা যশোদা সব জেনেও কেন গোপালকে বকতে পারতেন না?',
    curiosity_a_bn: '🌸 কারণ সন্তানের দুষ্টুমি আর মিষ্টি হাসির কাছে মায়ের সব রাগ নিমেষে গলে জল হয়ে যায়—ঠিক যেমন কৌশিক আর দিদির হাসিতে তোমার মন ভরে যায়!',
    yt_query: 'Bala Gopala makhan churi sweet Bengali story song'
  },
  {
    id: 'delight_3',
    vibe: 'laugh_gods',
    badge_bn: '😂 নদিয়ার রাজা কৃষ্ণচন্দ্র ও গোপাল ভাঁড়',
    title_bn: 'মহারাজ কৃষ্ণচন্দ্র ও গোপাল ভাঁড়ের ‘পৃথিবীর সবচেয়ে মিষ্টি জিনিস’!',
    hook_bn: 'তোমার নিজের নদিয়া জেলার মহারাজ কৃষ্ণচন্দ্র একদিন সভায় জিজ্ঞেস করলেন— “বলো তো গোপাল, পৃথিবীর সবচেয়ে মিষ্টি জিনিস কী?” সভার পণ্ডিতেরা কেউ বললেন রসগোল্লা, কেউ বললেন মধু। কিন্তু গোপাল ভাঁড় বলল— “মহারাজ, সবচেয়ে মিষ্টি হলো মাটির কুঁজোর ঠান্ডা জল আর দুপুরের আরামের ভাতঘুম!”',
    hitch_label_bn: '🦋 মনের জাদু (CBT Hitch): বিশ্রামের রাজকীয় অধিকার',
    hitch_bn: 'দুপুরে বা বিকেলে নিজের শরীরে একটু আরাম দেওয়া আর নিশ্চিন্তে বিশ্রাম নেওয়া কোনো আলস্য নয় মা—গোপাল ভাঁড়ের কথামতো ওটাই পৃথিবীর সবচেয়ে মিষ্টি সুখ!',
    curiosity_q_bn: '🔮 বলো তো মা, রাজা কৃষ্ণচন্দ্রের রাজবাড়ি আমাদের রানাঘাট থেকে কোনদিকে?',
    curiosity_a_bn: '🌸 তোমাদের নদিয়া জেলারই কৃষ্ণনগরে! রানাঘাট থেকে ট্রেনে বা গাড়িতে একটুখানি পথ গেলেই মহারাজ কৃষ্ণচন্দ্রের সেই বিখ্যাত রাজবাড়ি।',
    yt_query: 'Gopal Bhar Maharaj Krishnachandra Bengali funny story'
  },
  {
    id: 'delight_4',
    vibe: 'laugh_gods',
    badge_bn: '🐘 আদুরে পশুপাখির মজার কীর্তি',
    title_bn: 'ছোট্ট হাতির ছানার নিজের শুঁড় চোষা ও মায়ের আঁচলের পেছনে লুকানো',
    hook_bn: 'মানুষের ছোট্ট বাচ্চারা যেমন নিজের বুড়ো আঙুল মুখে দিয়ে চুষতে থাকে, ছোট্ট হাতির ছানারাও ঠিক তেমনই নিজের লম্বা শুঁড়ের ডগাটা মুখে পুরে চুষতে ভালোবাসে! জন্মের পর প্রথম কয়েক মাস তারা নিজের শুঁড়টা সামলাতেই পারে না—হাঁটতে গিয়ে নিজের শুঁড়েই পা দিয়ে গড়িয়ে পড়ে আর মা হাতি শুঁড় দিয়ে আদর করে তাকে তুলে দেয়।',
    hitch_label_bn: '🦋 মনের জাদু (CBT Hitch): ভুল হওয়াটাই স্বাভাবিক',
    hitch_bn: 'দেখো মা, প্রকৃতির এত বড় হাতিও প্রথম প্রথম নিজের শুঁড় সামলাতে গিয়ে দশবার হোঁচট খায়! তাই ফোনে বা নতুন কাজে ভুল হওয়া একদম স্বাভাবিক ও মিষ্টি ব্যাপার।',
    curiosity_q_bn: '🔮 জানো কি মা, হাতির ছানা মন খারাপ হলে কীভাবে আদর চায়?',
    curiosity_a_bn: '🌸 ওরা মা হাতির গায়ের সাথে নিজের মাথাটা আলতো করে ঘষে দেয়, আর মা হাতি তার কান দুটো নাড়িয়ে ছানাটিকে বুকের কাছে টেনে নেয়!',
    yt_query: 'cute baby elephant playing with trunk mother elephant video'
  },
  {
    id: 'delight_5',
    vibe: 'laugh_gods',
    badge_bn: '🐿️ ভুলোমনা কাঠবিড়ালির জাদু',
    title_bn: 'ভুলোমনা কাঠবিড়ালির লুকানো বাদাম থেকেই তৈরি হয় আস্ত ফলের বাগান!',
    hook_bn: 'গাছের ডালে যে ছোট্ট ডোরাকাটা কাঠবিড়ালিরা তিড়িং-বিড়িং করে লাফায়, তারা শীতকালে খাওয়ার জন্য মাটির নিচে প্রচুর ফল আর বাদাম লুকিয়ে রাখে। কিন্তু মজার ব্যাপার হলো, তারা এতটাই ভুলোমনা যে অর্ধেক বাদাম কোথায় লুকিয়েছে তা বেমালুম ভুলে যায়! আর সেই ভুলে যাওয়া বীজগুলো থেকেই বৃষ্টির জলে শত শত নতুন ফলের গাছ জন্মায়।',
    hitch_label_bn: '🦋 মনের জাদু (CBT Hitch): ভুলে যাওয়াও আশীর্বাদ',
    hitch_bn: 'ছোটখাটো কথা বা জিনিস কোথায় রেখেছো তা ভুলে গেলে একদম মন খারাপ করবে না মা—প্রকৃতিতেও ভুলে যাওয়া থেকেই নতুন বাগান তৈরি হয়!',
    curiosity_q_bn: '🔮 বলো তো মা, কাঠবিড়ালি কীভাবে নিজের লেজটাকে ছাতার মতো ব্যবহার করে?',
    curiosity_a_bn: '🌸 রোদ বা বৃষ্টি হলে ওরা নিজেদের তুলতুলে বড় লেজটা মাথার ওপর উল্টে মেলে ধরে—যেন একদম তৈরি করা প্রাকৃতিক ছাতা!',
    yt_query: 'cute squirrel hiding nuts funny animal video'
  },
  {
    id: 'delight_6',
    vibe: 'laugh_gods',
    badge_bn: '🦦 সমুদ্রের ভোঁদড় ছানার ভালোবাসা',
    title_bn: 'সমুদ্রের ভোঁদড় ছানাদের হাত ধরাধরি করে জলের ওপর ঘুমানো',
    hook_bn: 'সমুদ্রের নীল জলে যে ছোট্ট লোমশ ভোঁদড় ছানারা (Sea Otters) থাকে, তারা জলের ওপর চিত হয়ে ভাসতে ভাসতে ঘুমায়। কিন্তু জলের ঢেউয়ে যাতে ঘুমের মধ্যে মা বা বন্ধুর কাছ থেকে ভেসে দূরে চলে না যায়, তাই তারা ঘুমানোর সময় একে অপরের ছোট্ট হাত দুটো শক্ত করে ধরে রাখে!',
    hitch_label_bn: '🦋 মনের জাদু (CBT Hitch): অটুট পরিবারের বাঁধন',
    hitch_bn: 'ঠিক এই ভোঁদড় ছানাদের মতোই তুমি, কৌশিক আর দিদি মনে মনে সবসময় একে অপরের হাত ধরে আছো মা—দূরে থাকলেও ভালোবাসার টান কখনো কমে না।',
    curiosity_q_bn: '🔮 জানো কি মা, ভোঁদড় ছানাদের বগলের নিচে একটা ছোট্ট পকেট থাকে কেন?',
    curiosity_a_bn: '🌸 ওরা সমুদ্রের তলা থেকে নিজের সবচেয়ে প্রিয় গোল পাথরটা কুড়িয়ে ওই চামড়ার পকেটে যত্ন করে রেখে দেয়!',
    yt_query: 'sea otters holding hands sleeping cute animal video'
  },
  {
    id: 'delight_7',
    vibe: 'laugh_gods',
    badge_bn: '🛕 পুরীর জগন্নাথদেবের মিষ্টি মানভঞ্জন',
    title_bn: 'পুরীর জগন্নাথদেবের এক হাঁড়ি রসগোল্লা দিয়ে মা লক্ষ্মীর অভিমান ভাঙানো!',
    hook_bn: 'রথযাত্রায় জগন্নাথদেব যখন মা লক্ষ্মীকে মন্দিরে রেখে ভাই-বোন বলরাম ও সুভদ্রাকে নিয়ে মাসির বাড়ি বেড়াতে যান, মা লক্ষ্মী তখন অভিমান করে মন্দিরের দরজা বন্ধ করে দেন! ফিরে এসে জগন্নাথদেব মা লক্ষ্মীর অভিমান ভাঙানোর জন্য এক হাঁড়ি রসগোল্লা উপহার দেন।',
    hitch_label_bn: '🦋 মনের জাদু (CBT Hitch): অভিমান ভেঙে মিষ্টি কথা',
    hitch_bn: 'সংসারে বা ভাই-বোনের মধ্যে একটু-আধটু অভিমান তো স্বয়ং জগন্নাথদেবের ঘরেও হয় মা—একটু মিষ্টি কথা আর হাসিতেই সব অভিমান গলে যায়!',
    curiosity_q_bn: '🔮 বলো তো মা, পুরীর এই রসগোল্লা উৎসবকে কী বলা হয়?',
    curiosity_a_bn: '🌸 একে বলা হয় ‘নীলাদ্রি বিজে’! রথযাত্রার শেষে এই দিনেই পুরীতে রসগোল্লা খাওয়ার মহোৎসব হয়।',
    yt_query: 'Puri Jagannath Rasagolla Niladri Bije Maa Lakshmi sweet Bengali story'
  },
  {
    id: 'delight_8',
    vibe: 'laugh_gods',
    badge_bn: '👑 গোপাল ভাঁড়ের চটজলদি বুদ্ধি',
    title_bn: 'রাজ্যে মোট ক’টা কাক আছে? গোপাল ভাঁড়ের পেট ফাটা হাসির উত্তর!',
    hook_bn: 'একদিন মহারাজ কৃষ্ণচন্দ্র জিজ্ঞেস করলেন— “গোপাল, আমাদের নদিয়া রাজ্যে ঠিক ক’টা কাক আছে?” গোপাল আঙুল গুনে বলল— “মহারাজ, নিরানব্বই হাজার নয়শো নিরানব্বইটা! যদি দেখেন কম আছে তবে জানবেন তারা পাশের রাজ্যে মামাবাড়ি বেড়াতে গেছে, আর বেশি থাকলে জানবেন তাদের আত্মীয়রা আমাদের রাজ্যে বেড়াতে এসেছে!”',
    hitch_label_bn: '🦋 মনের জাদু (CBT Hitch): সব প্রশ্নের উত্তর জানার দরকার নেই',
    hitch_bn: 'কেউ কোনো কঠিন প্রশ্ন করলে ঘাবড়ে যাওয়ার কিচ্ছু নেই মা—গোপালের মতো হালকা হাসিমুখে উড়িয়ে দেওয়াই আসল বুদ্ধিমানের কাজ!',
    curiosity_q_bn: '🔮 বলো তো মা, গোপাল ভাঁড়ের এই উত্তর শুনে মহারাজ কী করেছিলেন?',
    curiosity_a_bn: '🌸 মহারাজ কৃষ্ণচন্দ্র হেসে গড়িয়ে পড়েছিলেন এবং গোপালকে খুশি হয়ে উপহার দিয়েছিলেন!',
    yt_query: 'Gopal Bhar counting crows funny Bengali comedy'
  }
];

function classifyAgendaToVibe(ag) {
  const p = String(ag.pillar || '');
  if (p === 'covert_cbt' || p === 'personal_therapy' || p === 'bengali_expr') return 'cbt_calm';
  if (p === 'music' || p === 'gk_inspiring' || p === 'english' || p === 'hindi' || p === 'tech_65') return 'curiosity_song';
  return 'laugh_gods';
}

function buildHitchForAgenda(ag, dayNum) {
  const p = String(ag.pillar || '');
  if (p === 'covert_cbt') {
    return {
      label_bn: '🦋 মনের আরাম (Subconscious CBT Hitch)',
      text_bn: 'তাজা ও ভালো জিনিস আজই আনন্দে ব্যবহার করো মা—সামান্য দু-টাকার তলানি বা তিতো খোসার জন্য নিজের শরীর ও মনকে একফোঁটাও কষ্ট দেবে না।'
    };
  }
  if (p === 'personal_therapy') {
    return {
      label_bn: '🌸 মনের হালকা হাওয়া (Heart Release Hitch)',
      text_bn: 'তুমি, কৌশিক আর দিদি—তোমরা তিনজনই এক মাটির নরম মনের মানুষ। পুরনো সব দুশ্চিন্তা নামিয়ে রেখে আজ শুধু নিজের আনন্দে থাকো মা।'
    };
  }
  if (p === 'english') {
    return {
      label_bn: '🔤 খেলার ছলে ১টি মিষ্টি ইংরেজি কথা (Spoken Hitch)',
      text_bn: String(ag.prompt_bn || '').replace(/^জেমিনি,?\s*(শোনো—?)?\s*/i, 'মুখে শুধু একবার আনন্দে বলো: ')
    };
  }
  if (p === 'hindi') {
    return {
      label_bn: '🗣️ প্রতিবেশীর সাথে মিষ্টি হিন্দি আড্ডা (Adda Hitch)',
      text_bn: String(ag.prompt_bn || '').replace(/^জেমিনি,?\s*(শোনো—?)?\s*/i, 'হাসিমুখে আড্ডার ছলে বলো: ')
    };
  }
  if (p === 'music') {
    return {
      label_bn: '🎵 গানের সুরের জাদু (Music Dopamine Hitch)',
      text_bn: 'গানের কথাগুলোর ভেতরে যে মিষ্টি ছবি লুকিয়ে আছে, চোখ বুজে শুধু সেই সুরটুকু উপভোগ করো মা—কোনো নিয়ম মনে রাখতে হবে না।'
    };
  }
  if (p === 'tech_65') {
    return {
      label_bn: '📱 ভয়হীন জাদুর কাঠি (Zero-Fear Tech Hitch)',
      text_bn: 'ফোনের কোনো বোতামে হাত পড়লে কিচ্ছু খারাপ হয় না মা! মন্দিরের হারমোনিয়ামের মতোই ফোন ছুঁলে তবেই তো সুর বাজবে।'
    };
  }
  return {
    label_bn: '🌍 অবাক করা কৌতূহল (Curiosity Hitch)',
    text_bn: 'পৃথিবীর এই সুন্দর রহস্যগুলো জানার জন্য কোনো পড়াশোনা লাগে না মা—শুধু গল্পের মতো শুনলেই মন আনন্দে উড়ে বেড়ায়!'
  };
}

function buildCuriosityBoxForAgenda(ag) {
  const follow = String(ag.followup_prompt_bn || ag.prompt_bn || '').replace(/^জেমিনি,?\s*/i, '');
  return {
    q_bn: '🔮 এক ছোঁয়ায় জাদুর পর্দা খোলো: এর পরের মজার কথাটা কী জানো মা?',
    a_bn: '✨ ' + (follow || 'তুমি যখনই খুশি নিচের মাইক বোতামে ছুঁয়ে কল্যাণীর সাথে এই নিয়ে গল্প করতে পারো মা!')
  };
}

function buildAllJhalakReels() {
  const delights = [];
  const cbts = [];
  const curiosities = [];

  JHALAK_DELIGHT_REELS.forEach((dr, idx) => {
    const refDay = DAYS_21[idx % DAYS_21.length] || DAYS_21[0];
    const refAg = (refDay.agendas && refDay.agendas[0]) ? refDay.agendas[0] : null;
    delights.push({
      id: dr.id,
      vibe: 'laugh_gods',
      badge_bn: dr.badge_bn,
      title_bn: dr.title_bn,
      hook_bn: dr.hook_bn,
      hitch_label_bn: dr.hitch_label_bn,
      hitch_bn: dr.hitch_bn,
      curiosity_q_bn: dr.curiosity_q_bn,
      curiosity_a_bn: dr.curiosity_a_bn,
      audio_url: refDay.audio_url || (refAg ? refAg.audio_url : ''),
      story_end: 0,
      yt_query: dr.yt_query,
      day_num: refDay.day,
      ag_idx: 0
    });
  });

  DAYS_21.forEach(d => {
    const dNum = Number(d.day) || 1;
    (d.agendas || []).forEach((ag, agIdx) => {
      const vibe = classifyAgendaToVibe(ag);
      const hitch = buildHitchForAgenda(ag, dNum);
      const curBox = buildCuriosityBoxForAgenda(ag);
      const card = {
        id: 'd' + dNum + '_g' + agIdx,
        vibe: vibe,
        badge_bn: ag.category || ag.short_bn || '✨ আনন্দের ঝলক',
        title_bn: ag.title_bn,
        hook_bn: ag.detail_bn,
        hitch_label_bn: hitch.label_bn,
        hitch_bn: hitch.text_bn,
        curiosity_q_bn: curBox.q_bn,
        curiosity_a_bn: curBox.a_bn,
        audio_url: ag.audio_url || d.audio_url || '',
        story_end: Number(ag.story_end) || 0,
        yt_query: ag.title_bn + ' Bengali',
        day_num: dNum,
        ag_idx: agIdx
      };
      if (vibe === 'cbt_calm') cbts.push(card);
      else if (vibe === 'curiosity_song') curiosities.push(card);
      else delights.push(card);
    });
  });

  // Interleave in Variable-Ratio Dopamine-Hitching Pattern:
  // 1 Delight/Laugh/Gods -> 1 Hitched Covert CBT -> 1 Curiosity/Song/Spoken Spark -> repeat
  const mixed = [];
  let iD = 0, iC = 0, iQ = 0;
  while (iD < delights.length || iC < cbts.length || iQ < curiosities.length) {
    if (iD < delights.length) mixed.push(delights[iD++]);
    if (iC < cbts.length) mixed.push(cbts[iC++]);
    if (iQ < curiosities.length) mixed.push(curiosities[iQ++]);
    if (iQ < curiosities.length) mixed.push(curiosities[iQ++]);
  }
  return mixed;
}

const ALL_JHALAK_REELS = buildAllJhalakReels();
