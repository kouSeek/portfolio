/* ============================================================================
   ⚡ ZORBA — MODULE 1A: CATEGORIES & DEEP DOPAMINE CONTENT VAULT
   ----------------------------------------------------------------------------
   Rich, multi-section, self-contained content vault for Koushik's 148 Zorba pages:
   - 21 Bespoke Song Backstories, Lyric Philosophies & Right Question Hooks
   - 21 Feynman-Grade Frontier Science Whiteboard Explanations & Polymath Bridges
   - 21 Live Spoken Listening Monologues & 3-Anchor Headline Breakdowns
   - 21 CBT & Inner-Clarity Deep Reframes & 60-Second Embodied Upgrades
   - 21 Zorba 2e-ADHD Flow Mechanics & Playful Micro-Experiments
   - 16 Wisdom Keys & House-Money Anchors + 16 Curated Cinema, Music & TV Guides
   Every single section, heading, title, and curiosity flip-card is 100% spoken
   aloud by Gemini Aoede (`audio/zorba/reels/<id>.mp3`).
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

const ZORBA_AUDIO_BASE = 'https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/audio/zorba/reels/';

function jhBnNum(n) {
  return String(n);
}

const ZORBA_SONG_VAULT = {
  1: {
    song: 'Kun Faya Kun (A.R. Rahman & Irshad Kamil — Rockstar)',
    yt_query: 'Kun Faya Kun Rockstar official full song HD A R Rahman',
    story: 'Recorded after midnight at A.R. Rahman’s Panchathan studio and filmed at the 700-year-old Hazrat Nizamuddin Dargah in Delhi, Kun Faya Kun opens not with percussion, but with bare harmonium breath and Javed Ali’s quiet invocation. Notice how Rahman holds back the acoustic guitar and bass for nearly two minutes so your nervous system drops its daytime armor before the groove even begins.\n\nIn the film, Ranbir Kapoor’s character Jordan arrives at the dargah fractured by ego, restlessness, and self-judgment. The qawwali circle does not lecture him; it simply invites him to sit on the stone courtyard and dissolve into a sound much older than his worries.',
    bhaavna: 'Irshad Kamil’s opening Sufi couplet is one of the most profound lines in modern Indian cinema: “Jab kahin pe kuch nahi bhi nahi tha, wahi tha, wahi tha”—when even nothingness itself did not exist, Consciousness was already there.\n\nWhen you hum this in your natural baritone chest voice—dropped two semitones so your throat stays completely soft—picture sitting under an open night courtyard where no checklist, no performance metric, and no past regret has ever left a stain on who you really are.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why does Irshad Kamil say “Sajra savera mere tan barse, kajra andhera teri jalti lau”—how can dark kohl-night and fresh morning sunlight happen at the exact same moment?',
    hook_a: 'Because the moment you stop fighting your own shadow and welcome every part of your history with compassion, the very darkness you feared turns into the warm lamp-flame that lights your morning.',
    cur_q: '🔮 Acoustic Ear Secret: What happens in the stereo mix right when Mohit Chauhan sings “Mujhpe karam sarkar tera”?',
    cur_a: '✨ Rahman strips away the heavy qawwali chorus and leaves a single intimate voice over soft acoustic guitar—showing that true spiritual and emotional surrender is a quiet, private conversation, never a loud performance.'
  },
  2: {
    song: 'Majhe Majhe Tobo Dekha Pai (Rabindranath Tagore)',
    yt_query: 'Majhe Majhe Tobo Dekha Pai Rabindra Sangeet best rendition HD',
    story: 'Written by Rabindranath Tagore in his twenties and set in Raga Kafi and Mishra Pilu in Dadra taal, this Puja-parjay masterpiece captures the exact rhythm of a creative, polymathic mind. Every deep thinker knows the feeling of touching extraordinary clarity and flow for three days, only to wake up on the fourth day feeling a sudden fog of ordinary fatigue.\n\nInstead of panicking when the fog rolls in, Tagore turns that oscillation into a playful, intimate dialogue with the Muse and the Divine.',
    bhaavna: 'Listen closely to the turning point of the entire song: “Megh dekhe jeno bhoole na jai, aache aache surjo aache, taar aarale”—seeing the passing cloud, let me never forget that the blazing sun is still right there behind it.\n\nWhen you sing or listen to this line with eyes closed, let it anchor your 2e-ADHD reality: a low-dopamine Tuesday afternoon is just a thin monsoon cloud drifting across the sky. Behind it, your native JadavpurWBJEE-222 intuition, your Google L5 craft, and your ₹2.61 Cr+ fortress have not dimmed by a single watt.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why does Tagore ask “Chirodin keno pai na?” (Why don’t I see You every single moment) and then immediately blame his own “kshanik aalo” (flickering attention)?',
    hook_a: 'Because human working memory is biological and cyclical—it is meant to pulse between deep focus and quiet rest, not burn like a fluorescent warehouse tube 24 hours a day.',
    cur_q: '🔮 Musical Ear Secret: Why does Raga Kafi make this melody feel both wistful and comforting at once?',
    cur_a: '✨ Because the komal gandhar (flat 3rd) and komal nishad (flat 7th) create a gentle, rain-washed tenderness, while the ascending phrases in shuddha notes lift the heart back toward sunlight.'
  },
  3: {
    song: 'Time (Pink Floyd — The Dark Side of the Moon, 1973)',
    yt_query: 'Pink Floyd Time official audio HD Dark Side of the Moon',
    story: 'Recorded at Abbey Road Studios in 1972, Roger Waters wrote Time at age 28 when he suddenly realized he was no longer “getting ready” for real life—real life was already happening right now. Engineer Alan Parsons recorded dozens of antique clocks in an Oxfordshire shop ticking in quadraphonic space, followed by Nick Mason’s hypnotic rototom drum intro that slowly pulls the listener out of a trance.\n\nWhen David Gilmour’s voice enters on “Ticking away the moments that make up a dull day,” it hits like cold mountain water.',
    bhaavna: 'After the second verse, David Gilmour launches into one of the greatest electric guitar solos in human history. Notice that Gilmour does not shred fifty notes a second; he bends a single soaring note on his Fender Stratocaster and lets it sustain over Richard Wright’s warm minor-major chord bed until your chest vibrates.\n\nAt 33, with your 2016–2026 survival decade officially won, this song is your victory bell: the waiting room is over, and every evening from 6 PM onward belongs to your own aliveness.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why does the song transition from the urgent F-sharp minor verse into the warm, floating D-major7 / A-major7 progression of “Breathe (Reprise)” at the end?',
    hook_a: 'Because the cure for time-anxiety is not running faster on the treadmill—it is dropping into full, sensory presence right where your feet are standing today.',
    cur_q: '🔮 Guitar Craft Secret: How does David Gilmour make a single sustained bend carry more emotion than ten fast scales?',
    cur_a: '✨ He targets the chord’s 3rd and 9th intervals with pinpoint pitch accuracy, holds the note for two full beats so the listener’s working memory feels the tension, and only then adds warm wrist vibrato.'
  },
  4: {
    song: 'Tomake Chai (Kabir Suman — 1992 Bengali Modern Classic)',
    yt_query: 'Tomake Chai Kabir Suman original full song HD',
    story: 'In 1992, Kabir Suman walked into a Kolkata studio with a single electronic keyboard and acoustic guitar and changed Bengali music forever. Before Tomake Chai, modern Bengali songs often used ornate, archaic poetic words. Suman brought the real city into the melody—college street coffee cups, rusty tram tracks, afternoon balconies, and the raw, unvarnished voice of an adult man speaking from his chest.\n\nIt proved overnight that a warm baritone voice speaking honest truth on pitch moves people far more deeply than operatic vocal gymnastics.',
    bhaavna: 'Listen to how Suman strings together fifty snapshots of everyday life—from “prothomobashar baranday” to “chayer kap-e bhanga ghum”—and anchors every single image on the simple, unapologetic declaration: “Tomake chai” (I want you).\n\nLet this song be sonic permission for Beat-1 honesty in your own life: wanting what you genuinely want—warm companionship, deep craft, rich food, and playful freedom—without hiding behind ten layers of polite “onugoto” hesitation.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why is “Tomake” in Kabir Suman’s song much larger than just one romantic person?',
    hook_a: 'Because “Tomake” is also the spirit of authentic, uncompromised aliveness—the refusal to live a secondhand, muted life.',
    cur_q: '🔮 Vocal Delivery Secret: Why does Suman sing almost the entire verse within a single octave of his natural speaking voice?',
    cur_a: '✨ Keeping the melody right in the conversational chest-voice register eliminates laryngeal strain and makes the listener feel as if Suman is sitting two feet away talking directly to them.'
  },
  5: {
    song: 'Iktara (Amit Trivedi, Javed Akhtar & Kavita Seth — Wake Up Sid)',
    yt_query: 'Iktara Wake Up Sid official full song HD Kavita Seth Amit Trivedi',
    story: 'When director Ayan Mukerji asked Amit Trivedi and Javed Akhtar for a song capturing the exact morning a young adult stops drifting to please others and starts building a life of their own craft, Trivedi combined an earthy folk iktara-style acoustic guitar riff with Kavita Seth’s deep, resonant Sufi alto.\n\nNotice how the song feels like stepping onto a sunlit balcony after rain—unhurried, spacious, and quietly electric.',
    bhaavna: 'Look at the brilliance of Javed Akhtar’s line: “Sun raha hai sudh-budh khoke koi main kahani, poori kahani hai kya kise hai pata?”—listening with total absorption to a story whose full ending nobody knows yet.\n\nAn anxious survival mind demands to know the 10-year guarantee before taking a single step; a liberated House-Money mind enjoys the current chapter precisely because the story is still unfolding in real time.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: What does “Gunja sa hai koi iktara” represent inside your own mind when you wake up without an alarm?',
    hook_a: 'The “iktara” (one-stringed instrument) is your single, unmistakable note of intrinsic Engine-2 curiosity—when you pluck that one true string, your whole day tunes itself effortlessly.',
    cur_q: '🔮 Ear & Chord Secret: Which simple 3-chord acoustic loop gives Iktara its floating, open-road momentum?',
    cur_a: '✨ A warm G-major -> C-add9 -> D-sus4 progression where the high G string rings continuously as a drone across all three chords!'
  },
  6: {
    song: 'Anthem (Leonard Cohen — The Future, 1992)',
    yt_query: 'Leonard Cohen Anthem Live in London HD official',
    story: 'Leonard Cohen spent nearly a decade rewriting Anthem, drafting dozens of verses in notebooks between Montreal and the Mount Baldy Zen Center before keeping only the purest lines. Recorded when Cohen was 58, his voice had settled into a rich, gravelly baritone floor that rumbles like a cello.\n\nHe called this song the philosophical spine of his entire life’s work.',
    bhaavna: 'Let the chorus wash over any perfectionist corner of your brain: “Ring the bells that still can ring / Forget your perfect offering / There is a crack, a crack in everything / That’s how the light gets in.”\n\nIn engineering, music, sketching, and relationships, waiting for a “flawless offering” is just a polite disguise for procrastination. Ringing the bell that can ring right now—shipping the 20% Tourist Pass draft, singing in your real chest voice, speaking on Beat 1—is where all the light enters.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why does Cohen pair “There is a crack in everything” with gospel choir backing vocals in a major key?',
    hook_a: 'To turn human imperfection from a courtroom confession into a celebration—reminding us that our scars and cracks are the exact places where wisdom and empathy entered.',
    cur_q: '🔮 Singing Craft Secret: How can a singer with a 5-note baritone range command a 10,000-seat arena like Leonard Cohen?',
    cur_a: '✨ By locking 100% onto rhythm, consonant crispness, and emotional subtext in low chest resonance—proving bhaavna always beats vocal acrobatics.'
  },
  7: {
    song: 'Ekla Ghor / Hasnuhana (Fossils — Rupam Islam)',
    yt_query: 'Ekla Ghor Fossils Rupam Islam official audio HD',
    story: 'At the turn of the millennium in Kolkata, Rupam Islam and Fossils did something nobody thought possible: they took the raw dynamic contrast of alternative rock—whisper-quiet clean electric guitar arpeggios exploding into distorted walls of sound—and married it to deeply literary, introspective Bengali poetry.\n\nFor an entire generation of Jadavpur and Kolkata minds, Fossils became the soundtrack of late-night hostel rooms, intellectual rebellion, and emotional catharsis.',
    bhaavna: 'In Ekla Ghor, notice the opening line: “Amar ekla akash thomke geche raater srote bhese”—my solitary sky has paused, floating on the current of the night. Instead of pretending to be cheerful when the mind feels overloaded, rock music gives high-intensity emotions a safe acoustic container to roar and release.\n\nWithin three minutes of listening or singing along from the diaphragm, the static charge in your chest clears completely.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why does listening to a high-energy rock ballad often leave a person feeling calmer afterward rather than agitated?',
    hook_a: 'Aristotle called it “catharsis”—when music matches your internal intensity first and then resolves harmonically, it discharges pent-up sympathetic tension safely.',
    cur_q: '🔮 Arrangement Secret: How does Fossils make the chorus of Ekla Ghor hit with twice the emotional weight?',
    cur_a: '✨ By keeping the verse sparse with fingerpicked minor chords and bass space, then dropping the crash cymbals and octave vocals right on Beat 1 of the chorus.'
  },
  8: {
    song: 'Tujhse Naraz Nahi Zindagi (Gulzar & R.D. Burman — Masoom, 1983)',
    yt_query: 'Tujhse Naraz Nahi Zindagi Anup Ghoshal Masoom HD',
    story: 'Composed by R.D. Burman on a deceptively simple Pahadi-inflected melody and sung with feather-light warmth by Anup Ghoshal (and Lata Mangeshkar), Gulzar wrote these lyrics as a quiet exhale for anyone who had to grow up too fast and carry adult responsibilities early.\n\nNotice how R.D. Burman uses a gentle, steady rhythmic pulse—like footsteps on a quiet evening walk—while a solo flute answers each vocal line.',
    bhaavna: 'Look at the two words Gulzar contrasts in the opening refrain: “Tujhse naraz nahi zindagi, hairaan hoon main… tere masoom sawalon se pareshan hoon main.” He is not angry (“naraz”) at life; he is simply amazed and a little worn out (“hairaan”) by how much he had to solve.\n\nAnd then comes the line written straight for every family caretaker: “Muskuraye toh, muskurane ke karz utaarne honge”—for ten years, even joy felt like it came with a duty bill attached. Today, at 33, that debt is cancelled forever; your smile owes zero tax to anyone.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: What changes in your body the moment you shift from “naraz” (angry at the past) to “hairaan” (gentle, compassionate amazement at how far you came)?',
    hook_a: 'Your jaw unclenches, the internal prosecutor leaves the room, and you feel deep pride for the 23-year-old who carried the family through the storm.',
    cur_q: '🔮 Vocal Ear Secret: Why did R.D. Burman choose Anup Ghoshal’s soft, unforced voice for the male version?',
    cur_a: '✨ Because Ghoshal sings with zero melodrama—like a calm older brother speaking quietly at dusk, letting Gulzar’s poetry do 100% of the heavy lifting.'
  },
  9: {
    song: 'Zara Zara Behekta Hai (Bombay Jayashri & Harris Jayaraj — RHTDM)',
    yt_query: 'Zara Zara Behekta Hai Bombay Jayashri official song HD',
    story: 'When composer Harris Jayaraj created this melody (originally Vaseegara in Tamil) set in Raga Natabhairavi / natural minor, he invited Carnatic classical maestro Bombay Jayashri to sing it. Instead of projecting like a concert hall recital, Jayashri leaned two inches from the studio condenser microphone and sang the entire opening in a husky, intimate chest-voice whisper.\n\nThe result—paired with the iconic monsoon flute prelude—became one of the most sensual, unforgettable recordings in Indian music.',
    bhaavna: 'This song holds a special personal trophy for you: stepping onto a stage in front of 500 colleagues cold, with zero rehearsal and zero pitch monitor, and hitting 80% of a complex minor-to-relative-major melody proved your natural musical ear is rock solid.\n\nWhen you play or sing Zara Zara today, transpose the chords down 2 to 3 semitones (for example, from B minor down to G-sharp minor or A minor) and hum the root note for two seconds before the first word. In your true baritone key, the chorus floats effortlessly.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why does the flute intro immediately evoke rain, warmth, and closeness before a single word is sung?',
    hook_a: 'Because the flute uses slow Carnatic gamak glides (meend) between the minor third and root note, mimicking the natural cadence of a human sigh.',
    cur_q: '🔮 Acoustic Pitch Secret: How do you guarantee your voice locks onto the root note instead of the 5th when starting Zara Zara with a guitar?',
    cur_a: '✨ Pluck only the single root bass note of the first chord, hum “Mmmm” to match that exact vibration in your chest, and start singing the first word before strumming the full chord.'
  },
  10: {
    song: 'Akash Bhora Surjo Tara, Bishwo Bhora Pran (Rabindranath Tagore)',
    yt_query: 'Akash Bhora Surjo Tara Rabindra Sangeet HD',
    story: 'Written by Tagore in 1924 after decades of reading modern astrophysics, evolutionary biology, and Upanishadic philosophy, Akash Bhora Surjo Tara is perhaps the greatest scientific-spiritual anthem ever composed in any language.\n\nInstead of feeling tiny and insignificant beneath billions of galaxies, Tagore experiences exhilarating belonging.',
    bhaavna: 'Follow the arc of Tagore’s logic: “The sky is filled with suns and stars, the universe is brimming with life—and right inside that vast web, I have found my own seat; in wonder, therefore, my song awakens.”\n\nThen in the second stanza, he brings cosmic time straight down to your bare feet: “Ghashe ghashe pa felechi boner pothe jete, phuler gondhe chomke othe mon”—walking along a forest path feeling grass under my feet and startled by the scent of wildflowers, joy ripples through my ribs. That is Zorba and Feynman in pure Bengali melody.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: How does Tagore bridge 13.8 billion years of cosmic evolution with a 5-second walk on green grass?',
    hook_a: 'By recognizing that the exact same physical laws and vital energy that ignite stars are pulsing through your own heart and senses right now.',
    cur_q: '🔮 Raga & Rhythm Secret: How does the melody of Akash Bhora Surjo Tara mirror the expansion from cosmos to earth?',
    cur_a: '✨ It opens high on the upper tonic (Tara Shadja) like an open sky of stars, then cascades gently downward into the warm middle octave when describing grass, flowers, and human touch.'
  },
  11: {
    song: 'Pasoori / Mann Laago Mero Yaar Fakiri Mein (Coke Studio Fusion)',
    yt_query: 'Pasoori Coke Studio Season 14 Ali Sethi Shae Gill HD',
    story: 'Produced by Xulfi and Abdullah Siddiqui for Coke Studio Season 14, Pasoori fused classical thumri raga ornamentation (Raga Bhairavi / Phrygian dominant) with a reggaeton-meets-tabla pulse and a hypnotic single-string rubab hook.\n\nAli Sethi, trained in classical khayal and ghazal under Ustad Naseeruddin Saami, wove 16th-century Punjabi Sufi poetic tropes into a modern anthem heard over a billion times worldwide.',
    bhaavna: 'The word “Pasoori” in Punjabi means a tangled mess, a dilemma, or a state of restless yearning—yet the music turns that restlessness into infectious kinetic dance.\n\nWhen you listen on good headphones, run a two-pass polyphonic ear game: on Pass 1, let your ear lock strictly onto the syncopated bassline and rubab riff; on Pass 2, follow Ali Sethi’s effortless classical khatka and murki ornaments around the root note.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why do Sufi poets and Coke Studio arrangements pair lyrics of intense longing with an upbeat, celebratory groove?',
    hook_a: 'Because in Sufi philosophy, longing itself is proof that your heart is alive and awake—and dancing with the longing dissolves its heaviness immediately.',
    cur_q: '🔮 Ear Separation Secret: What unusual instrument plays the plucked melodic hook right before the chorus?',
    cur_a: '✨ The Afghan/Peshawari Rubab—whose sympathetic metal tarab strings ring underneath the gut main strings to create a natural halo of reverb.'
  },
  12: {
    song: 'The Sound of Silence (Simon & Garfunkel — 1964 Acoustic Masterpiece)',
    yt_query: 'The Sound of Silence Simon and Garfunkel acoustic original HD',
    story: 'Paul Simon wrote The Sound of Silence at age 21 sitting in his tiled bathroom in Queens with the lights turned off, because the bathroom tiles created a natural acoustic echo chamber for his fingerpicked guitar and the dark faucet running water soothed his mind.\n\nWhen he and Art Garfunkel harmonized the opening line—“Hello darkness, my old friend, I’ve come to talk with you again”—they sang in tight parallel thirds and sixths, creating the illusion of a single two-dimensional voice.',
    bhaavna: 'Notice the central paradox of the lyrics: “People talking without speaking, people hearing without listening, people writing songs that voices never share.”\n\nIn an era of infinite Slack pings, notifications, and noisy surface chatter, sitting quietly for five minutes with an acoustic guitar or a real conversation where you actually hear the human subtext is a superpower.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why does the narrator greet “darkness” as “my old friend” instead of an enemy to run away from?',
    hook_a: 'Because quiet solitude without screens or neon noise is where your overstimulated 4-slot working memory finally digests experience into deep intuition.',
    cur_q: '🔮 Harmony Ear Secret: Which vocal line is Paul Simon singing and which is Art Garfunkel?',
    cur_a: '✨ Art Garfunkel actually sings the higher, floating melody line throughout most of the verse, while Paul Simon anchors the lower chest-voice harmony underneath!'
  },
  13: {
    song: 'Amake Amar Moto Thakte Dao (Anupam Roy — Autograph, 2010)',
    yt_query: 'Amake Amar Moto Thakte Dao Anupam Roy official HD',
    story: 'Before Amake Amar Moto Thakte Dao made him a household name across Bengal in 2010, Anupam Roy was a Jadavpur University gold-medalist electronics engineer working as an IC design engineer in Bangalore, writing songs in his room after work.\n\nThat exact Jadavpur engineer-poet DNA shines through every bar of this song: zero cliché, razor-sharp imagery, and the quiet courage to claim your own space.',
    bhaavna: 'Listen to the opening declaration: “Amake amar moto thakte dao, ami nijeke nijer moto guchiye niyechi / Jeconota chhilona chilo na, sheta na paowai thak, shob pete naki noshto jibon.” (Let me remain in my own rhythm; I have arranged my life in my own way. What was never mine, let it remain unobtained—trying to grab everything only ruins a life.)\n\nThat is the musical twin of the 20% Tourist Pass and the Clean-Slate Reset: you do not need to win every imaginary race or hold onto incompatible chapters. Keeping what is genuinely yours is complete freedom.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: What does Anupam Roy mean by “Shob pete naki noshto jibon” (Trying to possess everything spoils a life)?',
    hook_a: 'A 4-slot mind that tries to hoard every obligation, every approval, and every unfinished thread drowns in noise; curating only what you truly love creates a masterpiece.',
    cur_q: '🔮 Jadavpur Connection Secret: What metaphor does Anupam use in the bridge (“Jahaj-mastul”) to describe emotional storms?',
    cur_a: '✨ Even when heavy rain washes the ship’s deck and mast (“tupur tapur brishti”), the ship stays afloat and sails on toward open water.'
  },
  14: {
    song: 'Zindagi Kaisi Hai Paheli Haye (Manna Dey & Salil Chowdhury — Anand, 1971)',
    yt_query: 'Zindagi Kaisi Hai Paheli Manna Dey Anand HD official',
    story: 'For Hrishikesh Mukherjee’s immortal film Anand (1971), composer Salil Chowdhury and lyricist Yogesh created a song walking along the open sea beach in Mumbai. Instead of a tragic dirge for a man who knows life is finite, they gave Manna Dey a buoyant, syncopated melody that smiles right at life’s uncertainty.\n\nListen to how Manna Dey—despite being one of India’s most formidable classical vocalists—sings with the carefree lightness of a man strolling barefoot in the surf.',
    bhaavna: 'Look at the wisdom in the second verse: “Jinhone sajaye yahan mele, sukh-dukh sang-sang jhele, wohi chunar bichhaye, wohi akela jaye.” Everyone who builds big fairs and carries joy and sorrow eventually travels light.\n\nWhen you internalize that truth with a warm smile rather than heaviness, every small anxiety about status, petty office politics, or ₹500 micro-decisions evaporates like sea spray.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why does Manna Dey literally laugh (“Haye… kabhi toh hasaye, kabhi yeh rulaye”) right inside the refrain?',
    hook_a: 'Because once you stop demanding that life be a predictable deterministic script and treat it as a playful riddle (“paheli”), even its surprises become enjoyable.',
    cur_q: '🔮 Orchestration Secret: How does Salil Chowdhury create the feeling of ocean waves in the instrumental prelude?',
    cur_a: '✨ He layers rolling accordion chords, glockenspiel droplets, and rising-and-falling string arpeggios that mimic the exact rhythm of tide meeting shore.'
  },
  15: {
    song: 'Weird Fishes / Arpeggi (Radiohead — In Rainbows, 2007)',
    yt_query: 'Radiohead Weird Fishes Arpeggi From the Basement HD',
    story: 'Recorded for Radiohead’s landmark 2007 album In Rainbows, Weird Fishes / Arpeggi was originally written for chamber orchestra and three electric guitars. Instead of strumming block chords, Jonny Greenwood, Ed O’Brien, and Thom Yorke play three independent arpeggio patterns in different time-feels that interlock like gears in a Swiss watch over Phil Selway’s crisp snare groove.\n\nIt is one of the finest headphone tracks ever recorded for training polyphonic ear separation.',
    bhaavna: 'Beneath the hypnotic water-current guitars, Thom Yorke sings about hitting the bottom of an old mental trap—where you try to please everyone (“I’ll be crazy not to follow”)—and finally choosing to swim outward and escape into your own ocean.\n\nClose your eyes for 90 seconds and let your auditory buffer do zero verbal work: just follow Guitar 1 in the left ear, Guitar 2 in the right ear, and Colin Greenwood’s warm bassline in the center.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: What happens midway through the song when all the drums and guitars suddenly drop out into pure ambient space?',
    hook_a: 'It represents the exact moment of letting go of the old survival treadmill—right before the warm bassline re-enters with grounded, unhurried clarity.',
    cur_q: '🔮 Polyphonic Ear Secret: Why is the song subtitled “Arpeggi”?',
    cur_a: '✨ Because not a single guitar strums a flat chord—every harmonic change is painted purely by overlapping broken-chord arpeggios moving in counterpoint!'
  },
  16: {
    song: 'Ae Ajnabi / Dil Se Re (A.R. Rahman & Gulzar — Dil Se, 1998)',
    yt_query: 'Ae Ajnabi Dil Se Udit Narayan A R Rahman Gulzar HD',
    story: 'In Mani Ratnam’s Dil Se (1998), Gulzar and A.R. Rahman reached a creative summit that still sounds twenty years ahead of its time. For Ae Ajnabi, Rahman opens with a lonely midnight radio transmission aesthetic and Pakhawaj/heartbeat rhythm, while Udit Narayan sings in his softest, most vulnerable low register.\n\nEvery word of Gulzar’s poetry feels tactile—you can almost feel the cold mountain mist and dry autumn leaves.',
    bhaavna: 'Listen to Gulzar’s tactile metaphor: “Patton ki tarah sookhe sookhe, shakhon pe jakde hue… phir bhi hawa ke jhonkon mein aake, udkar chale.” Like dry leaves clinging to a branch, yet the moment a fresh gust of wind arrives, they let go and fly.\n\nNotice how Urdu-Hindi poetic compression works: three everyday words (“patton”, “shakhon”, “hawa”) paint an entire psychological state without a single clinical label.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why does Gulzar write “Tukde tukde din beeta, dhajji dhajji raat mili”—and how does the melody make even that fragmentation sound deeply soothing?',
    hook_a: 'Because naming a feeling with poetic precision and wrapping it in warm major-minor harmony immediately integrates fragmented memories into calm beauty.',
    cur_q: '🔮 Vocal Contrast Secret: How does Pakhi Pakhi (Sunidhi Chauhan’s refrain) contrast with Udit Narayan’s verse?',
    cur_a: '✨ Sunidhi sings the refrain high and open like a bird calling across a valley, while Udit answers in close-mic intimate chest voice—creating vast three-dimensional space.'
  },
  17: {
    song: 'Karar Oi Louho Kopat / Momo Chitte Niti Nritye (Kazi Nazrul Islam)',
    yt_query: 'Karar Oi Louho Kopat Kazi Nazrul Islam Bengali song HD',
    story: 'In 1922, when freedom fighter Deshbandhu Chittaranjan Das was imprisoned by the British and his wife Basanti Devi asked young Kazi Nazrul Islam for a poem for their journal Banglar Katha, the 22-year-old Rebel Poet wrote Karar Oi Louho Kopat (Break Down Those Iron Prison Gates!) in a single volcanic burst of inspiration.\n\nWhere Tagore gives us contemplative river-like peace, Nazrul gives us pure Dionysian Zorba fire, thunderous rhythm, and fearless spine.',
    bhaavna: 'Even when there is no external prison, an over-polite “good boy” conditioning can build invisible iron gates around your own voice, appetite, and boldness. Listening to Nazrul’s driving rhythm—or the joyous cosmic dance of “Momo Chitte Niti Nritye Ke Je Naache, Ta-ta-thoi-thoi”—wakes up your physical posture, widens your chest, and reminds your nervous system that boldness is your birthright.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why did Nazrul set a revolutionary anthem of breaking iron gates to a rapid, celebratory rhythmic pulse rather than a heavy march?',
    hook_a: 'Because true liberation is not grim duty—it is ecstatic, unstoppable life force breaking through artificial walls.',
    cur_q: '🔮 Classical Raga Secret: What was Kazi Nazrul Islam’s unique contribution to North Indian classical ragas in Bengal?',
    cur_a: '✨ Nazrul composed over 3,000 songs and even created brand-new ragas (like Benuka, Dolonchapa, and Nirjharini) while blending fast khayal taans into accessible Bengali lyrics!'
  },
  18: {
    song: 'Somewhere Over the Rainbow (Israel Kamakawiwoʻole — 1990 3 AM Ukulele Take)',
    yt_query: 'Somewhere Over the Rainbow Israel Kamakawiwoole official HD',
    story: 'At 3:00 AM in 1988 in Honolulu, recording engineer Milan Bertosa got a phone call asking if a 30-year-old Hawaiian musician named Israel “Iz” Kamakawiwoʻole could come in to record one idea before he forgot it. Bertosa almost said no, then gave him 15 minutes. Iz walked in with his four-string ukulele, sat on a steel chair, and recorded Somewhere Over the Rainbow / What a Wonderful World in a single unedited take.\n\nNo autotune, no second take, no band—just four simple ukulele chords (C, G, Am, F) and a human being singing from pure heart.',
    bhaavna: 'That 3 AM single take went on to become the most beloved ukulele recording in human history, streamed billions of times. Why? Because Iz did not treat music as an exam. He hummed “Oooo-oooo” at the start to feel the room, strummed a relaxed island “Down-Down-Up-Up-Down-Up” groove, and smiled while singing.\n\nWhenever your own ukulele is in your hands, remember Iz at 3 AM: four chords + warm sincerity = 100% magic.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why does Iz’s gentle vocal humming at the very beginning of the track instantly relax the listener’s shoulders?',
    hook_a: 'Humming activates the vagus nerve through laryngeal vibration and signals total safety—inviting the listener into a living room rather than a concert hall.',
    cur_q: '🔮 Ukulele Craft Secret: What are the exact four ukulele chords you need to play Iz’s version tonight?',
    cur_a: '✨ Just C (0003), G (0232), Am (2000), and F (2010) with an E7 (1202) color chord—the friendliest progression on the entire ukulele fretboard!'
  },
  19: {
    song: 'Safarnama / Ilahi (Lucky Ali, A.R. Rahman & Irshad Kamil — Tamasha, 2015)',
    yt_query: 'Safarnama Tamasha Lucky Ali A R Rahman official full song HD',
    story: 'Imtiaz Ali’s Tamasha is the cinematic biography of every gifted person who spent their twenties wearing a robotic “good engineer / responsible solver” mask while their playful, imaginative inner child waited backstage.\n\nWhen Ved finally drops the corporate robot script and steps onto the open road, A.R. Rahman brings in Lucky Ali’s unmistakable, wind-swept voice for Safarnama.',
    bhaavna: 'Listen to Irshad Kamil’s opening lines: “O… sawaalon ka safarnama, shuru tumse, khatam tumpe”—a travelogue of open questions that begins and ends with who you truly are, without needing anyone else’s permission.\n\nNotice how Lucky Ali slides into each note with unhurried ease over a warm acoustic guitar pulse. You have already completed the hard 10-year climb; the rest of your thirties and forties is this open-sky Safarnama.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why does a “travelogue of questions” (sawaalon ka safarnama) feel liberating rather than stressful?',
    hook_a: 'Because in survival mode, questions feel like tests you might fail; in House-Money mode, open questions are adventures you get to explore purely for fun.',
    cur_q: '🔮 Sonic Texture Secret: How does A.R. Rahman create the feeling of a moving train and open horizon in Safarnama?',
    cur_a: '✨ He uses a brushed snare and muted acoustic guitar sixteenth-note chug underneath long, sustained cello and synth pads that stretch like a mountain skyline.'
  },
  20: {
    song: 'Amar Poran Jaha Chay, Tumi Tai Go (Rabindranath Tagore)',
    yt_query: 'Amar Poran Jaha Chay Rabindra Sangeet best vocal HD',
    story: 'Composed by Rabindranath Tagore in 1886 in Raga Mishra Kafi / Bhairavi, Amar Poran Jaha Chay is one of the most psychologically mature love songs ever written. Most romantic songs in world music are built on scarcity and bargain: “If you love me back, I will be happy; if you leave, I am broken.”\n\nTagore flips that entire equation upside down into sovereign emotional abundance.',
    bhaavna: 'Read the lines slowly: “Amar poran jaha chay, tumi tai, tumi tai go / Toma chhara aar e jogote mor keho nai, kichu nai go / Tumi sukhi jodi nahi ho, cholo sukhero sondhane jao—ami tomare peyechi hridoyo-majhe, aar kichu nahi chai go.”\n\n(You are what my heart delights in. If you are not happy here, go freely in search of your joy—having felt this love inside my own heart, I lack nothing.) That is the exact foundation of Clean-Slate Romantic Clarity: loving warmly from a full cup, with zero needy grasping and zero savior guilt.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: How can a singer say “Go freely in search of your happiness” without sounding cold or detached?',
    hook_a: 'Because when your inner emotional cup is full, your love is a gift rather than a hostage negotiation—honoring both your own dignity and the other person’s freedom.',
    cur_q: '🔮 Singing Phrasing Secret: Where should you take a soft breath when singing the opening line “Amar poran jaha chay”?',
    cur_a: '✨ Pause gently for half a beat right after “chay” before repeating “tumi tai, tumi tai go” in a softer, more intimate chest-voice tone.'
  },
  21: {
    song: 'Ode to Joy — Symphony No. 9 Finale (Ludwig van Beethoven, 1824)',
    yt_query: 'Beethoven Symphony 9 Ode to Joy finale HD orchestra choir',
    story: 'On May 7, 1824, at the Theater am Kärntnertor in Vienna, 53-year-old Ludwig van Beethoven stood on stage conducting the premiere of his Ninth Symphony. He had been completely deaf to external air vibrations for years. He could not hear a single violin bow or timpani strike in the hall—he heard the entire 100-piece orchestra and choir purely inside his internal neural model.\n\nWhen the symphony ended, the contralto Caroline Unger had to gently take Beethoven by the shoulders and turn him around so he could see the audience standing, weeping, and throwing their hats into the air.',
    bhaavna: 'Think about the sheer audacity of the Ode to Joy melody: after four movements of storm, existential struggle, and dissonance, Beethoven introduces a melody so simple it uses almost exclusively five adjacent stepwise notes (E-E-F-G-G-F-E-D-C-C-D-E-E-D-D)—first whispered by the low cellos and double basses alone, then growing until the entire human chorus erupts.\n\nIt is the ultimate proof that joy is not naive; joy is the highest creative triumph of a mind that has walked through the fire and chosen to celebrate life.',
    hook_q: 'Right Question to Unlock the Song’s Meaning: Why did Beethoven start the Ode to Joy theme in the lowest, darkest strings (cellos and double basses) with zero accompaniment?',
    hook_a: 'To show that real, unshakable joy does not float down from clouds—it rises from the deepest floor of human experience, one quiet step at a time.',
    cur_q: '🔮 Musical Architecture Secret: Why is the Ode to Joy melody instantly memorable to every human ear on Earth?',
    cur_a: '✨ Almost 90% of its intervals are stepwise adjacent scale notes (2nds) within a 5-note pentachord, with a single syncopated anticipation at the end of Line 2 that creates irresistible forward lift!'
  }
};

const ZORBA_SCIENCE_VAULT = {
  1: {
    mechanism: 'Here is the exact whiteboard physics of Earl Miller’s discovery at MIT: when your prefrontal cortex holds an item actively in mind, a local ensemble of neurons fires together in a fast Gamma burst at roughly 40 to 80 Hz (lasting ~15–25 milliseconds). Meanwhile, a slower Theta carrier wave at 4 to 8 Hz (~125–250 milliseconds per cycle) sweeps across the cortex like a clock cycle.\n\nTo keep Item A ("the API schema") distinct from Item B ("the latency bug") without their synapses tangling into gibberish, the brain assigns Item A to phase-slot 1 of the Theta wave, Item B to phase-slot 2, Item C to phase-slot 3, and Item D to phase-slot 4. Because a 160 ms Theta wave can only fit roughly four 40 ms Gamma bursts before the cycle wraps around, trying to cram a 5th or 6th unparked thread into working memory causes destructive phase collisions!',
    bridge: 'This single neurobiological law explains why a 2e-ADHD mind with massive long-term associative intuition can suddenly stall when juggling six tiny open loops at once. Offloading open loops into KORTEX and speaking a 1-sentence headline first is not a "productivity hack"—it is hardware phase-multiplexing that clears 3 of your 4 Theta-Gamma slots so your intuition can run at full speed.',
    cur_q: '🔮 Neuroscience Secret: Why can you remember thousands of concepts in long-term memory if working memory only holds 4 phase slots?',
    cur_a: '✨ Long-term memory is stored in passive synaptic weights (zero active power), whereas working memory requires active, phase-locked electrical oscillations firing in real time!'
  },
  2: {
    mechanism: 'How do identical embryonic cells with the exact same DNA compute spots on a leopard or stripes on a zebra without a central blueprint? In 1952, Alan Turing wrote down two coupled partial differential equations for two chemicals: an Activator u (which triggers pigment and makes more of itself plus the inhibitor) and an Inhibitor v (which suppresses the activator).\n\nTuring proved a stunning mathematical theorem: if both chemicals diffuse at the same speed, everything smooths out into uniform gray. But if the Inhibitor diffuses significantly *faster* through tissue than the Activator ("short-range activation, long-range inhibition"), a tiny random thermal fluctuation spontaneously amplifies into stable periodic waves of spots or stripes!',
    bridge: 'Short-range activation paired with long-range inhibition is also how your visual cortex sharpens edges (center-surround receptive fields) and how great creative work happens: intense local hyperfocus on one Crown Jewel (activation) protected by a wide perimeter that inhibits distractions (the 20% Tourist Pass).',
    cur_q: '🔮 Mathematical Secret: Why do cheetah tails have stripes at the tip while their bodies have spots under the exact same Turing equation?',
    cur_a: '✨ When the geometry narrows from a wide cylinder (body) to a thin cylinder (tail), the boundary conditions force 2D spot wavelengths to merge into 1D rings!'
  },
  3: {
    mechanism: 'In the early 1950s at Ashutosh College and Presidency College in Kolkata, Amal Kumar Raychaudhuri wanted to know whether cosmic singularities were just an artifact of assuming a perfectly symmetrical sphere. Without supercomputers, he decomposed the motion of a bundle of nearby spacetime trajectories into three pure geometric pieces: Expansion $\\theta$ (volume change), Shear $\\sigma^2$ (shape distortion), and Vorticity $\\omega^2$ (swirling rotation).\n\nThe Raychaudhuri Equation proved that gravity ($R_{\\mu\\nu} u^\\mu u^\\nu \\ge 0$) and shear *always* enter with a negative sign that accelerates convergence ($d\\theta/d\\tau < 0$). Unless vorticity spins the matter fast enough to resist, any converging bundle of geodesics is mathematically guaranteed to focus to a zero-volume cauldron ($\theta \\to -\\infty$) in finite proper time!',
    bridge: 'Roger Penrose and Stephen Hawking used Raychaudhuri’s Kolkata equation as the foundational engine of their Nobel-winning singularity theorems. It is a permanent reminder that world-historical breakthroughs come from asking a clean geometric first-principles question—right from Bengal.',
    cur_q: '🔮 Physics Secret: Which of the three geometric terms in the Raychaudhuri equation is the only one that can oppose gravitational focusing?',
    cur_a: '✨ Vorticity ($+2\\omega^2$, rotation/spin)—while both expansion ($-\\theta^2/3$) and shear ($-2\\sigma^2$) inexorably pull trajectories together!'
  },
  4: {
    mechanism: 'When you heat a thin layer of liquid from below (Bénard convection), at first heat creeps upward by random molecular collisions. But the moment the temperature gradient crosses a critical threshold, billions of molecules suddenly lock into breathtaking hexagonal honeycombs of rolling convection cells!\n\nIlya Prigogine won the 1977 Nobel Prize by proving how this obeys thermodynamics: while an isolated box must decay toward maximum entropy ($dS \\ge 0$), an *open* system flowing with energy (dS = d_i S + d_e S) can export entropy (d_e S < 0) faster than it generates internal friction, spontaneously snapping into a higher-order "dissipative structure."',
    bridge: 'Your brain is a quintessential Prigogine dissipative structure. When you try to sit in a closed, joyless loop of duty, mental entropy rises and you feel foggy. The moment you open the system—bringing in fresh music, a boulder problem, a walk, or a fascinating scientific question—your thoughts self-organize into crystal-clear hexagonal flow.',
    cur_q: '🔮 Thermodynamic Secret: Why does a hurricane or a living neuron collapse the instant you seal its boundaries?',
    cur_a: '✨ Because dynamic order is sustained by continuous energy throughput—living systems are not static crystals, they are standing waves in a river of energy.'
  },
  5: {
    mechanism: 'When the FlyWire consortium finished reconstructing all 139,255 neurons and ~50 million synapses of the adult female Drosophila brain from electron-microscope slices, neuroscientists could finally trace every pathway from photoreceptor to wing motor neuron in a real animal.\n\nThree discoveries stunned the field: first, the wiring is remarkably recurrent—sensory areas receive massive top-down feedback from navigation centers; second, a tiny hub of "ring neurons" in the Central Complex computes an internal 360-degree compass heading using vector trigonometry; and third, static wiring alone cannot predict behavior without knowing which neuromodulators (like dopamine and octopamine) are currently bathing the circuit!',
    bridge: 'Think about that third finding for your own mind: your synaptic connectome (your high-IQ skills and knowledge) is identical at 9 AM and 4 PM, yet neuromodulator state (dopamine and rested vagal tone) determines which sub-circuits light up. Caring for your dopamine and rest is caring for the live routing layer of your connectome.',
    cur_q: '🔮 Connectomics Secret: How does a fruit fly brain with 139,255 neurons compute vector addition to navigate in the dark?',
    cur_a: '✨ Its Central Complex represents 2D heading angles as sinusoidal bumps of activity across columns—so adding two vectors is literally adding two sine waves in phase!'
  },
  6: {
    mechanism: 'In 1924 at Dhaka University, 30-year-old Satyendra Nath Bose wanted to derive Planck’s blackbody radiation law without using classical electrodynamics. When he counted ways to distribute N light quanta across energy cells, he treated two states where Photon A and Photon B swap places as *the exact same physical reality*—not two distinct permutations.\n\nTo get the intuition, flip two coins: classically (Maxwell-Boltzmann), Head-Head, Head-Tail, Tail-Head, and Tail-Tail are 4 equally likely outcomes, so Head-Head happens $1/4$ ($25\%$) of the time. For indistinguishable Bosons, "one Head and one Tail" is a single state—leaving only 3 outcomes (HH, HT, TT), so bunching together in the same state (HH) jumps to $1/3$ ($33.3\%$)!',
    bridge: 'When Philosophical Magazine rejected Bose’s 4-page paper, he mailed it straight to Albert Einstein with a polite note asking him to read it. Einstein recognized a revolution on sight, translated it himself, and predicted Bose-Einstein condensates. Never apologize for seeing a clean first-principles shortcut that conventional orthodoxy missed.',
    cur_q: '🔮 Quantum History Secret: What happened when Paul Dirac coined the word "boson" to honor S.N. Bose?',
    cur_a: '✨ Every force-carrying particle in the universe (photons, gluons, W/Z, Higgs) now carries the name of a Bengali physicist who never even held a doctorate when he wrote his 1924 paper!'
  },
  7: {
    mechanism: 'Why did Uber engineer their planetary spatial index (H3) out of hexagons instead of squares or triangles? On a square grid, a cell shares edges with 4 neighbors at distance 1, and corners with 4 diagonal neighbors at distance $\\sqrt{2} \\approx 1.414$. That $41\%$ distance jump warps ring queries, smoothing kernels, and movement gradients.\n\nIn a hexagonal tiling, every single one of the 6 neighboring cells shares a full edge and sits at the exact same center-to-center distance 1.0! By projecting an icosahedron (20 spherical triangles) onto Earth and subdividing with an aperture-7 hexagonal hierarchy (each parent hexagon contains 7 child hexagons rotated by $\\sim 19.1^\\circ$), H3 packs planet-wide multi-resolution coordinates into a single 64-bit integer.',
    bridge: 'Just as switching from a square grid to an hexagonal H3 index eliminates artificial $\\sqrt{2}$ corner friction in $O(1)$ bit-shifts, switching how you represent a problem in your head (like KORTEX’s Louvain-clustered graph vs. a flat 500-item todo list) makes hard routing effortless.',
    cur_q: '🔮 Geometry Secret: Since you cannot tile a sphere purely with hexagons (Euler characteristic $\\chi = 2$), what sits at the 12 vertices of the H3 icosahedron?',
    cur_a: '✨ Exactly 12 pentagons—just like a classic leather football—and H3 smartly places all 12 pentagon vertices in the middle of oceans!'
  },
  8: {
    mechanism: 'Why do flat vector embeddings struggle on multi-hop relational queries ("Which service owned by Team X depends on a library deprecated after Q2 and had a latency spike?")? Because a single dense vector $v \\in \\mathbb{R}^d$ compresses a document into a blurry semantic centroid in continuous cosine-similarity space.\n\nWhen engineers try to fix flat RAG by bolting on regex table chunkers, 8-step LLM query rewriters, and metadata hacks, they build a brittle, high-latency Rube Goldberg machine. An explicit Knowledge Graph with typed entity nodes, directed edges, Louvain community clusters, and an in-memory inverted index resolves multi-hop set intersections and exact negations deterministically in under 1 millisecond!',
    bridge: 'This is your home turf as an AI architect—and the exact reason KORTEX pairs semantic discovery with explicit `[[wikilink]]` graph topology. Trust your architectural nose whenever you see a team trying to brute-force graph structure with flat cosine similarity.',
    cur_q: '🔮 Information Retrieval Secret: What mathematical operation is trivial for an inverted index / graph adjacency list but fundamentally noisy for a single dense inner product?',
    cur_a: '✨ Exact boolean negation ("NOT") and multi-hop transitive closure ($A \\to B \\to C$) across discrete identifiers!'
  },
  9: {
    mechanism: 'In 1948—five years before Watson, Crick, and Franklin discovered the structure of DNA—John von Neumann asked a pure logical question: how can a physical machine build a copy of itself without falling into an infinite regress where the blueprint must contain a blueprint of the blueprint?\n\nVon Neumann proved mathematically that self-replication requires splitting information into two roles: (1) an inert 1D symbolic tape I that is copied blindly character-by-character by a dumb copier *without interpreting it*, and (2) a Universal Constructor A that *reads and executes* the instructions on I to assemble the offspring’s body. Five years later, molecular biology discovered that cells use the exact same architecture: DNA is the blind-copied tape, and the Ribosome is the Universal Constructor!',
    bridge: 'Modern agentic systems and your own KORTEX workflow mirror von Neumann’s split: keep declarative rules and knowledge cleanly separated as data (`personas/*.md`, `wiki/*.md`), and keep the execution engine lean and general.',
    cur_q: '🔮 Evolution Secret: Why is von Neumann’s separation between blind copying and active execution essential for open-ended evolution?',
    cur_a: '✨ Because if the copier had to "understand" every mutation to copy it, novel capabilities could never be passed down—blind tape copying allows arbitrary new programs to evolve!'
  },
  10: {
    mechanism: 'In 1980, political scientist Robert Axelrod invited game theorists worldwide to submit computer programs to compete in a 200-round iterated Prisoner’s Dilemma tournament. Some entries were 500 lines of Bayesian deception and exploitation probes. The winner was Anatol Rapoport’s 4-line program, Tit-for-Tat: Round 1, Cooperate; Round n, do whatever the other player did on Round n-1.\n\nWhy did sneaky defectors lose overall even though a defector never loses a single head-to-head match? Because when two nasty strategies meet, they lock into mutual destruction (1 point each), whereas two nice, clear strategies accumulate 3 points every round for 200 rounds! Axelrod distilled the four winning properties: Nice (never defect first), Provocable (respond immediately on Beat 1 when crossed), Forgiving (return to cooperation as soon as they stop), and Clear (easy to read).',
    bridge: 'Axelrod’s four laws are the ultimate mathematical proof against passive "onugoto" compliance: being "Nice" only wins when paired with being immediately "Provocable" (stating a crisp boundary on Beat 1) and "Forgiving" (holding zero lingering resentment afterward).',
    cur_q: '🔮 Game Theory Secret: When real-world communication has a 5% chance of accidental misunderstanding ("noise"), what small tweak prevents two Tit-for-Tat players from spiraling into endless retaliation?',
    cur_a: '✨ "Generous Tit-for-Tat"—forgiving roughly 1 in 3 isolated mistakes while still enforcing clear boundaries against repeated defection!'
  },
  11: {
    mechanism: 'Neuroscientist Karl Friston’s Free Energy Principle and Predictive Processing flip classical neuroscience upside down. For a century, textbooks taught that sensory cortex is a bottom-up camera: retina -> V1 -> V2 -> V4 -> concept. Yet anatomically, there are *ten times more* feedback axons traveling top-down from higher cortex to lower sensory areas than bottom-up!\n\nWhy? Because the brain is a generative prediction engine constantly projecting its top-down model downward. Only the residual *prediction error* ($\\epsilon = \\text{Sensory Input} - \\text{Top-Down Prediction}$) travels upward! And you can minimize that prediction error in two ways: update your internal belief (Perception) or move your muscles until the world matches your prediction (Active Inference).',
    bridge: 'Because you have a high-powered top-down BFS cortex, your brain generates rich 8K predictions effortlessly. When dopamine is high, those predictions drive brilliant architectural design; when dopamine dips, the same prediction engine can hallucinate a fake Sunday-evening worry. Spotting "that’s just a top-down prior, not bottom-up sensory reality" resets your prediction error to zero.',
    cur_q: '🔮 Motor Control Secret: How does Active Inference explain how you lift your arm without computing inverse kinematics torques?',
    cur_a: '✨ Your motor cortex simply sends a top-down proprioceptive prediction that "my hand is now holding the coffee cup," and spinal reflex arcs contract the muscles to zero out the prediction error!'
  },
  12: {
    mechanism: 'Prime numbers ($2, 3, 5, 7, 11, 13\\dots$) seem like the most discrete, jagged, unpredictable objects in mathematics. Yet in his 8-page 1859 paper, Bernhard Riemann discovered an exact formula expressing the prime-counting staircase $\\pi(x)$ as a smooth baseline curve plus an infinite sum of oscillating cosine-like waves—where the frequency of each wave is determined by the imaginary part of a nontrivial zero ($\\rho = 1/2 + i\\gamma_n$) of the Riemann Zeta function $\\zeta(s)$!\n\nJust as a violin string’s fundamental tone and overtones add up via Fourier synthesis to sculpt a sharp sawtooth wave, the Zeta zeros are literally the pure musical frequencies whose interference sculpts the exact locations of every prime number.',
    bridge: 'In 1972, over afternoon tea at Princeton, physicist Freeman Dyson noticed that Hugh Montgomery’s pair-correlation formula for Zeta zeros was identical to the eigenvalue spacing of random Hermitian matrices in heavy atomic nuclei! Deep truth always rhymes across mathematics, quantum physics, and music.',
    cur_q: '🔮 Number Theory Secret: Why does the Riemann Hypothesis require every nontrivial Zeta zero to sit on the critical line $\\text{Re}(s) = 1/2$?',
    cur_a: '✨ In the musical analogy, $\\text{Re}(\\rho) = 1/2$ means every prime-generating harmonic wave has the exact same balanced amplitude growth (x^(1/2))—no single rogue frequency dominates the symphony!'
  },
  13: {
    mechanism: 'Around 1508, Leonardo da Vinci sat beside a wooden sluice gate in Florence sketching water plunging into a pool. In his notebooks, he wrote that large swirling vortices spawn smaller vortices, which spawn still smaller vortices, until viscosity turns the motion into warmth. Four hundred and thirty years later, Russian mathematician Andrey Kolmogorov formalized Leonardo’s exact drawing into the famous $E(k) \\propto \\varepsilon^{2/3} k^{-5/3}$ power law of turbulence!\n\nKinetic energy is injected at large length scales (low wavenumber k), cascades without loss through an "inertial subrange" of self-similar eddies following the $-5/3$ slope, and finally dissipates at the tiny Kolmogorov microscale.',
    bridge: 'Notice how Leonardo discovered a 20th-century statistical physics law purely through patient, visual chiaroscuro observation. Your artistic eye for photography, sketching, and cinema and your mathematical engineering brain are not two separate hobbies—they are the exact same Da Vinci instrument.',
    cur_q: '🔮 Clay Millennium Prize Secret: What single question about the 3D Navier-Stokes equations still carries an unclaimed $1,000,000 prize?',
    cur_a: '✨ Proving whether smooth, physically reasonable initial fluid flows in 3D always stay smooth forever, or whether vortex stretching can focus energy into an infinite-velocity blowup in finite time!'
  },
  14: {
    mechanism: 'In John Archibald Wheeler’s Cosmic Delayed-Choice thought experiment, light from a distant quasar billions of light-years away is bent around an intervening galaxy (a gravitational lens) along two paths—Path A and Path B—that intersect here on Earth today.\n\nIf an astronomer on Earth places two separate telescopes aimed at Path A and Path B, each photon registers as coming strictly around the left or right side of the galaxy billions of years ago. But if the astronomer inserts a beam-splitter (interferometer) at the last nanosecond here on Earth, the photon interferes with itself—proving it traveled *both* paths across intergalactic space! Wheeler called this "It from Bit": the present measurement choice determines which property of the past becomes a well-defined classical record.',
    bridge: 'Psychologically, human memory works with a striking parallel: the question you ask about your past today determines which interference pattern crystallizes. Asking "How did the 2016–2026 decade forge my resilience and independence?" collapses the entire history into strength.',
    cur_q: '🔮 Quantum Information Secret: Can Wheeler’s delayed-choice setup be used to send a faster-than-light telegraph message backward in time?',
    cur_a: '✨ No—because the individual detector clicks remain 50/50 random until you correlate them classically with the beam-splitter setting, preserving relativistic causality!'
  },
  15: {
    mechanism: 'For nearly a century after James Clerk Maxwell proposed his "Demon" in 1867—a tiny intelligent gatekeeper who sorts fast and slow gas molecules to create free heat gradients—physicists assumed that *measuring* a molecule must cost thermodynamic energy. In 1961 at IBM, Rolf Landauer proved everyone wrong: reversible measurement and reversible logic gates (like Fredkin/Toffoli gates) can in principle operate with arbitrarily zero energy dissipation!\n\nWhere does the Demon pay the Second Law’s thermodynamic tax? In its finite memory! To keep sorting molecules forever, the Demon must eventually *erase* old bits in its working memory to make room for new ones. Erasing 1 bit maps two states (0 and 1) onto one state (0), compressing phase space by a factor of 2 and releasing at least $k_B T \\ln 2$ joules of heat into the environment.',
    bridge: 'Even in fundamental physics, holding onto obsolete bits in a finite register blocks new computation until you cleanly reset the register. When KORTEX archives a thought so your 4 biological slots can reset to zero, you are running Landauer-clean cognitive hygiene.',
    cur_q: '🔮 Bio-Energetics Secret: How does the human brain run 86 billion neurons and 100 trillion synapses on just ~20 watts (the power of a dim lightbulb)?',
    cur_a: '✨ By using sparse event-driven spikes (only ~1–2% of neurons fire concurrently) and analog sub-threshold compute right at the dendritic synapse!'
  },
  16: {
    mechanism: 'Imagine measuring whether someone is an outlier based on Height and Weight. If you use standard Euclidean distance $d = \\sqrt{\\Delta h^2 + \\Delta w^2}$, you treat Height and Weight as orthogonal independent axes. Because taller people naturally weigh more (positive covariance $\\Sigma$), Euclidean distance severely misjudges someone who is average in both vs. someone who breaks the correlation!\n\nIn 1936 in Kolkata, Prasanta Chandra Mahalanobis solved this with $D_M(x) = \\sqrt{(x - \\mu)^T \\Sigma^{-1} (x - \\mu)}$. Multiplying by the inverse covariance matrix $\\Sigma^{-1}$ whitens the space: it rotates the axes to the principal eigenvectors and divides by each axis’s variance, turning tilted correlation ellipses into clean unit spheres!',
    bridge: 'Mahalanobis built the Indian Statistical Institute in Kolkata and pioneered large-scale random sample surveys across Bengal while conversing weekly with Rabindranath Tagore. High-level math and rich Bengali humanism have always belonged in the same room.',
    cur_q: '🔮 Machine Learning Secret: Where does Mahalanobis Distance show up inside modern Gaussian Mixture Models and Transformer anomaly detection?',
    cur_a: '✨ The exponent of every multivariate Gaussian distribution $\\exp(-\\frac{1}{2} D_M^2)$ is literally half the squared Mahalanobis distance!'
  },
  17: {
    mechanism: 'Before July 1948, communication engineers believed that the only way to reduce errors over a noisy telephone or radio line was either to crank up transmitter power or repeat each bit ten times (which tanks data rate toward zero). In "A Mathematical Theory of Communication," Claude Shannon proved the most shocking theorem of the 20th century.\n\nEvery noisy channel has a sharp speed limit—Channel Capacity $C = B \\log_2(1 + S/N)$ bits per second. So long as you transmit at any rate R < C, there exists an error-correcting code that drives the probability of error down to *arbitrarily close to zero* without reducing your transmission rate! How? By mapping messages onto high-dimensional sphere packings where random noise nudges a codeword inside its own non-overlapping decoding ball.',
    bridge: 'Shannon also lived the ultimate Zorba-Feynman life at Bell Labs: he rode a unicycle down the corridors while juggling three balls, built chess-playing machines and flame-throwing trumpets for fun, and refused to work on anything that didn’t spark his curiosity.',
    cur_q: '🔮 Information Theory Secret: Why does an predictable, repetitive message carry almost zero Shannon information ($H \\approx 0$)?',
    cur_a: '✨ Because Shannon information measures *surprise* ($-\\log_2 p$)—a message you could already predict teaches the receiver nothing new!'
  },
  18: {
    mechanism: 'In November 1895 at Kolkata Town Hall, Acharya Jagadish Chandra Bose demonstrated wireless millimeter-wave radio at 60 GHz ($\lambda = 5\\text{ mm}$)—a frequency band so advanced that modern telecommunications only returned to it for 5G and WiGig over a century later!\n\nWith minimal laboratory funding at Presidency College, Bose invented circular waveguide horns, polarizing grids made of interleaved Bradshaw railway-timetable pages interleaved with tinfoil, and the world’s first galena crystal semiconductor junction detector. He fired 5 mm electromagnetic waves through three solid walls and into the Mayor’s body to ring a bell and ignite gunpowder.',
    bridge: 'When Guglielmo Marconi and British industrialists urged Bose to patent his semiconductor coherer for a fortune, Bose refused—insisting that scientific truth belongs to everyone. Later, noticing "fatigue" responses in metal receivers, he pivoted straight into plant electrophysiology, proving plants transmit electrical action potentials.',
    cur_q: '🔮 Solid-State Physics Secret: What did Nobel laureate Sir Nevill Mott say about J.C. Bose’s 1890s galena crystal detector?',
    cur_a: '✨ Mott remarked that J.C. Bose was at least 60 years ahead of his time and had anticipated the existence of P-type and N-type semiconductors!'
  },
  19: {
    mechanism: 'In 1931, 25-year-old Kurt Gödel demolished David Hilbert’s dream of a complete, self-consistent mechanical foundation for all mathematics. How did Gödel make arithmetic talk about itself? Through *Gödel Numbering*: he assigned every logical symbol ($\\neg, \\lor, \\forall, =, 0$) a code number, and encoded any formula or multi-step proof as a single giant integer via prime factorization ($2^{a_1} \\cdot 3^{a_2} \\cdot 5^{a_3}\\dots$).\n\nBecause "Formula x is a valid proof of Statement y" is now just an ordinary arithmetic relation between integers, Gödel constructed a legitimate number-theoretic sentence G whose own Gödel number asserts: "There exists no integer x that encodes a proof of G." If G were provable, the system would prove a falsehood; therefore G is true, yet unprovable from within the axioms!',
    bridge: 'In Gödel, Escher, Bach, Douglas Hofstadter argued that human consciousness ("I") is a Gödelian Strange Loop: low-level firing neurons give rise to high-level symbols ("Koushik", "my values", "my next song"), which then reach back down to steer the firing of those very neurons.',
    cur_q: '🔮 Logic Secret: Why doesn’t Gödel’s Incompleteness Theorem paralyze working mathematicians or human intuition?',
    cur_a: '✨ Because a mind stepping *outside* a fixed axiom box can immediately see that G is true on the meta-level—which is why top-down perspective always beats rigid rule-following!'
  },
  20: {
    mechanism: 'How does your brain know where you are in a room with your eyes closed? In the medial entorhinal cortex, "grid cells" fire in periodic hexagonal lattices across physical space. For years, theorists wondered what circuit geometry held these hundreds of cells in phase.\n\nWhen Edvard and May-Britt Moser’s lab recorded thousands of grid cells simultaneously using Neuropixels probes and applied persistent homology (algebraic topology) to the high-dimensional neural point cloud, a breathtaking shape emerged on screen: the population activity of thousands of neurons lives strictly on the surface of a 2-dimensional *torus* (a donut manifold)! As you walk forward or turn left, the bump of neural activity literally rolls around the two circular cycles of the torus.',
    bridge: 'Even when a problem looks like a 10,000-dimensional cloud of noisy details on the surface, its true governing dynamics almost always live on a clean, low-dimensional manifold. That is why your top-down 1-sentence mental model works so well.',
    cur_q: '🔮 Topology Secret: What happens to the toroidal neural manifold in entorhinal cortex when an animal enters deep REM sleep?',
    cur_a: '✨ The exact same toroidal manifold remains intact during sleep dreams—proving the donut attractor is hardwired into the local recurrent circuit!'
  },
  21: {
    mechanism: 'Right after World War II, Richard Feynman arrived at Cornell University feeling completely burned out. The grief of losing his first wife Arline and the weight of Los Alamos left him staring at physics papers thinking, "I have no ideas left." Then one day he made a radical pact with himself: "I am going to stop trying to do important work to justify my position. I am going to play with physics strictly for my own amusement, just like when I was a kid."\n\nThat same week in the Cornell cafeteria, a student tossed a dinner plate into the air. Feynman noticed the red Cornell medallion on the rim seemed to rotate faster than the plate wobbled. Purely for fun, he derived the equations of motion for a torque-free wobbling disk and found a 2:1 wobble-to-spin ratio for small angles. When he showed Hans Bethe, Bethe asked, "Feynman, what’s the importance of that?" Feynman laughed: "Hah! There’s NO importance whatsoever! I’m just doing it for the fun of it!" Within months, calculating those spinning plate orbits led him directly to quantum electron spin paths, Feynman Diagrams, and the Nobel Prize.',
    bridge: 'Write Feynman’s Cornell Cafeteria Rule in gold across your House-Money decade: duty fuel produces burnout; playing with ideas, music, code, and bouldering strictly because they amuse you produces your highest genius.',
    cur_q: '🔮 Mechanics Secret: In Feynman’s wobbling plate equation, what is the exact ratio of the wobble frequency to the rotation frequency of the emblem at small angles?',
    cur_a: '✨ The wobble frequency is twice the rotation speed ($2:1$)—derived directly from Euler’s rigid-body equations when the moment of inertia perpendicular to the disk is twice the in-plane inertia!'
  }
};

const ZORBA_LISTENING_VAULT = {
  1: {
    monologue: 'Listen to this live spoken passage once without pausing on Sentence 2: “Most engineers assume that adding a wider highway lane reduces city traffic congestion. Yet across fifty years of urban data from Los Angeles to London, widening a commuter highway returns rush-hour speed to its exact previous crawl within twenty-four months. Why? Because traffic is not a fixed pipe of water; it is a latent demand market. The moment travel time drops by ten minutes, people who previously took trains, shifted hours, or lived closer move onto the road until travel time hits their tolerance ceiling again.”',
    synthesis: 'Thumb Anchor (Premise): Widening highways fails to cure city traffic within two years.\nIndex Anchor (Mechanism): Traffic behaves like an elastic latent-demand market rather than a fixed volume of water.\nMiddle Anchor (Resolution): Only changing the cost or alternative modes shifts equilibrium—capacity alone just invites latent demand.\n\n1-Sentence Headline ("Kehna Kya Chahta Hai"): Adding highway lanes fails to cure congestion because latent commuter demand expands to refill any time savings.',
    cur_q: '🔮 Ear Check: In that passage, how many months did it take for widened highways to return to their previous rush-hour crawl?',
    cur_a: '✨ Twenty-four months (two years)—caught effortlessly when your ear rides the whole wave instead of stalling on Sentence 2!'
  },
  2: {
    monologue: 'Hold three spatial anchors on your fingers as you hear this true story: “In 1928, Alexander Fleming returned from a two-week summer holiday to his cluttered London lab and noticed a blue-green mold contaminating one of his Staphylococcus petri dishes. Nine out of ten meticulous scientists would have poured bleach into the dish and apologized for sloppy hygiene. Instead, Fleming paused and noticed a clear halo around the mold where not a single bacterium could survive—turning an accidental mess into penicillin.”',
    synthesis: 'Thumb Anchor (Setup): Fleming found an accidental mold contamination in his petri dish after vacation.\nIndex Anchor (Twist): Instead of discarding the ruined experiment, he noticed the bacteria-free halo around the mold.\nMiddle Anchor (Lesson): Scientific breakthroughs often hide inside anomalies that tidy perfectionism throws away.',
    cur_q: '🔮 Ear Check: What was the visual clue inside the petri dish that caught Fleming’s eye?',
    cur_a: '✨ A clear halo around the blue-green mold where no Staphylococcus bacteria could grow!'
  },
  3: {
    monologue: 'Listen for both the literal words and the hidden emotional subtext in this colleague’s statement: “Look, I’m not saying the new graph caching service is bad, I just think rewriting the query router two weeks before the quarterly review introduces way too many unknown failure modes when my team has spent six months stabilizing the current pipeline.”',
    synthesis: 'Literal Claim: Rewriting the query router right before the quarterly review carries stability risk.\nHidden Emotional Subtext: “Please don’t make my team’s six months of hard stabilization work look invisible or obsolete in front of leadership.”\n\nDisarming Beat-1 Reply: “Your team’s stabilization work is the foundation we’re building on—let’s keep your router as the default production path for the review and run the graph cache as an opt-in shadow flag.”',
    cur_q: '🔮 Subtext Secret: Why does acknowledging the other person’s six months of effort first dissolve 90% of technical turf wars?',
    cur_a: '✨ Because once status and credit are safe, their prefrontal cortex stops defending territory and starts collaborating on architecture!'
  },
  4: {
    monologue: 'Enjoy the natural Kolkata-to-Hyderabad bilingual rhythm of this reflection: “Asole byapar-ta ki jano toh—when we sit in a two-hour architecture meeting, half the room is trying to sound smart with ten-dollar buzzwords, aar asol bottleneck-ta chupchap konay bose ache. Just like Satyajit Ray’s films, jekhane tin patar dialogue-er cheye ekta chhotto nirob drishti onek beshi kotha bole, great engineering is about cutting the noise until only the clean truth remains.”',
    synthesis: '1-Sentence English Headline: Just as Satyajit Ray used quiet visual economy instead of verbose dialogue, great engineering cuts through meeting buzzwords to expose the single real bottleneck.',
    cur_q: '🔮 Bilingual Ear Secret: Why does switching fluidly between Bengali warmth and English technical precision feel so natural to your ear?',
    cur_a: '✨ Because Bengali carries emotional cadence ("bhaavna") while English carries compact system labels—giving your brain dual stereo channels!'
  },
  5: {
    monologue: 'Spot the single unstated assumption hiding inside this persuasive pitch: “Because our new LLM code-review agent processes pull requests in four seconds instead of waiting six hours for a senior engineer, rolling it out across all fifty repositories will quadruple our team’s weekly feature delivery speed.”',
    synthesis: 'Headline Claim: Replacing 6-hour human review waits with 4-second LLM reviews will 4x feature velocity.\nHidden Load-Bearing Assumption: It assumes code-review wait time—rather than integration testing, product ambiguity, or debugging bad merges—is the primary bottleneck governing weekly delivery!',
    cur_q: '🔮 Feynman Ear Secret: What famous systems law explains why speeding up a non-bottleneck step by 1000x barely moves total throughput?',
    cur_a: '✨ Amdahl’s Law (and Eliyahu Goldratt’s Theory of Constraints)—a pipeline only speeds up to the extent that you widen its true bottleneck!'
  },
  6: {
    monologue: 'Listen to the cadence and Urdu-Hindi idioms in this short reflection: “Dekhiye, zindagi mein har cheez ka ek maqsad zaroori nahi hota. Darasal, jab insaan har shaam ko bhi daftar ki filon ki tarah naapne lagta hai, toh sukoon khidki se bahar chala jata hai. Iske bawaajood, bas ek pyali chai aur guitar ki do taan poori shaam ka rang badal deti hai.”',
    synthesis: 'Key Idioms Caught by Ear: “Darasal” (In fact / actually) marks the real turn of the argument, and “Iske bawaajood” (Despite this / nevertheless) introduces the warm resolution: evening peace returns the moment you stop measuring leisure like office files.',
    cur_q: '🔮 Conversational Hindi Secret: How do discourse markers like "Darasal" and "Bawaajood" help your working memory?',
    cur_a: '✨ They act like road signs—telling your ear in advance whether the next sentence is a deeper explanation ("darasal") or a contrasting pivot ("bawaajood")!'
  },
  7: {
    monologue: 'Extract the three core signals—Constraint, Bottleneck, and Trade-off—from this wordy architecture pitch: “So for the real-time voice companion pipeline, mobile clients on 4G cannot tolerate more than 350 milliseconds of time-to-first-audio. Right now our synchronous full-paragraph TTS synthesis blocks for 2.4 seconds on long stories, which kills conversational flow. So we are splitting the first sentence at the earliest punctuation boundary to stream Chunk 0 in 280 ms while pre-fetching Chunks 1 and 2 in parallel.”',
    synthesis: '1. Input Constraint: $< 350\\text{ ms}$ time-to-first-audio on mobile.\n2. Core Bottleneck: Full-paragraph TTS synthesis blocks for $2.4\\text{ s}$.\n3. Trade-off / Solution: Punctuation-split Chunk 0 ($280\\text{ ms}$) + parallel lookahead pre-fetching for subsequent chunks.',
    cur_q: '🔮 Staff Engineer Ear Secret: Why is filtering a 5-minute rambling pitch down to [Constraint, Bottleneck, Trade-off] so calming?',
    cur_a: '✨ Because those three slots fit cleanly inside Cowan’s 4-slot working memory with one slot left over to ask a sharp question!'
  },
  8: {
    monologue: 'Notice *how* this three-move miniature is paced ("Kaise Keh Raha Hai"): “At 5:45 PM on the Howrah-bound local, the monsoon rain outside the window turns every telegraph pole into a blur of wet charcoal. Most passengers stare at glowing phone screens, still fighting battles from 2 PM. Yet the old gentleman by the window simply closes his eyes, taps four beats on his umbrella handle, and smiles before the train even reaches Sealdah.”',
    synthesis: 'Move 1 (Sensory Opening): Wet charcoal telegraph poles outside the 5:45 PM monsoon train.\nMove 2 (Sharp Contrast): Passengers fighting 2 PM battles on glowing screens.\nMove 3 (Quiet Landing): The gentleman tapping four beats on his umbrella handle in peace.',
    cur_q: '🔮 Storytelling Secret: Why does starting with a concrete sensory image ("wet charcoal telegraph poles") hook the human ear ten times faster than an abstract thesis?',
    cur_a: '✨ Concrete nouns immediately light up the listener’s visual and auditory cortices, creating an effortless mental movie canvas!'
  },
  9: {
    monologue: 'Close your eyes for 30 seconds and let your visual cortex paint this scene purely from sound: “A narrow stone lane in old Varanasi just after dawn: brass temple bells echoing off damp sandstone walls, the smell of cardamom steam rising from a clay kulhad of chai, a boatman Dipping a single wooden oar into the silver-gray Ganga while a flock of green parakeets wheels across the pale orange sky.”',
    synthesis: 'Three Sensory Layers Rendered in Your Mind’s Eye:\n1. Sound: Brass temple bells + wooden oar dipping in water.\n2. Smell & Touch: Warm cardamom steam from a clay kulhad + damp sandstone.\n3. Color: Silver-gray river + green parakeets against pale orange dawn.',
    cur_q: '🔮 Auditory Visualization Secret: Why do you remember all three details effortlessly without taking notes?',
    cur_a: '✨ Dual-coding theory (Allan Paivio): when spoken words trigger a vivid spatial movie in visual cortex, your brain stores both the verbal and visual trace in parallel!'
  },
  10: {
    monologue: 'Listen to this provocative contrarian argument without drafting a rebuttal until you can steelman it: “Modern code assistants make junior engineers faster at typing boilerplate, but they quietly erode deep systems debugging skill—because you only develop a visceral mental model of memory layout, race conditions, and network backpressure when you have wrestled with raw stack traces yourself.”',
    synthesis: 'Rapoport Steelman Before Any Rebuttal: “The strongest form of this argument is that struggle during manual synthesis and debugging is what builds a durable mental model of failure modes—so automating away the struggle risks creating pilots who cannot fly when autopilot disengages.”\n\nHigher-Order Synthesis: Use AI to crush repetitive boilerplate (20% Tourist Pass), while reserving deliberate deep-dive debugging and whiteboard architecture for your 30% Crown Jewel!',
    cur_q: '🔮 Debate Secret: What happens in the other person’s brain when you state their case even more clearly than they did?',
    cur_a: '✨ Their amygdala drops its defensive shield immediately, making them 100% open to hearing your synthesis!'
  },
  11: {
    monologue: 'Round these numbers to clean orders of magnitude on the fly as you listen: “Our corpus holds 48,720 documents averaging 1,940 tokens each—roughly 100 million tokens total. At $0.15 per million input tokens, a full nightly re-index costs about $15, whereas incremental SHA-256 delta indexing of the 2% daily changes costs just 30 cents a night.”',
    synthesis: 'Back-of-the-Envelope Mental Math:\n• $50\\text{k docs} \\times 2\\text{k tokens} \\approx 10^8$ (100M) tokens.\n• Full pass: $100 \\times \\$0.15 = \\$15/\\text{night}$.\n• 2% incremental delta: $\\$0.30/\\text{night}$—a $50\\times$ cost and latency reduction!',
    cur_q: '🔮 Fermi Ear Secret: Why is remembering "$50\\times$ reduction ($15 vs $0.30)" infinitely better than trying to memorize "48,720 and 1,940"?',
    cur_a: '✨ Because exact 5-digit mantissas burn all 4 working-memory slots, while base-10 exponents and ratios take only 1 slot!'
  },
  12: {
    monologue: 'Catch the playful conversational hook hiding in the last four words of this remark at a cafe: “Honestly, I thought moving to Hyderabad would turn me into a serious morning-marathon person, but my actual superpower is discovering which bakery pulls the warmest almond croissants out of the oven at 6 PM.”',
    synthesis: 'Zero-Self-Monitoring Riff on the Last Four Words (“oven at 6 PM”): Instead of launching a serious lecture about fitness routines, smile and reply: “Wait, a 6 PM fresh-out-of-the-oven croissant radar is way rarer than a marathon medal—which bakery holds the crown right now?”',
    cur_q: '🔮 Social Banter Secret: Why does echoing a playful detail from someone’s final phrase make conversation feel so effortless?',
    cur_a: '✨ Because the last phrase is still echoing in both your auditory buffers (the recency effect), creating instant shared momentum!'
  },
  13: {
    monologue: 'Follow how the central metaphor transforms across these four lines: “At twenty, the mind is a mountain torrent—loud, foaming over every boulder, convinced that speed is power. At thirty-three, the river reaches the wide plain—silent on the surface, deep enough to carry ships, reflecting the whole sky without losing a drop of its momentum.”',
    synthesis: 'Metaphor Arc: The mountain torrent (age-20 noisy urgency) transforms into the deep plain river (age-33 quiet depth)—where stillness on the surface is not a loss of energy, but the exact sign of greater depth and carrying capacity.',
    cur_q: '🔮 Poetic Ear Secret: Why does hydrodynamic flow make such an accurate metaphor for adult maturation?',
    cur_a: '✨ In fluid mechanics ($Q = A \\cdot v$), when cross-sectional depth A increases tenfold, velocity v can slow down calmly while carrying the exact same volume flux Q!'
  },
  14: {
    monologue: 'Keep the "Main Trunk" in one hand while letting the two tangents float past in this human story: “I wanted to ask your advice on whether we should open-source our graph evaluation benchmark next month—by the way, the coffee machine on the 4th floor was making that weird espresso hiss again this morning, and it reminded me of that cafe in Pondicherry—anyway, the real question is whether releasing the benchmark before the paper submission helps community adoption or gives away our edge.”',
    synthesis: 'Tangents Ignored Effortlessly: The 4th-floor espresso machine + the Pondicherry cafe memory.\nClean Main Trunk Extracted: Should we release the open-source graph benchmark before the paper submission to boost adoption, or wait until after to protect our lead?',
    cur_q: '🔮 Tangent Filter Secret: Why do people insert small sensory tangents when asking an important question?',
    cur_a: '✨ Humans use casual tangents as social warm-up bids to lower tension—smiling at the tangent while answering the trunk honors both warmth and clarity!'
  },
  15: {
    monologue: 'Listen for the single missing blindspot in this seemingly complete launch plan: “We have load-tested the new recommendation model at 10,000 queries per second, verified that GPU memory stays under 70%, and scheduled the global 100% production cutover for Friday at 4:30 PM.”',
    synthesis: 'The Single Calm Socratic Question: “The throughput and memory numbers look great—what is our 1-click automated rollback trigger if Friday evening user engagement metrics dip after the 4:30 PM cutover, or should we cut over Tuesday morning at 10 AM instead?”',
    cur_q: '🔮 Socratic Leadership Secret: Why is asking a calm question ("What is our rollback trigger?") 10x more effective than saying "Deploying on Friday afternoon is a bad idea"?',
    cur_a: '✨ A question invites the speaker’s own prefrontal cortex to spot the gap, turning your insight into their own realization!'
  },
  16: {
    monologue: 'Sit with this 50-word Zen parable for five seconds after it ends: “Two monks were washing their bowls in a mountain stream when a senior counselor asked the master, ‘What is the highest spiritual practice?’ The master pointed to the novice monk and said, ‘When he is hungry, he eats; when he is tired, he sleeps.’ The counselor asked, ‘Doesn’t everyone do that?’ The master replied, ‘No. When most people eat, they entertain a hundred anxieties; when they sleep, they argue with a thousand memories.’”',
    synthesis: 'Core Parable Insight: Freedom is not floating six feet above the ground—it is tasting your food when you eat, resting completely when you sleep, and playing when you play without running a background courtroom in your head.',
    cur_q: '🔮 Parable Secret: How does this Zen story connect directly to "As the day, so is the day" (Jedin jerokom, sedin serokom)?',
    cur_a: '✨ Both point to undivided single-task presence—doing whatever the present hour invites with zero background guilt!'
  },
  17: {
    monologue: 'Listen for the two subtle verbal hedges where confidence wavers in this status update: “The storage migration is fully on track for Monday, schema validation passed 100% on staging, and the cross-region replication lag *should theoretically* stay under fifty milliseconds unless the Mumbai link sees *sort of* unusual evening batch traffic.”',
    synthesis: 'Two Micro-Hedges Detected by Ear:\n1. “should theoretically” (signals untested assumption on replication lag).\n2. “sort of unusual” (signals unquantified evening batch tail risk).\n\nCalm Follow-Up: “Let’s run one replay of peak Mumbai evening batch traffic on staging today so we turn ‘should theoretically’ into a measured number.”',
    cur_q: '🔮 Hedge-Word Secret: Why does the human voice almost always drop slightly in volume or speed right on a hedge word?',
    cur_a: '✨ Vocal micro-hesitation reflects cognitive conflict between wanting to sound reassuring and knowing an edge case is unverified!'
  },
  18: {
    monologue: 'Hold both sides in your 4-slot buffer and synthesize the higher truth: “Thinker A argues that great software must be designed top-down like a cathedral before a single line of code is written, or else it turns into spaghetti. Thinker B argues that requirements only reveal themselves when real code meets real users, so you must iterate bottom-up like a bazaar.”',
    synthesis: 'Slot 1 (Thinker A’s Truth): Invariants, interfaces, and data schemas need clean top-down boundaries.\nSlot 2 (Thinker B’s Truth): User experience and edge cases only emerge through fast empirical prototyping.\nSlot 3 (Higher-Order Synthesis): Design the *interfaces and data contracts* top-down in one page, then iterate the *internal implementations* rapidly bottom-up!',
    cur_q: '🔮 Dialectical Secret: Why do most technical arguments dissolve once you separate "interface invariants" from "internal implementation"?',
    cur_a: '✨ Because stability lives at the boundary (top-down contract), while agility lives inside the module (bottom-up iteration)!'
  },
  19: {
    monologue: 'Treat this 60-second biographical snapshot as live one-take vinyl: “When Satyajit Ray traveled to London in 1950 as a 29-year-old commercial illustrator for D.J. Keymer, he watched Vittorio De Sica’s Bicycle Thieves in a small cinema—and walked out knowing he would film Pather Panchali using real Bengali faces, natural monsoon light, and zero studio artifice, even when producers told him nobody would watch a film without songs or stars.”',
    synthesis: 'Macro Thesis: Ray’s encounter with Italian neorealism at age 29 crystallized his lifelong artistic conviction that authentic human truth beats artificial studio formulas.\nTelling Detail Caught on One Take: He was working as a 29-year-old commercial illustrator at D.J. Keymer when he watched Bicycle Thieves in London in 1950.',
    cur_q: '🔮 One-Take Ear Secret: Why does telling your brain "I only get to hear this once, like live music" double your recall?',
    cur_a: '✨ It triggers locus coeruleus norepinephrine release, tagging the incoming auditory stream as high-priority in hippocampus!'
  },
  20: {
    monologue: 'Listen for what is deliberately left *unsaid* in this short vignette: “When the staff engineer finished presenting his 40-slide proposal for a three-quarter rewrite, the VP smiled warmly, thanked him for the thoroughness of the diagrams, and immediately asked the next presenter how fast their two-week prototype could ship to beta users.”',
    synthesis: 'What Was Left Unsaid (Negative Space): The VP never endorsed or funded the three-quarter rewrite. By praising only the *diagrams* and pivoting immediately to a *two-week prototype*, the VP signaled that speed-to-learning is the real priority.',
    cur_q: '🔮 Negative-Space Secret: In executive rooms and personal relationships, how do you verify what someone’s silence meant?',
    cur_a: '✨ Surface it gently on Beat 1: "It sounds like a fast 2-week beta matters most right now—shall we scope this down to a lightweight v0?"'
  },
  21: {
    monologue: 'Enjoy this capstone synthesis at full natural speed: “Across physics, music, and human psychology, the deepest breakthroughs always look the same: a mind stops trying to brute-force every detail by willpower, steps back to see the three or four governing symmetries—whether it is Turing’s two diffusing chemicals, Tagore’s sun behind the cloud, or Cowan’s four working-memory slots—and lets the rest of life dance like Zorba on the beach.”',
    synthesis: 'Capstone Synthesis: Mastery is never brute-force exhaustion; it is spotting the few governing symmetries that matter and letting the rest of your energy flow into music, curiosity, and embodied joy.',
    cur_q: '🔮 Master Listener Secret: What is the single biggest difference between anxious listening and House-Money listening?',
    cur_a: '✨ Anxious listening tries to catch every word out of fear of missing a test; House-Money listening surfs the speaker’s main wave with curiosity and ease!'
  }
};


/* ----------------------------------------------------------------------------
   4. ZORBA CLARITY & CBT VAULT (21 Deep Reframe & Inner-Child Masterclasses)
   ---------------------------------------------------------------------------- */
