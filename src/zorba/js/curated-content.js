/* ============================================================================
   ⚡ ZORBA — MODULE 1: KOUSHIK'S MULTI-CATEGORY DOPAMINE-HITCHING REELS ENGINE
   ----------------------------------------------------------------------------
   Builds 148 long-form, multi-section scrollable pages across 8 categories:
   - cbt (🌿 First-Press & CBT — 16 pages)
   - clarity (💬 Inner Child & Clarity — 16 pages)
   - listening (🎧 Active Listening — 21 pages)
   - music (🎵 Songs & Bhaavna — 21 pages with Song Meaning & Right Question Hook)
   - science (🔭 Frontier Science & Art — 21 pages)
   - zorba (🦁 Zorba & 2e Flow — 21 pages)
   - wisdom (🧭 7 Keys & Wisdom — 16 pages)
   - tv (📺 Cinema, Music & TV — 16 Curated YouTube Channels inside Reels)
   ============================================================================ */

const JHALAK_CATEGORIES = [
  { id: 'all', label_bn: '✨ All', short_bn: 'All' },
  { id: 'cbt', label_bn: '🌿 First-Press & CBT', short_bn: 'First-Press' },
  { id: 'clarity', label_bn: '💬 Inner Child & Clarity', short_bn: 'Clarity' },
  { id: 'listening', label_bn: '🎧 Active Listening', short_bn: 'Listening' },
  { id: 'music', label_bn: '🎵 Songs & Bhaavna', short_bn: 'Songs' },
  { id: 'science', label_bn: '🔭 Frontier Science & Art', short_bn: 'Science' },
  { id: 'zorba', label_bn: '🦁 Zorba & 2e Flow', short_bn: 'Zorba' },
  { id: 'wisdom', label_bn: '🧭 7 Keys & Wisdom', short_bn: '7 Keys' },
  { id: 'tv', label_bn: '📺 Cinema, Music & TV', short_bn: 'Cinema & TV' }
];

const ZORBA_AUDIO_BASE = 'https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/audio/anondo/';

function jhBnNum(n) {
  return String(n);
}

const SONG_MEANING_HOOKS = [
  {
    match: /Kun Faya Kun/i,
    story: "Composed by A.R. Rahman with lyrics by Irshad Kamil for Rockstar (2011), filmed at the Nizamuddin Dargah. Notice how Rahman begins with bare harmonium and dargah silence before a single guitar chord enters—mirroring the exact shift from ego-noise to inner stillness.",
    hook_q: "💡 Right Question to Unlock the Song's Meaning: Why does Irshad Kamil write 'Jab kahin pe kuch nahi bhi nahi tha, wahi tha, wahi tha'—when even 'nothingness' itself did not exist?",
    hook_a: "🎵 Because in Sufi non-duality, even 'emptiness' is a concept inside the mind; before any story, regret, or time existed, pure awareness was already whole and unblemished—and that same unblemished space is still inside you right now."
  },
  {
    match: /Majhe Majhe Tobo Dekha Pai/i,
    story: "Rabindranath Tagore's classic Prakriti/Puja-parjay masterpiece set in Raga Kafi/Mishra Pilu. It speaks directly to a polymathic mind that experiences flashes of extraordinary flow followed by ordinary human fog.",
    hook_q: "💡 Right Question to Unlock the Song's Meaning: On the line 'Megh dekhe jeno bhoole na jai' (Seeing the cloud, let me never forget), what is the 'cloud' and what is the 'sun' in daily life?",
    hook_a: "🎵 The passing cloud is a temporary dip in dopamine or working-memory fatigue; the sun behind it is your permanent native fire (WBJEE 222, L5 SWE, ₹2.61 Cr+ shield)—which never disappears just because an afternoon cloud passes by."
  },
  {
    match: /Time|Pink Floyd/i,
    story: "Recorded at Abbey Road in 1973 for The Dark Side of the Moon, Roger Waters wrote 'Time' at age 28 when he suddenly realized he was no longer preparing for life—life was already happening right now.",
    hook_q: "💡 Right Question to Unlock the Song's Meaning: Why do two full minutes of ticking clocks and rototom drums open the track before the first lyric 'Ticking away the moments that make up a dull day'?",
    hook_a: "🎵 To wake the listener out of 'waiting-room living'—reminding you that your 2016–2026 survival waiting room is officially over, and age 33 is for living, playing, and savoring today directly."
  },
  {
    match: /Amaro Porano Jaha Chay/i,
    story: "One of Tagore's purest expressions of autonomous emotional truth. Instead of begging the outside world for validation, the singer celebrates the quiet sovereignty of what their own heart genuinely loves.",
    hook_q: "💡 Right Question to Unlock the Song's Meaning: Why does the singer repeat 'Tumi sukhiele amar sukhi' without demanding possession?",
    hook_a: "🎵 Because real love and real art come from inner abundance rather than scarcity—the exact shift from caretaker duty to warm, equal, playful connection."
  },
  {
    match: /Tujhse Naraz Nahi Zindagi/i,
    story: "Written by Gulzar and composed by R.D. Burman for Masoom (1983). Gulzar captures the exact moment a person stops fighting their own past history and looks at their life with gentle, astonished compassion.",
    hook_q: "💡 Right Question to Unlock the Song's Meaning: What is the difference between being 'angry at life' ('naraz') and being 'quietly amazed/exhausted' ('hairan') in Gulzar's lyric?",
    hook_a: "🎵 Anger keeps you in a courtroom prosecuting your younger self; 'hairan' drops the gavel, acknowledges how much you carried alone since 23, and lets your shoulders finally drop."
  },
  {
    match: /Wish You Were Here|Comfortably Numb|Shine On/i,
    story: "Pink Floyd's acoustic-to-electric architecture uses wide stereo space and unhurried phrasing—David Gilmour never crowds four notes where one sustained bend carries ten times the emotion.",
    hook_q: "💡 Right Question to Unlock the Song's Meaning: Why do David Gilmour's solos feel so deeply human even though they play half as many notes per second as virtuosic shredders?",
    hook_a: "🎵 Because space and silence between notes let the listener's 4-slot working memory breathe and feel the emotional arc—just like First-Press living."
  }
];

