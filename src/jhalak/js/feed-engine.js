/* ============================================================================
   ✨ ঝলক (JHALAK) — MODULE 1B: MULTI-CATEGORY ENRICHMENT & FEED ENGINE
   ----------------------------------------------------------------------------
   Builds 152 long-form, multi-section scrollable pages across 8 categories:
   - gods (🪷 ভগবান — 18 pages)
   - laugh (😂 হাসি — 16 pages)
   - calm (🦋 শান্তি — 24 pages)
   - curiosity (🔍 কৌতূহল — 18 pages)
   - music (🎵 গান — 21 pages with Song Inspiration & Right Question Hook)
   - english (🔤 ইংরেজি — 25 pages of Simple English Words Learn)
   - hindi (🗣️ হিন্দি — 16 pages of Day-to-Day Hindi Conversation)
   - tv (📺 টিভি — 14 Curated TV & Cinema Channels inside Reels)
   Every page points to its dedicated full-content Aoede MP3 in `audio/jhalak/reels/<id>.mp3`.
   ============================================================================ */

const JHALAK_AUDIO_BASE = 'https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/audio/jhalak/reels/';

const ENGLISH_WORD_DICTIONARY = {
  COMFORTABLE: { pron: 'কমফোর্টেবল', mean: 'আরামদায়ক ও স্বস্তিদায়ক', ex: 'This chair is very comfortable. (দিস চেয়ার ইজ ভেরি কমফোর্টেবল — এই চেয়ারটা খুব আরামদায়ক।)' },
  'THANK YOU': { pron: 'থ্যাঙ্ক ইউ', mean: 'অনেক ধন্যবাদ', ex: 'Thank you for the warm tea. (থ্যাঙ্ক ইউ ফর দ্য ওয়ার্ম টি — গরম চায়ের জন্য ধন্যবাদ।)' },
  PEACEFUL: { pron: 'পিসফুল', mean: 'শান্তিপূর্ণ ও নিরিবিলি', ex: 'The morning is very peaceful. (দ্য মর্নিং ইজ ভেরি পিসফুল — সকালটা খুব শান্তিপূর্ণ।)' },
  ACTUALLY: { pron: 'অ্যাকচুয়ালি', mean: 'আসলে বা সত্যি বলতে', ex: 'Actually, I like light food. (অ্যাকচুয়ালি, আই লাইক লাইট ফুড — আসলে আমি হালকা খাবার পছন্দ করি।)' },
  PREFER: { pron: 'প্রেফার', mean: 'বেশি পছন্দ করা', ex: 'I prefer warm water. (আই প্রেফার ওয়ার্ম ওয়াটার — আমি হালকা গরম জল বেশি পছন্দ করি।)' },
  PLEASE: { pron: 'প্লিজ', mean: 'অনুগ্রহ করে', ex: 'Please come in and sit down. (প্লিজ কাম ইন অ্যান্ড সিট ডাউন — অনুগ্রহ করে ভেতরে এসে বসুন।)' },
  WONDERFUL: { pron: 'ওয়ান্ডারফুল', mean: 'চমৎকার বা অপূর্ব', ex: 'This song is wonderful! (দিস সং ইজ ওয়ান্ডারফুল — এই গানটা সত্যিই অপূর্ব!)' },
  CHOICE: { pron: 'চয়েস', mean: 'নিজের পছন্দ বা নির্বাচন', ex: 'Fresh fruit is my first choice. (ফ্রেশ ফ্রুট ইজ মাই ফার্স্ট চয়েস — তাজা ফলই আমার প্রথম পছন্দ।)' },
  DEFINITELY: { pron: 'ডেফিনিটলি', mean: 'অবশ্যই বা নিশ্চিতভাবে', ex: 'I will definitely go today. (আই উইল ডেফিনিটলি গো টুডে — আমি আজ অবশ্যই যাব।)' },
  EASY: { pron: 'ইজি', mean: 'সহজ ও সরল', ex: 'Speaking simple English is easy. (স্পিকিং সিম্পল ইংলিশ ইজ ইজি — সহজ ইংরেজি বলা একদম সোজা।)' },
  RELAX: { pron: 'রিল্যাক্স', mean: 'চাপ ছেড়ে বিশ্রাম ও আরাম করা', ex: 'I want to relax in the afternoon. (আই ওয়ান্ট টু রিল্যাক্স ইন দ্য আফটারনুন — আমি দুপুরে একটু আরাম করতে চাই।)' },
  MANAGE: { pron: 'ম্যানেজ', mean: 'সুন্দরভাবে নিজে সামলে নেওয়া', ex: 'Do not worry, I can manage. (ডু নট ওয়ারি, আই ক্যান ম্যানেজ — চিন্তা কোরো না, আমি সামলে নিতে পারব।)' }
};