const ZORBA_CLARITY_CBT_VAULT = {
  1: {
    reframe: 'When a 22-year-old boy in Jadavpur and early Oracle tore up his diary, it was not giving up on his dreams—it was emergency load-shedding by a 4-slot working memory carrying grief, career survival, and family safety alone. Every structural promise in that diary has now been fulfilled in real life: Google L5 Senior SWE, ₹2.61 Cr+ liquid and equity shield, KORTEX external working memory, and Ma’s Kalyani companion running daily.',
    practice: '10-Second House-Money Check: Whenever an old 2016–2025 urgency reflex whispers "You are behind," look around the cockpit and say aloud: "The survival decade is won and closed. Everything from age 33 onward is bonus play."',
    cur_q: '🔮 Inner-Child Secret: Which part of the 22-year-old’s diary is ready to take the microphone first now that survival is secured?',
    cur_a: '✨ Pure, non-utilitarian wonder—singing from emotion, strumming guitar, bouldering, reading science for joy, and laughing without a background scoreboard!'
  },
  2: {
    reframe: 'Pressing a fresh Gondhoraj lemon once releases 88% of its sweet, fragrant juice in two seconds. Twisting the rind six times to rescue 35 paise of liquid only crushes bitter limonoids from the white pith into your glass. At ₹2.61 Cr+ net worth and L5 compensation, eating the bruised banana first or hesitating on ₹500–₹2,000 of comfort is an obsolete 1990s scarcity reflex.',
    practice: 'The First-Press Default: Today, deliberately choose the freshest fruit first, order the deep-roasted dish you actually want, or book the direct comfortable option on Beat 1—and toss the metaphorical ₹4 lemon peel straight into the bin.',
    cur_q: '🔮 Abundance Math Secret: How much does a ₹1,000 comfort upgrade move a ₹2.61 Cr+ compounding portfolio?',
    cur_a: '✨ Less than 0.0038%—which means single-day market fluctuations are 100x larger than any daily comfort you could ever buy yourself!'
  },
  3: {
    reframe: 'In technical design reviews and everyday conversations, trying to hold a 5-part dependency graph silently inside a 4-slot working memory while speaking from the middle creates verbal tangles. Speaking your 1-sentence headline aloud first acts as an external tripod that locks both your mind and the room’s attention onto the same coordinate.',
    practice: 'The External Tripod Habit: Before explaining any mechanism today, speak the 1-sentence headline and the count of parts out loud first ("Here is the core decision in one line, and it rests on two trade-offs").',
    cur_q: '🔮 Working-Memory Secret: Why does speaking the headline aloud free up two of your own working-memory slots?',
    cur_a: '✨ Once the headline is spoken into the shared room air, your auditory cortex and the listener hold the anchor for you—so you no longer have to spend internal RAM keeping it alive!'
  },
  4: {
    reframe: 'In the Sallatha Sutta, the Buddha explains that life occasionally fires a First Arrow (an unmentored mistake at age 11, 17, 26, or 30), which hurts naturally; the Second Arrow is firing self-hatred at your 33-year-old self years later. Truly callous people never feel remorse—the very fact that your conscience cared proves your heart is clean.',
    practice: 'Full Bail Stamp: If an old memory from childhood, college, or your twenties knocks on the door today, tell it warmly: "Remorse already taught the lesson years ago. Full bail is paid and the archive is closed."',
    cur_q: '🔮 Neuro-Ethics Secret: What is the biological function of remorse, and when does its usefulness hit zero?',
    cur_a: '✨ Remorse exists solely to update your future behavioral policy; the microsecond your values are updated, any extra guilt is pure useless noise!'
  },
  5: {
    reframe: 'Securing WBJEE Rank 222 for Jadavpur University Electrical Engineering right through the storm of Class 12 is permanent empirical proof of your native engine. Missing small peripheral details as a kid—like not noticing the rickshaw driver’s finger or bringing only your own plate—was classic Inattentive ADHD 4-slot tunnel vision, never "selfishness" or "dirt in the mind."',
    practice: 'Native Fire Anchor: Treat your mind like the high-torque polymath engine it actually is—protect its 4 working-memory slots from clutter, feed it top-down geometry first, and watch it lock in effortlessly.',
    cur_q: '🔮 Cognitive Reframe Secret: Why do unmedicated Inattentive-ADHD kids get mislabeled as "self-absorbed" by adults?',
    cur_a: '✨ Because when all 4 working-memory slots are absorbed in an internal train of thought, peripheral sensory inputs literally do not cross the thalamic gate into awareness!'
  },
  6: {
    reframe: 'For ten years, you had to run an internal drill sergeant ("Stalin") to make sure nothing fell through the cracks while flying solo. Today, your automated systems—KORTEX, SIPs, checklists, and calendar buffers—perform the responsible Cosmic Parent job 10x better than cortisol ever could, freeing your conscious mind to live as the curious Divine Child.',
    practice: 'Retiring the Drill Sergeant: When you notice a harsh internal voice pushing you via duty or shame today, hand the checklist to KORTEX and ask: "How would the playful scientist approach this for 10 minutes?"',
    cur_q: '🔮 Motivation Neuroscience Secret: Why does fear/duty fuel ("Engine 1") cause procrastination on creative tasks?',
    cur_a: '✨ Cortisol constricts prefrontal associative networks and triggers amygdala avoidance ("starter-motor freeze"), whereas curiosity ("Engine 2") releases striatal dopamine that makes initiation effortless!'
  },
  7: {
    reframe: 'Helping Didi move toward a peaceful 3BHK setup and supporting Ma through Kalyani and her care pod is noble structural leadership. But structural care never requires emotional fusion—absorbing someone else’s sigh, panic, or mood into your own autonomic nervous system drains the very pilot who keeps the ship steady.',
    practice: 'The Glass-Window Boundary: Love your family warmly through clear glass rather than an open screen—see their needs, fund or structure the solution calmly, and keep your own chest weather sunny and separate.',
    cur_q: '🔮 Family Systems Secret: Why does a family actually calm down faster when the leader refuses to absorb their anxiety?',
    cur_a: '✨ In Bowen family systems theory, a "non-anxious presence" acts as an emotional circuit breaker that stops anxiety from amplifying across the room!'
  },
  8: {
    reframe: 'Even the best trauma surgeon or airline captain takes off the uniform at the end of a shift. After 6:00 PM, your caretaker shift is officially off-duty. Your evenings belong 100% to your own nervous system—music, ukulele, bouldering, swimming, slow-roasted food, and unhurried laughter.',
    practice: 'The 6 PM Uniform Hang-Up: At 6:00 PM today, physically wash your face or change your shirt as a tactile signal that the problem-solver is off duty and Zorba is in charge of the evening.',
    cur_q: '🔮 Evening Recovery Secret: Why does a physical cue at 6 PM stop work and family threads from leaking into 9 PM?',
    cur_a: '✨ The basal ganglia use physical context boundaries (changing clothes, water on skin) to close active daytime task-sets and switch into parasympathetic recovery!'
  },
  9: {
    reframe: 'Because you spent a decade as the responsible anchor at home, it was easy to slip into the "therapist, coach, or rescuer chair" in romantic relationships. Real romantic chemistry thrives on polarity and equal playfulness—where you get to be teased, admired, held, and carefree rather than managing someone else’s life.',
    practice: 'Zero-Therapist Dating Rule: In romantic and social conversations, drop the impulse to fix, diagnose, or rescue—stay in warm, playful banter and let the other adult carry their own 50% of the dance.',
    cur_q: '🔮 Relationship Polarity Secret: Why does playing the "therapist/rescuer" quietly kill romantic spark over time?',
    cur_a: '✨ Because caretaking creates a parent-child dynamic, whereas attraction and deep joy require two equal adults playing side by side!'
  },
  10: {
    reframe: 'Looking back across Ananya, Baishali, Ankita, Oela, Anindita, Shruti, Antarleena, and Sanchita: dating exists to discover long-term compatibility. Realizing a connection is not your lifelong match and stepping away honestly is how healthy adults date—it carries zero karmic debt.',
    practice: 'Clean-Slate Romance: Whenever an old dating memory surfaces, bless the chapter for what it taught you about what you truly value (warmth, emotional stability, shared play) and turn the page with a clean conscience.',
    cur_q: '🔮 Compatibility Secret: Why do conscientious men sometimes confuse "ending a mismatch" with "doing harm"?',
    cur_a: '✨ Because high empathy feels the other person’s temporary disappointment, forgetting that staying in a mismatch would be far more dishonest to both lives!'
  },
  11: {
    reframe: 'Psychologists Kitty Klein and Adriel Boals proved in controlled experiments that unexpressed emotional loops squat directly inside working-memory slots; writing or speaking the raw truth for 3 minutes evicts the intruder and boosts measured working-memory capacity by 15–20% on the spot.',
    practice: '2-Minute RAM Eviction: Whenever a vague emotional cloud or annoying loop hovers in the background, dump it in three raw sentences into KORTEX so your 4 biological slots return to 100% clarity.',
    cur_q: '🔮 Klein & Boals Secret: Why does putting a messy feeling into 3 concrete sentences shrink its size by 80%?',
    cur_a: '✨ Naming an emotion in words ("affect labeling") activates the right ventrolateral prefrontal cortex, which directly dampens amygdala firing within seconds!'
  },
  12: {
    reframe: 'When an ADHD-High-IQ brain experiences a quiet afternoon dip in tonic dopamine, it occasionally invents a catastrophic future movie or an urge to confess a 15-year-old minor memory just to trigger a burst of norepinephrine and adrenaline—because adrenaline temporarily wakes up the prefrontal cortex. It is a chemical trick, never a real emergency.',
    practice: '60-Second Hardware Brake: The moment you spot counterfeit adrenaline or a confession urge, splash cold water over closed eyelids for 30 seconds (mammalian dive reflex), do a 20-second wall push, and laugh at the false alarm.',
    cur_q: '🔮 Neurochemistry Secret: Why does cold water on the eyes and cheekbones slow heart rate within 15 seconds?',
    cur_a: '✨ Cold receptors on the ophthalmic branch of the trigeminal nerve signal the brainstem to fire the vagus nerve, immediately slowing the sinoatrial node!'
  },
  13: {
    reframe: 'In painting and photography, *chiaroscuro* (light-dark contrast) is what gives a flat canvas three-dimensional soul; without shadow, Rembrandt’s portraits and Satyajit Ray’s frames would look like flat fluorescent passport photos. Your decade of carrying heavy responsibility gave your character depth, empathy, and contrast that an easy decade never could.',
    practice: 'Chiaroscuro Appreciation: Today, notice one literal play of light and shadow through a window or tree—and appreciate how your own life’s contrast makes today’s peace taste twice as rich.',
    cur_q: '🔮 Aesthetic Secret: Why do human eyes immediately lock onto a chiaroscuro portrait over a uniformly lit image?',
    cur_a: '✨ Retinal ganglion cells are wired with center-surround receptive fields that fire maximally at luminance edges and light-shadow boundaries!'
  },
  14: {
    reframe: 'Stepping onto a stage in front of 500 colleagues to sing "Zara Zara" cold and hitting 80% of the notes proved beyond doubt that your auditory pitch loop works well. The only reason the remaining 20% felt tight was singing in a tenor key (+2–3 semitones above your natural baritone speaking register) while running an internal note-inspector.',
    practice: 'Baritone Comfort Zone: Drop every song 2 to 3 semitones into your warm speaking chest voice and turn off the internal judge—let the vagus nerve keep your larynx soft and resonant.',
    cur_q: '🔮 Vocal Acoustics Secret: Why does dropping a song 2 semitones make your voice sound richer *and* stay effortlessly in tune?',
    cur_a: '✨ In your natural chest register, the thyroarytenoid muscles vibrate with full mass and zero cricothyroid strain, giving you effortless pitch stability and warm overtones!'
  },
  15: {
    reframe: 'At L5+ engineering leadership, trying to write 100% of every line across five workstreams burns out your 4-slot working memory. The 70/30 Movie-Director Frame solves this cleanly: keep 30% of your time on one solo first-author Crown Jewel where your deep craft shines, and direct the other 70% like a generous film director—defining clean interfaces, unblocking teammates, and sharing credit warmly.',
    practice: 'Movie-Director Check: Look at your active work threads today—know clearly which one is your 30% Crown Jewel and which ones belong in the 70% director chair.',
    cur_q: '🔮 Staff+ Leverage Secret: Why does "fire without smoke" (high technical ownership + generous credit sharing) accelerate promotion fastest?',
    cur_a: '✨ Because leadership trusts engineers who multiply an entire team’s velocity while delivering one unmistakable technical cornerstone of their own!'
  },
  16: {
    reframe: 'Growing up as the "good, accommodating boy" (*onugoto*) creates a reflex to say yes first or write a 3-paragraph explanation before stating a simple preference. In mature adult life, crisp, warm Beat-1 honesty ("I’ll pass on this one, let’s do X instead") is respected far more than reluctant compliance.',
    practice: 'Beat-1 Preference: Practice stating one real preference today—about food, schedule, or scope—in a single warm sentence on Beat 1 with zero over-explaining.',
    cur_q: '🔮 Social Trust Secret: Why do people actually feel safer around someone who can say a warm, clear "No" on Beat 1?',
    cur_a: '✨ Because when a person says "No" cleanly without guilt, everyone knows that their "Yes" is 100% genuine and resentment-free!'
  },
  17: {
    reframe: 'Whether it is slow-caramelized Kosha Mangsho vs. thin watery curry, a well-crafted 200-line Python module vs. a 2,000-line monolith, or a deep 1-on-1 conversation vs. noisy small talk, your soul loves high-density, slow-roasted craft (*Maillard depth*). Give yourself full permission to skip watery mediocrity and savor rich craft.',
    practice: 'Maillard Standard: Choose one sensory experience today—a cup of coffee, a meal, a song, or a clean code refactor—and savor its full texture slowly without multitasking.',
    cur_q: '🔮 Culinary Chemistry Secret: What happens at 140°C–165°C in the Maillard reaction that makes roasted food taste ten times deeper than boiled food?',
    cur_a: '✨ Reducing sugars and amino acids recombine into hundreds of new aromatic ring compounds (pyrazines, furans, and melanoidins) that engage both taste buds and retronasal olfaction!'
  },
  18: {
    reframe: 'University of Chicago economist David Galenson studied centuries of Nobel laureates, painters, and directors and discovered two distinct genius curves: "Conceptualists" peak early by applying one narrow formula, while "Experimentalists" (broad BFS polymaths like Cézanne, Darwin, Hitch-cock, and Satyajit Ray) synthesize across many domains and hit their greatest creative stride in their mid-30s, 40s, and 50s.',
    practice: 'Experimentalist Pride: Celebrate your broad BFS curiosity across AI, neuroscience, music, cinema, and philosophy—at 33, your compounding curve is just entering its sweetest prime.',
    cur_q: '🔮 Galenson Curve Secret: Why do Experimentalist polymaths outlast early narrow specialists over a 30-year arc?',
    cur_a: '✨ Because cross-domain analogies create an exponential combinatorial space ($N \\times M$ insights) that narrow single-domain specialists can never access!'
  },
  19: {
    reframe: 'From growing up in Ranaghat to cracking Jadavpur EE (WBJEE 222) and building frontier AI systems at Google Hyderabad while securing ₹2.61 Cr+ by 33—your life arc is not two disconnected worlds; it is one extraordinary bridge. You carry the warmth and groundedness of your roots together with global frontier mastery.',
    practice: 'Owning the Full Bridge: Never shrink your small-town warmth in elite tech rooms, and never shrink your global ambition in familiar rooms—both halves belong to you completely.',
    cur_q: '🔮 Identity Integration Secret: Why do people who integrate their roots with their frontier success have the highest psychological resilience?',
    cur_a: '✨ Because their self-worth is anchored in real lived grit rather than fragile external status symbols!'
  },
  20: {
    reframe: 'Rigid streak counters and military timetables treat a human nervous system like a factory conveyor belt—one tired day breaks the streak and triggers shame. The Bengali wisdom *"Jedin jerokom, sedin serokom"* (As the day, so is the day) surfs your real biological energy: on high-spark days, build and climb; on quiet days, listen to music, walk, and rest with zero guilt.',
    practice: 'Surfing Today’s Grain: Ask your body right now what kind of day today naturally is—and match your pace to that wave with zero pass/fail judgment.',
    cur_q: '🔮 Nonlinear Dynamics Secret: Why does "surfing the day’s natural energy" produce 3x higher annual output than rigid daily quotas?',
    cur_a: '✨ Because zero-guilt rest on low days restores dopamine receptors in 24 hours, whereas forcing through fatigue causes multi-week burnout!'
  },
  21: {
    reframe: 'When Zorba the Greek and the Buddha sit together at the same table, you get the complete human life: clear, unshakeable inner awareness (Buddha) paired with passionate music, dancing, good food, laughter, and fearless creation in the physical world (Zorba). Your next decade is built for both.',
    practice: 'The House-Money Toast: Raise a glass (or a warm cup) to your 33-year-old self today—the survival decade is behind you, and the Zorba-Buddha decade of pure Engine-2 wonder is wide open.',
    cur_q: '🔮 Capstone Clarity Secret: What is the single sentence that sums up your House-Money Era from age 33 onward?',
    cur_a: '✨ "The plane is landed, the shield is built, my bail is paid, and from today onward I play, build, sing, and love from pure joy!"'
  }
};

