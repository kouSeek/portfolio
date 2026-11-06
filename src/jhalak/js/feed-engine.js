/* ============================================================================
   ✨ ঝলক (JHALAK) — MODULE 1: 3-BEAT DOPAMINE-HITCHING REELS ENGINE
   ----------------------------------------------------------------------------
   Neuro-UX Architecture for Ma:
   - Beat 1 (15s Dopamine Hook): Effortless laughter, Gopal Bhar, ठाकुर-মা সারদা,
     Bala Gopala, cute animals, Ranaghat nostalgia, or golden Bengali music.
   - Beat 2 (The Hitch): Piggybacks 1 gentle Covert CBT reframe (melting kanjoosi,
     button fear, judgment fear, family stress), 1 curiosity spark, or 1 spoken line
     right when dopamine is elevated.
   - Beat 3 (1-Tap Curiosity Flip): Zero-failure tap-to-reveal magic box with
     lotus/sparkle burst.
   ============================================================================ */

const JHALAK_DELIGHT_REELS = [
  {
    id: 'delight_1',
    vibe: 'laugh_gods',
    is_music: false,
    badge_bn: '😂 হাসি',
    title_bn: 'বাটা মাছের ঝোল আর গোপাল ভাঁড়ের চশমা!',
    hook_bn: 'একদিন মহারাজ কৃষ্ণচন্দ্র গোপালকে বললেন— “গোপাল, আজ রাজবাড়িতে গরম ভাতের সাথে সর্ষে বাটা মাছের ঝোল হয়েছে, কিন্তু তোমাকে তখনি দেব যদি বলো পৃথিবীর সবচেয়ে সুন্দর দৃশ্য কী!” গোপাল এক গাল হেসে বলল— “মহারাজ, খিদের সময় কলাপাতার ওপর ধোঁয়া-ওঠা ভাত আর বাটা মাছের পেটি—এর চেয়ে সুন্দর দৃশ্য স্বর্গের দেবতারাও দেখেননি!”',
    hitch_label_bn: '🦋 মনের আরাম',
    hitch_bn: 'নিজের পছন্দের টাটকা খাবার তৃপ্তি করে খাওয়া ভগবানেরই প্রসাদ মা—শরীর ও মন খুশি থাকলে তবেই তো সব ভালো থাকবে!',
    curiosity_q_bn: '🔮 জাদুর পর্দা খোলো: মহারাজ খুশি হয়ে গোপালকে কী দিয়েছিলেন?',
    curiosity_a_bn: '🌸 মহারাজ হেসে গড়িয়ে পড়েছিলেন আর গোপালকে পুরো এক হাঁড়ি দই ও বাটা মাছের ঝোল উপহার দিয়েছিলেন!',
    yt_query: 'Gopal Bhar funny Bengali cartoon stories',
    yt_label_bn: 'গোপাল ভাঁড়ের হাসির গল্প'
  },
  {
    id: 'delight_2',
    vibe: 'laugh_gods',
    is_music: false,
    badge_bn: '🪷 ভক্তি',
    title_bn: 'মা সারদার পোষা টিয়াপাখি ‘গঙ্গারাম’-এর আবদার!',
    hook_bn: 'জয়রামবাটীতে মা সারদার একটি অত্যন্ত প্রিয় টিয়াপাখি ছিল, তার নাম ছিল গঙ্গারাম। সকাল হলেই গঙ্গারাম খাঁচা থেকে ডেকে উঠত— “মা, খোকাকে পাকা কলা দাও! মা, খোকাকে ছানা দাও!” মা সারদা নিজের হাতে তাকে ছানা আর পাকা ফলের সেরা অংশটুকু খাইয়ে তবেই নিজে প্রসাদ নিতেন।',
    hitch_label_bn: '🦋 মায়ের আশীর্বাদ',
    hitch_bn: 'মা সারদা যেমন পশুপাখিকেও পাকা ও টাটকা ফল খাওয়াতেন, তেমনই তুমিও নিজের জন্য সবসময় পাকা, মিষ্টি ও ভালো অংশটুকুই প্রথমে নেবে মা!',
    curiosity_q_bn: '🔮 জাদুর পর্দা খোলো: গঙ্গারাম টিয়াপাখি আর কী ডাকতে পারত?',
    curiosity_a_bn: '🌸 গঙ্গারাম স্পষ্ট বাংলায় “হরে কৃষ্ণ” আর “মা, মা” বলে ডাকতে পারত!',
    yt_query: 'Maa Sarada story Jayrambati Bengali',
    yt_label_bn: 'মা সারদার অমৃতকথা'
  },
  {
    id: 'delight_3',
    vibe: 'laugh_gods',
    is_music: false,
    badge_bn: '🧈 নাড়ুগোপাল',
    title_bn: 'যশোদা মায়ের হাঁড়ি থেকে ননী চুরি করে গোপালের দুষ্টুমি!',
    hook_bn: 'ছোট্ট গোপাল শিকেয় ঝোলানো মাখনের হাঁড়ি থেকে একমুঠো তাজা ননী নিয়ে নিজে খেল আর অর্ধেকটা খাইয়ে দিল পাশের এক ছোট্ট বাঁদরছানাকে! যশোদা মা এসে বকতে যেতেই গোপাল মিটমিট করে হেসে বলল— “মা, ননী কি শুধু তুলে রাখার জন্য? তাজা থাকতে থাকতেই তো আনন্দ করে খেতে হয়!”',
    hitch_label_bn: '🦋 মনের জাদু',
    hitch_bn: 'স্বয়ং ভগবানও তাজা মাখন জমিয়ে না রেখে আনন্দে খেতে ভালোবাসেন মা—তাই ভালো জিনিস ফেলে না রেখে আজই আনন্দে ব্যবহার করো!',
    curiosity_q_bn: '🔮 জাদুর পর্দা খোলো: বৃন্দাবনে গোপালের প্রিয় বন্ধু কারা ছিল?',
    curiosity_a_bn: '🌸 মধুমঙ্গল, সুবল আর বৃন্দাবনের ছোট্ট বাছুর ও ময়ূররা ছিল গোপালের খেলার সঙ্গী!',
    yt_query: 'Little Krishna Makhan Chor Bengali cartoon',
    yt_label_bn: 'ছোট্ট কৃষ্ণের মাখন চুরির লীলা'
  },
  {
    id: 'delight_4',
    vibe: 'curiosity_song',
    is_music: false,
    badge_bn: '🐾 কৌতূহল',
    title_bn: 'সমুদ্রের ভোদড় ছানারা হাত ধরে ঘুমায় কেন জানো মা?',
    hook_bn: 'সমুদ্রের জলে ভেসে ঘুমানোর সময় মা-ভোড়ড় ও তার ছোট্ট ছানা একে অপরের হাত শক্ত করে ধরে ঘুমায়, যাতে ঢেউ এসে তাদের কখনো আলাদা না করে দেয়! এমনকি তাদের বুকের কাছে একটা ছোট্ট পকেটের মতো ভাঁজ থাকে যেখানে তারা নিজেদের প্রিয় রঙিন পাথর লুকিয়ে রাখে।',
    hitch_label_bn: '🦋 ভালোবাসার টান',
    hitch_bn: 'প্রকৃতির প্রতিটি মা ও সন্তানের টান ঠিক এমনই অটুট মা—কৌশিক ও দিদি দূরে বা কাজে ব্যস্ত থাকলেও মনে মনে সবসময় তোমার হাত ধরেই আছে।',
    curiosity_q_bn: '🔮 জাদুর পর্দা খোলো: ভোদড় ছানারা ওই পাথর দিয়ে কী করে?',
    curiosity_a_bn: '✨ ওই প্রিয় পাথরটা দিয়ে তারা খেলার ছলে ঝিনুকের খোলা ঠুকে খুলে ফেলে!',
    yt_query: 'Cute sea otters holding hands sleeping video',
    yt_label_bn: 'হাত ধরে ঘুমানো মিষ্টি ভোদড় ছানা'
  },
  {
    id: 'delight_5',
    vibe: 'curiosity_song',
    is_music: true,
    badge_bn: '🎵 গান',
    title_bn: '“এই রাত তোমার আমার”—হেমন্ত মুখোপাধ্যায়ের জাদুকরী কণ্ঠ!',
    hook_bn: '১৯৫৯ সালের ‘দীপ জ্বেলে যাই’ ছবির এই অমর গানটি যখন হেমন্ত মুখোপাধ্যায় রেকর্ড করছিলেন, তখন স্টুডিওর সবাই এতটাই মুগ্ধ হয়ে গিয়েছিলেন যে গান শেষ হওয়ার পরও কয়েক সেকেন্ড কেউ কথা বলতে পারেননি! শুধুমাত্র শিস আর পিয়ানোর মৃদু সুরে এমন মায়া আর কোনো গানে পাওয়া যায় না।',
    hitch_label_bn: '🎵 সুরের আরাম',
    hitch_bn: 'মন কখনো একটুও ক্লান্ত লাগলে শুধু গুনগুন করে প্রিয় পুরনো গানের দু-কলি গেয়ে উঠবে মা—দেখবে এক নিমেষে মন হালকা হয়ে গেছে।',
    curiosity_q_bn: '🔮 জাদুর পর্দা খোলো: এই গানে পর্দায় অভিনয় করেছিলেন কে?',
    curiosity_a_bn: '🌸 মহানায়িকা সুচিত্রা সেন ও বসন্ত চৌধুরী!',
    yt_query: 'Ei Raat Tomar Amar Hemanta Mukherjee original song',
    yt_label_bn: 'হেমন্ত মুখোপাধ্যায়ের ‘এই রাত তোমার আমার’'
  },
  {
    id: 'delight_6',
    vibe: 'cbt_calm',
    is_music: false,
    badge_bn: '🚂 নস্টালজিয়া',
    title_bn: 'রানাঘাট জংশনের ঝালমুড়ি আর বিকেলের মিষ্টি রোদ!',
    hook_bn: 'মনে পড়ে মা, ছোটবেলায় ট্রেনের জানলার ধারে বসলে কীভাবে সর্ষে ক্ষেত আর পুকুরপাড়ের তালগাছগুলো সাঁইসাঁই করে পেছনে ছুটে যেত? স্টেশনে ট্রেন থামলেই কাগজের ঠোঙায় সর্ষের তেল-মাখা গরম ঝালমুড়ি আর মাটির ভাঁড়ে চায়ের সেই গন্ধ আজও যেন বাতাসে ভেসে আসে।',
    hitch_label_bn: '🦋 মনের মুক্তি',
    hitch_bn: 'ট্রেনের জানলার বাইরের গাছপালার মতোই সংসারের ছোটখাটো রাগ বা কথা মনে ধরে রাখবে না মা—সব পেছনে ফেলে শুধু নিজের আনন্দে সামনের দিকে চলো!',
    curiosity_q_bn: '🔮 জাদুর পর্দা খোলো: ভারতের প্রথম ট্রেনগুলির মধ্যে রানাঘাট লাইনের বিশেষত্ব কী?',
    curiosity_a_bn: '✨ ১৮৬২ সালে শিয়ালদহ থেকে রানাঘাট হয়ে কুষ্টিয়া লাইনটি পূর্ব ভারতের অন্যতম প্রাচীন ও ঐতিহাসিক রেলপথ!',
    yt_query: 'Ranaghat Junction railway station nostalgia Bengal',
    yt_label_bn: 'রানাঘাট জংশন ও বাংলার ট্রেন ভ্রমণ'
  },
  {
    id: 'delight_7',
    vibe: 'laugh_gods',
    is_music: false,
    badge_bn: '🪷 ভক্তি',
    title_bn: 'মা লক্ষ্মীর মান ভাঙাতে মহাপ্রভু জগন্নাথের এক হাঁড়ি রসগোল্লা!',
    hook_bn: 'রথযাত্রায় মা লক্ষ্মীকে না নিয়ে ভাই-বোনকে সাথে করে মাসির বাড়ি যাওয়ায় মা লক্ষ্মী ভীষণ অভিমান করে মন্দিরের দরজা বন্ধ করে দেন! তখন স্বয়ং জগন্নাথদেব দরজার বাইরে দাঁড়িয়ে মা লক্ষ্মীর হাতে এক হাঁড়ি নরম রসগোল্লা তুলে দিয়ে বলেন— “লক্ষ্মীটি, এবার দরজা খোলো!”',
    hitch_label_bn: '🦋 সংসারের মিষ্টি মন্ত্র',
    hitch_bn: 'স্বয়ং ভগবানের সংসারেও মাঝে মাঝে একটু মান-অভিমান হয় মা—একটু মিষ্টি কথা আর হাসিতেই সব অভিমান গলে যায়!',
    curiosity_q_bn: '🔮 জাদুর পর্দা খোলো: পুরীর এই রসগোল্লা উৎসবকে কী বলা হয়?',
    curiosity_a_bn: '🌸 একে বলা হয় ‘নীলাদ্রি বিজে’! রথযাত্রার শেষে এই দিনেই পুরীতে রসগোল্লা খাওয়ার মহোৎসব হয়।',
    yt_query: 'Puri Jagannath Rasagolla Niladri Bije Bengali story',
    yt_label_bn: 'জগন্নাথদেবের রসগোল্লা ও নীলাদ্রি বিজে'
  },
  {
    id: 'delight_8',
    vibe: 'laugh_gods',
    is_music: false,
    badge_bn: '😂 হাসি',
    title_bn: 'রাজ্যে মোট ক’টা কাক আছে? গোপাল ভাঁড়ের পেট ফাটা হাসির উত্তর!',
    hook_bn: 'একদিন মহারাজ কৃষ্ণচন্দ্র জিজ্ঞেস করলেন— “গোপাল, আমাদের নদিয়া রাজ্যে ঠিক ক’টা কাক আছে?” গোপাল আঙুল গুনে বলল— “মহারাজ, নিরানব্বই হাজার নয়শো নিরানব্বইটা! যদি দেখেন কম আছে তবে জানবেন তারা পাশের রাজ্যে মামাবাড়ি বেড়াতে গেছে, আর বেশি থাকলে জানবেন তাদের আত্মীয়রা আমাদের রাজ্যে বেড়াতে এসেছে!”',
    hitch_label_bn: '🦋 মনের জাদু',
    hitch_bn: 'কেউ কোনো কঠিন প্রশ্ন করলে ঘাবড়ে যাওয়ার কিচ্ছু নেই মা—গোপালের মতো হালকা হাসিমুখে উড়িয়ে দেওয়াই আসল বুদ্ধিমানের কাজ!',
    curiosity_q_bn: '🔮 জাদুর পর্দা খোলো: গোপাল ভাঁড়ের এই উত্তর শুনে মহারাজ কী করেছিলেন?',
    curiosity_a_bn: '🌸 মহারাজ কৃষ্ণচন্দ্র হেসে গড়িয়ে পড়েছিলেন এবং গোপালকে খুশি হয়ে উপহার দিয়েছিলেন!',
    yt_query: 'Gopal Bhar counting crows funny Bengali comedy',
    yt_label_bn: 'গোপাল ভাঁড়ের কাক গোনার গল্প'
  }
];