function stripGeminiBoilerplate(txt) {
  return String(txt || '')
    .replace(/টাইপ করে গান খোঁজার কোনো ঝামেলা নেই।[^।]*।/g, '')
    .replace(/ফোনের জেমিনির ইউটিউব মিউজিকের সাথে সরাসরি যোগ আছে[^।]*।/g, '')
    .replace(/ইউটিউব মিউজিকে গান চালানো এখন তোমার কাছে একদম চেনা কাজ।/g, '')
    .replace(/গানের পুরো নাম মনে না থাকলেও জেমিনি ইউটিউব মিউজিকে ঠিক গানটা খুঁজে বাজিয়ে দিতে পারে।/g, '')
    .replace(/প্রথম দিনের মতোই আজ আবার মুখে এক লাইনে বলে ইউটিউব মিউজিকে/g, 'আজ')
    .replace(/নিজের গলায় ইউটিউব মিউজিকে গানটা চালিয়ে শোনো এবং/g, 'এই অমর গানটি শুনে')
    .replace(/ইউটিউব মিউজিকে গানটা চালিয়ে শোনো এবং/g, 'এই গানটি শুনে')
    .replace(/জেমিনির কাছ থেকে[^।]*শোনো।/g, 'এই অপূর্ব রহস্যের কথা জেনে নাও।')
    .replace(/জেমিনির কাছে[^।]*শোনো।/g, 'এর সুন্দর ইতিহাসটি জেনে নাও।')
    .replace(/জেমিনিকে বলে শোনাও!?/g, 'মনের আনন্দে একবার বলো!')
    .replace(/জেমিনিকে বলো!?/g, 'সহজভাবে বলো!')
    .replace(/জেমিনির সাথে[^।]*।/g, '')
    .replace(/জেমিনি,?\s*(শোনো—?)?\s*/gi, '')
    .trim();
}