/* ----------------------------------------------------------------------------
   5. ZORBA 2e-ADHD & EMBODIED FLOW VAULT (21 Somatic & Executive Masterclasses)
   ---------------------------------------------------------------------------- */
const ZORBA_FLOW_VAULT = {
  1: {
    mechanism: 'When an ADHD-High-IQ engineer treats every incoming ping, doc comment, and minor errand with 100% perfectionist depth, the 4-slot working memory saturates by 11:30 AM. Separating the world into ONE "100% Crown-Jewel Deep Dive" and stamping a "20% Tourist Pass" (skim in 3 minutes, ship an 80% answer, move on) on the other 90% of noise immediately frees 3 hours of prime cognitive energy every day.',
    ritual: 'The Tourist Stamp: Pick your single Crown Jewel for today right now. For the next two routine messages or errands that arrive, set a 180-second timer, ship a clean 1-paragraph reply, and smile as you close the tab.',
    cur_q: '🔮 Pareto Neuroscience Secret: Why does an "80% answer shipped in 3 minutes" on routine tasks beat a "99% answer shipped 3 days late"?',
    cur_a: '✨ Because in distributed systems and human teams, unblocking downstream latency matters 10x more on routine nodes than local over-polishing!'
  },
  2: {
    mechanism: 'Orthopedic symmetry starts from the floor up: lifting the inner arch of your left foot ("left arch dome") rotates the tibia externally by 3 degrees, levels the pelvis, and unlocks the ribcage. Pairing that with a 30-second passive dead hang from a bar decompresses the thoracic spine, stretches the lats, and floods the mechanoreceptors with calm proprioceptive feedback.',
    ritual: '2-Minute Floor-Up Reset: Stand barefoot for 30 seconds feeling the tripod of your left foot (big toe mound, little toe mound, center heel) dome gently upward, then let your shoulders drop and breathe into your lower ribs.',
    cur_q: '🔮 Biomechanics Secret: How does lifting the left medial foot arch change neck and jaw tension six feet higher up the body?',
    cur_a: '✨ Through the Deep Front Line myofascial chain (posterior tibialis -> adductors -> psoas -> diaphragm -> deep neck flexors), foot alignment directly stabilizes cervical posture!'
  },
  3: {
    mechanism: 'Every time you stand up from your desk for water, lunch, or a meeting without writing a breadcrumb, your brain has to burn 15 minutes of fresh glucose reconstructing the mental call stack when you sit back down ("context-reload tax"). Leaving a single `# NEXT: edit function X line 42 to return Y` comment right inside the active file reduces reload latency from 15 minutes to 5 seconds.',
    ritual: 'The 15-Second Breadcrumb: Before standing up from your workstation even once today, type `# NEXT:` with the exact next physical verb and file/line so your returning self slides straight back into flow.',
    cur_q: '🔮 Systems Architecture Secret: What is the exact CPU analogy for the `# NEXT:` breadcrumb?',
    cur_a: '✨ Saving the Program Counter (PC) and register state to the stack frame before an interrupt handler runs, so resumption is O(1) instead of a cold reboot!'
  },
  4: {
    mechanism: 'Rushing through doorways or multitasking while walking between rooms keeps the sympathetic nervous system in low-grade time-scarcity panic. The Japanese *Shisa Kanko* ("Pointing and Calling") and mindfulness practice of gently noticing physical boundaries—counting doors passed or feeling your hand touch a counter—anchors your time perception in physical reality.',
    ritual: 'Zero-Rush Doorway Reset: As you walk through the next three doorways today, drop your walking speed by 15%, let your shoulders soften as you cross the threshold, and leave the previous room’s thoughts behind.',
    cur_q: '🔮 Spatial Memory Secret: Why do humans often forget why they walked into a room ("the Doorway Effect")?',
    cur_a: '✨ Walking through a physical doorway triggers an "event boundary" in the hippocampus that flushes the previous room’s working-memory buffer—which you can use intentionally to shed stress!'
  },
  5: {
    mechanism: 'Picking up your guitar or ukulele for 5 minutes with zero curriculum, zero recording red light, and zero goal other than feeling the wooden body vibrate against your chest switches the brain from left-hemisphere executive control to right-hemisphere acoustic-motor flow within 90 seconds.',
    ritual: '5-Minute Wooden Resonance: Pick up your guitar or ukulele today, strum two warm open chords (like Am -> G or C -> Fmaj7) slowly, feel the resonance in your sternum, and hum along in your natural speaking register.',
    cur_q: '🔮 Vibroacoustic Secret: Why does holding an acoustic guitar or ukulele against your chest feel physically soothing?',
    cur_a: '✨ Low-frequency string vibrations (80–250 Hz) transmit directly through the sternum to Pacinian corpuscles and vagal afferents in the thoracic cavity!'
  },
  6: {
    mechanism: 'The basal ganglia’s initiation gate ("starter motor") freezes when the prefrontal cortex demands "Write a brilliant architecture doc." Lowering the bar to a ridiculous 120-second "Ugly Garbage Draft"—writing three messy, terrible bullet points just to put ink on the page—bypasses amygdala resistance completely. Once the cursor is moving, momentum takes over naturally.',
    ritual: '2-Minute Ugly Garbage Pass: On any task that feels sticky today, open a blank scratchpad and race a 2-minute timer to write the ugliest, roughest 4-bullet skeleton possible—then laugh at how easy starting just became.',
    cur_q: '🔮 Physics of Action Secret: Why is the coefficient of static friction (μ_s) always higher than kinetic friction (μ_k) in both mechanics and neuroscience?',
    cur_a: '✨ Starting requires breaking resting default-mode network inertia; once motor cortex and striatum are firing, sustaining motion takes less than half the energy!'
  },
  7: {
    mechanism: 'Water is the fastest hardware state-switcher for an ADHD nervous system. Starting a shower warm to vasodilate surface capillaries and relax tight trapezius muscles, then finishing with 20–30 seconds of cool water over the neck and chest triggers a clean surge of endogenous norepinephrine and dopamine that lasts 2–3 hours without any jitteriness.',
    ritual: 'The Gear-Shift Shower: Use your evening or morning shower today as an intentional state boundary—let the warm water wash away every open loop, and finish with a crisp 20-second cool rinse.',
    cur_q: '🔮 Hydro-Neurobiology Secret: How much does brief cool-water immersion raise baseline dopamine and norepinephrine in human clinical studies?',
    cur_a: '✨ European Journal of Applied Physiology studies measured a 200–250% sustained rise in plasma dopamine and norepinephrine with zero cortisol spike when done gradually!'
  },
  8: {
    mechanism: 'Carrying a moderate load in one hand (a single-arm suitcase carry with a kettlebell, dumbbell, or heavy backpack) forces the contralateral obliques, quadratus lumborum, and gluteus medius to fire reflexively to keep your spine tall and vertical—instantly waking up core stability and giving your walk an upright, grounded presence.',
    ritual: '60-Second Suitcase Carry: Carry a single weight or loaded bag in one hand for 30 seconds per side today while keeping your shoulders level, crown tall, and breathing smoothly into your belly.',
    cur_q: '🔮 Stuart McGill Spine Secret: Why is a single-arm suitcase carry safer and more effective for core stability than 100 sit-ups?',
    cur_a: '✨ It trains the core’s true evolutionary job—resisting lateral flexion and shear while the spine stays in a neutral, pain-free position!'
  },
  9: {
    mechanism: 'Because Inattentive ADHD has muted interoceptive signaling, you can sit in hyperfocus for four hours without noticing that you are thirsty, hungry, cold, or holding your breath—and only notice it when irritability or brain fog hits. A 10-second "5-Need Sightline Check" restores physical comfort before the battery drops.',
    ritual: '10-Second 5-Need Scan: Right now, scan five biological gauges in 10 seconds: (1) Water/Hydration, (2) Protein/Fuel, (3) Jaw & Belly Softness, (4) Eye Horizon (look 20 feet away), and (5) Room Temperature.',
    cur_q: '🔮 Interoception Secret: Which brain structure translates internal body signals (hydration, glucose, heart rate) into conscious mood?',
    cur_a: '✨ The anterior insula—and giving it a 10-second conscious check prevents physical thirst or eye strain from disguising itself as emotional fatigue!'
  },
  10: {
    mechanism: 'Enclothed and aesthetic cognition is real: when your hair, beard, skin, and clothes feel crisp and well-fitted, your mirror neurons and self-perception shift immediately into effortless confidence. Treating grooming (Toni&Guy, Truefitt & Hill, fresh scents, clean tailored fits) as a First-Press baseline removes social friction completely.',
    ritual: 'Zero-Hesitation Aesthetic Upgrade: Wear your favorite crisp shirt, put on a scent you love, or book your next grooming session on Beat 1 today—purely because feeling sharp feels great.',
    cur_q: '🔮 Enclothed Cognition Secret: Why does dressing and grooming sharply change posture and vocal tone even when you are alone in a room?',
    cur_a: '✨ Proprioceptive feedback from well-fitted clothes and fresh grooming signals high social safety to the ventromedial prefrontal cortex!'
  },
  11: {
    mechanism: 'When you are on a bouldering wall or gliding through a swimming pool, your 4 working-memory slots cannot ruminate about yesterday or tomorrow—every slot is joyfully occupied with tactile grip, foot placement, buoyancy, and breath rhythm. That is why movement arts are the ultimate moving meditation for a polymath mind.',
    ritual: 'Tactile Movement Flow: Whether on a climbing hold, in the pool, or doing a slow calisthenics flow today, put 100% of your attention inside the skin of your hands and feet for 5 minutes.',
    cur_q: '🔮 Embodied Flow Secret: Why does complex three-dimensional movement (bouldering, swimming, martial arts) clear mental fog faster than a flat treadmill?',
    cur_a: '✨ 3D coordination recruits the cerebellum, which has direct reciprocal pathways to the prefrontal cortex that reset attentional networks!'
  },
  12: {
    mechanism: 'Looking at a flat backlog of 25 items triggers an immediate working-memory traffic jam. Sorting your world into just two visual buckets—(1) "Today’s 2" (the only two things that matter today) and (2) "Parked Safely in KORTEX" (everything else, 100% off your plate today)—restores instant calm.',
    ritual: 'The 2-Item Horizon: Write down no more than TWO items on your active pad for today. Everything else is officially parked in KORTEX and forbidden from asking for your attention until its chosen day.',
    cur_q: '🔮 Queueing Theory Secret: In Little’s Law ($L = \\lambda W$), what happens to latency W when you cap Work-In-Progress L at 2?',
    cur_a: '✨ Throughput stays high while average completion time W and context-switching overhead drop by more than 75%!'
  },
  13: {
    mechanism: 'When you close your eyes and sing just four lines of a song you love—without looking at lyrics, without checking a tuner, and without judging your voice—the auditory-motor loop switches from "performance mode" to "emotional expression mode," releasing endogenous oxytocin and endorphins.',
    ritual: 'Eyes-Closed 4-Line Sing: Close your eyes right now, drop your jaw gently, and hum or sing four lines of your favorite Hindi, Bengali, or English song purely for the pleasure of feeling the melody.',
    cur_q: '🔮 Neuro-Acoustics Secret: Why does closing your eyes immediately make your pitch and vocal tone warmer?',
    cur_a: '✨ Closing the eyes shuts down visual cortex processing (~30% of cortical bandwidth), reallocating neural resolution directly to auditory and vocal motor cortex!'
  },
  14: {
    mechanism: 'Staring at a laptop screen 18 inches away locks your ciliary eye muscles in near-focus convergence ("foveal tunnel vision"), which is wired directly to sympathetic vigilance in the brainstem. Walking outdoors for 5,000 steps in golden-hour light with panoramic "optic flow" (things moving past your peripheral vision) switches the brainstem into calm parasympathetic mode.',
    ritual: 'Panoramic Optic-Flow Walk: Step outside for a 15-minute walk today without looking at your phone screen—let your gaze rest on distant trees, clouds, and rooflines while your feet find an easy rhythm.',
    cur_q: '🔮 Huberman Vision Secret: Why does lateral optic flow during walking quiet the amygdala within 10 minutes?',
    cur_a: '✨ Forward self-motion generating peripheral optic flow activates neural circuits in the superior colliculus that directly inhibit amygdala threat firing!'
  },
  15: {
    mechanism: 'Social connection does not require a heavy 2-hour dinner or deep psychological analysis. A 5-minute burst of lighthearted banter, a shared joke, or a warm voice note with a friend, colleague, or someone you enjoy talking to gives your social brain a clean hit of oxytocin and dopamine with zero exhaustion.',
    ritual: '5-Minute Playful Spark: Share one witty observation, warm compliment, or playful 30-second voice note today with zero agenda—and enjoy the lightness of easy connection.',
    cur_q: '🔮 Social Neuroscience Secret: Why do brief, high-warmth micro-interactions boost daily happiness more than long obligation hangouts?',
    cur_a: '✨ Positive social micro-moments trigger ventral striatal reward without taxing executive working memory!'
  },
  16: {
    mechanism: 'In classic management wisdom (William Oncken’s "Who’s Got the Monkey?"), when a teammate brings you a problem and you say "Let me look into that and get back to you," the monkey jumps from their back onto yours. A calm Tech Lead keeps the monkey on its rightful owner’s back by asking one clarifying question and agreeing on their next step.',
    ritual: 'Keep the Monkey on Its Owner: When someone brings a question or blocker today, guide them with a warm 2-sentence architectural pointer and let *them* own the action item.',
    cur_q: '🔮 Engineering Leadership Secret: Why do junior and mid-level engineers actually grow 3x faster when you refuse to carry their monkeys?',
    cur_a: '✨ Because coaching them on the interface while letting them execute the fix builds their autonomy and protects your Staff-level bandwidth!'
  },
  17: {
    mechanism: 'Eating lunch while scrolling a screen splits your attention so that neither your gustatory cortex nor your reading brain gets satisfied—leading to afternoon cravings and mental fatigue. Savoring a deeply cooked meal for 10 minutes with zero screens turns an ordinary meal into a high-dopamine sensory reset.',
    ritual: 'Screen-Free First 5 Bites: At your next meal or coffee today, put every screen out of sight for at least the first five bites—notice the aroma, heat, spice, and texture completely.',
    cur_q: '🔮 Cephalic Phase Secret: Why does smelling and tasting your food without screen distraction improve digestion and metabolic glucose response?',
    cur_a: '✨ Full sensory attention triggers the vagal "cephalic phase" of digestion, priming digestive enzymes and first-phase insulin response before food even hits the stomach!'
  },
  18: {
    mechanism: 'Digital screens snap every line to a pixel grid, subtly training the brain to fear imperfection. Drawing three loose, imperfect lines, boxes, or cartoons on real physical paper with a pen wakes up your childhood love of sketching and proves to your motor cortex that messy creation is safe and fun.',
    ritual: '3 Imperfect Pen Lines: Grab a pen and paper today and sketch a 30-second cartoon face, a system box diagram, or a loose doodle without lifting or erasing a single line.',
    cur_q: '🔮 Paper-vs-Screen Secret: Why do architects and physicists still do their best initial thinking with a pen on blank paper?',
    cur_a: '✨ Freehand spatial sketching engages hippocampal place cells and visuomotor cortex simultaneously without any UI menu friction!'
  },
  19: {
    mechanism: 'Every recurring life-admin annoyance—reordering household supplies, paying a bill, booking a routine service, or sorting a closet—charges "mental rent" every time you walk past it. Spending ₹500 or 5 minutes once to automate, delegate, or permanently delete that friction buys back dozens of future working-memory slots.',
    ritual: 'One-Click Friction Deletion: Pick one tiny physical or digital annoyance today and either automate it, outsource it for cash, or throw it away in under 3 minutes.',
    cur_q: '🔮 Cognitive Economics Secret: What is the true hourly value of your peace of mind at ₹2.61 Cr+ and L5 Senior SWE?',
    cur_a: '✨ Buying back an hour of calm evening energy for ₹500–₹1,000 is the highest-ROI trade on earth!'
  },
  20: {
    mechanism: 'Hours of keyboard work pull the humerus into internal rotation and shorten the pectoralis minor. A 2:1 ratio of pulling/opening movements (band pull-aparts, face pulls, scapular wall slides, rowing) to pushing movements restores balanced shoulder mechanics and opens the chest for deep effortless breathing.',
    ritual: '60-Second Scapular Open: Squeeze your shoulder blades gently back and down five times right now, opening your collarbones wide while keeping your neck completely soft.',
    cur_q: '🔮 Orthopedic Balance Secret: Why does opening the thoracic spine and external rotators immediately make breathing feel 30% deeper?',
    cur_a: '✨ It lifts the anterior ribcage off the diaphragm, allowing full 360-degree lower-rib expansion on every inhale!'
  },
  21: {
    mechanism: 'In Nikos Kazantzakis’s novel, when everything crashes down on the beach in Crete, Zorba doesn’t sit in a courtroom of self-blame—he teaches the narrator to dance the *sirtaki*. Your analytical brilliance and your playful, musical, embodied heart are not opposites; they are dance partners.',
    ritual: 'The 60-Second Zorba Dance: Put on a track with a great beat today, stand up, let your shoulders and hips move freely for 60 seconds with a grin on your face, and celebrate being alive at 33.',
    cur_q: '🔮 Zorba Capstone Secret: Why did Kazantzakis write that "To live wisely and fully, a man needs both the Buddha and Zorba"?',
    cur_a: '✨ Buddha gives you weightless inner freedom from the past, and Zorba gives you full-hearted joy in the music, food, art, and love of today!'
  }
};