function classifyAgendaToVibe(ag) {
  const p = String(ag.pillar || '');
  if (p === 'covert_cbt' || p === 'personal_therapy' || p === 'bengali_expr') return 'cbt_calm';
  if (p === 'music' || p === 'gk_inspiring' || p === 'english' || p === 'hindi' || p === 'tech_65') return 'curiosity_song';
  return 'laugh_gods';
}

function getSimpleBadgeForAgenda(ag, vibe) {
  const p = String(ag.pillar || '');
  if (p === 'music') return '🎵 গান';
  if (vibe === 'cbt_calm') return '🦋 শান্তি';
  if (vibe === 'curiosity_song') return '🔍 কৌতূহল';
  return '😂 হাসি';
}

function getRelevantYoutubeForAgenda(ag) {
  const p = String(ag.pillar || '');
  const title = String(ag.title_bn || '');
  if (p === 'music') {
    return {
      query: title + ' Bengali song',
      label_bn: title
    };
  }
  if (p === 'gk_inspiring') {
    return {
      query: title + ' Bengali',
      label_bn: title
    };
  }
  if (/গোপাল|রামকৃষ্ণ|সারদা|জগন্নাথ|উত্তম|সুচিত্রা|হেমন্ত|সন্ধ্যা|মান্না|রবীন্দ্র|নজরুল|ফেলুদা|ব্যোমকেশ|রানাঘাট|শান্তিনিকেতন/.test(title)) {
    return {
      query: title + ' Bengali',
      label_bn: title
    };
  }
  return { query: '', label_bn: '' };
}