function buildSongDeepMeaning(ag) {
  const rawPrompt = String(ag.prompt_bn || '');
  const m = rawPrompt.match(/‘([^’]+)’/);
  const songName = m ? m[1] : String(ag.title_bn || '');
  const cleanDetail = stripGeminiBoilerplate(ag.detail_bn);

  const songHooks = [
    {
      match: /এই রাত তোমার আমার/,
      story: '১৯৫৯ সালের ‘দীপ জ্বেলে যাই’ ছবির এই কালজয়ী গানটি গেয়েছেন ও সুর করেছেন হেমন্ত মুখোপাধ্যায় এবং কথা লিখেছেন গৌরীপ্রসন্ন মজুমদার। শুধুমাত্র মৃদু শিস আর পিয়ানোর ছোঁয়ায় রাতের নিস্তব্ধতাকে এমন মায়াবী রূপ আর কোনো বাংলা গানে দেওয়া হয়নি।',
      meaning: 'গানের কথায় রাত শুধু ঘড়ির সময় নয়—রাত হলো সংসারের সব কোলাহল থেমে যাওয়ার পর নিজের মনের সবচেয়ে প্রিয় মানুষ ও শান্ত স্মৃতির সাথে একান্তে কথা বলার আশ্রয়।',
      hook_q: '💡 গানের অর্থ বোঝার সঠিক প্রশ্ন: এই গানে হেমন্ত মুখোপাধ্যায় কেন শুরুতেই যন্ত্রসঙ্গীতের বদলে কেবল মিষ্টি ‘শিস’ ব্যবহার করেছিলেন?',
      hook_a: '🎵 কারণ গভীর রাতে নিস্তব্ধ ঘরে একা বসে মানুষ যখন প্রিয়জনের কথা ভাবে, তখন তার মনের ভেতর থেকে আপনাআপনি যেমন সুরের গুঞ্জন ওঠে—সেই অকৃত্রিম মায়া ফুটিয়ে তুলতেই এই শিসের সুর!'
    },
    {
      match: /একদিন পাখি উড়ে যাবে/,
      story: 'কিশোর কুমারের দরাজ কণ্ঠে গাওয়া এই গানটি মানুষের জীবন ও মনের চিরন্তন মুক্তির গান। সংসারের হাজারো নিয়ম ও বাঁধনের মাঝেও মানুষের মন যে আসলে খোলা আকাশের পাখির মতো মুক্ত, এই গানে সেই সত্যই ফুটে উঠেছে।',
      meaning: 'পাখি যেমন খাঁচার মায়া কাটিয়ে নীল আকাশে ডানা মেলে দেয়, মানুষের মনও তেমনই সব তুচ্ছ দুশ্চিন্তা পেরিয়ে আনন্দের আকাশে উড়ে যেতে চায়।',
      hook_q: '💡 গানের অর্থ বোঝার সঠিক প্রশ্ন: এই গানে ‘পাখি’ বলতে কবি আসলে আমাদের জীবনের কোন জিনিসটিকে বুঝিয়েছেন?',
      hook_a: '🎵 ‘পাখি’ হলো আমাদের প্রাণ ও মুক্ত মন—যা কোনো ছোটখাটো সংসারের হিসাব বা দুশ্চিন্তার খাঁচায় আটকে থাকার জন্য তৈরি হয়নি!'
    },
    {
      match: /মায়ের পায়ের জবা/,
      story: 'পান্নালাল ভট্টাচার্যের কণ্ঠে এই শ্যামাসঙ্গীতটি শুনলে ভক্তিতে চোখ ভিজে আসে। সাধক কবি এখানে বনের সাধারণ জবা ফুলের সাথে মানুষের মনের তুলনা করেছেন।',
      meaning: 'জবা ফুল যেমন কোনো ফলের আশা না করে কেবল মা কালীর চরণে ফুটেই সার্থক হয়, মানুষের মনও যখন সব অহংকার ও ভয় ঝেড়ে ফেলে সরল ভক্তিতে ফুটে ওঠে, তখনই জীবন সুন্দর হয়।',
      hook_q: '💡 গানের অর্থ বোঝার সঠিক প্রশ্ন: কবি কেন মনকে অন্য কোনো ফুল না বলে ঠিক ‘মায়ের পায়ের জবা’ হয়েই ফুটতে বলেছেন?',
      hook_a: '🎵 কারণ লাল জবা হলো মায়ের সবচেয়ে প্রিয় ও নিঃস্বার্থ ভক্তির প্রতীক—যে ফুল নিজের জন্য কিছু না চেয়ে পুরোপুরি মায়ের চরণে সমর্পিত থাকে!'
    },
    {
      match: /ও নদীরে|এই যে নদী/,
      story: 'হেমন্ত মুখোপাধ্যায়ের গাওয়া নদী-কেন্দ্রিক এই গানগুলো বাংলার প্রকৃতি ও জীবনদর্শনের অমূল্য সম্পদ। নদীর বয়ে চলার সাথে মানুষের জীবনের সুখ-দুঃখের প্রবাহ এক হয়ে গেছে।',
      meaning: 'নদী যেমন পথে পাথর বা বাঁক এলেও থেমে থাকে না, সব পেছনে ফেলে সাগরের দিকে এগিয়ে চলে—মানুষের জীবনও তেমনই পুরনো কষ্ট ধরে না রেখে সামনের আনন্দের দিকে বয়ে চলে।',
      hook_q: '💡 গানের অর্থ বোঝার সঠিক প্রশ্ন: গানের কথায় নদীকে কেন মানুষের জীবনের সবচেয়ে বড় শিক্ষক বলা হয়েছে?',
      hook_a: '🎵 কারণ নদী শেখায়—থেকে গেলে জল ঘোলা হয়, আর সব বাধা পেরিয়ে বয়ে চললেই জীবন স্বচ্ছ ও আনন্দময় থাকে!'
    },
    {
      match: /কফি হাউসের/,
      story: 'গৌরীপ্রসন্ন মজুমদারের লেখা, সুপর্ণকান্তি ঘোষের সুর এবং মান্না দে-র কণ্ঠে গাওয়া ‘কফি হাউসের সেই আড্ডাটা আজ আর নেই’ বাংলা গানের ইতিহাসে এক জীবন্ত মহাকাব্য।',
      meaning: 'সময় বদলে যায়, মানুষ জীবিকার টানে ছড়িয়ে পড়ে চারদিকে, কিন্তু যৌবনের নিখাদ বন্ধুত্ব আর একসাথে কাটানো সোনালী মুহূর্তগুলো চিরকাল মনের মণিকোঠায় অমর হয়ে থাকে।',
      hook_q: '💡 গানের অর্থ বোঝার সঠিক প্রশ্ন: কফি হাউসের আড্ডা ফুরিয়ে যাওয়ার কথা বললেও এই গানটি শুনলে আমাদের মন কেন ভালোবাসায় ভরে ওঠে?',
      hook_a: '🎵 কারণ গানটি আমাদের মনে করিয়ে দেয় যে পুরনো বন্ধু ও প্রিয় মানুষদের সাথে কাটানো প্রতিটি হাসির মুহূর্তই জীবনের আসল অমূল্য সম্পদ!'
    }
  ];

  const matched = songHooks.find(h => h.match.test(songName));
  return {
    song_name: songName,
    story_bn: matched
      ? matched.story + '\n\n' + cleanDetail
      : cleanDetail + '\n\nবাংলা গানের স্বর্ণযুগে ‘' + songName + '’ গানটি তার অনবদ্য কথা ও সুরের মাধুর্যে প্রজন্মের পর প্রজন্ম ধরে শ্রোতাদের হৃদয়ে চিরস্থায়ী জায়গা করে নিয়েছে।',
    meaning_bn: matched
      ? matched.meaning
      : '‘' + songName + '’ গানের প্রতিটি ছত্রে প্রকৃতির ছবি এবং মানুষের মনের সূক্ষ্ম অনুভূতির এক অপূর্ব মেলবন্ধন ঘটেছে। চোখ বুজে শুনলে মনে হয় সুর যেন মনের সব ক্লান্তি ধুয়ে দিচ্ছে।',
    hook_q_bn: matched
      ? matched.hook_q
      : '💡 গানের অর্থ বোঝার সঠিক প্রশ্ন: ‘' + songName + '’ গানটি শোনার সময় কোন মূল প্রশ্নটি মনে রাখলে এর গভীর ভাবার্থ সহজেই ধরা দেয়?',
    hook_a_bn: matched
      ? matched.hook_a
      : '🎵 নিজেকে প্রশ্ন করো: “কবি এই গানের প্রকৃতির উপমার আড়ালে আমাদের মনের কোন শান্ত ও চিরন্তন অনুভূতির কথা বলছেন?”—দেখবে গানের প্রতিটি লাইন ছবির মতো স্পষ্ট হয়ে উঠবে!'
  };
}