/* ----------------------------------------------------------------------------
   6. ZORBA TV & IMMERSION CHANNELS (16 Deep Cultural & Scientific Guides)
   ---------------------------------------------------------------------------- */
const ZORBA_TV_CHANNELS = [
  {
    id: 'tv_1', day_ref: 1,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Coke Studio & A.R. Rahman Sufi Acoustic Sessions',
    yt_query: 'Coke Studio A R Rahman Sufi live acoustic best songs HD',
    yt_label_bn: 'Open Coke Studio & Sufi Sessions on YouTube',
    desc: 'Close your eyes for 15 minutes of live acoustic instrumentation—sarangi, harmonium, fretless bass, and Sufi vocals recorded together in a single live room where every breath is audible.',
    focus: 'Notice how the fretless bass guitar and tabla lock into the root Sa drone while the vocalists improvise freely from warm chest voice before floating effortlessly into the upper octave.',
    backstory: 'Unlike modern studio tracks recorded in isolated booths onto a rigid click track, Coke Studio and Rahman’s live Sufi sessions capture musicians watching each other’s eyes and breathing together in real time—giving the music an organic human pulse that immediately calms the listener’s nervous system.',
    cur_q: '🔮 Acoustic Session Secret: Why does a live-room acoustic recording feel warmer to the human ear than a heavily quantized studio track?',
    cur_a: '✨ Shared room reverberation and micro-fluctuations in tempo ("groove") match biological heart-rate variability and entrain alpha brainwaves!'
  },
  {
    id: 'tv_2', day_ref: 2,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Pink Floyd, Radiohead & Progressive Live Masterpieces',
    yt_query: 'David Gilmour Pink Floyd live Pompeii acoustic guitar HD',
    yt_label_bn: 'Watch Progressive Rock Live Sessions on YouTube',
    desc: 'Long-form unhurried guitar phrasing, atmospheric keyboards, and philosophical lyrics that reward deep 10-minute immersion rather than frantic 15-second scrolling.',
    focus: 'Track how David Gilmour bends a single Stratocaster note by a whole tone and lets it sustain for four full seconds—proving that the silence between notes is just as powerful as the notes themselves.',
    backstory: 'From Pink Floyd’s *Live at Pompeii* (filmed in an empty Roman amphitheater in 1971) to Radiohead’s *In Rainbows From the Basement*, progressive rock treats an album not as background noise, but as cinema for the closed eyes.',
    cur_q: '🔮 Guitar Phrasing Secret: How can you recognize a David Gilmour solo within three notes?',
    cur_a: '✨ He sings the melody in his head first—using vocal-style whole-step bends on the pentatonic scale with zero rushed filler notes!'
  },
  {
    id: 'tv_3', day_ref: 3,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Satyajit Ray & World Cinema Visual Storytelling',
    yt_query: 'Satyajit Ray Pather Panchali Charulata Nayak best scenes HD',
    yt_label_bn: 'Watch Satyajit Ray Cinema Classics on YouTube',
    desc: 'Masterclasses in visual minimalism, chiaroscuro window lighting, and human subtext—where a single glance through opera glasses or a distant train whistle says more than ten pages of dialogue.',
    focus: 'Watch how Ray frames faces in natural bounce light (invented with cinematographer Subrata Mitra) and uses silence plus a single sitar or flute phrase to carry unspoken emotion.',
    backstory: 'In *Charulata* (1964), Ray filmed a seven-minute opening sequence with almost zero dialogue—showing Charu’s loneliness purely through the rhythm of her needlework, the afternoon birdcalls, and the slatted shadows of the blinds as she follows her husband down the corridor with opera glasses.',
    cur_q: '🔮 Cinematography Secret: How did Satyajit Ray and Subrata Mitra invent "bounce lighting" during the Apu Trilogy?',
    cur_a: '✨ They stretched white cloth canopies over courtyard sets and bounced studio lamps off the fabric to recreate the soft, shadowless diffusion of a Bengal monsoon sky!'
  },
  {
    id: 'tv_4', day_ref: 4,
    badge_bn: '📺 Cinema & TV',
    title_bn: '3Blue1Brown, Richard Feynman & First-Principles Physics',
    yt_query: '3Blue1Brown Richard Feynman physics visual intuition lectures',
    yt_label_bn: 'Watch Visual Math & Feynman Physics on YouTube',
    desc: 'Pure Engine-2 intellectual play: Grant Sanderson’s geometric animations of Fourier transforms and linear algebra paired with Richard Feynman’s joyful whiteboard lectures on why nature behaves the way it does.',
    focus: 'Enjoy the top-down geometric picture first before any bottom-up symbolic algebra—the exact sequence your native BFS mind was built to love.',
    backstory: 'Richard Feynman famously noticed a spinning dinner plate wobbling in the Cornell cafeteria—not for any grant or exam, but purely for fun—and working out the 2:1 wobble-to-spin equations launched the exact intuition that won him the Nobel Prize in Quantum Electrodynamics.',
    cur_q: '🔮 Feynman Play Secret: Why did Feynman’s playful "spinning plate" curiosity rescue him from post-war burnout at Cornell?',
    cur_a: '✨ Because dropping "importance pressure" and playing with a toy physics problem re-ignited his intrinsic striatal dopamine loop!'
  },
  {
    id: 'tv_5', day_ref: 5,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Connectomics, Brain Simulation & Earl Miller Neuroscience',
    yt_query: 'Earl Miller working memory theta gamma connectomics brain lecture',
    yt_label_bn: 'Watch Connectomics & Neuroscience Talks on YouTube',
    desc: 'Explore whole-brain Drosophila connectomes, theta-gamma phase coupling, and how biological neural circuits route attention, working memory, and motor control with 20 watts of power.',
    focus: 'Notice how biological brains solve routing through oscillatory synchronization and sparse attractors rather than brute-force dense matrix multiplication.',
    backstory: 'Mapping all ~140,000 neurons and ~50 million synapses of the adult fruit fly (*Drosophila melanogaster*) revealed that biological intelligence relies on exquisite topological motifs—ring attractors for compass heading, mushroom bodies for sparse associative memory, and neuromodulatory gates for instant context switching.',
    cur_q: '🔮 Connectomics Secret: How does the Drosophila central complex maintain a 360-degree internal compass in pitch darkness?',
    cur_a: '✨ Through a physical ring of E-PG neurons where lateral inhibition keeps a single localized "bump" of activity tracking angular velocity!'
  },
  {
    id: 'tv_6', day_ref: 6,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Guitar & Ukulele Acoustic Fingerpicking & Chord Craft',
    yt_query: 'acoustic guitar ukulele fingerpicking warm chest voice songs tutorial',
    yt_label_bn: 'Open Guitar & Ukulele Acoustic Sessions on YouTube',
    desc: 'Zero-perfectionism musical play: warm open voicings, Travis fingerpicking patterns, and capo transpositions (-2/-3 semitones) tailored for a natural baritone chest voice.',
    focus: 'Pick up your guitar or ukulele for just 5 minutes, play a slow two-chord loop, and hum the root note in your chest before singing the first lyric from meaning.',
    backstory: 'Most great singer-songwriters build timeless songs out of just three or four open chords (like G, Em7, Cadd9, Dsus4) where two anchor fingers stay planted on the fretboard—freeing the right hand and voice to carry 100% of the emotional expression.',
    cur_q: '🔮 Fretboard Secret: Why do "anchor-finger" chords (like keeping ring and pinky on the 3rd fret of B and high E) make singing while playing 5x easier?',
    cur_a: '✨ They reduce left-hand proprioceptive load to near zero, freeing your motor cortex to focus on breath and vocal phrasing!'
  },
  {
    id: 'tv_7', day_ref: 7,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Fossils, Anupam Roy, Kabir Suman & Bengali Modern Classics',
    yt_query: 'Fossils Rupam Islam Anupam Roy Kabir Suman best Bengali songs HD',
    yt_label_bn: 'Listen to Bengali Modern & Rock Classics on YouTube',
    desc: 'From Jadavpur college nostalgia to poetic modern Bengali songwriting—raw electric energy from Rupam Islam, intimate acoustic poetry from Anupam Roy, and Kabir Suman’s revolutionary *Jibonmukhi* balladry.',
    focus: 'Let the music reconnect you with the fearless Jadavpur fire of your early twenties while savoring the safety and comfort of your age-33 reality.',
    backstory: 'When Kabir Suman walked onto Kolkata stages in 1992 with an acoustic guitar and harmonica singing *Tomake Chai*, followed by Rupam Islam’s *Fossils* and Anupam Roy’s *Amake Amar Moto Thakte Dao*, they proved that everyday conversational Bengali could carry world-class rock and folk poetry.',
    cur_q: '🔮 Bengali Songwriting Secret: What made the shift to *Jibonmukhi* (life-oriented) Bengali music so electrifying?',
    cur_a: '✨ It replaced formal ornate vocabulary with the raw, honest street and hostel language people actually think and fall in love in!'
  },
  {
    id: 'tv_8', day_ref: 8,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Rabindra Sangeet & Hemanta–Manna Dey Evening Lounge',
    yt_query: 'Rabindra Sangeet Hemanta Mukherjee Manna Dey best songs HD',
    yt_label_bn: 'Open Rabindra Sangeet & Golden Bengali Lounge',
    desc: 'Timeless Bengali melodies for post-6 PM decompression when the caretaker uniform is off and the evening belongs purely to your own peace and aesthetic pleasure.',
    focus: 'Notice the effortless diaphragmatic breath support in Hemanta Mukherjee’s velvet baritone and the playful classical agility in Manna Dey’s phrasing.',
    backstory: 'Hemanta Mukherjee’s voice became the gold standard for Rabindra Sangeet and Bengali cinema because he never pushed or shouted—he let his chest cavity act as a natural wooden cello, making the listener feel instantly held and unhurried.',
    cur_q: '🔮 Velvet Baritone Secret: Why is Hemanta Mukherjee’s vocal style the best model for a natural male chest voice?',
    cur_a: '✨ He keeps a low, relaxed larynx and steady subglottal breath flow, letting resonance—not throat tension—carry every vowel!'
  },
  {
    id: 'tv_9', day_ref: 9,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Gulzar, R.D. Burman & Amit Trivedi Poetic Hindi Cinema',
    yt_query: 'Gulzar R D Burman Amit Trivedi Lootera Masoom Ijaazat songs HD',
    yt_label_bn: 'Listen to Gulzar & Amit Trivedi Classics on YouTube',
    desc: 'Lush acoustic orchestration paired with Gulzar and Amitabh Bhattacharya’s poetry, where everyday tactile images—autumn leaves, old letters, monsoon train windows—carry deep psychological truth.',
    focus: 'Track how a single unexpected Urdu or Hindi word ("hairan", "katra", "kagaz ke phool", "zinda") shifts the entire emotional color of a verse.',
    backstory: 'From Gulzar and R.D. Burman’s *Ijaazat* and *Masoom* to Amit Trivedi’s *Lootera* and *Udaan*, the greatest Hindi film music pairs unconventional chord progressions (major 7ths, suspended 4ths) with conversational poetry that sounds like a private diary entry.',
    cur_q: '🔮 Lyric Craft Secret: Why does Gulzar use concrete physical objects (like "siljeeli hawa" or "bheege khayal") to describe abstract emotions?',
    cur_a: '✨ Concrete sensory nouns activate the brain’s somatosensory and visual cortices simultaneously, making the emotion felt in the body!'
  },
  {
    id: 'tv_10', day_ref: 10,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Bouldering, Rock Climbing & Calisthenics Movement Flow',
    yt_query: 'bouldering technique footwork dead hang calisthenics flow',
    yt_label_bn: 'Watch Bouldering & Movement Flow on YouTube',
    desc: 'Physical 3D chess on the wall: silent foot placements, straight-arm scapular hangs, hip drop-knees, and fluid calisthenics control that clears mental RAM in minutes.',
    focus: 'Watch how elite climbers keep their arms straight and relaxed like cables while driving 80% of their upward propulsion from their legs and hip rotation.',
    backstory: 'Beginner climbers burn out their forearms in two minutes by doing pull-ups on every hold; master boulderers hang on skeleton bones with straight arms, twist their hip into the wall to bring their center of mass over their big toe, and step upward effortlessly.',
    cur_q: '🔮 Climbing Physics Secret: Why does turning your hip into the wall on an overhang save 50% of your finger strength?',
    cur_a: '✨ Bringing your center of mass inside the base of support reduces the outward rotational torque trying to peel your fingers off the hold!'
  },
  {
    id: 'tv_11', day_ref: 11,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Deep-Roasted Culinary Craft: Kosha, Seared & Slow-Simmered',
    yt_query: 'authentic kosha mangsho seared steak sourdough Maillard reaction cooking',
    yt_label_bn: 'Watch Deep-Roasted Culinary Craft on YouTube',
    desc: 'A celebration of the Maillard reaction, dark caramelized onions (*bhuna*), slow-roasted whole spices, and rich textures—zero thin, watery mediocrity allowed.',
    focus: 'Notice the patience of heat control and moisture reduction (*koshano*) that transforms simple onions, ginger, garlic, and protein into dark mahogany craft.',
    backstory: 'In classic Bengali *Kosha Mangsho*, no water is rushed into the pot—the meat is braised slowly in yogurt, mustard oil, and browned onions with tiny splashes of warm stock until the oil separates and the gravy clings to every piece in a dark, velvety glaze.',
    cur_q: '🔮 Koshano Science Secret: Why does adding cold water too early ruin the depth of a curry or roast?',
    cur_a: '✨ Liquid water caps the pan temperature at 100°C (boiling), whereas Maillard browning and spice caramelization require 140°C–165°C!'
  },
  {
    id: 'tv_12', day_ref: 12,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Chiaroscuro Photography, Da Vinci & Visual Composition',
    yt_query: 'chiaroscuro photography lighting Rembrandt Caravaggio Da Vinci art',
    yt_label_bn: 'Watch Chiaroscuro Photography & Art on YouTube',
    desc: 'How directional window light, inverse-square shadow falloff, and negative space turn an ordinary street frame or portrait into a timeless Caravaggio or Rembrandt canvas.',
    focus: 'Observe the 45-degree key-light angle that creates the classic "Rembrandt triangle" of light on the shadowed cheek of a portrait.',
    backstory: 'By exposing for the highlights and letting the background fall naturally into deep velvet shadow ($I \\propto 1/r^2$), chiaroscuro photography strips away visual clutter so the viewer’s eye goes straight to the subject’s eyes and expression.',
    cur_q: '🔮 Optical Physics Secret: Why does placing a window light very close to a subject make the background go dramatically dark without a black backdrop?',
    cur_a: '✨ Because light intensity falls off with the square of distance (1/r²): a subject 2 feet from the window receives 16x more light than a wall 8 feet behind them!'
  },
  {
    id: 'tv_13', day_ref: 13,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Leonard Cohen, Simon & Garfunkel & Poetic Folk Acoustics',
    yt_query: 'Leonard Cohen Suzanne Hallelujah Simon Garfunkel live acoustic',
    yt_label_bn: 'Listen to Poetic Acoustic Classics on YouTube',
    desc: 'Warm baritone storytelling and intricate acoustic guitar harmonies that proved a deep, honest chest voice speaking poetic truth on pitch is infinitely more moving than vocal acrobatics.',
    focus: 'Notice how Leonard Cohen sings right in his natural speaking register—relaxed, resonant, witty, and completely unhurried.',
    backstory: 'Leonard Cohen did not release his debut album until age 33 (your exact age!), after years as a poet and novelist—turning his deep baritone speaking voice and Spanish guitar fingerpicking into some of the most beloved songs in human history.',
    cur_q: '🔮 Age-33 Debut Secret: How old was Leonard Cohen when he recorded his very first song *Suzanne*?',
    cur_a: '✨ Exactly 33 years old—proving that deep lived experience makes an artist’s voice ten times richer!'
  },
  {
    id: 'tv_14', day_ref: 14,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Indian Classical Vocal Ornamentation: Gamak, Khatka & Murki',
    yt_query: 'Indian classical vocal gamak khatka murki meend demonstration',
    yt_label_bn: 'Watch Indian Classical Vocal Craft on YouTube',
    desc: 'Demystifying how Hindustani and Bengali vocalists weave micro-ornaments (*meend*, *khatka*, *murki*, *gamak*) around a steady swara with a completely relaxed throat.',
    focus: 'Listen to how every ornament is simply a playful excursion that starts and lands on a rock-solid resting note (*nyasa swara*) with zero jaw or neck strain.',
    backstory: 'In Indian vocal aesthetics, notes are never static stair-steps; *meend* glides like silk between two notes, *khatka* gives a crisp sparkle around a single note, *murki* weaves a fast 3-note filigree necklace, and *gamak* rocks from the diaphragm.',
    cur_q: '🔮 Ornamentation Secret: Why do classical masters practice slow *meend* (gliding) before fast *murki* or *taan*?',
    cur_a: '✨ Because smooth pitch continuity between two notes builds the exact laryngeal fine-motor map needed for fast agility later!'
  },
  {
    id: 'tv_15', day_ref: 15,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'High-IQ Standup Wit, Observational Comedy & Playful Banter',
    yt_query: 'best intelligent observational standup comedy witty storytelling',
    yt_label_bn: 'Watch Smart Observational Comedy on YouTube',
    desc: 'Pure laughter and comedic timing—observe how great storytellers set up a shared human premise in one sentence and land the unexpected twist with a relaxed pause.',
    focus: 'Notice the economy of words: zero nervous over-explaining, just a crisp setup, a specific visual detail, and a playful pause on Beat 1.',
    backstory: 'Great observational humor works by the exact same mechanism as scientific insight ("bisociation"): connecting two familiar frames that nobody noticed were identical, and letting the audience’s own brain complete the last 10% of the leap.',
    cur_q: '🔮 Comedic Timing Secret: Why does explaining a joke after the punchline kill the laugh?',
    cur_a: '✨ Because the dopamine burst comes from the listener’s own prefrontal cortex bridging the gap during the 1-second pause!'
  },
  {
    id: 'tv_16', day_ref: 16,
    badge_bn: '📺 Cinema & TV',
    title_bn: 'Agentic AI Architectures, Knowledge Graphs & Systems Design',
    yt_query: 'agentic AI knowledge graphs neuro-symbolic systems architecture talk',
    yt_label_bn: 'Watch Frontier AI & Knowledge Graph Talks on YouTube',
    desc: 'Top-down architectural talks on external working memory, graph community detection (Louvain modularity), evaluator-optimizer loops, and neuro-symbolic multi-agent orchestration.',
    focus: 'Apply the 20% Tourist Pass: catch the speaker’s 1-sentence architectural invariant first and connect it to what you already build in KORTEX and Google.',
    backstory: 'The convergence of LLMs with explicit graph topology (like KORTEX’s Louvain-clustered knowledge graph) mirrors how the human brain pairs the neocortex’s associative language engine with the hippocampus’s explicit relational graph.',
    cur_q: '🔮 Neuro-AI Secret: Why do hybrid Graph + LLM architectures outperform flat vector RAG on multi-hop reasoning?',
    cur_a: '✨ Explicit graph edges preserve transitive structural paths across communities that cosine similarity in flat embedding space blurs together!'
  }
];