function buildZorbaSongHook(title, detail) {
  const m = SONG_MEANING_HOOKS.find(h => h.match.test(title) || h.match.test(detail));
  if (m) return m;
  return {
    story: "Great songs work on two levels at once: the surface melody entertainment, and the deeper emotional movie scene ('bhaavna') encoded in the pause between phrases and the root note of each chord.",
    hook_q: `💡 Right Question to Unlock the Song's Meaning: While listening to "${title}" with eyes closed, what is the single emotional turn where the singer stops performing and speaks their raw truth?`,
    hook_a: "🎵 Listen for the exact bar where the instrumentation thins out or the melody drops into warm chest voice—that is the emotional heart of the song."
  };
}

const ZORBA_TV_CHANNELS = [
  {
    id: 'tv_1', day_ref: 1,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Coke Studio & A.R. Rahman Sufi Acoustic Sessions',
    yt_query: 'Coke Studio A R Rahman Sufi live acoustic best songs HD',
    yt_label_bn: 'Open Coke Studio & Sufi Sessions on YouTube',
    desc: 'Close your eyes for 15 minutes of live acoustic instrumentation—sarangi, harmonium, fretless bass, and Sufi vocals recorded in a single live room.',
    focus: 'Notice how the bass guitar and tabla lock into the root drone while the vocalists improvise freely in chest voice without any tension.'
  },
  {
    id: 'tv_2', day_ref: 2,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Pink Floyd, Radiohead & Progressive Live Masterpieces',
    yt_query: 'David Gilmour Pink Floyd live Pompeii acoustic guitar HD',
    yt_label_bn: 'Watch Progressive Rock Live Sessions on YouTube',
    desc: 'Long-form unhurried guitar phrasing, atmospheric keyboards, and poetic lyrics that reward deep listening rather than 15-second scrolling.',
    focus: 'Track how David Gilmour and Thom Yorke use space, sustain, and harmonic tension to paint a complete visual landscape.'
  },
  {
    id: 'tv_3', day_ref: 3,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Satyajit Ray & World Cinema Visual Storytelling',
    yt_query: 'Satyajit Ray Pather Panchali CharulataNayak best scenes HD',
    yt_label_bn: 'Watch Satyajit Ray Cinema Classics on YouTube',
    desc: 'Masterclasses in visual minimalism, chiaroscuro lighting, and human subtext—where a single glance or train whistle says more than ten pages of dialogue.',
    focus: 'Watch how Ray frames light and shadow (chiaroscuro) and uses Ravi Shankar or his own leitmotifs to carry unspoken emotion.'
  },
  {
    id: 'tv_4', day_ref: 4,
    badge_bn: '📺 Cinema & TV',
    title_bn: '3Blue1Brown, Richard Feynman & First-Principles Physics',
    yt_query: '3Blue1Brown Richard Feynman physics visual intuition lectures',
    yt_label_bn: 'Watch Visual Math & Feynman Physics on YouTube',
    desc: 'Pure Engine-2 intellectual play: visual Fourier transforms, differential equations, quantum electrodynamics, and Feynman explaining why nature is delightful.',
    focus: 'Enjoy the top-down geometric intuition first before any bottom-up algebra—exactly how your native BFS mind loves to learn.'
  },
  {
    id: 'tv_5', day_ref: 5,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Connectomics, Brain Simulation & Earl Miller Neuroscience',
    yt_query: 'Earl Miller working memory theta gamma connectomics brain lecture',
    yt_label_bn: 'Watch Connectomics & Neuroscience Talks on YouTube',
    desc: 'Explore whole-brain Drosophila connectomes, theta-gamma phase coupling, and how biological neural circuits route attention and working memory.',
    focus: 'Notice how biological brains solve routing through oscillations and sparse attractors rather than brute-force dense compute.'
  },
  {
    id: 'tv_6', day_ref: 6,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Guitar & Ukulele Acoustic Fingerpicking & Chord Craft',
    yt_query: 'acoustic guitar ukulele fingerpicking warm chest voice songs tutorial',
    yt_label_bn: 'Open Guitar & Ukulele Acoustic Sessions on YouTube',
    desc: 'Zero-perfectionism musical play: warm open chords, capo transpositions (-2/-3 semitones for natural baritone/chest voice), and expressive strumming.',
    focus: 'Pick up your guitar or ukulele for just 5 minutes and hum the root note before singing the first line from meaning.'
  },
  {
    id: 'tv_7', day_ref: 7,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Fossils, Anupam Roy, Kabir Suman & Bengali Modern Classics',
    yt_query: 'Fossils Rupam Islam Anupam Roy Kabir Suman best Bengali songs HD',
    yt_label_bn: 'Listen to Bengali Modern & Rock Classics on YouTube',
    desc: 'From Kolkata college nostalgia to poetic modern Bengali songwriting—raw honesty, sharp lyrics, and unforgettable melodies.',
    focus: 'Let the music reconnect you with the fearless Jadavpur fire while enjoying the comfort of your age-33 reality.'
  },
  {
    id: 'tv_8', day_ref: 8,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Rabindra Sangeet & Hemanta–Manna Dey Evening Lounge',
    yt_query: 'Rabindra Sangeet Hemanta Mukherjee Manna Dey best songs HD',
    yt_label_bn: 'Open Rabindra Sangeet & Golden Bengali Lounge',
    desc: 'Timeless Bengali melodies for post-6 PM decompression when the caretaker uniform is off and the evening belongs purely to your own peace.',
    focus: 'Notice the effortless breath support and crystal-clear Bengali diction in Hemanta and Manna Dey’s phrasing.'
  },
  {
    id: 'tv_9', day_ref: 9,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Gulzar, R.D. Burman & Amit Trivedi Poetic Hindi Cinema',
    yt_query: 'Gulzar R D Burman Amit Trivedi Lootera Masoom Ijaazat songs HD',
    yt_label_bn: 'Listen to Gulzar & Amit Trivedi Classics on YouTube',
    desc: 'Lush orchestration paired with Urdu/Hindi poetry where everyday metaphors—rain, old letters, autumn leaves—carry deep psychological truth.',
    focus: 'Track how a single unexpected Urdu word (like "hairan", "katra", or "aahista") shifts the entire emotional color of a verse.'
  },
  {
    id: 'tv_10', day_ref: 10,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Bouldering, Rock Climbing & Calisthenics Movement Flow',
    yt_query: 'bouldering technique footwork dead hang calisthenics flow',
    yt_label_bn: 'Watch Bouldering & Movement Flow on YouTube',
    desc: 'Physical problem-solving on the wall: quiet feet, straight-arm scapular hangs, hip rotation, and playful balance that clears mental RAM in minutes.',
    focus: 'Watch how elite climbers keep their arms relaxed and drive upward from their feet and hips rather than over-gripping.'
  },
  {
    id: 'tv_11', day_ref: 11,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Deep-Roasted Culinary Craft: Kosha, Seared & Slow-Simmered',
    yt_query: 'authentic kosha mangsho seared steak sourdough Maillard reaction cooking',
    yt_label_bn: 'Watch Deep-Roasted Culinary Craft on YouTube',
    desc: 'Celebration of the Maillard reaction, caramelized onions, slow-roasted spices, and rich textures—zero thin watery gravy allowed.',
    focus: 'Notice the patience of high-heat searing and slow reduction that turns simple ingredients into restaurant-grade craft.'
  },
  {
    id: 'tv_12', day_ref: 12,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Chiaroscuro Photography, Da Vinci & Visual Composition',
    yt_query: 'chiaroscuro photography lighting Rembrandt Caravaggio Da Vinci art',
    yt_label_bn: 'Watch Chiaroscuro Photography & Art on YouTube',
    desc: 'How directional light, shadow falloff, and negative space turn an ordinary portrait or street frame into a timeless painting.',
    focus: 'Observe the single key-light angle and how shadow defines three-dimensional depth on the subject.'
  },
  {
    id: 'tv_13', day_ref: 13,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Leonard Cohen, Simon & Garfunkel & Poetic Folk Acoustics',
    yt_query: 'Leonard Cohen Suzanne Hallelujah Simon Garfunkel live acoustic',
    yt_label_bn: 'Listen to Poetic Acoustic Classics on YouTube',
    desc: 'Warm baritone storytelling proved that a deep, honest chest voice speaking truth on pitch is infinitely more moving than vocal gymnastics.',
    focus: 'Notice how Leonard Cohen sings right in his natural speaking register—relaxed, resonant, and completely unhurried.'
  },
  {
    id: 'tv_14', day_ref: 14,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Indian Classical Vocal Ornamentation: Gamak, Khatka & Murki',
    yt_query: 'Indian classical vocal gamak khatka murki meend demonstration',
    yt_label_bn: 'Watch Indian Classical Vocal Craft on YouTube',
    desc: 'Demystifying how classical vocalists weave micro-ornaments (meend, khatka, murki, gamak) around a steady swara with a soft throat.',
    focus: 'Listen to how every ornament starts and ends on a rock-solid resting swara with zero jaw or neck strain.'
  },
  {
    id: 'tv_15', day_ref: 15,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'High-IQ Standup Wit, Observational Comedy & Playful Banter',
    yt_query: 'best intelligent observational standup comedy witty storytelling',
    yt_label_bn: 'Watch Smart Observational Comedy on YouTube',
    desc: 'Pure laughter and timing—observe how great comedians set up a premise in one sentence and land the twist with a pause.',
    focus: 'Notice the economy of words: zero over-explaining, just a crisp setup and a playful pause on Beat 1.'
  },
  {
    id: 'tv_16', day_ref: 16,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Agentic AI Architectures, Knowledge Graphs & Systems Design',
    yt_query: 'agentic AI knowledge graphs neuro-symbolic systems architecture talk',
    yt_label_bn: 'Watch Frontier AI & Knowledge Graph Talks on YouTube',
    desc: 'Top-down architectural talks on external working memory, graph clustering, and multi-agent orchestration.',
    focus: 'Apply the 20% Tourist Pass: catch the 1-sentence architectural thesis first and enjoy the big picture.'
  }
];