function buildEnglishSimpleLearnCard(ag, dNum, agIdx) {
  const id = 'd' + dNum + '_g' + agIdx;
  const rawSentence = String(ag.prompt_bn || '').replace(/^জেমিনি,?\s*(শোনো—?)?\s*/i, '').trim();
  const cleanIntro = stripGeminiBoilerplate(ag.detail_bn);
  const foundWords = [];
  Object.keys(ENGLISH_WORD_DICTIONARY).forEach(w => {
    if (ag.title_bn.toUpperCase().includes(w) || rawSentence.toUpperCase().includes(w)) {
      foundWords.push({ word: w, ...ENGLISH_WORD_DICTIONARY[w] });
    }
  });
  if (foundWords.length === 0) {
    foundWords.push(
      { word: 'COMFORTABLE', ...ENGLISH_WORD_DICTIONARY.COMFORTABLE },
      { word: 'PLEASE', ...ENGLISH_WORD_DICTIONARY.PLEASE }
    );
  }

  const wordBreakdown = foundWords.map(item =>
    `• ${item.word} (${item.pron}) — অর্থ: ${item.mean}\n  উদাহরণ: ${item.ex}`
  ).join('\n\n');

  return {
    id: id,
    vibe: 'english',
    badge_bn: '🔤 ইংরেজি',
    title_bn: ag.title_bn,
    sections: [
      {
        heading_bn: '📖 আজকের সহজ ইংরেজি শব্দ ও বাংলা উচ্চারণ',
        body_bn: cleanIntro + '\n\n' + wordBreakdown,
        tone: 'story'
      },
      {
        heading_bn: '💬 রোজকার জীবনে সহজ বাক্যে ব্যবহার',
        body_bn: `আজকের মূল ইংরেজি বাক্য:\n“${rawSentence}”\n\nরোজকার কথাবার্তায় এই বাক্যটি যেভাবে ব্যবহার করবে:\n১. বাড়িতে বা বাইরে নিজের আরাম ও পছন্দ জানাতে একদম শান্ত গলায় এই ছোট্ট বাক্যটি বলো।\n২. পুরো লম্বা বাক্য মনে না এলেও শুধু মূল ইংরেজি শব্দটি (${foundWords.map(w => w.word).join(' / ')}) বাংলা কথার মাঝে ব্যবহার করলেই কথাটা খুব সুন্দর ও আধুনিক শোনায়!`,
        tone: 'hitch'
      },
      {
        heading_bn: '🌟 মনে রাখার সহজ কৌশল',
        body_bn: 'ইংরেজি কোনো পরীক্ষার বিষয় নয় মা—যখনই চা খাবে, বিশ্রাম নেবে বা কারো সাথে কথা বলবে, তখন খেলার ছলে আজকের শব্দগুলো মুখে একবার উচ্চারণ করো।',
        tone: 'extra'
      }
    ],
    hitch_label_bn: '💬 রোজকার ইংরেজি বাক্য',
    hitch_bn: rawSentence,
    curiosity_q_bn: '🔮 চটপট ঝালাই: আজকের মূল ইংরেজি বাক্যটি মুখে কীভাবে বলবে?',
    curiosity_a_bn: '✨ “' + rawSentence + '” — একদম সহজ ও সাবলীল!',
    audio_url: JHALAK_AUDIO_BASE + id + '.mp3',
    story_end: 0,
    yt_query: '',
    yt_label_bn: ''
  };
}