function buildHitchForAgenda(ag) {
  const p = String(ag.pillar || '');
  if (p === 'covert_cbt') {
    return {
      label_bn: '🦋 মনের আরাম',
      text_bn: 'তাজা ও ভালো জিনিস আজই আনন্দে ব্যবহার করো মা—সামান্য দু-টাকার তলানি বা তিতো খোসার জন্য নিজের শরীর ও মনকে একফোঁটাও কষ্ট দেবে না।'
    };
  }
  if (p === 'personal_therapy') {
    return {
      label_bn: '🌸 মনের হালকা হাওয়া',
      text_bn: 'তুমি, কৌশিক আর দিদি—তোমরা তিনজনই এক মাটির নরম মনের মানুষ। পুরনো সব দুশ্চিন্তা নামিয়ে রেখে আজ শুধু নিজের আনন্দে থাকো মা।'
    };
  }
  if (p === 'english') {
    return {
      label_bn: '🔤 মিষ্টি ইংরেজি কথা',
      text_bn: String(ag.prompt_bn || '').replace(/^জেমিনি,?\s*(শোনো—?)?\s*/i, 'মুখে শুধু একবার আনন্দে বলো: ')
    };
  }
  if (p === 'hindi') {
    return {
      label_bn: '🗣️ মিষ্টি হিন্দি আড্ডা',
      text_bn: String(ag.prompt_bn || '').replace(/^জেমিনি,?\s*(শোনো—?)?\s*/i, 'হাসিমুখে আড্ডার ছলে বলো: ')
    };
  }
  if (p === 'music') {
    return {
      label_bn: '🎵 গানের সুরের জাদু',
      text_bn: 'গানের কথাগুলোর ভেতরে যে মিষ্টি ছবি লুকিয়ে আছে, চোখ বুজে শুধু সেই সুরটুকু উপভোগ করো মা—কোনো নিয়ম মনে রাখতে হবে না।'
    };
  }
  if (p === 'tech_65') {
    return {
      label_bn: '📱 ভয়হীন জাদুর কাঠি',
      text_bn: 'ফোনের কোনো বোতামে হাত পড়লে কিচ্ছু খারাপ হয় না মা! মন্দিরের হারমোনিয়ামের মতোই ফোন ছুঁলে তবেই তো সুর বাজবে।'
    };
  }
  return {
    label_bn: '🌍 অবাক করা কৌতূহল',
    text_bn: 'পৃথিবীর এই সুন্দর রহস্যগুলো জানার জন্য কোনো পড়াশোনা লাগে না মা—শুধু গল্পের মতো শুনলেই মন আনন্দে উড়ে বেড়ায়!'
  };
}