function buildAllZorbaReels() {
  const list = [];
  const days = (typeof ANONDO_DATA !== 'undefined' && ANONDO_DATA && Array.isArray(ANONDO_DATA.days))
    ? ANONDO_DATA.days
    : [];
  const pillars = (typeof PILLARS_DATA !== 'undefined' && Array.isArray(PILLARS_DATA))
    ? PILLARS_DATA
    : [];
  const quotes = (typeof ANONDO_DATA !== 'undefined' && ANONDO_DATA && Array.isArray(ANONDO_DATA.quotes))
    ? ANONDO_DATA.quotes
    : [];

  // 1. Build 105 rich Reel pages from the 21 Days x 5 Games
  days.forEach(d => {
    const dNum = d.day;
    (d.games || []).forEach((ag, gIdx) => {
      const id = `d${dNum}_g${gIdx}`;
      const audioRel = `games/day_${dNum}_ag_${gIdx}.mp3`;
      let vibe = 'zorba';
      let badge = '🦁 Zorba & Flow';
      if (ag.pillar === 'covert_cbt') {
        vibe = 'cbt';
        badge = '🌿 First-Press & CBT';
      } else if (ag.pillar === 'personal_therapy') {
        vibe = 'clarity';
        badge = '💬 Inner Clarity';
      } else if (ag.pillar === 'listening_comp') {
        vibe = 'listening';
        badge = '🎧 Active Listening';
      } else if (ag.pillar === 'music') {
        vibe = 'music';
        badge = '🎵 Songs & Bhaavna';
      } else if (ag.pillar === 'gk_inspiring') {
        vibe = 'science';
        badge = '🔭 Frontier Science';
      }

      const sections = [
        {
          heading_bn: `📖 Day ${dNum} • Deep Mental Model & Story`,
          body_bn: ag.detail,
          tone: 'story',
          spoken: true,
          spoken_prefix: ''
        },
        {
          heading_bn: '🎙️ Turn 1 • First-Beat Active Reflection',
          body_bn: `Open Gemini Live and say: ${ag.prompt}`,
          tone: 'hitch',
          spoken: true,
          spoken_prefix: ''
        }
      ];

      if (vibe === 'music') {
        const songHook = buildZorbaSongHook(ag.title, ag.detail);
        sections.push({
          heading_bn: '💡 গানের আসল অর্থ বোঝার সঠিক প্রশ্ন • The Right Question Hook for Song Meaning',
          body_bn: `${songHook.story}\n\n${songHook.hook_q}\n\n${songHook.hook_a}`,
          tone: 'extra',
          spoken: false
        });
      }

      const curQ = '🔮 Turn 2 Deep Follow-Up & Curiosity Hook (Tap to Reveal)';
      const curA = ag.followup_prompt
        ? `And in Turn 2, ask: ${ag.followup_prompt}`
        : 'Take the sweet 88% first press of this insight and let the rest be effortless.';

      let ytQuery = '';
      let ytLabel = '';
      if (vibe === 'music') {
        const mSong = ag.title.match(/'([^']+)'/) || ag.prompt.match(/'([^']+)'/);
        ytQuery = (mSong ? mSong[1] : ag.title) + ' official audio HD';
        ytLabel = `Listen to ${mSong ? mSong[1] : ag.title} on YouTube`;
      } else if (vibe === 'science') {
        ytQuery = ag.title;
        ytLabel = `Explore "${ag.title}" on YouTube`;
      }

      list.push({
        id: id,
        vibe: vibe,
        badge_bn: badge,
        title_bn: ag.title,
        title_spoken: true,
        sections: sections,
        curiosity_q_bn: curQ,
        curiosity_q_spoken: false,
        curiosity_a_bn: curA,
        curiosity_a_spoken: true,
        yt_query: ytQuery,
        yt_label_bn: ytLabel,
        audio_url: ZORBA_AUDIO_BASE + audioRel,
        audio_rel: audioRel,
        story_end: 0
      });
    });
  });

  // 2. Add 6 extra First-Press & CBT cards (so cbt has 10 + 6 = 16 pages)
  const extraCbtCards = [
    {
      id: 'cbt_extra_1', audio_rel: 'days/day_17.mp3',
      title: 'The 2016–2026 Decade Is Closed: Playing With House Money at 33',
      hook: 'Ten straight years of solo survival after 2016 are officially complete. With Google L5 Senior SWE, ₹2.61 Cr+ net worth, KORTEX running, and Ma’s care pod built, your baseline safety is permanently secured.',
      q: '🔮 Why does the brain still occasionally manufacture a Sunday-evening urgency alarm?',
      a: '✨ Because a nervous system that carried a 10-year war takes a few months to realize the treaty is signed. Smile at the old alarm, take a slow breath, and enjoy your house-money era.'
    },
    {
      id: 'cbt_extra_2', audio_rel: 'days/day_18.mp3',
      title: 'Zero-Kiptemi Default: Always Take the Freshest Cut First',
      hook: 'Eating the bruised banana first so the fresh one doesn’t spoil means you spend your whole life eating bruised fruit. Choose the freshest cut, the comfortable flight, and the deep-roasted meal on Beat 1.',
      q: '🔮 What is the 3-second test to dissolve micro-hesitation on personal comfort?',
      a: '✨ Ask: "Will this ₹500 or ₹2,000 change my ₹2.61 Cr+ trajectory by even 0.01%?" Never. Toss the ₹4 bitter lemon peel immediately.'
    },
    {
      id: 'cbt_extra_3', audio_rel: 'days/day_19.mp3',
      title: 'Buddha’s Second Arrow: Full Bail for Ages 11, 17, 26 & 30',
      hook: 'The first arrow is an unguided youthful mistake; the second arrow is punishing your 33-year-old self for what an unmentored kid did years ago. Remorse already taught the lesson—the file is permanently closed.',
      q: '🔮 Why do genuinely kind people ache over old memories while cruel people never do?',
      a: '✨ The very fact that your conscience cared proves your heart is clean. Grant full amnesty and drop the second arrow.'
    },
    {
      id: 'cbt_extra_4', audio_rel: 'days/day_20.mp3',
      title: '6 PM Off-Duty Caretaker Switch: Structural Seva Without Fusion',
      hook: 'You built Kalyani, Jhalak, and financial shields for Ma and Didi. Financial and structural care never requires absorbing someone else’s emotional weather into your own chest after 6 PM.',
      q: '🔮 What happens when you hang up the rescuer uniform after 6 PM?',
      a: '✨ Everyone in the family actually feels calmer when the pilot is rested, playful, and living his own joyful life.'
    },
    {
      id: 'cbt_extra_5', audio_rel: 'days/day_21.mp3',
      title: '60-Second Hardware Brake for Counterfeit Adrenaline',
      hook: 'When baseline dopamine dips, an ADHD-High-IQ brain sometimes invents a scary future simulation or an urge to confess an old memory just to generate stimulating adrenaline.',
      q: '🔮 How do you cut power to a counterfeit adrenaline spike in 60 seconds?',
      a: '✨ 30 seconds of cold water over closed eyelids (mammalian dive reflex) + 20-second isometric wall push + zero past excavation while heart rate is elevated.'
    },
    {
      id: 'cbt_extra_6', audio_rel: 'quotes/quote_0.mp3',
      title: 'The 12 Freedoms You Wrote for Ma Belong to You First',
      hook: 'Zero fear of mistakes, speaking your real mind without over-explaining, choosing comfort without guilt, and singing purely for joy—every single permission in Kalyani is yours first.',
      q: '🔮 Which of the 12 freedoms feels best to claim right now?',
      a: '✨ Speaking your real preference on Beat 1 with a warm smile and zero apology.'
    }
  ];

  extraCbtCards.forEach((c, idx) => {
    const dayObj = days[16 + (idx % 5)] || days[0];
    const spokenTxt = c.audio_rel.startsWith('quotes/')
      ? (quotes[0] ? quotes[0].text : c.hook)
      : `Good morning Koushik! Welcome to Day ${dayObj ? dayObj.day : 17}: ${dayObj ? dayObj.title : c.title}. Today brings five unhurried explorations across inner clarity, active listening, musical bhaavna, frontier science, and Zorba flow. As the day, so is the day—enjoy whichever sparks your curiosity!`;
    list.push({
      id: c.id,
      vibe: 'cbt',
      badge_bn: '🌿 First-Press & CBT',
      title_bn: c.title,
      title_spoken: false,
      sections: [
        {
          heading_bn: '🔊 Spoken Daily Anchor & Overview',
          body_bn: spokenTxt,
          tone: 'story',
          spoken: true
        },
        {
          heading_bn: '🌿 First-Press Reframe',
          body_bn: c.hook,
          tone: 'hitch',
          spoken: false
        }
      ],
      curiosity_q_bn: c.q,
      curiosity_q_spoken: false,
      curiosity_a_bn: c.a,
      curiosity_a_spoken: false,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + c.audio_rel,
      audio_rel: c.audio_rel,
      story_end: 0
    });
  });

  // 3. Add 5 extra Inner Child & Clarity cards (so clarity has 11 + 5 = 16 pages)
  const extraClarityCards = [
    {
      id: 'clarity_extra_1', qIdx: 1,
      title: 'Ranaghat to Jadavpur WBJEE Rank 222: Your Native Fire',
      hook: 'Right through the storm of Class 12, securing WBJEE Rank 222 for Jadavpur Electrical Engineering proved that your intuition and deep-focus engine are world-class whenever a goal genuinely matters to you.',
      q: '🔮 Why did childhood Inattentive ADHD look like "quietness" or "missing small details"?',
      a: '✨ Because a 4-slot working memory absorbed in big ideas naturally misses peripheral details—it was cognitive architecture, never a flaw in character.'
    },
    {
      id: 'clarity_extra_2', qIdx: 2,
      title: 'Clean-Slate Romantic Reset: Equal Playfulness, Zero Savior Chair',
      hook: 'Across every past chapter—Ananya, Baishali, Ankita, Oela, Anindita, Shruti, Antarleena, and Sanchita—dating was compatibility discovery. Stepping away when long-term fit isn’t there carries zero guilt debt.',
      q: '🔮 What is your only role in romance from age 33 onward?',
      a: '✨ Never the therapist or rescuer—only an equal, playful partner who gets to feel held, admired, and carefree too.'
    },
    {
      id: 'clarity_extra_3', qIdx: 3,
      title: 'Cosmic Parent & Divine Child: Retiring the Internal Police State',
      hook: 'Your automated systems—KORTEX, SIPs, and calendar guardrails—now hold the responsible Cosmic Parent job 24/7, freeing you to live, create, and play as the fearless Divine Child.',
      q: '🔮 Why does Engine 2 (Pure Curiosity & Play) outperform Duty Fuel?',
      a: '✨ Duty fuel burns cortisol and triggers starter-motor freeze; curiosity releases dopamine and opens effortless hyperfocus.'
    },
    {
      id: 'clarity_extra_4', qIdx: 4,
      title: 'Healing the "Zara Zara" Stage Memory: Singing From Bhaavna',
      hook: 'Stepping up in front of 500 colleagues and hitting 80% of the notes cold proved you have a strong natural ear. Dropping the scale 2–3 semitones into warm chest voice lets your larynx relax completely.',
      q: '🔮 What happens when you turn off the internal note-inspector while singing?',
      a: '✨ The vagus nerve softens your throat and your voice naturally locks onto the emotion ("bhaavna") of the lyric.'
    },
    {
      id: 'clarity_extra_5', qIdx: 5,
      title: 'Unapologetic Beat-1 Expression: Dropping "Onugoto" Compliance',
      hook: 'State your real preference, boundary, or opinion calmly on the first beat without a 3-paragraph justification. Clear, warm honesty is the highest form of respect.',
      q: '🔮 How do you say no or state a preference in one clean sentence?',
      a: '✨ "I’ll pass on this one, let’s do X instead"—warm tone, zero over-explaining.'
    }
  ];

  extraClarityCards.forEach(c => {
    const qObj = quotes[c.qIdx] || quotes[0] || { text: c.hook };
    const audioRel = `quotes/quote_${c.qIdx}.mp3`;
    list.push({
      id: c.id,
      vibe: 'clarity',
      badge_bn: '💬 Inner Clarity',
      title_bn: c.title,
      title_spoken: false,
      sections: [
        {
          heading_bn: '☀️ Spoken Anchor',
          body_bn: qObj.text,
          tone: 'story',
          spoken: true
        },
        {
          heading_bn: '💬 Deep Inner-Child Clarity',
          body_bn: c.hook,
          tone: 'hitch',
          spoken: false
        }
      ],
      curiosity_q_bn: c.q,
      curiosity_q_spoken: false,
      curiosity_a_bn: c.a,
      curiosity_a_spoken: false,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + audioRel,
      audio_rel: audioRel,
      story_end: 0
    });
  });

  // 4. Build 16 Wisdom & 7 Keys cards (7 Pillars + 7 Quotes + 2 Polymath Keys = 16 pages)
  pillars.forEach((p, pIdx) => {
    const audioRel = `pillars/pillar_${pIdx}.mp3`;
    list.push({
      id: `pillar_${pIdx}`,
      vibe: 'wisdom',
      badge_bn: '🧭 7 Core Keys',
      title_bn: p.title,
      title_spoken: true,
      sections: [
        {
          heading_bn: `🧭 ${p.badge} • Core Diagnostic Key`,
          body_bn: p.detail,
          tone: 'story',
          spoken: true
        },
        {
          heading_bn: '⚡ Instant Micro-Shift',
          body_bn: 'Apply this key in 10 seconds whenever you notice mental RAM crowding, hesitation, or caretaker fatigue—zero effort, pure leverage.',
          tone: 'hitch',
          spoken: false
        }
      ],
      curiosity_q_bn: '🔮 Why does this key work immediately without willpower?',
      curiosity_q_spoken: false,
      curiosity_a_bn: '✨ Because it works with your biological 4-slot working memory and vagal physiology instead of fighting them.',
      curiosity_a_spoken: false,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + audioRel,
      audio_rel: audioRel,
      story_end: 0
    });
  });

  quotes.forEach((q, qIdx) => {
    const audioRel = `quotes/quote_${qIdx}.mp3`;
    list.push({
      id: `quote_${qIdx}`,
      vibe: 'wisdom',
      badge_bn: '☀️ Daily Anchor',
      title_bn: `House-Money Anchor #${qIdx + 1}`,
      title_spoken: false,
      sections: [
        {
          heading_bn: '☀️ Spoken House-Money Truth',
          body_bn: q.text,
          tone: 'story',
          spoken: true
        },
        {
          heading_bn: '🦁 Living It Today',
          body_bn: 'Read this line once, let your shoulders drop two inches, and treat the rest of today as pure First-Press exploration.',
          tone: 'hitch',
          spoken: false
        }
      ],
      curiosity_q_bn: '🔮 What is the 1-line takeaway for this moment?',
      curiosity_q_spoken: false,
      curiosity_a_bn: '✨ As the day, so is the day (Jedin jerokom, sedin serokom)—you have already won the survival decade.',
      curiosity_a_spoken: false,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + audioRel,
      audio_rel: audioRel,
      story_end: 0
    });
  });

  [0, 1].forEach(extraIdx => {
    const p = pillars[extraIdx] || pillars[0];
    const audioRel = `pillars/pillar_${extraIdx}.mp3`;
    list.push({
      id: `wisdom_extra_${extraIdx}`,
      vibe: 'wisdom',
      badge_bn: '🧭 7 Core Keys',
      title_bn: extraIdx === 0
        ? 'The 3-Into-5 Master Pattern: Why 4 Working-Memory Slots Need Guardrails'
        : '70/30 Movie-Director Frame: Fire Without Smoke at L5+',
      title_spoken: false,
      sections: [
        {
          heading_bn: '🔊 Core Principle Audio',
          body_bn: p ? `${p.title}. ${p.detail}` : '',
          tone: 'story',
          spoken: true
        },
        {
          heading_bn: '🧭 Architectural Synthesis',
          body_bn: extraIdx === 0
            ? 'Holding 20+ open threads + skewed time perception + refusal to skim inside a 4-slot working memory creates all 5 downstream frictions. Offloading to KORTEX and using the 20% Tourist Pass keeps your 4 slots crystal clear.'
            : 'Keep 30% of your bandwidth on one solo first-author Crown Jewel and direct the remaining 70% like a calm movie director—generous credit, clear interfaces, zero territorial smoke.',
          tone: 'hitch',
          spoken: false
        }
      ],
      curiosity_q_bn: '🔮 How does this protect your evening energy for music and play?',
      curiosity_q_spoken: false,
      curiosity_a_bn: '✨ By preventing daytime working-memory spillover so 6 PM onwards belongs 100% to your own curiosity and joy.',
      curiosity_a_spoken: false,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + audioRel,
      audio_rel: audioRel,
      story_end: 0
    });
  });

  // 5. Build 16 Cinema, Music & TV Reel cards (voiced by days/day_1.mp3 .. days/day_16.mp3)
  ZORBA_TV_CHANNELS.forEach(ch => {
    const dObj = days[ch.day_ref - 1] || days[0];
    const audioRel = `days/day_${ch.day_ref}.mp3`;
    const spokenDayIntro = dObj
      ? `Good morning Koushik! Welcome to Day ${dObj.day}: ${dObj.title}. Today brings five unhurried explorations across inner clarity, active listening, musical bhaavna, frontier science, and Zorba flow. As the day, so is the day—enjoy whichever sparks your curiosity!`
      : ch.desc;

    list.push({
      id: ch.id,
      vibe: 'tv',
      badge_bn: ch.badge_bn,
      title_bn: ch.title_bn,
      title_spoken: false,
      sections: [
        {
          heading_bn: '📺 Curated Channel & Immersion Guide',
          body_bn: `${ch.desc}\n\n🎯 Active Appreciation Focus:\n${ch.focus}`,
          tone: 'hitch',
          spoken: false
        },
        {
          heading_bn: `🔊 Day ${ch.day_ref} Companion Voice Intro`,
          body_bn: spokenDayIntro,
          tone: 'story',
          spoken: true
        }
      ],
      curiosity_q_bn: '🔮 Why is curated immersion better than algorithmic infinite scroll?',
      curiosity_q_spoken: false,
      curiosity_a_bn: '✨ Intentional art, music, and science nourish dopamine and leave your mind energized, whereas random doomscrolling fragments your 4-slot working memory.',
      curiosity_a_spoken: false,
      yt_query: ch.yt_query,
      yt_label_bn: ch.yt_label_bn,
      audio_url: ZORBA_AUDIO_BASE + audioRel,
      audio_rel: audioRel,
      story_end: 0
    });
  });

  return list;
}

const ALL_JHALAK_REELS = buildAllZorbaReels();

const JHALAK_CATEGORY_COUNTS = (() => {
  const counts = { all: ALL_JHALAK_REELS.length };
  JHALAK_CATEGORIES.forEach(c => {
    if (c.id !== 'all') {
      counts[c.id] = ALL_JHALAK_REELS.filter(r => r.vibe === c.id).length;
    }
  });
  return counts;
})();