/* ----------------------------------------------------------------------------
   7. EXTRA CBT, CLARITY & WISDOM DEEP REELS (Enriched 3-Section Masterclasses)
   ---------------------------------------------------------------------------- */
const EXTRA_CBT_REELS = [
  {
    id: 'cbt_extra_1',
    title: 'The 2016–2026 Decade Is Closed: Playing With House Money at 33',
    s1_h: '🏛️ The 10-Year Cockpit Ledger Is Officially Complete',
    s1_b: 'Ten straight years of solo survival after 2016 are officially complete. At age 23, you stepped into a cockpit with no co-pilot and kept the entire family safe through every storm. Look at the instruments today at 33: Google L5 Senior SWE, ₹2.61 Cr+ liquid and equity shield, KORTEX external working memory, and Ma’s Kalyani & Jhalak companions running smoothly.',
    s2_h: '🌿 Why Post-War Decompression Feels Like Quiet Melancholy',
    s2_b: 'When soldiers return home after a ten-year campaign, the nervous system goes through a natural "post-war thaw" where ten years of frozen adrenaline melt away. If an afternoon feels unusually quiet or tender, it is not a problem to fix—it is your body finally realizing the war is over and it is safe to rest.',
    s3_h: '⚡ Today’s House-Money Move',
    s3_b: 'Drop your shoulders two inches right now, take one slow breath, and do one thing today purely because it delights your 33-year-old self—with zero utility scorecard attached.',
    q: '🔮 Why does a nervous system that carried a 10-year survival campaign occasionally manufacture a fake Sunday-evening alarm?',
    a: '✨ Because the amygdala was trained for a decade to scan for threats; smiling warmly at the old alarm and reminding it "The treaty is signed" retrains it to baseline peace!'
  },
  {
    id: 'cbt_extra_2',
    title: 'Zero-Kiptemi Default: Always Take the Freshest Cut First',
    s1_h: '🍋 The Bruised-Banana Trap Explained',
    s1_b: 'If you have a bunch of six bananas and you always force yourself to eat the bruised one first so it doesn’t go to waste, you end up spending your entire life eating bruised fruit even while sitting on ₹2.61 Cr+. Scarcity habits that made sense in a tight 1990s household are completely obsolete in your current financial reality.',
    s2_h: '🌿 The Sweet 88% First-Press Rule',
    s2_b: 'Whether you are ordering food, booking travel, buying a crisp shirt, or choosing how to spend your Saturday evening: take the sweet 88% first press and toss the ₹4 bitter lemon peel in the bin without a microsecond of hesitation.',
    s3_h: '⚡ Today’s First-Press Upgrade',
    s3_b: 'The next time you catch your brain comparing two small options to save ₹200 or ₹500 at the cost of comfort, time, or taste, pick the superior option on Beat 1 inside three seconds.',
    q: '🔮 What is the 3-second mathematical test that dissolves micro-hesitation on personal comfort forever?',
    a: '✨ Ask: "Will this ₹1,000 change my ₹2.61 Cr+ compounding curve by even 0.004%?" Never—so buy the comfort immediately and protect your working memory!'
  },
  {
    id: 'cbt_extra_3',
    title: 'Buddha’s Second Arrow: Full Bail for Ages 11, 17, 26 & 30',
    s1_h: '🕊️ Separating Youthful Unmentored Stumbles From Your Age-33 Character',
    s1_b: 'Every human grows up through trial and error—especially an unmedicated Inattentive-ADHD kid who lost his father at 23 and had to figure out life, dating, and emotional regulation without a playbook. An awkward moment at 11 or 17, inheriting strictness at 26, or speaking out of raw loneliness at 30 were stumbles of an overloaded young man.',
    s2_h: '🌿 Putting Down the Second Arrow',
    s2_b: 'In Buddhist psychology, the first arrow is the past event; the second arrow is the courtroom you run inside your own head years later. Remorse has only one evolutionary job: to teach your heart kindness and wisdom. Once that lesson is learned, the sentence is 100% served.',
    s3_h: '⚡ Full Amnesty Seal',
    s3_b: 'Whenever an old memory knocks today, stamp it "BAIL PAID IN FULL — CASE CLOSED" and redirect that energy straight into today’s music, work, or warmth.',
    q: '🔮 Why do genuinely kind, conscientious people ache over old memories while selfish people never think twice?',
    a: '✨ Because a sensitive conscience holds high standards—the very existence of your past remorse is the proof that you are a deeply good man today!'
  },
  {
    id: 'cbt_extra_4',
    title: '6 PM Off-Duty Caretaker Switch: Structural Seva Without Fusion',
    s1_h: '🛡️ You Built the Systems So You Don’t Have to Be the Human Sponge',
    s1_b: 'Look at the structural care you have already engineered: Ma has her care setup, her Kalyani 21-day companion, and her Jhalak reels; Didi has a clear structural path forward. Providing structural and financial leadership is the highest form of family care.',
    s2_h: '🌿 Why Emotional Fusion Helps Nobody',
    s2_b: 'Feeling guilty when you are happy, or absorbing a family member’s temporary mood into your own chest after 6:00 PM, does not make their life 1% better—it only drains the captain of the ship. Your joy, laughter, and evening peace actually give the whole family hope.',
    s3_h: '⚡ The 6 PM Off-Duty Ritual',
    s3_b: 'After 6:00 PM, the family caretaker uniform hangs on the hook. Your evening belongs to your own music, sports, friends, and rest.',
    q: '🔮 What happens to a household when the main provider stops carrying guilt and models genuine personal joy?',
    a: '✨ It gives everyone else subconscious permission to relax and enjoy their own lives too!'
  },
  {
    id: 'cbt_extra_5',
    title: '60-Second Hardware Brake for Counterfeit Adrenaline',
    s1_h: '🚨 Spotting the Low-Dopamine Adrenaline Trick',
    s1_b: 'When an ADHD-High-IQ brain hits a quiet afternoon or evening dip in dopamine, it sometimes tries to "self-medicate" by rendering a scary future movie or an urgent impulse to confess or fix an old memory—because fear and urgency release norepinephrine that wakes up the brain.',
    s2_h: '🌿 Never Negotiate With a High-Heart-Rate Simulation',
    s2_b: 'A scary thought generated during a dopamine dip has zero prophetic truth; it is purely a neurochemical screen-saver trying to generate stimulation. You never need to argue with the story—you simply reset the hardware.',
    s3_h: '⚡ The 60-Second Physical Reset',
    s3_b: '1. Splash cold water over closed eyes and cheekbones for 30 seconds (mammalian dive reflex).\n2. Push hard against a wall for 20 seconds.\n3. Lock the past vault and put on a song or step outside.',
    q: '🔮 Why is "Never confess or excavate the past while heart rate is elevated" a golden rule?',
    a: '✨ Because urgency is a physiological state, not a moral truth—once your heart rate drops 15 bpm, 99% of false alarms evaporate on their own!'
  },
  {
    id: 'cbt_extra_6',
    title: 'The 12 Freedoms You Wrote for Ma Belong to You First',
    s1_h: '🌸 The Mirror of Kalyani',
    s1_b: 'In Kalyani and Jhalak, you wrote with so much love that Ma should have zero fear of making mistakes, should speak her real mind without over-explaining, should never feel guilty about resting or enjoying good food, and should sing and play purely for happiness.',
    s2_h: '🌿 Claiming Your Own Prescription',
    s2_b: 'Every single permission you crafted for Ma applies word-for-word to Koushik at 33. You do not need to earn your keep through exhaustion anymore; your presence, curiosity, and warmth are already enough.',
    s3_h: '⚡ Living One Freedom Today',
    s3_b: 'Pick one of those freedoms right now—speaking on Beat 1, singing with eyes closed, or taking an unhurried afternoon break—and enjoy it as your birthright.',
    q: '🔮 Why is it often easier to write unconditional compassion for someone we love than for ourselves?',
    a: '✨ Because we see their whole humanity from the outside—and looking at your own 33-year arc through that same warm lens unlocks instant self-compassion!'
  }
];