function buildCuriosityBoxForAgenda(ag) {
  const follow = String(ag.followup_prompt_bn || ag.prompt_bn || '').replace(/^জেমিনি,?\s*/i, '');
  return {
    q_bn: '🔮 জাদুর পর্দা খোলো: এর পরের মজার কথাটা কী জানো মা?',
    a_bn: '✨ ' + (follow || 'এই সুন্দর কথাটি মনের আনন্দে উপভোগ করো মা!')
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
      vibe: dr.vibe,
      is_music: !!dr.is_music,
      badge_bn: dr.badge_bn,
      title_bn: dr.title_bn,
      hook_bn: dr.hook_bn,
      hitch_label_bn: dr.hitch_label_bn,
      hitch_bn: dr.hitch_bn,
      curiosity_q_bn: dr.curiosity_q_bn,
      curiosity_a_bn: dr.curiosity_a_bn,
      audio_url: refDay.audio_url || (refAg ? refAg.audio_url : ''),
      story_end: 0,
      yt_query: dr.yt_query || '',
      yt_label_bn: dr.yt_label_bn || dr.title_bn,
      day_num: refDay.day,
      ag_idx: 0
    });
  });

  DAYS_21.forEach(d => {
    const dNum = Number(d.day) || 1;
    (d.agendas || []).forEach((ag, agIdx) => {
      const vibe = classifyAgendaToVibe(ag);
      const hitch = buildHitchForAgenda(ag);
      const curBox = buildCuriosityBoxForAgenda(ag);
      const ytInfo = getRelevantYoutubeForAgenda(ag);
      const card = {
        id: 'd' + dNum + '_g' + agIdx,
        vibe: vibe,
        is_music: String(ag.pillar || '') === 'music',
        badge_bn: getSimpleBadgeForAgenda(ag, vibe),
        title_bn: ag.title_bn,
        hook_bn: ag.detail_bn,
        hitch_label_bn: hitch.label_bn,
        hitch_bn: hitch.text_bn,
        curiosity_q_bn: curBox.q_bn,
        curiosity_a_bn: curBox.a_bn,
        audio_url: ag.audio_url || d.audio_url || '',
        story_end: Number(ag.story_end) || 0,
        yt_query: ytInfo.query,
        yt_label_bn: ytInfo.label_bn,
        day_num: dNum,
        ag_idx: agIdx
      };
      if (vibe === 'cbt_calm') cbts.push(card);
      else if (vibe === 'curiosity_song') curiosities.push(card);
      else delights.push(card);
    });
  });

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

function jhBnNum(n) {
  return String(n).replace(/\d/g, d => '০১২৩৪৫৬৭৮৯'[d]);
}