function buildHindiConversationCard(ag, id) {
  const spokenLine = String(ag.prompt_bn || '').replace(/^জেমিনি,?\s*(শোনো—?)?\s*/i, '').trim();
  const cleanIntro = stripGeminiBoilerplate(ag.detail_bn);

  return {
    id: id,
    vibe: 'hindi',
    badge_bn: '🗣️ হিন্দি',
    title_bn: ag.title_bn,
    sections: [
      {
        heading_bn: '🗣️ রোজকার পরিস্থিতি ও হিন্দি কথোপকথন',
        body_bn: `${cleanIntro}\n\nপ্রাত্যহিক জীবনের কথোপকথন (বাংলা হরফে উচ্চারণ ও অর্থ):\n• তুমি বলবে: “${spokenLine}”\n• সামনের মানুষটি খুশি হয়ে উত্তর দেবে: “হাঁ দিদি, আপ বড়িয়া বোল রহে হ্যাঁয়! সব ঠিক হ্যায়।” (হ্যাঁ দিদি, আপনি খুব সুন্দর বলছেন! সব ঠিক আছে।)\n• তুমি হাসিমুখে যোগ করতে পারো: “চলিযে, মিলকর বহুত অচ্ছা লগা!” (চলুন, দেখা হয়ে খুব ভালো লাগল!)`,
        tone: 'story'
      },
      {
        heading_bn: '🔑 প্রতিদিনের কাজের হিন্দি শব্দভাণ্ডার',
        body_bn: '• ক্যায়া চল রহা হ্যায়? — কী চলছে / কেমন কাটছে?\n• বৈঠিযে না — বসুন না\n• থোড়া গপশপ করতে হ্যাঁয় — একটু গল্পগুজব করি\n• কাফি বেহতর — আগের চেয়ে অনেক ভালো\n• মেরে খয়াল সে — আমার মনে হয় / আমার মতে',
        tone: 'hitch'
      },
      {
        heading_bn: '😊 সাবলীলভাবে হিন্দি বলার ঘরোয়া টিপস',
        body_bn: 'হায়দরাবাদে বা বাইরে অবাঙালি প্রতিবেশীদের সাথে কথা বলার সময় ব্যাকরণের চিন্তা একদম করবে না মা। তোমার মিষ্টি হাসির সাথে এই ঘরোয়া হিন্দি লাইনগুলো বললেই সবাই আপন হয়ে যাবে!',
        tone: 'extra'
      }
    ],
    hitch_label_bn: '🗣️ আজকের হিন্দি সংলাপ',
    hitch_bn: spokenLine,
    curiosity_q_bn: '🔮 কথার জাদু: আজকের এই পরিস্থিতিতে প্রথম হিন্দি লাইনটি কী বলবে?',
    curiosity_a_bn: '🌸 “' + spokenLine + '”',
    audio_url: JHALAK_AUDIO_BASE + id + '.mp3',
    story_end: 0,
    yt_query: '',
    yt_label_bn: ''
  };
}