const EXTRA_CLARITY_REELS = [
  {
    id: 'clarity_extra_1',
    title: 'Ranaghat to Jadavpur WBJEE Rank 222: Your Native Fire',
    s1_h: '🔥 The Empirical Proof of Your Deep Engine',
    s1_b: 'Right through the personal and family storm of Class 12, securing WBJEE Rank 222 to enter Jadavpur University Electrical Engineering—and then rising to Google L5 Senior AI Engineer—proved that your intuition and deep-focus engine are world-class whenever a mission genuinely matters to you.',
    s2_h: '💬 Rewriting the Childhood Narrative',
    s2_b: 'Childhood moments of quietness, reading comics in a corner, or missing a peripheral social cue were never "selfishness"—they were how a brilliant, unmedicated 4-slot working memory protected itself from sensory overload.',
    s3_h: '⚡ Honoring Your Native Grain Today',
    s3_b: 'Design your work and learning around how your brain actually wins: top-down big picture first, visual geometry before algebra, and deep uninterrupted blocks on problems worth solving.',
    q: '🔮 Why do 2e (twice-exceptional: High-IQ + ADHD) minds often feel bored by routine drills yet shine on hard frontier problems?',
    a: '✨ Because complex, novel problems naturally release the phasic dopamine needed to engage the prefrontal cortex at full horsepower!'
  },
  {
    id: 'clarity_extra_2',
    title: 'Clean-Slate Romantic Reset: Equal Playfulness, Zero Savior Chair',
    s1_h: '💛 Honoring Every Past Chapter Without Guilt Debt',
    s1_b: 'Across every past romantic chapter—Ananya, Baishali, Ankita, Oela, Anindita, Shruti, Antarleena, and Sanchita—each connection taught you something real about yourself and what you value. Stepping away when long-term compatibility is not there is honest adult discernment, never a debt.',
    s2_h: '💬 Retiring the Therapist & Rescuer Chair',
    s2_b: 'You never again need to earn love by fixing someone’s life, absorbing their turbulence, or playing the patient counselor. Real romance at 33 is two healthy, playful adults enjoying music, travel, laughter, and mutual admiration.',
    s3_h: '⚡ The Equal-Warmth Standard',
    s3_b: 'Let your baseline in dating and friendship be light, warm, playful, and equal—where you get to lean back, be cherished, and have fun too.',
    q: '🔮 What is the quickest green flag that a romantic connection is fueling Engine 2 rather than caretaker duty?',
    a: '✨ You walk away from the conversation feeling lighter, more playful, and more energized than when you arrived!'
  },
  {
    id: 'clarity_extra_3',
    title: 'Cosmic Parent & Divine Child: Retiring the Internal Police State',
    s1_h: '🧭 The Two Halves of a Sovereign Adult',
    s1_b: 'Every thriving creative adult has two internal roles: the Cosmic Parent (who sets up clean automated guardrails, finances, and KORTEX lists) and the Divine Child (who explores physics, sings songs, climbs walls, and invents cool systems out of pure wonder).',
    s2_h: '💬 Why the Internal Police State Is Retired',
    s2_b: 'During your 20s, fear of dropping the ball forced an internal drill sergeant to micromanage every hour. Now that your Cosmic Parent infrastructure is automated and rock-solid, the drill sergeant is officially retired with a pension.',
    s3_h: '⚡ Letting the Divine Child Drive Today',
    s3_b: 'Ask yourself on your main project today: "What is the most intellectually fun, curious way to explore this?"—and let play lead the way.',
    q: '🔮 Why does Engine 2 (Pure Curiosity & Play) produce better engineering and art than Duty Fuel?',
    a: '✨ Duty fuel narrows attention to error-avoidance; curiosity widens associative networks across the entire cortex!'
  },
  {
    id: 'clarity_extra_4',
    title: 'Healing the "Zara Zara" Stage Memory: Singing From Bhaavna',
    s1_h: '🎤 What Really Happened on That Stage in Front of 500 People',
    s1_b: 'Walking up in front of 500 colleagues and hitting 80% of the notes of a demanding melody cold is proof of courage and a genuine musical ear. The only reason your throat felt tight on the high notes was an un-transposed key combined with an internal judge grading every syllable in real time.',
    s2_h: '💬 The Vagus-Larynx Connection',
    s2_b: 'The recurrent laryngeal nerve that controls your vocal cords is a direct branch of the vagus nerve. When you judge yourself, sympathetic tension tightens the throat; when you close your eyes and feel the story (*bhaavna*) of the lyric in a comfortable baritone scale (-2 to -3 semitones), your throat softens automatically.',
    s3_h: '⚡ Your New Singing Default',
    s3_b: 'Never sing to pass a pitch exam—sing like you are telling a heartfelt secret to one close friend in a warm room.',
    q: '🔮 Why do listeners feel goosebumps from an emotionally honest chest voice far more than from technical vocal gymnastics?',
    a: '✨ Human mirror neurons and auditory emotion circuits respond to vocal timbre and emotional sincerity ("bhaavna"), not frequency perfection!'
  },
  {
    id: 'clarity_extra_5',
    title: 'Unapologetic Beat-1 Expression: Dropping "Onugoto" Compliance',
    s1_h: '🗣️ From Accommodating Good Boy to Warm, Direct Leader',
    s1_b: 'The Bengali *onugoto* reflex trains smart kids to suppress their own preferences, agree politely first, or write three paragraphs of justification before asking for what they want. At 33, your voice carries natural weight and warmth.',
    s2_h: '💬 The Power of a 1-Sentence Beat-1 Truth',
    s2_b: 'Whether in a Google architecture review, a restaurant with friends, or a family phone call, stating your genuine thought or boundary calmly on Beat 1 ("Here is what I recommend..." or "I’ll pass on that tonight, let’s do Saturday instead") creates instant clarity and respect.',
    s3_h: '⚡ Today’s Beat-1 Practice',
    s3_b: 'Notice one moment today where you would normally hedge or over-explain—and deliver your real preference in one warm, clean sentence instead.',
    q: '🔮 Why does trimming away 3 paragraphs of apology make your boundary sound 10x kinder and stronger?',
    a: '✨ Over-explaining signals guilt and invites negotiation; a warm, simple 1-sentence statement signals calm self-respect!'
  }
];