function buildAllJhalakReels() {
  const byCat = {
    gods: [],
    laugh: [],
    calm: [],
    curiosity: [],
    music: [],
    english: [],
    hindi: [],
    tv: []
  };

  // 1. Curated Gods Stories (15)
  JHALAK_GODS_STORIES.forEach(gs => {
    byCat.gods.push({
      id: gs.id,
      vibe: 'gods',
      badge_bn: gs.badge_bn,
      title_bn: gs.title_bn,
      sections: [
        { heading_bn: '📖 অমৃত লীলা ও সম্পূর্ণ গল্প', body_bn: gs.story_bn, tone: 'story' },
        { heading_bn: gs.hitch_title_bn, body_bn: gs.hitch_bn, tone: 'hitch' },
        { heading_bn: gs.extra_title_bn, body_bn: gs.extra_bn, tone: 'extra' }
      ],
      hitch_label_bn: gs.hitch_title_bn,
      hitch_bn: gs.hitch_bn,
      curiosity_q_bn: gs.curiosity_q_bn,
      curiosity_a_bn: gs.curiosity_a_bn,
      audio_url: JHALAK_AUDIO_BASE + gs.id + '.mp3',
      story_end: 0,
      yt_query: gs.yt_query,
      yt_label_bn: gs.yt_label_bn
    });
  });

  // 2. Curated Laugh Stories (16)
  JHALAK_LAUGH_STORIES.forEach(ls => {
    byCat.laugh.push({
      id: ls.id,
      vibe: 'laugh',
      badge_bn: ls.badge_bn,
      title_bn: ls.title_bn,
      sections: [
        { heading_bn: '📖 পেট ফাটা হাসির সম্পূর্ণ গল্প', body_bn: ls.story_bn, tone: 'story' },
        { heading_bn: ls.hitch_title_bn, body_bn: ls.hitch_bn, tone: 'hitch' },
        { heading_bn: ls.extra_title_bn, body_bn: ls.extra_bn, tone: 'extra' }
      ],
      hitch_label_bn: ls.hitch_title_bn,
      hitch_bn: ls.hitch_bn,
      curiosity_q_bn: ls.curiosity_q_bn,
      curiosity_a_bn: ls.curiosity_a_bn,
      audio_url: JHALAK_AUDIO_BASE + ls.id + '.mp3',
      story_end: 0,
      yt_query: ls.yt_query,
      yt_label_bn: ls.yt_label_bn
    });
  });

  // 3. Curated TV Cards (14)
  JHALAK_TV_CARDS.forEach(tv => {
    byCat.tv.push({
      id: tv.id,
      vibe: 'tv',
      badge_bn: tv.badge_bn,
      title_bn: tv.title_bn,
      sections: [
        { heading_bn: '📺 অনুষ্ঠানের বিস্তারিত পরিচয়', body_bn: tv.story_bn, tone: 'story' },
        { heading_bn: tv.hitch_title_bn, body_bn: tv.hitch_bn, tone: 'hitch' },
        { heading_bn: tv.extra_title_bn, body_bn: tv.extra_bn, tone: 'extra' }
      ],
      hitch_label_bn: tv.hitch_title_bn,
      hitch_bn: tv.hitch_bn,
      curiosity_q_bn: '🔮 টিভি গাইড: এই চ্যানেলটি কীভাবে চালু করবে?',
      curiosity_a_bn: '✨ নিচের ইউটিউব লিঙ্কে একবার ছুঁলেই সরাসরি ভিডিও চালু হয়ে যাবে!',
      audio_url: JHALAK_AUDIO_BASE + tv.id + '.mp3',
      story_end: 0,
      yt_query: tv.yt_query,
      yt_label_bn: tv.yt_label_bn
    });
  });

  // 4. Enrich Curriculum Items (Excluding tech_65 phone/camera tutorials)
  DAYS_21.forEach(d => {
    const dNum = Number(d.day) || 1;
    (d.agendas || []).forEach((ag, agIdx) => {
      const p = String(ag.pillar || '');
      if (p === 'tech_65') return;
      if (dNum === 20 && agIdx === 0) return;
      const cid = 'd' + dNum + '_g' + agIdx;

      if (p === 'english') {
        byCat.english.push(buildEnglishSimpleLearnCard(ag, dNum, agIdx));
        return;
      }
      if (p === 'hindi') {
        byCat.hindi.push(buildHindiConversationCard(ag, cid));
        return;
      }
      if (p === 'music') {
        const sInfo = buildSongDeepMeaning(ag);
        byCat.music.push({
          id: cid,
          vibe: 'music',
          badge_bn: '🎵 গান',
          title_bn: '🎵 ' + sInfo.song_name + ' — গানের গল্প ও গভীর অর্থ',
          sections: [
            { heading_bn: '🎼 গানের নেপথ্যের অনুপ্রেরণা ও ইতিহাস', body_bn: sInfo.story_bn, tone: 'story' },
            { heading_bn: '🌺 গানের কথার অপূর্ব অর্থ ও ভাবার্থ', body_bn: sInfo.meaning_bn, tone: 'hitch' },
            { heading_bn: '💡 গানের আসল অর্থ বোঝার সঠিক প্রশ্ন (The Right Hook)', body_bn: sInfo.hook_q_bn + '\n\n' + sInfo.hook_a_bn, tone: 'extra' }
          ],
          hitch_label_bn: '💡 গানের অর্থ বোঝার সঠিক প্রশ্ন',
          hitch_bn: sInfo.hook_q_bn,
          curiosity_q_bn: sInfo.hook_q_bn,
          curiosity_a_bn: sInfo.hook_a_bn,
          audio_url: JHALAK_AUDIO_BASE + cid + '.mp3',
          story_end: 0,
          yt_query: sInfo.song_name + ' Bengali song',
          yt_label_bn: '‘' + sInfo.song_name + '’ গানটি ইউটিউবে শোনো'
        });
        return;
      }

      const cleanStory = stripGeminiBoilerplate(ag.detail_bn);
      const isGodsTopic = /সারদা|রামকৃষ্ণ|রাসমণি|দক্ষিণেশ্বর|নিবেদিতা/.test(ag.title_bn);

      if (isGodsTopic) {
        byCat.gods.push({
          id: cid,
          vibe: 'gods',
          badge_bn: '🪷 ভগবান',
          title_bn: ag.title_bn,
          sections: [
            {
              heading_bn: '📖 অমৃত কথা ও অনুপ্রেরণার গল্প',
              body_bn: cleanStory + '\n\nবাংলার আধ্যাত্মিক ইতিহাসে এই ঘটনাটি আমাদের শেখায় যে মনের সরলতা, ভয়হীনতা এবং পরম ঈশ্বরের ওপর ভরসা রাখলে সংসারের কোনো বাধাই মানুষকে দমিয়ে রাখতে পারে না।',
              tone: 'story'
            },
            {
              heading_bn: '🪷 মনের শক্তি ও আশীর্বাদ',
              body_bn: 'মা সারদা ও ঠাকুর সবসময় বলতেন—নিজের মনকে ছোট কোরো না মা; তোমার ভেতরেই মায়ের অসীম শক্তি ও স্নেহের আলো রয়েছে।',
              tone: 'hitch'
            }
          ],
          hitch_label_bn: '🪷 মায়ের আশীর্বাদ',
          hitch_bn: 'নিজের মনকে সর্বদা প্রসন্ন ও ভয়হীন রাখাই ভগবানের সবচেয়ে বড় পূজা মা।',
          curiosity_q_bn: '🔮 অমৃত ভাবনা: এই জীবনকথা থেকে আমাদের প্রতিদিনের জীবনে কোন শান্তির শিক্ষাটি মেলে?',
          curiosity_a_bn: '🌸 সংসারের সব কাজের মাঝেও নিজের মনকে শান্ত, উদার ও আনন্দময় রাখা!',
          audio_url: JHALAK_AUDIO_BASE + cid + '.mp3',
          story_end: 0,
          yt_query: ag.title_bn + ' Bengali story',
          yt_label_bn: ag.title_bn
        });
        return;
      }

      if (p === 'gk_inspiring') {
        byCat.curiosity.push({
          id: cid,
          vibe: 'curiosity',
          badge_bn: '🔍 কৌতূহল',
          title_bn: ag.title_bn,
          sections: [
            {
              heading_bn: '📖 অবাক পৃথিবীর বিস্ময়কর কথা',
              body_bn: cleanStory + '\n\nআমাদের চারপাশের প্রকৃতি ও পৃথিবীর এই আশ্চর্য ঘটনাগুলো জানলে মন যেমন আনন্দে ভরে ওঠে, তেমনই নতুন কিছু জানার কৌতূহল মনকে চিরতরুণ ও সতেজ রাখে।',
              tone: 'story'
            },
            {
              heading_bn: '🔬 সহজ ভাষায় এর আসল রহস্য',
              body_bn: 'প্রকৃতি ও বিজ্ঞানের প্রতিটি নিয়মের পেছনেই রয়েছে এক আশ্চর্য ভারসাম্য। বয়স যতই হোক না কেন, প্রতিদিন এমন একটি করে নতুন বিস্ময়ের কথা জানলে মস্তিষ্ক ও মন দুটোই দারুণ চনমনে থাকে মা!',
              tone: 'hitch'
            }
          ],
          hitch_label_bn: '🌍 অবাক কৌতূহল',
          hitch_bn: 'রোজ একটি করে নতুন ও অবাক করা বিষয় জানার আনন্দ মনকে সবসময় সজীব ও তরুণ রাখে মা!',
          curiosity_q_bn: '🔮 জাদুর পর্দা খোলো: এই বিস্ময়কর বিষয়টির সবচেয়ে সুন্দর দিক কোনটি?',
          curiosity_a_bn: '✨ প্রকৃতির অসীম বুদ্ধি আর মানুষের অদম্য মনের জোর!',
          audio_url: JHALAK_AUDIO_BASE + cid + '.mp3',
          story_end: 0,
          yt_query: ag.title_bn + ' Bengali',
          yt_label_bn: ag.title_bn
        });
        return;
      }

      const calmReframe = p === 'covert_cbt'
        ? 'তাজা ও ভালো জিনিস আজই আনন্দে ব্যবহার করো মা—পুরনো বা সামান্য জিনিসের মায়ায় নিজের বর্তমানের আনন্দকে কখনো তুলে রাখবে না।'
        : (p === 'bengali_expr'
          ? 'কে কী ভাববে সেই অহেতুক সঙ্কোচ ঝেড়ে ফেলে নিজের খাবারের পছন্দ, বিশ্রামের প্রয়োজন এবং মনের কথা হাসিমুখে স্পষ্ট করে বলাই আত্মসম্মানের লক্ষণ মা।'
          : 'রানাঘাটের শৈশব থেকে শুরু করে কৌশিক ও দিদিকে মানুষ করা—তোমার জীবনের প্রতিটি অধ্যায় গর্বের ও ভালোবাসার। আজ সব পুরনো ভার নামিয়ে রেখে কেবল নিজের আনন্দে থাকো মা।');

      byCat.calm.push({
        id: cid,
        vibe: 'calm',
        badge_bn: '🦋 শান্তি',
        title_bn: ag.title_bn,
        sections: [
          {
            heading_bn: '📖 মনের গল্প ও স্মৃতির ঝাঁপি',
            body_bn: cleanStory + '\n\nসংসারের দীর্ঘ পথ চলতে চলতে অনেক সময় আমরা নিজেদের খুশি ও আরামের কথা ভুলে যাই। কিন্তু একটু থেমে নিজের মনের দিকে তাকালেই বোঝা যায়—নিজেকে ভালো রাখা এবং মনের কথা খোলাখুলি বলা কতটা আনন্দের!',
            tone: 'story'
          },
          {
            heading_bn: '🦋 মনের আরাম ও নতুন দৃষ্টিভঙ্গি',
            body_bn: calmReframe,
            tone: 'hitch'
          },
          {
            heading_bn: '🌿 আজকের শান্ত অনুভব',
            body_bn: 'তুমি, কৌশিক আর দিদি—তোমরা তিনজনই এক মাটির মানুষ। আজকের দিনটা কোনো তাড়াহুড়ো ছাড়া নিজের পছন্দের খাবার, গান আর বিশ্রামে উপভোগ করো মা।',
            tone: 'extra'
          }
        ],
        hitch_label_bn: '🦋 মনের আরাম',
        hitch_bn: calmReframe,
        curiosity_q_bn: '🔮 মনের আয়না: আজ নিজেকে কোন মিষ্টি সত্যিটা মনে করিয়ে দেবে মা?',
        curiosity_a_bn: '🌸 “আমার নিজের আরাম, তাজা খাবার ও মনের আনন্দই আজ সবার আগে!”',
        audio_url: JHALAK_AUDIO_BASE + cid + '.mp3',
        story_end: 0,
        yt_query: /রানাঘাট|শান্তিনিকেতন|দুর্গাপুজো/.test(ag.title_bn) ? ag.title_bn + ' Bengali' : '',
        yt_label_bn: ag.title_bn
      });
    });
  });

  // 5. Extra Day-to-Day Hindi Conversations (3 more -> 16 total)
  if (typeof JHALAK_EXTRA_HINDI !== 'undefined') {
    JHALAK_EXTRA_HINDI.forEach(eh => {
      byCat.hindi.push(buildHindiConversationCard(eh, eh.id));
    });
  }

  const order = ['gods', 'laugh', 'calm', 'music', 'curiosity', 'english', 'hindi', 'tv'];
  const ptr = { gods: 0, laugh: 0, calm: 0, music: 0, curiosity: 0, english: 0, hindi: 0, tv: 0 };
  const mixed = [];
  let added = true;
  while (added) {
    added = false;
    for (let i = 0; i < order.length; i++) {
      const k = order[i];
      if (ptr[k] < byCat[k].length) {
        mixed.push(byCat[k][ptr[k]++]);
        added = true;
      }
    }
  }
  return mixed;
}

const ALL_JHALAK_REELS = buildAllJhalakReels();

function jhBnNum(n) {
  return String(n).replace(/\d/g, d => '০১২৩৪৫৬৭৮৯'[d]);
}

function getJhalakCategoryCounts() {
  const counts = { all: ALL_JHALAK_REELS.length };
  JHALAK_CATEGORIES.forEach(c => {
    if (c.id !== 'all') counts[c.id] = 0;
  });
  ALL_JHALAK_REELS.forEach(r => {
    counts[r.vibe] = (counts[r.vibe] || 0) + 1;
  });
  return counts;
}

const JHALAK_CATEGORY_COUNTS = getJhalakCategoryCounts();