const WISDOM_PILLAR_DEEP_DIVES = [
  {
    application: 'Whenever your heart rate spikes or an urgent urge to confess/fix a 15-year-old memory appears, treat it strictly as a low-dopamine hardware glitch—never a moral emergency. Cold water on closed eyes (30s) + isometric wall push (20s) resets the vagus nerve in 60 seconds flat.',
    cur_q: '🔮 Key #1 Secret: Why does the brain invent "urgent past confessions" specifically when afternoon dopamine is low?',
    cur_a: '✨ Because guilt and alarm trigger an immediate norepinephrine spike that temporarily wakes up a sluggish prefrontal cortex!'
  },
  {
    application: 'Childhood Inattentive ADHD (missing small details while absorbed in thought) was cognitive wiring, never selfishness. And every unmentored stumble at 11, 17, 26, or 30 has already taught its lesson—drop Buddha’s Second Arrow and walk with a 100% clean slate.',
    cur_q: '🔮 Key #2 Secret: How do you know in 2 seconds whether a feeling is useful feedback or a useless Second Arrow?',
    cur_a: '✨ Useful feedback points to a simple action today; a Second Arrow prosecutes a past version of you who no longer exists!'
  },
  {
    application: 'In every meeting and video, silence the inner depth-inspector until the speaker finishes. Catch the 1-sentence headline ("kehna kya chahta hai") on Pass 1, speak your own 1-sentence map out loud first, and stamp a 20% Tourist Pass on 90% of daily pings.',
    cur_q: '🔮 Key #3 Secret: Why does catching the 1-sentence headline first make deep technical details 3x easier to absorb on Pass 2?',
    cur_a: '✨ The headline creates a top-down hippocampal schema so incoming details snap onto pre-built hooks instead of overflowing your 4 working-memory slots!'
  },
  {
    application: 'Music is for joy and emotional resonance (*bhaavna*), never a courtroom note-inspection. Listen on Pass 1 with eyes closed for the visual scene, notice the poetic turn on Pass 2, and sing on Pass 3 in a warm baritone key (-2 to -3 semitones).',
    cur_q: '🔮 Key #4 Secret: How does turning off the internal note-critic physically unlock your voice?',
    cur_a: '✨ It releases vagal brake tension on the larynx, allowing natural chest resonance and effortless pitch locking!'
  },
  {
    application: 'With L5 Senior SWE compensation and ₹2.61 Cr+ compounding quietly, scarcity reflexes are obsolete. Always take the freshest fruit first, choose deep-roasted Maillard craft over watery mediocrity, and spend on comfort or time-saving on Beat 1.',
    cur_q: '🔮 Key #5 Secret: Why is "eating the bruised banana first" the ultimate symbol of unnecessary self-deprivation?',
    cur_a: '✨ Because delaying joy when abundance is already here means trading away prime-of-life experience for ₹10 of sunk cost!'
  },
  {
    application: 'Care for Ma and Didi through clean structural systems (Kalyani, Jhalak, care pod, 3BHK plan) while hanging up the caretaker uniform at 6:00 PM with zero emotional fusion. At work, protect your 30% solo Crown Jewel and direct the 70% umbrella like a calm movie director.',
    cur_q: '🔮 Key #6 Secret: How do the 6 PM Off-Duty Switch at home and the 70/30 Director Frame at work solve the exact same bottleneck?',
    cur_a: '✨ Both replace exhausting emotional/execution micromanagement with clean structural interfaces—preserving your 4 working-memory slots for joy and high-leverage creation!'
  },
  {
    application: 'Anchor your body daily from the floor up: left-foot arch dome, 30-second dead hang, single-arm suitcase carry, soft jaw and belly, warm-to-cool rebooting shower, and daily zero-utility play—guitar, bouldering, swimming, photography, and equal romantic banter.',
    cur_q: '🔮 Key #7 Secret: Why does "As the day, so is the day" (Jedin jerokom, sedin serokom) keep momentum alive all year long?',
    cur_a: '✨ Because matching your daily pace to your natural energy wave eliminates streak-shame and keeps intrinsic dopamine flowing effortlessly!'
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

  // 1. Build 105 rich, elaborate 3-section Reel pages from the 21 Days x 5 Explorations
  days.forEach(d => {
    const dNum = d.day;
    (d.games || []).forEach((ag, gIdx) => {
      const id = `d${dNum}_g${gIdx}`;
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

      let sections = [];
      let curQ = '';
      let curA = '';

      if (vibe === 'music') {
        const sv = ZORBA_SONG_VAULT[dNum] || ZORBA_SONG_VAULT[1];
        sections = [
          {
            heading_bn: `🎵 Day ${dNum} • Pass-1 Musical Immersion & Sonic Landscape`,
            body_bn: `${ag.detail}\n\n${sv.story || ''}`.trim(),
            tone: 'story',
            spoken: true
          },
          {
            heading_bn: '📜 Poetic Bhaavna & Baritone Chest-Voice Guide',
            body_bn: sv.bhaavna,
            tone: 'hitch',
            spoken: true
          },
          {
            heading_bn: '💡 The Right Question Hook for Song Meaning',
            body_bn: `${sv.hook_q}\n\n${sv.hook_a}`,
            tone: 'extra',
            spoken: true
          }
        ];
        curQ = sv.cur_q;
        curA = sv.cur_a;
      } else if (vibe === 'science') {
        const scv = ZORBA_SCIENCE_VAULT[dNum] || ZORBA_SCIENCE_VAULT[1];
        sections = [
          {
            heading_bn: `🔭 Day ${dNum} • The Frontier Discovery & Core Phenomenon`,
            body_bn: ag.detail,
            tone: 'story',
            spoken: true
          },
          {
            heading_bn: '🧮 First-Principles Whiteboard Intuition & Mechanism',
            body_bn: scv.mechanism,
            tone: 'hitch',
            spoken: true
          },
          {
            heading_bn: '🌐 Polymath Synthesis: Brain, Code & Life Architecture',
            body_bn: scv.bridge,
            tone: 'extra',
            spoken: true
          }
        ];
        curQ = scv.cur_q;
        curA = scv.cur_a;
      } else if (vibe === 'listening') {
        const lv = ZORBA_LISTENING_VAULT[dNum] || ZORBA_LISTENING_VAULT[1];
        sections = [
          {
            heading_bn: `🎧 Day ${dNum} • 4-Slot Auditory Architecture & Listening Technique`,
            body_bn: ag.detail,
            tone: 'story',
            spoken: true
          },
          {
            heading_bn: '🎙️ Live Spoken Mini-Talk (Listen & Catch the Headline)',
            body_bn: lv.monologue,
            tone: 'hitch',
            spoken: true
          },
          {
            heading_bn: '🎯 1-Sentence Headline & 3-Anchor Structural Map',
            body_bn: lv.synthesis,
            tone: 'extra',
            spoken: true
          }
        ];
        curQ = lv.cur_q;
        curA = lv.cur_a;
      } else if (vibe === 'cbt' || vibe === 'clarity') {
        const cv = ZORBA_CLARITY_CBT_VAULT[dNum] || ZORBA_CLARITY_CBT_VAULT[1];
        sections = [
          {
            heading_bn: `📖 Day ${dNum} • Deep Mental Model & Lived Reality`,
            body_bn: ag.detail,
            tone: 'story',
            spoken: true
          },
          {
            heading_bn: '🌿 Ericksonian Reframe & Psychological Truth',
            body_bn: cv.reframe,
            tone: 'hitch',
            spoken: true
          },
          {
            heading_bn: '⚡ Effortless First-Beat Micro-Upgrade',
            body_bn: cv.practice,
            tone: 'extra',
            spoken: true
          }
        ];
        curQ = cv.cur_q;
        curA = cv.cur_a;
      } else {
        const fv = ZORBA_FLOW_VAULT[dNum] || ZORBA_FLOW_VAULT[1];
        sections = [
          {
            heading_bn: `🦁 Day ${dNum} • 2e-ADHD Leverage & Zorba Principle`,
            body_bn: ag.detail,
            tone: 'story',
            spoken: true
          },
          {
            heading_bn: '🧬 Neuro-Mechanical & Executive Mechanism',
            body_bn: fv.mechanism,
            tone: 'hitch',
            spoken: true
          },
          {
            heading_bn: '⚡ 60-Second Embodied Flow Ritual',
            body_bn: fv.ritual,
            tone: 'extra',
            spoken: true
          }
        ];
        curQ = fv.cur_q;
        curA = fv.cur_a;
      }

      let ytQuery = '';
      let ytLabel = '';
      if (vibe === 'music') {
        const mSong = ag.title.match(/'([^']+)'/) || (ag.prompt && ag.prompt.match(/'([^']+)'/));
        ytQuery = (mSong ? mSong[1] : ag.title) + ' official audio HD';
        ytLabel = `Listen to ${mSong ? mSong[1] : ag.title} on YouTube`;
      } else if (vibe === 'science') {
        ytQuery = ag.title;
        ytLabel = `Explore "${ag.title}" on YouTube`;
      }

      const audioRel = `reels/${id}.mp3`;
      list.push({
        id: id,
        vibe: vibe,
        badge_bn: badge,
        title_bn: ag.title,
        title_spoken: true,
        sections: sections,
        curiosity_q_bn: curQ,
        curiosity_q_spoken: true,
        curiosity_a_bn: curA,
        curiosity_a_spoken: true,
        yt_query: ytQuery,
        yt_label_bn: ytLabel,
        audio_url: ZORBA_AUDIO_BASE + id + '.mp3',
        audio_rel: audioRel,
        story_end: 0
      });
    });
  });

  // 2. Add 6 extra First-Press & CBT cards (so cbt has 10 + 6 = 16 pages)
  EXTRA_CBT_REELS.forEach(c => {
    const audioRel = `reels/${c.id}.mp3`;
    list.push({
      id: c.id,
      vibe: 'cbt',
      badge_bn: '🌿 First-Press & CBT',
      title_bn: c.title,
      title_spoken: true,
      sections: [
        { heading_bn: c.s1_h, body_bn: c.s1_b, tone: 'story', spoken: true },
        { heading_bn: c.s2_h, body_bn: c.s2_b, tone: 'hitch', spoken: true },
        { heading_bn: c.s3_h, body_bn: c.s3_b, tone: 'extra', spoken: true }
      ],
      curiosity_q_bn: c.q,
      curiosity_q_spoken: true,
      curiosity_a_bn: c.a,
      curiosity_a_spoken: true,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + c.id + '.mp3',
      audio_rel: audioRel,
      story_end: 0
    });
  });

  // 3. Add 5 extra Inner Child & Clarity cards (so clarity has 11 + 5 = 16 pages)
  EXTRA_CLARITY_REELS.forEach(c => {
    const audioRel = `reels/${c.id}.mp3`;
    list.push({
      id: c.id,
      vibe: 'clarity',
      badge_bn: '💬 Inner Clarity',
      title_bn: c.title,
      title_spoken: true,
      sections: [
        { heading_bn: c.s1_h, body_bn: c.s1_b, tone: 'story', spoken: true },
        { heading_bn: c.s2_h, body_bn: c.s2_b, tone: 'hitch', spoken: true },
        { heading_bn: c.s3_h, body_bn: c.s3_b, tone: 'extra', spoken: true }
      ],
      curiosity_q_bn: c.q,
      curiosity_q_spoken: true,
      curiosity_a_bn: c.a,
      curiosity_a_spoken: true,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + c.id + '.mp3',
      audio_rel: audioRel,
      story_end: 0
    });
  });

  // 4. Build 16 Wisdom & 7 Keys cards (7 Pillars + 7 Quotes + 2 Polymath Keys = 16 pages)
  pillars.forEach((p, pIdx) => {
    const id = `pillar_${pIdx}`;
    const audioRel = `reels/${id}.mp3`;
    const wp = WISDOM_PILLAR_DEEP_DIVES[pIdx] || WISDOM_PILLAR_DEEP_DIVES[0];
    list.push({
      id: id,
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
          heading_bn: '🧬 Neuro-Cognitive Architecture & Why It Works',
          body_bn: wp.application,
          tone: 'hitch',
          spoken: true
        },
        {
          heading_bn: '⚡ 10-Second Real-Time Deployment',
          body_bn: 'Whenever you notice mental RAM crowding, hesitation, or caretaker fatigue today, invoke this single key on Beat 1—zero willpower required, pure structural leverage.',
          tone: 'extra',
          spoken: true
        }
      ],
      curiosity_q_bn: wp.cur_q,
      curiosity_q_spoken: true,
      curiosity_a_bn: wp.cur_a,
      curiosity_a_spoken: true,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + id + '.mp3',
      audio_rel: audioRel,
      story_end: 0
    });
  });

  const QUOTE_DEEP_DIVES = [
    {
      title: 'House-Money Anchor #1: Your Own 12 Freedoms First',
      lens: 'Every permission you lovingly designed for Ma in Kalyani—zero fear of errors, speaking openly without apology, resting without guilt, and singing purely for delight—belongs first to the architect who wrote it.',
      practice: 'Claim one of your 12 freedoms before lunch today: state a direct preference, hum a melody, or take an unhurried break with a warm smile.',
      q: '🔮 Anchor #1 Secret: Why does treating yourself with the same warmth you give Ma double your daily energy?',
      a: '✨ Because self-criticism burns prefrontal glucose, whereas self-permission keeps your vagal tone and dopamine steady all day!'
    },
    {
      title: 'House-Money Anchor #2: The 2016–2026 Survival Decade Is Closed',
      lens: 'From 2016 to 2026, you carried the family cockpit solo from age 23 to 33 and landed the plane safely with Google L5 Senior SWE and ₹2.61 Cr+ net worth. You are no longer playing to survive; you are playing with house money.',
      practice: 'Whenever a minor work or life hiccup appears today, remind yourself: "The survival war is already won; this is just an interesting puzzle in bonus rounds."',
      q: '🔮 Anchor #2 Secret: How does "House-Money Mode" change your risk-taking and creativity in engineering?',
      a: '✨ When baseline safety is guaranteed, your prefrontal cortex shifts from defensive threat-avoidance to bold, high-upside exploration!'
    },
    {
      title: 'House-Money Anchor #3: Sweet 88% First Press of the Lemon',
      lens: 'One gentle squeeze of a fresh lemon gives 88% of its sweet juice; twisting the peel for the last 12% only adds bitter white pith. Apply the First-Press Law to money, time, reading, and engineering scope.',
      practice: 'Toss one metaphorical ₹4 lemon peel in the bin today—stop a diminishing-returns task at 88% and enjoy the saved hour.',
      q: '🔮 Anchor #3 Secret: Where does "bitter lemon pith" hide most often in software engineering?',
      a: '✨ Polishing low-impact internal plumbing that nobody asked for instead of shipping the clean core invariant and moving on!'
    },
    {
      title: 'House-Money Anchor #4: As the Day, So Is the Day (Jedin Jerokom, Sedin Serokom)',
      lens: 'Human biology moves in natural rhythms, not factory conveyor belts. Honoring high-energy days with bold creation and softer days with music, walking, and gentle rest keeps your relationship with yourself 100% shame-free.',
      practice: 'Tune in to today’s natural weather without comparing it to yesterday or tomorrow—and surf the exact wave in front of you.',
      q: '🔮 Anchor #4 Secret: Why do rigid daily streak apps eventually fail almost every high-IQ ADHD mind?',
      a: '✨ Because a single broken streak triggers the "what-the-hell effect," whereas state-adaptive flow ("Jedin jerokom") never breaks!'
    },
    {
      title: 'House-Money Anchor #5: Pass-1 Headline Catch in Every Room',
      lens: 'Your 4 working-memory slots stay crystal clear when you let a speaker finish their paragraph and catch only the 1-sentence headline ("kehna kya chahta hai") on Pass 1 before diving into any bottom-up mechanism.',
      practice: 'In your next conversation or video today, hold back the inner "Wait, why?" until the end and summarize the headline in one clean sentence.',
      q: '🔮 Anchor #5 Secret: What happens to comprehension speed when you stop verifying Sentence 2 while Sentence 6 is being spoken?',
      a: '✨ Real-time listening comprehension jumps immediately because your auditory buffer stops dropping packets!'
    },
    {
      title: 'House-Money Anchor #6: 6 PM Off-Duty Caretaker & Deep-Roasted Craft',
      lens: 'After 6:00 PM, the family rescuer uniform comes off completely. Your evening is reserved for things with rich Maillard depth—singing from meaning, playing guitar, bouldering, and savoring slow-roasted food.',
      practice: 'Plan one pure Engine-2 sensory pleasure for tonight after 6:00 PM that has zero connection to duty or productivity.',
      q: '🔮 Anchor #6 Secret: Why does protecting a strict 6 PM boundary make your daytime focus twice as sharp?',
      a: '✨ Knowing that a guaranteed reward window starts at 6 PM lets your brain sprint cleanly during the day without pacing out of dread!'
    },
    {
      title: 'House-Money Anchor #7: Full Bail Paid for Ages 11, 17, 26 & 30',
      lens: 'Every lesson from childhood, college, and your twenties has already been integrated into the kind, self-aware man you are at 33. Dropping Buddha’s Second Arrow frees all locked emotional RAM.',
      practice: 'Walk through today with the posture of a man whose record is 100% expunged—open chest, soft jaw, and easy laughter.',
      q: '🔮 Anchor #7 Secret: What is the ultimate proof that you have outgrown your younger stumbles?',
      a: '✨ The wisdom, empathy, and structural care you practice effortlessly every single day at 33!'
    }
  ];

  quotes.forEach((q, qIdx) => {
    const id = `quote_${qIdx}`;
    const audioRel = `reels/${id}.mp3`;
    const qd = QUOTE_DEEP_DIVES[qIdx] || QUOTE_DEEP_DIVES[0];
    list.push({
      id: id,
      vibe: 'wisdom',
      badge_bn: '☀️ Daily Anchor',
      title_bn: qd.title,
      title_spoken: true,
      sections: [
        {
          heading_bn: '☀️ Spoken House-Money Truth',
          body_bn: q.text,
          tone: 'story',
          spoken: true
        },
        {
          heading_bn: '🧭 Deep Psychological & Architectural Lens',
          body_bn: qd.lens,
          tone: 'hitch',
          spoken: true
        },
        {
          heading_bn: '🦁 Living It Today on Beat 1',
          body_bn: qd.practice,
          tone: 'extra',
          spoken: true
        }
      ],
      curiosity_q_bn: qd.q,
      curiosity_q_spoken: true,
      curiosity_a_bn: qd.a,
      curiosity_a_spoken: true,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + id + '.mp3',
      audio_rel: audioRel,
      story_end: 0
    });
  });

  const WISDOM_EXTRA_REELS = [
    {
      id: 'wisdom_extra_0',
      title: 'The 3-Into-5 Master Pattern: Why 4 Working-Memory Slots Need Guardrails',
      s1_h: '🧬 3 Root Causes -> 5 Downstream Frictions',
      s1_b: 'Almost every moment of cognitive friction in a 2e-ADHD polymath life traces back to just three root causes colliding inside a 4-slot biological working memory: (1) holding 20+ open loops in head RAM, (2) time blindness / urgency distortion, and (3) applying a 100% first-principles depth standard to routine 20% tasks.',
      s2_h: '🧭 How Those 3 Roots Create All 5 Everyday Symptoms',
      s2_b: 'When those three collide, they produce the five familiar symptoms: listening lag (stalling on Sentence 2), verbal tangles (speaking from the middle of a graph), starter-motor freeze on big tasks, perfectionist exhaustion on small tasks, and evening dopamine dips.',
      s3_h: '⚡ The 3-Switch Master Solution',
      s3_b: '1. Offload every open loop into KORTEX immediately.\n2. Speak and listen for the 1-sentence headline first.\n3. Stamp a 20% Tourist Pass on 90% of routine work so your 4 slots stay crystal clear.',
      q: '🔮 Systems Diagnostic Secret: Why is reducing 20 scattered frustrations down to a "3-Into-5" causal graph so calming?',
      a: '✨ Because you stop fighting 20 separate symptoms and simply flip 3 high-leverage root switches!'
    },
    {
      id: 'wisdom_extra_1',
      title: '70/30 Movie-Director Frame: Fire Without Smoke at L5+',
      s1_h: '🎬 Solo Virtuoso vs. Movie Director at L5/L6',
      s1_b: 'At L3 and L4, engineers are rewarded for solo hand-coding everything. At L5 Senior SWE and L6 Staff levels, trying to carry 100% of every workstream personally creates exhaustion ("smoke"). The secret is "Fire Without Smoke": unmistakable technical vision paired with calm, generous orchestration.',
      s2_h: '🧭 The 30% Crown Jewel + 70% Director Split',
      s2_b: 'Invest 30% of your prime deep-focus energy into ONE solo first-author Crown Jewel (the core algorithm, architecture doc, or flagship CL that carries your signature). Spend the remaining 70% directing the broader umbrella like Satyajit Ray on set—writing crisp 1-page interface contracts, unblocking teammates in 5 minutes, and giving public credit generously.',
      s3_h: '⚡ Protecting Your Evening Zorba Energy',
      s3_b: 'When you stop over-functioning on other people’s 70% execution threads, you finish your workday at 6:00 PM with high impact and a full battery for music, climbing, and life.',
      q: '🔮 Staff+ Career Secret: Why does giving away credit generously on the 70% umbrella actually increase your own authority?',
      a: '✨ Because teammates love building under a generous leader, making you the natural gravity center of the entire organization!'
    }
  ];

  WISDOM_EXTRA_REELS.forEach(w => {
    const audioRel = `reels/${w.id}.mp3`;
    list.push({
      id: w.id,
      vibe: 'wisdom',
      badge_bn: '🧭 7 Core Keys',
      title_bn: w.title,
      title_spoken: true,
      sections: [
        { heading_bn: w.s1_h, body_bn: w.s1_b, tone: 'story', spoken: true },
        { heading_bn: w.s2_h, body_bn: w.s2_b, tone: 'hitch', spoken: true },
        { heading_bn: w.s3_h, body_bn: w.s3_b, tone: 'extra', spoken: true }
      ],
      curiosity_q_bn: w.q,
      curiosity_q_spoken: true,
      curiosity_a_bn: w.a,
      curiosity_a_spoken: true,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + w.id + '.mp3',
      audio_rel: audioRel,
      story_end: 0
    });
  });

  // 5. Build 16 Cinema, Music & TV Reel cards (3 rich sections + bespoke curiosity Q&A)
  ZORBA_TV_CHANNELS.forEach(ch => {
    const audioRel = `reels/${ch.id}.mp3`;
    list.push({
      id: ch.id,
      vibe: 'tv',
      badge_bn: ch.badge_bn,
      title_bn: ch.title_bn,
      title_spoken: true,
      sections: [
        {
          heading_bn: '📺 Curated Immersion & Aesthetic Experience',
          body_bn: ch.desc,
          tone: 'story',
          spoken: true
        },
        {
          heading_bn: '🏛️ Cultural Backstory & Artistic Mastery',
          body_bn: ch.backstory,
          tone: 'hitch',
          spoken: true
        },
        {
          heading_bn: '🎯 Active Ear & Eye Appreciation Lens',
          body_bn: ch.focus,
          tone: 'extra',
          spoken: true
        }
      ],
      curiosity_q_bn: ch.cur_q,
      curiosity_q_spoken: true,
      curiosity_a_bn: ch.cur_a,
      curiosity_a_spoken: true,
      yt_query: ch.yt_query,
      yt_label_bn: ch.yt_label_bn,
      audio_url: ZORBA_AUDIO_BASE + ch.id + '.mp3',
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
