/* ============================================================================
   ⚡ ZORBA — MODULE 1A: LANGUAGE-ORGANIZED SONGS & CLEAN CURATED CONTENT VAULT
   ----------------------------------------------------------------------------
   Clean, timeless, zero-burden content vault for Koushik's Zorba companion:
   - 🎸 English Songs (8 iconic progressive, folk, acoustic & symphonic works)
   - 🎶 Hindi Songs (8 Sufi, poetic cinema & classical-fusion masterpieces)
   - 🪷 Bengali Songs (8 Rabindra Sangeet, Nazrul Geeti & modern classics with
     100% verified authentic lyrics)
   - 🔭 Frontier Science (16 first-principles physics, math & neuroscience gems)
   - 🌿 Inner Clarity (12 grounded mindset & emotional freedom insights)
   - 🎧 Active Listening (12 practical real-time comprehension & ear exercises)
   - 🦁 Embodied Flow (12 somatic, movement & creative-momentum practices)
   Zero "Day X" progression labels, zero filler padding, and 100% spoken aloud
   by the warm British female VoiceLM XL voice (`audio/zorba/reels/<id>.mp3`).
   ============================================================================ */

const JHALAK_CATEGORIES = [
  { id: 'all', label_bn: '✨ All', short_bn: 'All' },
  { id: 'songs_en', label_bn: '🎸 English Songs', short_bn: 'English Songs' },
  { id: 'songs_hi', label_bn: '🎶 Hindi Songs', short_bn: 'Hindi Songs' },
  { id: 'songs_bn', label_bn: '🪷 Bengali Songs', short_bn: 'Bengali Songs' },
  { id: 'science', label_bn: '🔭 Frontier Science', short_bn: 'Science' },
  { id: 'clarity', label_bn: '🌿 Inner Clarity', short_bn: 'Clarity' },
  { id: 'listening', label_bn: '🎧 Active Listening', short_bn: 'Listening' },
  { id: 'zorba', label_bn: '🦁 Embodied Flow', short_bn: 'Flow' }
];

const ZORBA_AUDIO_BASE = 'https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/audio/zorba/reels/';

function jhBnNum(n) {
  return String(n);
}

/* ----------------------------------------------------------------------------
   1. 🎸 ENGLISH SONGS (8 Timeless Masterpieces)
   ---------------------------------------------------------------------------- */
const ZORBA_ENGLISH_SONGS = [
  {
    id: 'd3_g2',
    title: 'Pink Floyd — Time (The Dark Side of the Moon, 1973)',
    yt_query: 'Pink Floyd Time official audio HD Dark Side of the Moon',
    story: 'Recorded at Abbey Road Studios in 1972, Roger Waters wrote Time at age 28 when he suddenly realized he was no longer getting ready for real life—real life was already happening right now. Engineer Alan Parsons recorded antique clocks ticking in quadraphonic space, followed by Nick Mason’s hypnotic rototom drum intro that slowly pulls the listener out of a trance.',
    bhaavna: 'Listen to the opening verse: “Ticking away the moments that make up a dull day, fritter and waste the hours in an offhand way... And then one day you find ten years have got behind you, no one told you when to run, you missed the starting gun.”\n\nRight after that verse, David Gilmour launches into one of the greatest electric guitar solos ever recorded—bending single soaring notes on his Fender Stratocaster over Richard Wright’s minor-major chord bed. With your ten-year survival climb already behind you at 33, this song is a reminder that the waiting room is over and every evening belongs to your own aliveness.',
    hook_q: 'Why does the song resolve from the urgent F-sharp minor verse into the warm, floating major-seventh chords of Breathe (Reprise) at the end?',
    hook_a: 'Because the cure for time-anxiety is not running faster on a treadmill—it is dropping into full sensory presence right where your feet are standing today.',
    cur_q: '🔮 Guitar Craft: How does David Gilmour make a single sustained bend carry more emotion than ten fast scales?',
    cur_a: '✨ He targets the chord’s 3rd and 9th intervals with pinpoint pitch accuracy, holds the note for two full beats so the listener feels the harmonic tension, and only then adds warm wrist vibrato.'
  },
  {
    id: 'd6_g2',
    title: 'Leonard Cohen — Anthem (The Future, 1992)',
    yt_query: 'Leonard Cohen Anthem Live in London HD official',
    story: 'Leonard Cohen spent nearly a decade rewriting Anthem, drafting dozens of verses in notebooks between Montreal and Mount Baldy before keeping only the purest lines. Recorded when Cohen was 58, his voice had settled into a rich, gravelly baritone floor that rumbles like a cello.',
    bhaavna: 'Let the chorus wash over any perfectionist corner of your mind: “Ring the bells that still can ring / Forget your perfect offering / There is a crack, a crack in everything / That’s how the light gets in.”\n\nIn engineering, music, sketching, and relationships, waiting for a flawless offering is just a polite disguise for hesitation. Ringing the bell that can ring right now—shipping a clean first draft or singing in your natural chest voice—is where all the light enters.',
    hook_q: 'Why does Leonard Cohen pair “There is a crack in everything” with warm gospel choir backing vocals in a major key?',
    hook_a: 'To turn human imperfection from a courtroom confession into a celebration—reminding us that our cracks are the exact places where wisdom and empathy enter.',
    cur_q: '🔮 Vocal Craft: How can a singer with a five-note baritone range command a ten-thousand-seat arena like Leonard Cohen?',
    cur_a: '✨ By locking completely onto rhythm, crisp consonants, and emotional subtext in low chest resonance—proving that sincerity always beats vocal acrobatics.'
  },
  {
    id: 'd12_g2',
    title: 'Simon & Garfunkel — The Sound of Silence (1964 Acoustic Original)',
    yt_query: 'The Sound of Silence Simon and Garfunkel acoustic original HD',
    story: 'Paul Simon wrote The Sound of Silence at age 21 sitting in his tiled bathroom in Queens with the lights turned off, because the bathroom tiles created a natural acoustic echo chamber for his fingerpicked guitar.\n\nWhen he and Art Garfunkel harmonized the opening line—“Hello darkness, my old friend, I’ve come to talk with you again”—they sang in tight parallel thirds and sixths, creating the sound of a single two-dimensional voice.',
    bhaavna: 'Notice the central paradox of the lyrics: “People talking without speaking, people hearing without listening, people writing songs that voices never share.”\n\nIn a noisy world of endless notifications and surface chatter, sitting quietly for five minutes with an acoustic guitar or having a real conversation where you hear the human subtext is a rare superpower.',
    hook_q: 'Why does the narrator greet darkness as “my old friend” instead of something to run away from?',
    hook_a: 'Because quiet solitude without screens or neon noise is where an overstimulated working memory finally digests experience into deep intuition.',
    cur_q: '🔮 Harmony Ear Check: Which vocal line is Paul Simon singing and which is Art Garfunkel?',
    cur_a: '✨ Art Garfunkel sings the higher, floating lead melody line throughout most of the verse, while Paul Simon anchors the lower chest-voice harmony underneath!'
  },
  {
    id: 'd15_g2',
    title: 'Radiohead — Weird Fishes / Arpeggi (In Rainbows, 2007)',
    yt_query: 'Radiohead Weird Fishes Arpeggi From the Basement HD',
    story: 'Recorded for Radiohead’s landmark 2007 album In Rainbows, Weird Fishes / Arpeggi was written for three interlocking electric guitars. Instead of strumming block chords, Jonny Greenwood, Ed O’Brien, and Thom Yorke play three independent broken-chord arpeggio patterns in different time-feels that interlock like gears in a watch over Phil Selway’s crisp drum groove.',
    bhaavna: 'Beneath the shimmering guitar currents, Thom Yorke sings: “In the deepest ocean, the bottom of the sea, your eyes, they turn me... I’ll hit the bottom, hit the bottom and escape.”\n\nClose your eyes for ninety seconds and let your ears do zero verbal work: just follow Guitar 1 in the left channel, Guitar 2 in the right channel, and Colin Greenwood’s warm bassline in the center.',
    hook_q: 'What happens midway through the song when all the drums and guitars suddenly drop out into quiet ambient space?',
    hook_a: 'It captures the exact feeling of letting go of a frantic treadmill—right before the warm bassline re-enters with grounded, unhurried clarity.',
    cur_q: '🔮 Polyphonic Ear Check: Why is the song subtitled “Arpeggi”?',
    cur_a: '✨ Because not a single guitar strums a flat block chord—every harmonic change is woven purely from overlapping arpeggios moving in counterpoint!'
  },
  {
    id: 'd18_g2',
    title: 'Israel Kamakawiwoʻole — Somewhere Over the Rainbow (1988 Ukulele Take)',
    yt_query: 'Somewhere Over the Rainbow Israel Kamakawiwoole official HD',
    story: 'At 3:00 AM in 1988 in Honolulu, recording engineer Milan Bertosa got a phone call asking if a Hawaiian musician named Israel “Iz” Kamakawiwoʻole could come in to record one idea before he forgot it. Bertosa gave him fifteen minutes. Iz walked in with his four-string ukulele, sat on a steel chair, and recorded Somewhere Over the Rainbow in a single unedited take.',
    bhaavna: 'Listen to how Iz opens with a gentle “Oooo-oooo” hum before singing: “Somewhere over the rainbow, way up high, and the dreams that you dare to dream really do come true.”\n\nThat single 3 AM take became the most beloved ukulele recording in history because Iz did not treat music like a technical exam. Four simple ukulele chords plus warm human sincerity created pure magic.',
    hook_q: 'Why does Iz’s gentle vocal humming at the very beginning of the track immediately relax the listener’s shoulders?',
    hook_a: 'Humming vibrates the vocal cords gently and signals total safety—inviting the listener into a warm living room rather than a formal concert hall.',
    cur_q: '🔮 Ukulele Craft: What are the four ukulele chords you need to play Iz’s arrangement?',
    cur_a: '✨ Just C (0003), G (0232), Am (2000), and F (2010), with an optional E7 (1202) color chord—the friendliest progression on the ukulele fretboard!'
  },
  {
    id: 'd21_g2',
    title: 'Ludwig van Beethoven — Ode to Joy (Symphony No. 9 Finale, 1824)',
    yt_query: 'Beethoven Symphony 9 Ode to Joy finale HD orchestra choir',
    story: 'On May 7, 1824, in Vienna, 53-year-old Ludwig van Beethoven stood on stage conducting the premiere of his Ninth Symphony. He had been completely deaf to external sound waves for years—he heard the entire orchestra and choir purely inside his internal mental model. When the music ended, contralto Caroline Unger gently turned him around so he could see the audience standing and cheering.',
    bhaavna: 'After three movements of storm and struggle, Beethoven introduces a melody built almost entirely from five adjacent stepwise notes (E–E–F–G–G–F–E–D–C–C–D–E–E–D–D)—first whispered by the low cellos and double basses alone, then growing until the full choir sings Schiller’s words: “Freude, schöner Götterfunken” (Joy, bright spark of divinity).\n\nIt proves that real joy is not naive—it is the highest creative triumph of a mind that has walked through the storm and chosen to celebrate life.',
    hook_q: 'Why did Beethoven start the Ode to Joy melody in the lowest, darkest strings (cellos and double basses) with zero accompaniment?',
    hook_a: 'To show that lasting joy does not float down from the clouds—it rises steadily from the deepest floor of lived human experience.',
    cur_q: '🔮 Musical Architecture: Why is the Ode to Joy theme instantly memorable to every human ear?',
    cur_a: '✨ Nearly 90% of its intervals move by adjacent scale steps within a five-note range, with a single syncopated tie at the end of the second phrase that gives it irresistible forward lift!'
  },
  {
    id: 'song_en_7',
    title: 'Pink Floyd — Wish You Were Here (1975 Acoustic 12-String Classic)',
    yt_query: 'Pink Floyd Wish You Were Here official audio HD',
    story: 'Recorded at Abbey Road Studios in 1975 as a tribute to their childhood friend and co-founder Syd Barrett, Wish You Were Here opens with the sound of an old car radio tuning across stations until a 12-string acoustic guitar riff emerges in the room—and David Gilmour joins in on a second acoustic guitar from the center of the stereo stage.',
    bhaavna: 'Listen to Roger Waters’s lyrics sung in Gilmour’s warm, unhurried chest register: “So, so you think you can tell, Heaven from hell, blue skies from pain / Can you tell a green field from a cold steel rail? A smile from a veil? Do you think you can tell?”\n\nIt is an invitation to drop artificial masks and stay connected to raw, sensory reality—green fields, real warmth, and honest presence.',
    hook_q: 'Why did Pink Floyd make the intro guitar sound as if it is playing through a small transistor radio before the full studio acoustic guitar enters?',
    hook_a: 'To create an acoustic contrast between distant, tinny memory (the radio) and warm, present-moment human reality (the live guitar sitting right in front of you).',
    cur_q: '🔮 Fretboard Craft: What open chord shape anchors the entire intro of Wish You Were Here?',
    cur_a: '✨ An open G-major chord where the ring and pinky fingers stay planted on the 3rd fret of the B and high-E strings while the index and middle fingers move between Em7 and G!'
  },
  {
    id: 'song_en_8',
    title: 'Leonard Cohen — Suzanne (Songs of Leonard Cohen, 1967)',
    yt_query: 'Leonard Cohen Suzanne original audio HD',
    story: 'Leonard Cohen did not release his debut album until age 33, after years of writing poetry and novels in Montreal and Hydra. When he nervous-heartedly played Suzanne for folksinger Judy Collins over the telephone, she told him on the spot that it was a masterpiece and brought him onto stage for his very first concert.',
    bhaavna: 'Notice how Cohen sings right in his natural speaking register over a steady hypnotic guitar fingerpicking pattern: “Suzanne takes you down to her place near the river / You can hear the boats go by, you can spend the night beside her / And you know that she’s half-crazy but that’s why you want to be there / And she feeds you tea and oranges that come all the way from China.”\n\nDebuting at 33 proved that lived experience makes an artist’s voice ten times richer than rushing in your twenties.',
    hook_q: 'Why does the guitar accompaniment in Suzanne use a steady, unchanging triplet fingerpicking roll underneath every verse?',
    hook_a: 'Because keeping the guitar pulse as calm and continuous as a flowing river lets the listener’s imagination focus completely on the vivid visual poetry.',
    cur_q: '🔮 Debut History: How old was Leonard Cohen when he recorded his very first album featuring Suzanne?',
    cur_a: '✨ Exactly 33 years old—turning his natural baritone speaking voice and simple Spanish guitar picking into timeless art!'
  }
];

/* ----------------------------------------------------------------------------
   2. 🎶 HINDI SONGS (8 Poetic Cinema & Sufi Masterpieces)
   ---------------------------------------------------------------------------- */
const ZORBA_HINDI_SONGS = [
  {
    id: 'd1_g2',
    title: 'A.R. Rahman & Irshad Kamil — Kun Faya Kun (Rockstar, 2011)',
    yt_query: 'Kun Faya Kun Rockstar official full song HD A R Rahman',
    story: 'Recorded after midnight at A.R. Rahman’s studio and filmed at the 700-year-old Hazrat Nizamuddin Dargah in Delhi, Kun Faya Kun opens not with heavy drums, but with bare harmonium breath and Javed Ali’s quiet invocation. Rahman holds back the acoustic guitar and bass for nearly two minutes so your nervous system drops its daytime armor before the groove even begins.',
    bhaavna: 'Irshad Kamil’s opening Sufi couplet is one of the deepest lines in Indian cinema: “Jab kahin pe kuch nahi bhi nahi tha, wahi tha, wahi tha”—when even nothingness itself did not exist, Consciousness was already there.\n\nAnd listen to the verse: “Sajra savera mere tan barse, kajra andhera teri jalti lau.” When you hum this in your natural baritone chest voice—dropped two semitones so your throat stays soft—it reminds you that no checklist or past regret has ever left a stain on who you really are.',
    hook_q: 'Why does Irshad Kamil write “Sajra savera mere tan barse, kajra andhera teri jalti lau”—how can dark night and fresh morning light happen at once?',
    hook_a: 'Because the moment you welcome every part of your history with compassion, the very shadow you feared turns into the warm lamp-flame that lights your morning.',
    cur_q: '🔮 Acoustic Mix Check: What happens in the arrangement right when Mohit Chauhan sings “Mujhpe karam sarkar tera”?',
    cur_a: '✨ Rahman strips away the full qawwali chorus and leaves a single intimate voice over soft acoustic guitar—showing that emotional peace is a quiet private conversation, never a loud performance.'
  },
  {
    id: 'd5_g2',
    title: 'Amit Trivedi & Javed Akhtar — Iktara (Wake Up Sid, 2009)',
    yt_query: 'Iktara Wake Up Sid official full song HD Kavita Seth Amit Trivedi',
    story: 'When director Ayan Mukerji asked Amit Trivedi and Javed Akhtar for a song capturing the morning a young adult stops drifting to please others and starts building a life of their own craft, Trivedi paired an earthy folk acoustic guitar riff with Kavita Seth’s deep, resonant Sufi alto.',
    bhaavna: 'Look at the beauty of Javed Akhtar’s lines: “O re manwa tu toh bavra hai, tu hi jaane tu kya sochta hai... Sun rahi hai sudh-budh khoke koi main kahani, poori kahani hai kya kise hai pata? Goonja sa hai koi iktara.”\n\nListening with total absorption to a story whose full ending nobody knows yet is the essence of living freely—enjoying the current chapter because it is unfolding in real time.',
    hook_q: 'What does “Goonja sa hai koi iktara” (a single string ringing inside) represent when you wake up on a free morning?',
    hook_a: 'The “iktara” (one-stringed instrument) is the single, unmistakable note of your own genuine curiosity—when you follow that one true string, your whole day tunes itself.',
    cur_q: '🔮 Chord Progression Check: Which simple three-chord acoustic loop gives Iktara its open-air momentum?',
    cur_a: '✨ A warm G major, to C add 9, to D sus 4 progression where the high G string rings continuously as a drone across all three chords!'
  },
  {
    id: 'd8_g2',
    title: 'R.D. Burman & Gulzar — Tujhse Naraz Nahi Zindagi (Masoom, 1983)',
    yt_query: 'Tujhse Naraz Nahi Zindagi Anup Ghoshal Masoom HD',
    story: 'Composed by R.D. Burman on a gentle Pahadi-inflected melody and sung with feather-light warmth by Anup Ghoshal, Gulzar wrote these lyrics as a quiet exhale for anyone who had to grow up early and carry adult responsibilities through a long storm.',
    bhaavna: 'Look at the two words Gulzar contrasts in the opening refrain: “Tujhse naraz nahi zindagi, hairaan hoon main... tere masoom sawalon se pareshan hoon main.” He is not angry (“naraz”) at life; he is simply amazed and a little worn out (“hairaan”) by how much he had to solve.\n\nAnd then comes the line written for every family caretaker: “Jeene ke liye socha hi nahi, dard sambhalne honge / Muskuraye toh, muskurane ke karz utaarne honge.” Today at 33, that old caretaker debt is cancelled—your smile owes zero tax to anyone.',
    hook_q: 'What changes in your body the moment you shift from “naraz” (angry at the past) to “hairaan” (compassionate amazement at how far you came)?',
    hook_a: 'Your jaw unclenches, the internal prosecutor leaves the room, and you feel genuine pride for the 23-year-old who carried the family safely through the storm.',
    cur_q: '🔮 Vocal Choice: Why did R.D. Burman choose Anup Ghoshal’s soft, unforced voice for the male version?',
    cur_a: '✨ Because Ghoshal sings with zero melodrama—like a calm older brother speaking quietly at dusk, letting Gulzar’s poetry carry all the emotion.'
  },
  {
    id: 'd9_g2',
    title: 'Harris Jayaraj & Bombay Jayashri — Zara Zara Behekta Hai (RHTDM, 2001)',
    yt_query: 'Zara Zara Behekta Hai Bombay Jayashri official song HD',
    story: 'When composer Harris Jayaraj created this melody set in Raga Natabhairavi (natural minor), he invited Carnatic classical vocalist Bombay Jayashri to sing it. Instead of projecting like a concert hall recital, Jayashri leaned close to the studio condenser microphone and sang the opening in a husky, intimate chest-voice whisper after the iconic monsoon flute prelude.',
    bhaavna: 'Listen to the opening verse: “Zara zara behekta hai, mehekta hai, aaj toh mera tan badan / Main pyaasi hoon, mujhe bhar le apni baahon mein.”\n\nStepping onto a stage in front of 500 colleagues cold and hitting 80% of this complex minor-to-major melody proved your natural musical ear is strong. When you play or sing Zara Zara for yourself, drop the key by two or three semitones into your warm baritone chest register and hum the root bass note for two seconds before starting.',
    hook_q: 'Why does the flute prelude immediately evoke monsoon rain and closeness before a single word is sung?',
    hook_a: 'Because the flute uses slow classical meend glides between the minor third and the root note, echoing the natural cadence of a human sigh.',
    cur_q: '🔮 Pitch Locking Tip: How do you guarantee your voice locks onto the root note instead of the 5th when starting a song with a guitar?',
    cur_a: '✨ Pluck only the single root bass string of the first chord, hum “Mmmm” to match that exact vibration in your chest, and sing the first word before strumming the full chord.'
  },
  {
    id: 'd11_g2',
    title: 'Ali Sethi & Shae Gill — Pasoori (Coke Studio Season 14, 2022)',
    yt_query: 'Pasoori Coke Studio Season 14 Ali Sethi Shae Gill HD',
    story: 'Produced by Xulfi and Abdullah Siddiqui for Coke Studio, Pasoori fused classical thumri raga ornamentation (Raga Bhairavi) with a syncopated modern bass pulse and a plucked rubab hook. Ali Sethi, trained in classical khayal and ghazal, wove Punjabi Sufi poetic imagery into a global phenomenon.',
    bhaavna: 'In Punjabi, “Pasoori” means a tangled dilemma or restless yearning—yet look at how the chorus turns that tension into kinetic joy: “Agg laawan majboori nu, aan jaan di pasoori nu” (Set fire to helplessness and to this back-and-forth dilemma).\n\nOn headphones, try a two-pass ear game: on Pass 1, lock your ear onto the bassline and rubab riff; on Pass 2, follow Ali Sethi’s effortless khatka and murki vocal ornaments.',
    hook_q: 'Why does Sufi-inspired music often pair lyrics of longing with an upbeat, celebratory dance groove?',
    hook_a: 'Because dancing with restlessness transforms heavy mental tension into warm physical energy within minutes.',
    cur_q: '🔮 Instrument Check: What traditional plucked instrument plays the signature melodic hook right before the chorus?',
    cur_a: '✨ The rubab—whose sympathetic metal tarab strings resonate underneath the main strings to create a natural acoustic halo.'
  },
  {
    id: 'd14_g2',
    title: 'Salil Chowdhury, Yogesh & Manna Dey — Zindagi Kaisi Hai Paheli (Anand, 1971)',
    yt_query: 'Zindagi Kaisi Hai Paheli Manna Dey Anand HD official',
    story: 'For Hrishikesh Mukherjee’s classic film Anand (1971), composer Salil Chowdhury and lyricist Yogesh created a song set along the open sea beach in Mumbai. Instead of a heavy dirge, they gave Manna Dey a buoyant, syncopated melody that smiles warmly at life’s uncertainty.',
    bhaavna: 'Listen to Yogesh’s exact words in the second stanza: “Jinhone sajaaye yahan mele, sukh-dukh sang-sang jhele / Wohi chunkar khamoshi, yoon chale jaaye akele, kahan? Zindagi kaisi hai paheli, haaye, kabhi toh hansaye, kabhi yeh rulaaye.”\n\nWhen you hold that perspective with a warm smile, small daily worries about office politics or minor decisions evaporate like sea spray.',
    hook_q: 'Why does Manna Dey sing “Haaye, kabhi toh hansaye, kabhi yeh rulaaye” with a light smile in his voice rather than sadness?',
    hook_a: 'Because once you stop demanding that life follow a rigid deterministic script and treat it as an open riddle (“paheli”), even its surprises become lighter to carry.',
    cur_q: '🔮 Orchestration Craft: How does Salil Chowdhury create the feeling of ocean waves in the instrumental prelude?',
    cur_a: '✨ He layers rolling accordion chords, glockenspiel notes, and rising-and-falling string arpeggios that mirror the rhythm of tide meeting the shore.'
  },
  {
    id: 'd16_g2',
    title: 'A.R. Rahman & Gulzar — Ae Ajnabi (Dil Se, 1998)',
    yt_query: 'Ae Ajnabi Dil Se Udit Narayan A R Rahman Gulzar HD',
    story: 'In Mani Ratnam’s Dil Se (1998), Gulzar and A.R. Rahman created an unforgettable nocturnal soundscape. After Mahalakshmi Iyer’s haunting “Paakhi paakhi pardesi” refrain, Udit Narayan enters in his softest, most intimate low chest register over a quiet heartbeat pulse.',
    bhaavna: 'Listen to Gulzar’s exact lines: “Ae ajnabi, tu bhi kabhi, aawaaz de kahin se / Main yahan tukdon mein jee raha hoon, tu kahin tukdon mein jee rahi hai / Roz roz resham si hawa, aate jaate kehti hai bata, woh jo doodh dhuli maasoom kali, woh hai kahan?”\n\nNotice how Gulzar uses simple, tactile Urdu-Hindi words—“tukdon mein” (in fragments), “resham si hawa” (silk-like breeze)—to express deep emotion without a single heavy or complicated word.',
    hook_q: 'How does singing “Main yahan tukdon mein jee raha hoon” over a warm, steady melody make a feeling of fragmentation feel comforting rather than bleak?',
    hook_a: 'Because naming a vulnerable feeling honestly in gentle music integrates scattered emotions into calm beauty.',
    cur_q: '🔮 Vocal Contrast: How does Mahalakshmi Iyer’s opening “Paakhi paakhi pardesi” contrast with Udit Narayan’s verse?',
    cur_a: '✨ Mahalakshmi sings high and open like a bird calling across a misty valley, while Udit answers in close-mic chest voice—creating a three-dimensional sense of distance and warmth.'
  },
  {
    id: 'd19_g2',
    title: 'A.R. Rahman, Irshad Kamil & Lucky Ali — Safarnama (Tamasha, 2015)',
    yt_query: 'Safarnama Tamasha Lucky Ali A R Rahman official full song HD',
    story: 'Imtiaz Ali’s Tamasha tells the story of a gifted young man who spent his twenties wearing a robotic “responsible solver” mask while his playful, creative self waited backstage. When he finally steps off the corporate treadmill onto the open road, A.R. Rahman brings in Lucky Ali’s wind-swept voice for Safarnama.',
    bhaavna: 'Listen to Irshad Kamil’s exact opening lines: “O... safarnama... Sawaalon ka safarnama, shuru tumse, khatam tumpe safarnama / O jisey dhoonda zamaane mein, mujh hi mein tha / O mere saare jawaabon ka safarnama.”\n\nThat line—“What I searched for across the whole world was already inside me”—is the heart of your thirties: the hard ten-year climb is finished, and the rest of the road is an open-sky Safarnama.',
    hook_q: 'Why does Irshad Kamil call the song both “Sawaalon ka safarnama” (a journey of questions) and “Mere saare jawaabon ka safarnama” (the journey of all my answers)?',
    hook_a: 'Because once you stop looking for external validation and come home to yourself, the open questions themselves become the answer.',
    cur_q: '🔮 Sonic Texture: How does A.R. Rahman create the feeling of a moving train and an open horizon in Safarnama?',
    cur_a: '✨ He pairs a brushed snare and muted acoustic guitar sixteenth-note rhythm underneath long, sustained cello and synth chords that stretch like a mountain skyline.'
  }
];

/* ----------------------------------------------------------------------------
   3. 🪷 BENGALI SONGS (8 Classics — 100% Double-Checked Authentic Lyrics)
   ---------------------------------------------------------------------------- */
const ZORBA_BENGALI_SONGS = [
  {
    id: 'd2_g2',
    title: 'Rabindranath Tagore — Majhe Majhe Tobo Dekha Pai (Puja Parjay)',
    yt_query: 'Majhe Majhe Tobo Dekha Pai Rabindra Sangeet best rendition HD',
    story: 'Composed by Rabindranath Tagore in 1885 and set in Raga Kafi / Mishra Pilu in Dadra taal, this Puja-parjay song from Gitabitan captures the honest rhythm of a creative mind. Every deep thinker knows what it feels like to touch effortless clarity for a few days, only to feel a passing cloud of ordinary fatigue drift in.',
    bhaavna: 'Here are Tagore’s exact original lyrics from Gitabitan: “Majhe majhe tobo dekha pai, chirodin keno pai na / Keno megh ashe hridoyo-akashe, tomare dekhite dey na? / Kshanik aloke ankhir poloke tomay jobe pai dekhite / Ohe ‘harai harai’ soda bhoy hoy, haraiya feli chokite.”\n\nNotice Tagore’s psychological insight in that second couplet: when we catch a glimpse of clarity or joy (“kshanik aloke ankhir poloke”), it is the anxious fear of losing it (“ohe harai harai soda bhoy hoy”) that makes us lose sight of it! Relaxing that fear lets clarity return naturally.',
    hook_q: 'Why does Tagore say that shouting “Ohe harai harai” (Oh no, I might lose this state!) is what actually makes the light disappear?',
    hook_a: 'Because anxious self-monitoring crowds working memory—whereas trusting that the sun is still behind the passing cloud keeps your mind calm until flow returns.',
    cur_q: '🔮 Raga Craft: Why does Raga Kafi make Majhe Majhe Tobo Dekha Pai feel both tender and hopeful at once?',
    cur_a: '✨ Because the komal gandhar (flat 3rd) and komal nishad (flat 7th) express gentle monsoon longing, while the ascending shuddha phrases lift the melody back toward light.'
  },
  {
    id: 'd4_g2',
    title: 'Kabir Suman — Tomake Chai (1992 Bengali Modern Classic)',
    yt_query: 'Tomake Chai Kabir Suman original full song HD',
    story: 'In 1992, Kabir Suman walked into a Kolkata studio with an acoustic guitar, harmonica, and keyboard and changed modern Bengali songwriting forever. Instead of archaic poetic language, he sang in the real everyday voice of Kolkata—tram tracks, tired evening crowds, Shirshendu novels, and a cup of tea.',
    bhaavna: 'Listen to Kabir Suman’s exact iconic lines: “Prothomoto ami tomake chai / Dwitiyoto ami tomake chai / Tritiyoto ami tomake chai / Shesh porjonto tomake chai... Nagorik klantite tomake chai, ek phonta shantite tomake chai... Ek kap chaye ami tomake chai, daine o baye ami tomake chai.”\n\nSuman proved that a warm baritone chest voice speaking honest truth on pitch moves listeners far more deeply than theatrical vocal shouting.',
    hook_q: 'Why does Kabir Suman open the song like a logical manifesto—“Prothomoto... Dwitiyoto... Tritiyoto... Shesh porjonto ami tomake chai”?',
    hook_a: 'Because stating what you love and want clearly on Beat 1—without ten layers of polite hesitation—is the foundation of an authentic adult life.',
    cur_q: '🔮 Vocal Delivery: Why does Suman sing almost the entire verse within a single octave of his natural speaking register?',
    cur_a: '✨ Keeping the melody in conversational chest resonance removes throat strain and makes the listener feel as if Suman is sitting right across the table talking to them.'
  },
  {
    id: 'd7_g2',
    title: 'Fossils (Rupam Islam) — Ekla Ghor (Bengali Rock Classic)',
    yt_query: 'Ekla Ghor Fossils Rupam Islam official audio HD',
    story: 'At the turn of the millennium in Kolkata, Rupam Islam and Fossils married the dynamic contrast of alternative rock—quiet fingerpicked minor guitar arpeggios exploding into soaring electric choruses—with sharp, introspective Bengali lyrics that became an anthem across Jadavpur and Kolkata college hostels.',
    bhaavna: 'Here are Rupam Islam’s exact opening lyrics for Ekla Ghor: “Ei ekla ghor amar desh, amar ekla thakar obbhesh / Bhabi kichhutei bhabbo na tomar kotha, boba telephone-er pashe boshe / Tobu gobhir raater ogobhir cinemay, jodi prem chay natuke biday / Ami achchhonno hoye porechi abar, dekhi chokh bhije jay kannay.”\n\nInstead of pretending to be cheerful when the mind feels heavy, great rock music gives intense emotion a safe acoustic container to roar and release.',
    hook_q: 'Why does listening to a high-energy rock ballad like Ekla Ghor leave you feeling calmer afterward rather than agitated?',
    hook_a: 'Aristotle called it catharsis—when music matches your internal intensity first and then resolves harmonically, it discharges pent-up tension cleanly.',
    cur_q: '🔮 Arrangement Craft: How does Fossils make the chorus (“Na, na, kandchi na, tomay bhabchi na”) hit with twice the emotional weight?',
    cur_a: '✨ By keeping the opening verse sparse over clean guitar arpeggios and bass space, then bringing in the full distorted guitars and drums right on the chorus downbeat.'
  },
  {
    id: 'd10_g2',
    title: 'Rabindranath Tagore — Akash Bhora Surjo Tara (Prakriti Parjay, 1924)',
    yt_query: 'Akash Bhora Surjo Tara Rabindra Sangeet HD',
    story: 'Written by Rabindranath Tagore in 1924 after decades of reading modern astrophysics, biology, and Upanishadic philosophy, Akash Bhora Surjo Tara is one of the greatest scientific-spiritual anthems ever composed. Instead of feeling tiny beneath billions of stars, Tagore feels exhilarating belonging.',
    bhaavna: 'Here are Tagore’s exact lyrics from Gitabitan: “Akash-bhora surjo-tara, bishwo-bhora pran, tahari majhkhane ami peyechi mor sthan, bismoye tai jage amar gaan.”\n\nAnd in the third stanza, he brings cosmic wonder straight down to your bare feet on the earth: “Ghashe ghashe pa felechi boner pothe jete, phuler gondhe chomok lege utheche mon mete, chhoriye ache anonderi daan, bismoye tai jage amar gaan.” Walking on forest grass and startled by the scent of flowers, joy is scattered everywhere.',
    hook_q: 'How does Tagore connect the vast scale of suns and stars (“Akash-bhora surjo-tara”) with stepping on blades of grass (“Ghashe ghashe pa felechi”)?',
    hook_a: 'By recognizing that the same physical laws and living energy that light the stars are pulsing right through your own senses and footsteps today.',
    cur_q: '🔮 Melodic Contour: How does the melody of Akash Bhora Surjo Tara mirror the movement from the cosmos down to earth?',
    cur_a: '✨ It opens high on the upper tonic (Tara Shadja) like an open sky of stars, then steps gently down into the warm middle octave when describing grass, flowers, and human touch.'
  },
  {
    id: 'd13_g2',
    title: 'Anupam Roy — Amake Amar Moto Thakte Dao (Autograph, 2010)',
    yt_query: 'Amake Amar Moto Thakte Dao Anupam Roy official HD',
    story: 'Before Amake Amar Moto Thakte Dao became a modern Bengali landmark in Srijit Mukherji’s 2010 film Autograph, Anupam Roy was a Jadavpur University gold-medalist electronics engineer working as a chip designer and writing songs in his room after work.',
    bhaavna: 'Here are Anupam Roy’s exact opening lyrics: “Amake amar moto thakte dao / Ami nijeke nijer moto guchiye niyechi / Jeta chhilo na chhilo na sheta na paowai thak / Shob pele noshto jibon.” (Let me remain in my own way; I have arranged myself in my own rhythm. What was never there, let it remain unobtained—getting everything ruins a life.)\n\nAnd in the bridge, he sings: “Ei jahaj mastul chharkhar, tobu golpo likhchi banchbar / Ami rakhte chai na aar tar, kono raat dupurer abdar / Tai cheshta korchi barbar, santre paar khojar.”',
    hook_q: 'Why does the line “Jeta chhilo na chhilo na sheta na paowai thak, shob pele noshto jibon” bring instant relief to a perfectionist mind?',
    hook_a: 'Because trying to hoard every obligation and every incompatible chapter drowns your mind in noise—letting go of what was never yours leaves room for a real life.',
    cur_q: '🔮 Lyric Imagery Check: What do the bridge lines “Ei jahaj mastul chharkhar, tobu golpo likhchi banchbar” mean?',
    cur_a: '✨ Even after the ship and its mast have been battered by a storm, the narrator refuses to sink—writing a fresh story of living and swimming toward the shore.'
  },
  {
    id: 'd17_g2',
    title: 'Kazi Nazrul Islam — Karar Oi Louho Kopat (Bhangar Gaan, 1922)',
    yt_query: 'Karar Oi Louho Kopat Kazi Nazrul Islam Bengali song HD',
    story: 'In 1922, when freedom fighter Deshbandhu Chittaranjan Das was imprisoned by the British and his wife Basanti Devi asked 22-year-old Kazi Nazrul Islam for a poem for their journal Banglar Katha, the Rebel Poet wrote Karar Oi Louho Kopat (Bhangar Gaan) in a single fiery burst of inspiration.',
    bhaavna: 'Here are Kazi Nazrul Islam’s exact opening lines: “Karar oi louho-kopat, bhenge phel, kor re lopat, rokto-jomat shikol-pujar pashan-bedi! Ore o torun Ishan! Baja tor proloy-bishan! Dhongsho-nishan uruk prachir prachir bhedi!”\n\nEven when there is no external prison, over-polite “good boy” conditioning can build invisible iron gates around your own voice and appetite. Nazrul’s thunderous rhythm wakes up your spine and reminds your body that boldness is your birthright.',
    hook_q: 'Why did Kazi Nazrul Islam set an anthem about breaking iron prison gates to a fast, driving rhythmic pulse rather than a slow, heavy march?',
    hook_a: 'Because real liberation is not grim duty—it is unstoppable life force breaking through artificial walls.',
    cur_q: '🔮 Nazrul Geeti Craft: What was Kazi Nazrul Islam’s unique contribution to Bengali music?',
    cur_a: '✨ Nazrul composed nearly 4,000 songs, blending North Indian classical ragas, folk rhythms, and fearless Bengali poetry into a genre all his own!'
  },
  {
    id: 'd20_g2',
    title: 'Rabindranath Tagore — Amar Poran Jaha Chay (Prem Parjay, 1886)',
    yt_query: 'Amar Poran Jaha Chay Rabindra Sangeet best vocal HD',
    story: 'Composed by Rabindranath Tagore in 1886 for his musical drama Mayar Khela and set in Raga Mishra Kafi / Bhairavi, Amar Poran Jaha Chay is one of the most emotionally mature love songs in world literature. Most romantic songs are built on bargaining; Tagore writes from sovereign abundance.',
    bhaavna: 'Here are Tagore’s exact lyrics from Gitabitan: “Amar poran jaha chay tumi tai, tumi tai go / Toma chhara aar e jogote mor keho nai, kichu nai go / Tumi sukh jodi nahi pao, jao sukhero sondhane jao—ami tomare peyechi hridoyomajhe, aar kichu nahi chai go.”\n\n(You are what my heart desires. If you do not find happiness here, go freely in search of your joy—for I have found you within my own heart, and I ask for nothing more.) Loving from a full cup carries zero clinginess and zero guilt.',
    hook_q: 'How can the singer say “Tumi sukh jodi nahi pao, jao sukhero sondhane jao” (Go freely in search of your happiness) with warmth rather than bitterness?',
    hook_a: 'Because when your inner life is whole, love is a free gift rather than a hostage negotiation—honoring both your own dignity and the other person’s freedom.',
    cur_q: '🔮 Vocal Phrasing Tip: Where should you take a gentle breath when singing the opening line “Amar poran jaha chay tumi tai”?',
    cur_a: '✨ Pause softly for half a beat right after “chay” before singing “tumi tai, tumi tai go” in a warm, intimate chest-voice tone.'
  },
  {
    id: 'song_bn_8',
    title: 'Rabindranath Tagore — Momo Chitte Niti Nritye (Bichitro Parjay)',
    yt_query: 'Momo Chitte Niti Nritye Rabindra Sangeet HD',
    story: 'Composed by Rabindranath Tagore (NOT Kazi Nazrul Islam, as people sometimes mistakenly assume because of its lively rhythm!), Momo Chitte Niti Nritye is a joyous masterpiece from the Bichitro Parjay of Gitabitan celebrating the eternal dance of life inside human consciousness.',
    bhaavna: 'Here are Tagore’s exact lyrics: “Momo chitte niti nritye ke je naache, tata thoithoi, tata thoithoi, tata thoithoi / Tari songe ki mridonge soda baje, tata thoithoi, tata thoithoi, tata thoithoi / Hashi-kanna hira-panna dole bhale, kanpe chhonde bhalo-mondo taale taale... Ki anondo, ki anondo, ki anondo—dibaratri naache mukti naache bondho!”\n\nLook at that philosophy: laughter and tears (“hashi-kanna”) sway like diamonds and emeralds, and freedom and form (“mukti” and “bondho”) dance together in sheer joy (“Ki anondo, ki anondo, ki anondo”).',
    hook_q: 'Why does Tagore use the percussive dance syllables “tata thoithoi, tata thoithoi” inside a philosophical song about life, birth, and liberation?',
    hook_a: 'To show that the deepest spiritual truth is not a dry lecture—it is a rhythmic, embodied dance that welcomes both laughter and tears.',
    cur_q: '🔮 Attribution Check: Which poet composed “Momo Chitte Niti Nritye Ke Je Naache, Tata Thoithoi”?',
    cur_a: '✨ Rabindranath Tagore (in Gitabitan, Bichitro Parjay)—using rhythmic mridanga bol syllables (“tata thoithoi”) to celebrate cosmic joy!'
  }
];

/* ----------------------------------------------------------------------------
   4. 🔭 FRONTIER SCIENCE (16 First-Principles Science, Math & Brain Gems)
   ---------------------------------------------------------------------------- */
const ZORBA_SCIENCE_CARDS = [
  {
    id: 'd1_g3',
    title: 'Earl Miller’s Theta-Gamma Working Memory (~4 Slots)',
    yt_query: 'Earl Miller working memory theta gamma oscillations MIT lecture',
    phenomenon: 'MIT neuroscientist Earl Miller discovered why human working memory caps at roughly four items at once: individual thoughts ride on fast Gamma oscillations (~40–80 Hz) nested inside slower Theta brainwaves (~4–8 Hz), and only about four Gamma bursts fit inside a single Theta wave cycle before phase collisions scramble them.',
    mechanism: 'When your prefrontal cortex holds an item actively in mind, a local ensemble of neurons fires together in a ~25 ms Gamma burst. Meanwhile, a slower ~160 ms Theta carrier wave sweeps across the cortex like a clock cycle.\n\nTo keep Item A ("the API schema") distinct from Item B ("the latency bug"), the brain assigns Item A to phase-slot 1 of the Theta wave, Item B to phase-slot 2, Item C to phase-slot 3, and Item D to phase-slot 4. Trying to hold a 5th or 6th unparked thread in head RAM causes physical phase interference!',
    bridge: 'This single biological law explains why a high-IQ mind with huge long-term intuition can stall when juggling six tiny open loops at once. Offloading open loops onto external paper or KORTEX clears three of your four Theta-Gamma slots so your intuition runs at full speed.',
    cur_q: '🔮 Neuroscience Question: Why can you remember thousands of concepts in long-term memory if working memory only holds four phase slots?',
    cur_a: '✨ Long-term memory is stored in passive synaptic weights (requiring zero active oscillation), whereas working memory requires live, phase-locked electrical firing in real time!'
  },
  {
    id: 'd2_g3',
    title: 'Alan Turing’s Morphogenesis: How Leopard Spots Compute Themselves',
    yt_query: 'Alan Turing reaction diffusion morphogenesis leopard spots',
    phenomenon: 'Two years before his death in 1952, Alan Turing asked how a symmetrical cluster of identical embryo cells with the exact same DNA breaks symmetry into leopard spots, zebra stripes, and fingers—inventing reaction-diffusion morphogenesis.',
    mechanism: 'Turing wrote down two coupled differential equations for two diffusing chemicals: an Activator u (which triggers pigment and produces more of itself plus the inhibitor) and an Inhibitor v (which suppresses the activator).\n\nTuring proved that if both chemicals diffuse at the same speed, everything smooths out into uniform gray. But if the Inhibitor diffuses significantly faster than the Activator ("short-range activation, long-range inhibition"), tiny random fluctuations spontaneously self-organize into stable periodic spots or stripes!',
    bridge: 'Short-range activation paired with long-range inhibition is also how your visual cortex sharpens edges (center-surround receptive fields) and how great creative work happens: intense local focus on one core problem protected by a wide perimeter that blocks distractions.',
    cur_q: '🔮 Mathematical Question: Why do cheetah tails have stripes at the tip while their bodies have spots under the exact same Turing equation?',
    cur_a: '✨ When the geometry narrows from a wide cylinder (the body) to a thin cylinder (the tail), boundary conditions force 2D spot wavelengths to merge into 1D rings!'
  },
  {
    id: 'd3_g3',
    title: 'Amal Kumar Raychaudhuri & The Equation of Spacetime Singularities',
    yt_query: 'Amal Kumar Raychaudhuri equation general relativity singularities',
    phenomenon: 'Working in Kolkata in the early 1950s at Ashutosh College and Presidency College, physicist Amal Kumar Raychaudhuri derived the geometric equation showing how nearby trajectories focus under gravity—handing Roger Penrose and Stephen Hawking the mathematical key to prove black-hole and Big Bang singularities.',
    mechanism: 'To test whether singularities were just an artifact of assuming a perfectly symmetrical sphere, Raychaudhuri decomposed the motion of a bundle of nearby spacetime trajectories into three pure geometric pieces: Expansion $\\theta$ (volume change), Shear $\\sigma^2$ (shape distortion), and Vorticity $\\omega^2$ (swirling rotation).\n\nThe Raychaudhuri Equation proved that attractive gravity ($R_{\\mu\\nu} u^\\mu u^\\nu \\ge 0$) and shear always enter with a negative sign that accelerates convergence ($d\\theta/d\\tau < 0$). Unless vorticity spins fast enough to resist, any converging bundle is guaranteed to focus to zero volume ($\\theta \\to -\\infty$) in finite proper time!',
    bridge: 'Penrose and Hawking built their Nobel-winning singularity theorems directly on Raychaudhuri’s Kolkata equation—a permanent reminder that world-class breakthroughs come from asking a clean geometric first-principles question.',
    cur_q: '🔮 Physics Question: Which of the three geometric terms in the Raychaudhuri equation is the only one that can oppose gravitational focusing?',
    cur_a: '✨ Vorticity ($+2\\omega^2$, rotation)—while both expansion ($-\\theta^2/3$) and shear ($-2\\sigma^2$) pull trajectories inexorably together!'
  },
  {
    id: 'd4_g3',
    title: 'Ilya Prigogine’s Dissipative Structures: Order Far From Equilibrium',
    yt_query: 'Ilya Prigogine dissipative structures Benard convection self organization',
    phenomenon: 'Closed physical systems decay toward maximum entropy, yet living cells, hurricanes, and creative minds grow more ordered over time. Nobel laureate Ilya Prigogine proved why: open systems flowing with energy self-organize into dynamic "dissipative structures."',
    mechanism: 'When you heat a thin layer of liquid from below (Bénard convection), at first heat creeps upward by random molecular collisions. The moment the temperature gradient crosses a critical threshold, billions of molecules suddenly lock into hexagonal honeycombs of rolling convection cells!\n\nPrigogine showed that while an isolated box must increase entropy ($dS \\ge 0$), an open system ($dS = d_i S + d_e S$) exports entropy ($d_e S < 0$) by taking in fresh energy—snapping into a higher-order dynamic state.',
    bridge: 'Your brain is an open dissipative system. When you sit in a closed loop of joyless routine, mental fog rises; the moment you open the system—bringing in music, movement, fresh air, or a genuinely interesting problem—your thoughts self-organize into clear flow.',
    cur_q: '🔮 Thermodynamics Question: Why does a Bénard honeycomb or a living neuron collapse the instant you seal its boundaries?',
    cur_a: '✨ Because dynamic order is sustained by continuous energy flow—living systems are not static crystals, they are standing waves in a river of energy.'
  },
  {
    id: 'd5_g3',
    title: 'The 139,255-Neuron FlyWire Connectome & Live Neuromodulation',
    yt_query: 'FlyWire Drosophila connectome 139255 neurons ring attractor',
    phenomenon: 'When the FlyWire consortium finished mapping all 139,255 neurons and ~50 million synapses of the adult Drosophila brain from electron-microscope slices, neuroscientists could finally trace every circuit from eye photoreceptor to wing motor neuron.',
    mechanism: 'Three discoveries stood out: first, sensory areas receive massive top-down feedback from navigation centers; second, a tiny ring of neurons in the Central Complex computes a 360-degree internal compass heading using sinusoidal phase bumps; and third, static synaptic wiring alone cannot predict behavior without knowing which neuromodulators (like dopamine and octopamine) are bathing the circuit!',
    bridge: 'Think about that third finding for your own brain: your synaptic wiring (your skills and knowledge) is identical at 10 AM and 4 PM, yet your neuromodulator state (dopamine and rest) determines which circuits light up. Taking care of your rest and enjoyment is taking care of your brain’s live routing layer.',
    cur_q: '🔮 Connectomics Question: How does a fruit fly brain compute vector addition to navigate in pitch darkness?',
    cur_a: '✨ Its Central Complex represents 2D heading angles as sinusoidal bumps of neural activity across columns—so adding two vectors is literally adding two sine waves in phase!'
  },
  {
    id: 'd6_g3',
    title: 'Satyendra Nath Bose’s 1924 Quantum Counting Breakthrough in Dhaka',
    yt_query: 'Satyendra Nath Bose Einstein statistics quantum mechanics history',
    phenomenon: 'In 1924 at Dhaka University, 30-year-old Satyendra Nath Bose derived Planck’s radiation law from pure photon statistics by treating identical light quanta as fundamentally indistinguishable—birthing quantum statistics.',
    mechanism: 'To see Bose’s insight, flip two coins: in classical Maxwell-Boltzmann statistics, Head-Head, Head-Tail, Tail-Head, and Tail-Tail are 4 separate outcomes, so Head-Head occurs $1/4$ ($25\\%$) of the time.\n\nFor indistinguishable Bosons, swapping Photon A and Photon B produces the exact same physical state, so "one Head and one Tail" is a single state—leaving only 3 outcomes (HH, HT, TT). The probability of bunching into the same state (HH) jumps to $1/3$ ($33.3\\%$)!',
    bridge: 'When Philosophical Magazine rejected Bose’s 4-page paper, he mailed it directly to Albert Einstein. Einstein recognized a breakthrough immediately, translated it into German himself, and predicted Bose-Einstein condensates.',
    cur_q: '🔮 Quantum History: What happened when Paul Dirac coined the word "boson" to honor S.N. Bose?',
    cur_a: '✨ Every force-carrying particle in the universe (photons, gluons, W and Z bosons, and the Higgs boson) now carries the name of the Bengali physicist!'
  },
  {
    id: 'd7_g3',
    title: 'Uber H3: Why Hexagons Beat Squares for Planetary Spatial Indexing',
    yt_query: 'Uber H3 hexagonal hierarchical spatial index geometry',
    phenomenon: 'On a grid of squares, diagonal neighbors sit $\\sqrt{2} \\approx 1.414$ farther away than edge neighbors, distorting radius queries and movement gradients. On a hexagonal grid (Uber H3), all six neighbors sit at the exact same distance $1.0$.',
    mechanism: 'By projecting an icosahedron (20 spherical triangles) onto Earth and subdividing each face with an aperture-7 hexagonal hierarchy (where each parent hexagon contains 7 child hexagons rotated by $\\sim 19.1^\\circ$), H3 packs planet-wide multi-resolution coordinates into a single 64-bit integer—turning complex geographic lookups into $O(1)$ bit-shifts.',
    bridge: 'Just as switching from a square grid to a hexagonal coordinate system eliminates artificial $\\sqrt{2}$ corner distortion, choosing the right mental representation for a problem makes hard engineering decisions simple.',
    cur_q: '🔮 Geometry Question: Since Euler’s theorem ($\\chi = 2$) forbids tiling a sphere purely with hexagons, what sits at the 12 vertices of the H3 icosahedron?',
    cur_a: '✨ Exactly 12 pentagons—just like a classic football—and H3 orients the icosahedron so all 12 pentagon vertices sit in the middle of oceans!'
  },
  {
    id: 'd8_g3',
    title: 'Explicit Knowledge Graphs vs. Flat Vector RAG on Multi-Hop Queries',
    yt_query: 'Knowledge Graphs vs Vector RAG multi-hop reasoning architecture',
    phenomenon: 'Flat vector embeddings struggle on multi-hop relational queries and boolean negations because a single dense vector $v \\in \\mathbb{R}^d$ compresses an entire document into one blurry semantic centroid.',
    mechanism: 'When teams try to patch flat cosine-similarity search with regex table chunkers and multi-step query rewriters, latency and hallucinations compound at every hop.\n\nIn contrast, pairing semantic embeddings with an explicit Knowledge Graph—typed entity nodes, directed relational edges, Louvain community clusters, and an in-memory inverted index—resolves multi-hop set intersections ($A \\to B \\to C$) and exact negations deterministically in under 1 millisecond.',
    bridge: 'This mirrors how the human brain pairs the neocortex’s associative semantic network with the hippocampus’s explicit relational map.',
    cur_q: '🔮 Information Retrieval Question: What operation is trivial for an inverted index or graph adjacency list but noisy for a single dense dot product?',
    cur_a: '✨ Exact boolean negation ("NOT") and multi-hop transitive closure across discrete identifiers!'
  },
  {
    id: 'd9_g3',
    title: 'John von Neumann’s Self-Replicating Constructor (Before DNA!)',
    yt_query: 'John von Neumann universal constructor self replication DNA',
    phenomenon: 'In 1948—five years before Watson, Crick, and Franklin discovered the structure of DNA—John von Neumann proved mathematically how a physical machine can build a copy of itself without falling into an infinite regress.',
    mechanism: 'If a machine’s blueprint had to contain a smaller physical blueprint of the blueprint, self-replication would be impossible. Von Neumann proved that any self-replicating system must split information into two roles:\n\n1. An inert 1D symbolic tape I that is copied blindly character-by-character without being interpreted.\n2. A Universal Constructor A that reads and executes the instructions on I to build the body. Five years later, biology found the exact same split: DNA is the passive tape, and the ribosome is the constructor!',
    bridge: 'Clean software architecture uses von Neumann’s exact split: keep declarative knowledge and configuration cleanly separated as data, and keep the execution engine lean and general.',
    cur_q: '🔮 Evolution Question: Why is separating blind copying from active execution essential for open-ended evolution?',
    cur_a: '✨ Because if the copier had to "understand" every mutation before copying it, novel capabilities could never be inherited—blind tape copying lets new programs evolve!'
  },
  {
    id: 'd10_g3',
    title: 'Robert Axelrod’s Tournament: Why Nice, Provocable & Forgiving Wins',
    yt_query: 'Robert Axelrod Tit for Tat prisoners dilemma game theory',
    phenomenon: 'When political scientist Robert Axelrod pitted complex game-theory programs against each other in a 200-round iterated Prisoner’s Dilemma tournament, Anatol Rapoport’s 4-line program Tit-for-Tat beat every deceptive strategy.',
    mechanism: 'Tit-for-Tat follows two simple rules: cooperate on Round 1, and on Round n, do whatever the other player did on Round n-1.\n\nWhy did sneaky defectors lose overall even though a defector never loses a single head-to-head match? Because when two nasty strategies meet, they lock into mutual 1-point destruction, whereas two clear, cooperative strategies accumulate 3 points every round for 200 rounds! Axelrod distilled the four winning properties: Nice (start warm), Provocable (respond immediately on Beat 1 when crossed), Forgiving (return to cooperation once they stop), and Clear.',
    bridge: 'Axelrod’s tournament is the mathematical proof that warmth works best when paired with crisp, immediate Beat-1 boundaries and zero lingering resentment.',
    cur_q: '🔮 Game Theory Question: When real-world communication has a 5% chance of accidental misunderstanding, what small tweak prevents endless retaliation?',
    cur_a: '✨ "Generous Tit-for-Tat"—forgiving isolated accidental slips while still enforcing clear boundaries against repeated defection!'
  },
  {
    id: 'd11_g3',
    title: 'Karl Friston’s Predictive Processing & Active Inference',
    yt_query: 'Karl Friston predictive processing active inference neuroscience',
    phenomenon: 'Anatomically, there are ten times more feedback axons traveling top-down from higher cortex to lower sensory areas than bottom-up—because the brain is an active prediction engine rather than a passive camera.',
    mechanism: 'In Predictive Processing, higher cortical areas continuously project a top-down prediction downward, and only the residual prediction error ($\\epsilon = \\text{Sensory Input} - \\text{Prediction}$) travels upward.\n\nYou can minimize prediction error in two ways: update your internal belief to match the world (Perception), or move your muscles until the world matches your prediction (Active Inference).',
    bridge: 'When energy or dopamine dips in the afternoon, a vivid top-down imagination can sometimes project a worrisome future simulation. Recognizing "that is just a top-down prior, not bottom-up sensory reality" resets the prediction error to zero.',
    cur_q: '🔮 Motor Control Question: How does Active Inference explain how you lift a coffee cup without solving inverse-kinematics torque matrices?',
    cur_a: '✨ Motor cortex sends a top-down proprioceptive prediction that your hand is holding the cup, and spinal reflex arcs contract the muscles to zero out the error!'
  },
  {
    id: 'd12_g3',
    title: 'Riemann’s Zeta Function & The Harmonic Music of Prime Numbers',
    yt_query: 'Riemann hypothesis zeta zeros music of the primes 3Blue1Brown',
    phenomenon: 'Prime numbers ($2, 3, 5, 7, 11, 13\\dots$) look jagged and random, yet Bernhard Riemann showed in 1859 that the exact prime-counting staircase $\\pi(x)$ is formed by adding smooth harmonic waves—one wave for each nontrivial zero of the Riemann Zeta function $\\zeta(s)$.',
    mechanism: 'In Riemann’s Explicit Formula, the smooth curve $\\text{Li}(x)$ gives the average density of primes, while an infinite sum of oscillating waves over the Zeta zeros ($\\rho = 1/2 + i\\gamma_n$) adds constructive and destructive interference that sculpts the exact step at every prime number—just like Fourier overtones sculpt a musical waveform.',
    bridge: 'In 1972, over afternoon tea at Princeton, physicist Freeman Dyson noticed that Hugh Montgomery’s spacing formula for Zeta zeros was identical to the eigenvalue spacing of random Hermitian matrices in heavy atomic nuclei—connecting number theory directly to quantum physics.',
    cur_q: '🔮 Number Theory Question: What does the Riemann Hypothesis ($\text{Re}(\\rho) = 1/2$) mean in the musical wave analogy?',
    cur_a: '✨ It means every prime-generating harmonic wave grows with the exact same balanced amplitude ($x^{1/2}$)—so no single rogue frequency dominates the primes!'
  },
  {
    id: 'd13_g3',
    title: 'Da Vinci’s Vortex Sketches & Kolmogorov’s Turbulence Cascade',
    yt_query: 'Leonardo da Vinci turbulence sketches Kolmogorov 5/3 cascade',
    phenomenon: 'Around 1508, Leonardo da Vinci sketched water plunging into a pool and wrote that large swirling eddies split into smaller eddies until viscosity turns motion into warmth—anticipating Andrey Kolmogorov’s 1941 statistical law of turbulence by over four centuries.',
    mechanism: 'In Kolmogorov’s theory, kinetic energy enters a fluid at large scales (low wavenumber k), cascades without loss through a self-similar "inertial subrange" of eddies following the exact power law $E(k) \\propto \\varepsilon^{2/3} k^{-5/3}$, and finally dissipates as heat at the tiny Kolmogorov microscale.',
    bridge: 'Notice how Leonardo uncovered a 20th-century physics law through patient visual observation of light, shadow, and water. Artistic observation and mathematical physics are two sides of the same curiosity.',
    cur_q: '🔮 Millennium Prize Question: What single question about the 3D Navier-Stokes equations still carries an unclaimed $1,000,000 Clay Mathematics prize?',
    cur_a: '✨ Proving whether smooth initial fluid flows in 3D always stay smooth forever, or whether vortex stretching can focus energy into an infinite-velocity blowup in finite time!'
  },
  {
    id: 'd16_g3',
    title: 'Prasanta Chandra Mahalanobis: Covariance Geometry in Kolkata',
    yt_query: 'Mahalanobis distance intuition covariance matrix statistics',
    phenomenon: 'In 1936 in Kolkata, physicist and statistician Prasanta Chandra Mahalanobis solved how to measure true outlier distance across correlated variables—and pioneered large-scale random sample surveys across Bengal.',
    mechanism: 'If you measure whether someone is an outlier in Height and Weight using ordinary Euclidean distance $d = \\sqrt{\\Delta h^2 + \\Delta w^2}$, you treat Height and Weight as independent axes. Because taller people naturally weigh more (positive covariance $\\Sigma$), Euclidean distance misjudges correlated data.\n\nMahalanobis Distance $D_M(x) = \\sqrt{(x - \\mu)^T \\Sigma^{-1} (x - \\mu)}$ multiplies by the inverse covariance matrix $\\Sigma^{-1}$, rotating the axes to the principal eigenvectors and dividing by each variance so tilted correlation ellipses become clean unit spheres!',
    bridge: 'Mahalanobis founded the Indian Statistical Institute out of Presidency College while conversing regularly with Rabindranath Tagore—showing how world-class mathematical rigor and Bengali humanism grew side by side.',
    cur_q: '🔮 Machine Learning Question: Where does Mahalanobis Distance sit inside every multivariate Gaussian distribution?',
    cur_a: '✨ The exponent of a multivariate normal distribution $\\exp(-\\frac{1}{2} D_M^2)$ is literally negative one-half times the squared Mahalanobis distance!'
  },
  {
    id: 'd17_g3',
    title: 'Claude Shannon’s Noisy-Channel Theorem & Unicycle Play at Bell Labs',
    yt_query: 'Claude Shannon information theory noisy channel capacity Bell Labs',
    phenomenon: 'Before July 1948, engineers believed the only way to reduce errors over a noisy wire was to crank up power or repeat every bit ten times. In a single paper, Claude Shannon proved that any noisy channel can transmit data with arbitrarily zero error at any rate below Channel Capacity $C = B \\log_2(1 + S/N)$.',
    mechanism: 'Shannon separated "information" from semantic meaning, defining information purely as the mathematical reduction of uncertainty ($H = -\\sum p_i \\log_2 p_i$).\n\nBy encoding messages into high-dimensional geometric sphere packings, random thermal noise keeps a transmitted codeword inside its own non-overlapping decoding sphere—allowing the receiver to snap it back to the exact original message!',
    bridge: 'At Bell Labs, Shannon rode a unicycle down the corridors while juggling three balls, built chess-playing machines and mechanical mice for fun, and insisted that pure play was the engine of every breakthrough he ever made.',
    cur_q: '🔮 Information Theory Question: Why does a predictable, repetitive message carry almost zero Shannon information ($H \\approx 0$)?',
    cur_a: '✨ Because Shannon entropy measures surprise ($-\\log_2 p$)—a message you can already predict adds zero new bits of knowledge!'
  },
  {
    id: 'd21_g3',
    title: 'Richard Feynman’s Spinning Cafeteria Plate -> The Nobel Prize',
    yt_query: 'Richard Feynman wobbling plate Cornell cafeteria Nobel Prize story',
    phenomenon: 'Right after World War II, Richard Feynman arrived at Cornell University feeling burned out from forcing himself to do "important, dignified" physics—until a wobbling dinner plate in the cafeteria reignited his joy and led directly to Quantum Electrodynamics.',
    mechanism: 'Feynman made a quiet pact with himself: "I am going to stop trying to do important work to justify my position. I am going to play with physics strictly for my own amusement."\n\nThat week, watching a student toss a Cornell plate in the cafeteria, he noticed the red medallion on the rim rotated faster than the plate wobbled. Purely for fun, he derived the rigid-body equations and found a $2:1$ wobble-to-spin ratio at small angles. Within months, calculating those spinning trajectories led him straight to quantum electron spin paths, Feynman Diagrams, and the Nobel Prize.',
    bridge: 'Duty pressure narrows attention and creates fatigue; playing with ideas, code, music, and movement simply because they spark your curiosity unlocks your best work effortlessly.',
    cur_q: '🔮 Classical Mechanics Question: In Feynman’s torque-free thin disk calculation, what is the ratio of wobble frequency to spin frequency at small angles?',
    cur_a: '✨ Exactly $2:1$—derived from Euler’s equations because a flat disk’s perpendicular moment of inertia $I_z$ is twice its transverse inertia $I_x$!'
  }
];

/* ----------------------------------------------------------------------------
   5. 🌿 INNER CLARITY (12 Grounded Mindset & Emotional Freedom Insights)
   ---------------------------------------------------------------------------- */
const ZORBA_CLARITY_CARDS = [
  {
    id: 'd1_g0',
    title: 'Closing the 2016–2026 Survival Decade: Playing With House Money',
    insight: 'Back in college and your early twenties, carrying grief, career survival, and family safety simultaneously overloaded a 4-slot working memory. Look around at 33: Google L5 Senior SWE, ₹2.61 Cr+ net worth shield, KORTEX external memory, and Ma’s care and companion apps running smoothly. The ten-year survival campaign (2016–2026) is officially won.',
    reframe: 'When a ten-year solo climb ends and the plane is safely landed, the nervous system goes through a natural decompression thaw. Whenever an old 2016–2025 urgency reflex whispers that you need to be on high alert, you can remind your body that baseline safety is already secured—everything from 33 onward is bonus play.',
    practice: 'Drop your shoulders two inches, take one slow breath, and choose one activity today purely because you enjoy it—with zero utility scorecard attached.',
    cur_q: '🔮 Nervous System Question: Why does a brain that carried a ten-year survival campaign occasionally trigger a false Sunday-evening alarm?',
    cur_a: '✨ Because the amygdala was trained for a decade to scan for storms; meeting that old habit with a warm smile ("The plane has already landed") retrains it to baseline calm!'
  },
  {
    id: 'd2_g0',
    title: 'The First-Press Lemon Law: Toss the ₹4 Bitter Pith',
    insight: 'Pressing a fresh Gondhoraj lemon once releases 88% of its sweet, fragrant juice in two seconds. Twisting and crushing the peel six times to rescue 35 paise of liquid only squeezes bitter white pith into the glass.',
    reframe: 'If you have a bunch of six bananas and always force yourself to eat the bruised one first so nothing goes to waste, you end up eating bruised fruit your entire life even while sitting on ₹2.61 Cr+. Scarcity habits from the 1990s are completely obsolete in your current financial reality.',
    practice: 'Always take the freshest cut first: pick the comfortable flight, order the dish you actually want, and stop diminishing-returns tasks at the sweet 88% mark.',
    cur_q: '🔮 Abundance Math: How much does a ₹1,000 comfort upgrade move a ₹2.61 Cr+ compounding portfolio?',
    cur_a: '✨ Less than 0.0038%—single-hour market movements are a hundred times larger than any daily comfort upgrade you could ever buy yourself!'
  },
  {
    id: 'd3_g0',
    title: 'Speak the 1-Sentence Headline Out Loud First',
    insight: 'An intuitive polymath mind sees a problem as a simultaneous 3D web of connections, whereas spoken English is a narrow 1D stream of words. Diving straight into the middle of the web while trying to hold the whole map silently in your head crowds your 4 working-memory slots.',
    reframe: 'Speaking a single clean headline sentence out loud first ("Here is the core decision in one line, and it rests on two trade-offs") places an external tripod in the room. Once the headline is spoken into the air, both your ear and the listener hold the anchor for you.',
    practice: 'In your next explanation or design discussion, state your 1-sentence conclusion first before unpacking the supporting mechanisms.',
    cur_q: '🔮 Working-Memory Question: Why does speaking the headline aloud immediately make the rest of your explanation smoother?',
    cur_a: '✨ Externalizing the top-level node into shared auditory memory frees up two internal prefrontal working-memory slots on the spot!'
  },
  {
    id: 'd4_g0',
    title: 'Buddha’s Second Arrow: Full Amnesty for Your Younger Self',
    insight: 'In the Sallatha Sutta, the Buddha distinguishes the First Arrow (an unavoidable pain or an unmentored stumble in youth) from the Second Arrow—running a harsh courtroom inside your own head years later over the exact same memory.',
    reframe: 'Childhood Inattentive ADHD (missing peripheral details while absorbed in thought) was cognitive wiring, never selfishness. And every unmentored stumble at age 11, 17, 26, or 30 has already taught its lesson in full. Callous people never feel remorse; the fact that your conscience cared is the proof that you are a kind, principled man today.',
    practice: 'Whenever an old memory knocks, stamp it "Lesson learned years ago—full bail paid, archive closed" and return your energy to the present.',
    cur_q: '🔮 Cognitive Ethics: What is the evolutionary purpose of remorse, and when does its usefulness drop to zero?',
    cur_a: '✨ Remorse exists only to update your future values; the instant your character has integrated the lesson, any further guilt is pure wasted noise!'
  },
  {
    id: 'd5_g0',
    title: 'Jadavpur WBJEE Rank 222: Trusting Your Native Curiosity Engine',
    insight: 'Right through personal and family storms in Class 12 with zero coaching-factory scaffolding, you secured WBJEE Rank 222 to enter Jadavpur University Electrical Engineering—and went on to become a Google L5 Senior AI Engineer.',
    reframe: 'That deep-focus fire never came from fear or self-criticism; it came from your native curiosity when your mind locks onto a clean, meaningful problem. You work best when you start with the top-down geometric big picture before diving into bottom-up details.',
    practice: 'Approach your main project through curiosity rather than pressure: ask what makes the problem genuinely interesting from first principles.',
    cur_q: '🔮 2e Neuroscience: Why do high-IQ ADHD minds feel drained by routine drills yet come alive on hard architectural problems?',
    cur_a: '✨ Complex, novel patterns trigger natural phasic dopamine release in the striatum, engaging the prefrontal cortex without artificial willpower!'
  },
  {
    id: 'd6_g0',
    title: 'Cosmic Parent & Playful Child: Retiring the Inner Drill Sergeant',
    insight: 'When you lost your father at 23 with no safety net, your mind had to invent a strict internal drill sergeant just to make sure no ball was dropped. Today, your external systems—automated investments, KORTEX lists, and Ma’s care pod—handle that protective role reliably.',
    reframe: 'Because your external guardrails (the Cosmic Parent) are rock-solid, the internal drill sergeant can retire. That frees your daily awareness to live as Nietzsche’s third stage and Ramakrishna’s Santan Bhava: the curious, creative Child who builds, sings, and explores out of wonder.',
    practice: 'When a task feels heavy, hand the tracking checklist to KORTEX and ask how a curious scientist would play with the core idea for ten minutes.',
    cur_q: '🔮 Motivation Science: Why does fear-driven duty fuel cause procrastination on creative engineering work?',
    cur_a: '✨ Cortisol narrows associative networks in the prefrontal cortex, whereas curiosity widens connectivity across the whole brain!'
  },
  {
    id: 'd8_g0',
    title: 'The 6 PM Off-Duty Caretaker Switch: Structural Care Without Fusion',
    insight: 'True family leadership is structural: building financial security, setting up Ma’s care pod and companion apps, and planning clean household boundaries. Emotional fusion—absorbing someone else’s bad mood or stress into your own chest after 6:00 PM—helps nobody.',
    reframe: 'Even the most dedicated surgeon takes off the hospital coat at the end of a shift. Loving your family warmly through a clear glass window—providing structural support while keeping your own evening peace intact—actually gives the whole household a calmer anchor.',
    practice: 'At 6:00 PM, treat your caretaker role as officially off-duty so your evening belongs freely to your own music, sports, food, and laughter.',
    cur_q: '🔮 Family Systems Theory: Why does a household settle down faster when the leader refuses to absorb everyone else’s anxiety?',
    cur_a: '✨ In Murray Bowen’s family systems theory, a calm, non-anxious presence acts as an emotional circuit breaker that stops stress from amplifying!'
  },
  {
    id: 'd9_g0',
    title: 'Clean-Slate Romance: Equal Playfulness & Dropping the Rescuer Chair',
    insight: 'Dating exists to discover whether two people genuinely fit long-term. Stepping back honestly when long-term compatibility is not there is healthy adult integrity, leaving a 100% clean slate across every past chapter.',
    reframe: 'Because you spent ten years being the steady problem-solver at home, it was easy to slip into the "understanding therapist or rescuer" chair on dates. Real romantic chemistry happens between two equals bantering at eye level—where you get to lean back, be cherished, and have fun too.',
    practice: 'In romantic and social conversations, drop the impulse to diagnose or fix anyone’s life—stay in warm, playful, equal banter.',
    cur_q: '🔮 Relationship Dynamics: What is the clearest sign that a connection is built on equal playfulness rather than caretaker duty?',
    cur_a: '✨ You walk away from the conversation feeling lighter, more energized, and more yourself than when you arrived!'
  },
  {
    id: 'd11_g0',
    title: '2-Minute Expressive RAM Eviction (Klein & Boals’ Reset)',
    insight: 'Psychologists Kitty Klein and Adriel Boals proved in controlled experiments that unexpressed emotional friction squats directly inside prefrontal working-memory slots, quietly reducing available cognitive bandwidth.',
    reframe: 'Putting a nagging annoyance or open loop into three plain, unfiltered sentences on paper or in KORTEX evicts it from biological working memory—measurably restoring 15–20% of prefrontal capacity within minutes.',
    practice: 'Whenever a vague annoyance or unfinished thought hovers in the background, write it down in two raw sentences so your 4 slots return to full clarity.',
    cur_q: '🔮 Affect Labeling Neuroscience: Why does naming a messy feeling in plain words shrink its emotional intensity within seconds?',
    cur_a: '✨ Putting feelings into words activates the right ventrolateral prefrontal cortex, which sends inhibitory signals that quiet the amygdala!'
  },
  {
    id: 'd12_g0',
    title: 'Spotting Low-Dopamine Counterfeit Adrenaline in 5 Seconds',
    insight: 'When an active brain hits a quiet afternoon or evening dip in dopamine, it sometimes tries to wake itself up by rendering a scary future simulation or an urgent impulse to revisit an old memory—because alarm releases norepinephrine and adrenaline.',
    reframe: 'An urgent or gloomy thought that appears during an afternoon energy dip has zero prophetic truth; it is just a low-dopamine hardware trick trying to generate stimulation. You never need to argue with the story—you simply reset your physiology.',
    practice: 'When a sudden wave of false urgency appears, splash cold water over your closed eyes for 20 seconds, do a brief wall push, and put on a favorite song.',
    cur_q: '🔮 Autonomic Physiology: Why does cold water over the eyes and cheekbones slow your heart rate within 15 seconds?',
    cur_a: '✨ Cold receptors on the ophthalmic branch of the trigeminal nerve trigger the mammalian dive reflex, firing the vagus nerve to slow the heart!'
  },
  {
    id: 'd15_g0',
    title: 'The 70/30 Movie-Director Frame at L5+: Fire Without Smoke',
    insight: 'At junior engineering levels, writing every line of code solo is rewarded. From L5 Senior SWE and L6 Staff levels onward, trying to hand-carry 100% of five simultaneous workstreams creates exhaustion ("smoke").',
    reframe: 'The secret of sustainable senior technical leadership is the 70/30 Movie-Director split: invest 30% of your prime deep-focus energy into ONE solo first-author Crown Jewel (the core algorithm, architecture doc, or flagship CL), and direct the remaining 70% like Satyajit Ray on set—defining clean 1-page interfaces, unblocking teammates in 5 minutes, and sharing credit generously.',
    practice: 'Look at your active workstreams and clearly name which single one is your 30% Crown Jewel and which ones belong in the 70% director chair.',
    cur_q: '🔮 Technical Leadership: Why does sharing credit generously on the 70% umbrella actually increase a senior engineer’s authority?',
    cur_a: '✨ Because engineers love building inside a generous architect’s vision, making you the natural gravity center of the team!'
  },
  {
    id: 'd16_g0',
    title: 'Dropping Polite "Onugoto" Compliance for Warm Beat-1 Honesty',
    insight: 'Growing up keeping the peace in a traditional household can train an over-accommodating "onugoto" reflex—agreeing politely first or writing three paragraphs of justification before stating a simple preference.',
    reframe: 'In adult work and friendships, stating your genuine preference or boundary calmly on Beat 1 ("That won’t work for me today, let’s do Thursday" or "Here is the approach I recommend") creates instant clarity, earns respect, and leaves zero resentment.',
    practice: 'Notice one moment where you would normally hedge or over-explain, and state your real preference in one warm, direct sentence instead.',
    cur_q: '🔮 Social Psychology: Why do people feel more relaxed and trusting around someone who can say a warm, simple "No" on Beat 1?',
    cur_a: '✨ Because when someone says "No" cleanly without guilt, everyone knows that their "Yes" is 100% genuine!'
  }
];

/* ----------------------------------------------------------------------------
   6. 🎧 ACTIVE LISTENING (12 Real-Time Comprehension & Ear Exercises)
   ---------------------------------------------------------------------------- */
const ZORBA_LISTENING_CARDS = [
  {
    id: 'd1_g1',
    title: 'Pass-1 Headline Catch: Zero Sentence-2 Stalling',
    lens: 'Listening lag happens when your analytical instinct pauses on Sentence 2 to ask "Wait, why does that work?" while the speaker is already on Sentence 6. Keep your inner critic silent until the speaker finishes, and catch only the 1-sentence core thesis first.',
    monologue: 'Listen to this passage straight through without pausing on the second sentence: “Most engineers assume that adding a wider highway lane reduces city traffic congestion. Yet across fifty years of urban data from Los Angeles to London, widening a commuter highway returns rush-hour speed to its exact previous crawl within twenty-four months. Why? Because traffic is not a fixed pipe of water; it is a latent demand market. The moment travel time drops by ten minutes, people who previously took trains or shifted hours move onto the road until travel time hits their tolerance ceiling again.”',
    synthesis: 'Thumb Anchor (Premise): Widening highways fails to cure city traffic within two years.\nIndex Anchor (Mechanism): Traffic behaves like an elastic latent-demand market rather than a fixed volume of water.\nMiddle Anchor (Takeaway): Adding capacity alone just invites latent demand.\n\n1-Sentence Headline: Widening highways fails to cure congestion because latent commuter demand expands to refill any time savings.',
    cur_q: '🔮 Ear Check: In that passage, how many months did it take for widened highways to return to their previous rush-hour crawl?',
    cur_a: '✨ Twenty-four months (two years)—caught effortlessly when your ear rides the whole paragraph instead of stalling early!'
  },
  {
    id: 'd2_g1',
    title: 'Holding 3 Finger Anchors in a 4-Slot Working Memory',
    lens: 'Instead of trying to transcribe every spoken word in your head, tag three spatial anchors gently on your fingers as you listen: Thumb = Setup, Index = Twist, Middle = Takeaway.',
    monologue: 'Hold three finger anchors as you hear this true story: “In 1928, Alexander Fleming returned from a two-week summer holiday to his cluttered London lab and noticed a blue-green mold contaminating one of his Staphylococcus petri dishes. Nine out of ten tidy scientists would have poured bleach into the dish and discarded it. Instead, Fleming paused and noticed a clear halo around the mold where not a single bacterium could survive—turning an accidental mess into penicillin.”',
    synthesis: 'Thumb Anchor (Setup): Fleming found an accidental mold contamination in his petri dish after holiday.\nIndex Anchor (Twist): Instead of throwing out the spoiled dish, he noticed the bacteria-free halo around the mold.\nMiddle Anchor (Takeaway): Breakthroughs often hide inside anomalies that rigid perfectionism throws away.',
    cur_q: '🔮 Ear Check: What was the visual clue inside the petri dish that caught Fleming’s eye?',
    cur_a: '✨ A clear halo around the blue-green mold where no Staphylococcus bacteria could grow!'
  },
  {
    id: 'd3_g1',
    title: 'Hearing the Hidden Emotional Subtext Beneath Literal Words',
    lens: 'In engineering reviews and personal life, people rarely state their real worry in plain words—a colleague arguing fiercely about a minor rollout detail is often asking "Please don’t make my team’s hard work look invisible."',
    monologue: 'Listen for both the literal claim and the unspoken need in this statement: “Look, I’m not saying the new graph caching service is bad, I just think rewriting the query router two weeks before the quarterly review introduces way too many unknown failure modes when my team has spent six months stabilizing the current pipeline.”',
    synthesis: 'Literal Claim: Rewriting the query router right before the quarterly review carries stability risk.\nUnspoken Emotional Subtext: “Please protect my team’s six months of stabilization credit in front of leadership.”\n\nWarm Beat-1 Reply: “Your team’s stabilization work is the foundation we’re building on—let’s keep your router as the default production path for the review and run the graph cache as an opt-in shadow flag.”',
    cur_q: '🔮 Subtext Insight: Why does acknowledging the other person’s six months of effort first dissolve 90% of technical turf wars?',
    cur_a: '✨ Because once status and credit feel safe, their prefrontal cortex stops defending territory and starts collaborating on architecture!'
  },
  {
    id: 'd5_g1',
    title: 'Spotting the Single Unstated Load-Bearing Assumption',
    lens: 'Every persuasive pitch rests on one unstated assumption that the speaker hopes you accept automatically. Listening like Richard Feynman means catching the headline first and spotting that single load-bearing premise.',
    monologue: 'Spot the unstated assumption inside this pitch: “Because our new AI code-review assistant processes pull requests in four seconds instead of waiting six hours for a senior engineer, rolling it out across all fifty repositories will quadruple our team’s weekly feature delivery speed.”',
    synthesis: 'Headline Claim: Replacing 6-hour human review waits with 4-second AI reviews will quadruple feature delivery.\nHidden Assumption: It assumes code-review wait time—rather than integration testing, design clarity, or debugging—is the primary bottleneck governing weekly delivery!',
    cur_q: '🔮 Systems Law: What famous engineering law explains why speeding up a non-bottleneck step by 1000x barely moves total throughput?',
    cur_a: '✨ Amdahl’s Law (and Goldratt’s Theory of Constraints)—a pipeline only speeds up to the extent that you widen its true bottleneck!'
  },
  {
    id: 'd7_g1',
    title: 'Compressing a Wordy Pitch Into Constraint, Bottleneck & Trade-Off',
    lens: 'When a speaker rambles through five layers of technical jargon, filter the stream into just three clean slots: (1) Input Constraint, (2) Core Bottleneck, and (3) Trade-Off Chosen.',
    monologue: 'Extract the three core signals from this architecture update: “For our real-time voice companion pipeline, mobile clients on 4G cannot tolerate more than 350 milliseconds of time-to-first-audio. Right now our synchronous full-paragraph TTS synthesis blocks for 2.4 seconds on long stories, which stalls the conversation. So we are splitting the first sentence at the earliest punctuation boundary to stream Chunk 0 in 280 milliseconds while pre-fetching Chunks 1 and 2 in parallel.”',
    synthesis: '1. Input Constraint: Under $350\\text{ ms}$ time-to-first-audio on mobile.\n2. Core Bottleneck: Full-paragraph synthesis blocks for $2.4\\text{ s}$.\n3. Trade-Off / Solution: Stream a short first clause in $280\\text{ ms}$ while pre-fetching subsequent chunks in parallel.',
    cur_q: '🔮 Architecture Ear Check: Why is filtering a rambling technical update down to [Constraint, Bottleneck, Trade-Off] so calming?',
    cur_a: '✨ Because those three items fit cleanly inside a 4-slot working memory with one slot left over to ask a sharp follow-up question!'
  },
  {
    id: 'd8_g1',
    title: 'Storyteller’s Pacing: Sensory Opening, Contrast & Quiet Landing',
    lens: 'Great speakers hold attention not just by what they say, but by how they pace three moves: a concrete visual opening, a human contrast, and a quiet landing.',
    monologue: 'Notice the three moves in this short miniature: “At 5:45 PM on the evening train, the monsoon rain outside the window turns every telegraph pole into a blur of wet charcoal. Most passengers stare at glowing phone screens, still fighting battles from 2 PM. Yet the old gentleman by the window simply closes his eyes, taps four gentle beats on his umbrella handle, and smiles before the train reaches the station.”',
    synthesis: 'Move 1 (Sensory Opening): Wet charcoal telegraph poles outside the monsoon train window.\nMove 2 (Contrast): Passengers still fighting 2 PM battles on glowing screens.\nMove 3 (Quiet Landing): The gentleman tapping four beats on his umbrella handle in peace.',
    cur_q: '🔮 Storytelling Insight: Why does starting with a concrete visual image hook the human ear ten times faster than an abstract statement?',
    cur_a: '✨ Concrete nouns immediately light up the listener’s visual and auditory cortices, painting a mental movie with zero effort!'
  },
  {
    id: 'd9_g1',
    title: 'Eyes-Closed Auditory Cinema: Dual-Coding in Visual Cortex',
    lens: 'Reading text occupies visual cortex bandwidth; listening with your eyes closed frees your visual cortex to render a live movie scene of what you hear, doubling recall without taking notes.',
    monologue: 'Close your eyes as you hear this scene: “A narrow stone lane in old Varanasi just after dawn: brass temple bells echoing off damp sandstone walls, the smell of warm cardamom steam rising from a clay cup of chai, and a boatman dipping a single wooden oar into the silver-gray river while a flock of green parakeets wheels across the pale orange sky.”',
    synthesis: 'Three Sensory Layers Painted in Your Mind’s Eye:\n1. Sound: Brass bells echoing + wooden oar dipping into water.\n2. Smell & Touch: Warm cardamom steam from clay + damp sandstone.\n3. Color: Silver-gray water + green parakeets against pale orange dawn.',
    cur_q: '🔮 Memory Science: Why do you remember all three sensory layers effortlessly without memorizing a list?',
    cur_a: '✨ Allan Paivio’s Dual-Coding Theory: when spoken words trigger a vivid spatial scene in visual cortex, the brain stores both the verbal and visual trace in parallel!'
  },
  {
    id: 'd10_g1',
    title: 'The Rapoport Steelman: Stating Their Case Better Than They Did',
    lens: 'When someone says something you half-disagree with, the brain’s reflex is to start drafting a rebuttal at Sentence 2—which mutes comprehension of Sentences 3 to 5. Listening to state their strongest case first keeps your ear 100% open.',
    monologue: 'Listen to this contrarian view without drafting a rebuttal until the end: “Modern AI coding assistants make engineers faster at generating boilerplate, but they quietly erode deep systems debugging skill—because you only build a visceral intuition for memory layout, race conditions, and network backpressure when you have wrestled with raw stack traces yourself.”',
    synthesis: 'Steelman Summary: Hands-on struggle with raw failure modes is what builds durable debugging intuition, so automating every step risks creating pilots who struggle when autopilot disengages.\n\nBalanced Synthesis: Use AI to clear repetitive boilerplate, while reserving deliberate deep-dive debugging and core architecture for your own hands!',
    cur_q: '🔮 Communication Insight: What happens in the other person’s mind when you summarize their argument even more clearly than they did?',
    cur_a: '✨ Their defensive guard drops immediately, making them completely open to hearing your synthesis!'
  },
  {
    id: 'd11_g1',
    title: 'Numbers in Motion: Order-of-Magnitude Fermi Listening',
    lens: 'When spoken numbers fly past in a meeting, trying to hold exact 5-digit figures jams working memory. Round immediately to clean powers of ten and ratios.',
    monologue: 'Round these numbers on the fly as you listen: “Our corpus holds 48,720 documents averaging 1,940 tokens each—roughly 100 million tokens total. At $0.15 per million input tokens, a full nightly re-index costs about $15, whereas incremental hash-delta indexing of the 2% daily changes costs just $0.30 a night.”',
    synthesis: 'Effortless Mental Math:\n• $50\\text{k docs} \\times 2\\text{k tokens} \\approx 10^8$ (100M) tokens.\n• Full pass: $100 \\times \\$0.15 = \\$15$ per night.\n• 2% incremental delta: $\\$0.30$ per night—a $50\\times$ reduction!',
    cur_q: '🔮 Fermi Ear Tip: Why is holding "$50\\times$ reduction ($15 vs $0.30)" infinitely easier than memorizing "48,720 and 1,940"?',
    cur_a: '✨ Exact 5-digit numbers fill all 4 working-memory slots, whereas an order-of-magnitude ratio takes only 1 slot!'
  },
  {
    id: 'd12_g1',
    title: 'Zero-Self-Monitoring Banter: Riffing on the Last Four Words',
    lens: 'In warm social conversations or dates, listening feels effortless when you turn off the internal monitor asking "What clever thing should I say next?" and simply riff on the playful image in the speaker’s final phrase.',
    monologue: 'Catch the playful hook in the last phrase of this remark at a cafe: “Honestly, I thought moving to Hyderabad would turn me into a serious morning-marathon person, but my actual superpower is discovering which bakery pulls the warmest almond croissants out of the oven at 6 PM.”',
    synthesis: 'Playful Hook in the Final Words (“oven at 6 PM”): Instead of switching into a serious discussion about exercise habits, smile and riff on the croissant radar: “A 6 PM fresh-out-of-the-oven croissant radar beats a marathon medal any day—which bakery holds the crown right now?”',
    cur_q: '🔮 Conversational Flow: Why does echoing a concrete detail from someone’s final phrase make banter feel so natural?',
    cur_a: '✨ Because the final phrase is still resonating in both auditory buffers (the recency effect), creating instant shared momentum!'
  },
  {
    id: 'd14_g1',
    title: 'Signal vs. Tangent Filtering: Holding the Main Trunk',
    lens: 'Real humans speak with charming tangents and side stories. Instead of losing the thread when a speaker meanders, hold the "Main Trunk" lightly in one hand and let the tangents float past with a smile.',
    monologue: 'Keep the Main Trunk as two tangents float past: “I wanted to ask your advice on whether we should open-source our graph evaluation benchmark next month—by the way, the espresso machine on the fourth floor was making that steam hiss again this morning, and it reminded me of that cafe in Pondicherry—anyway, the real question is whether releasing the benchmark before the paper submission helps adoption or gives away our lead.”',
    synthesis: 'Warm Tangents Noted & Released: The 4th-floor espresso machine + Pondicherry cafe.\nClean Main Trunk: Should we open-source the graph benchmark before the paper submission to grow adoption, or wait until after to protect our lead?',
    cur_q: '🔮 Human Communication: Why do people naturally weave small sensory tangents into important questions?',
    cur_a: '✨ Casual tangents act as social warm-up bids that lower tension—smiling at the tangent while answering the trunk honors both warmth and clarity!'
  },
  {
    id: 'd15_g1',
    title: 'Socratic Listening: Spotting What Was Left Unspoken',
    lens: 'The sharpest leader in a room rarely talks the most—they listen all the way through a plan and ask one calm question about the single piece that was left unspoken.',
    monologue: 'Listen for the missing piece in this launch plan: “We have load-tested the new recommendation service at 10,000 queries per second, verified that GPU memory stays under 70%, and scheduled the global 100% production cutover for Friday at 4:30 PM.”',
    synthesis: 'What Was Left Unspoken: Rollback safety and Friday-evening timing.\nSingle Calm Socratic Question: “The throughput and memory numbers look rock-solid—what is our automated rollback trigger if Friday evening metrics dip, or would cutting over Tuesday morning at 10 AM give the team a cleaner window?”',
    cur_q: '🔮 Leadership Insight: Why is asking a calm question ten times more effective than saying "Deploying on Friday afternoon is a mistake"?',
    cur_a: '✨ A calm question invites the speaker’s own prefrontal cortex to spot the gap, turning your insight into shared ownership!'
  }
];

/* ----------------------------------------------------------------------------
   7. 🦁 EMBODIED FLOW (12 Somatic, Movement & Creative-Momentum Practices)
   ---------------------------------------------------------------------------- */
const ZORBA_FLOW_CARDS = [
  {
    id: 'd1_g4',
    title: 'One 100% Crown Jewel vs. The 20% Tourist Pass',
    principle: 'Your first-principles depth standard is a superpower on one flagship problem and a trap when applied to routine emails, minor reviews, or errands. Crown ONE piece of craft for deep focus, and stamp a "20% Tourist Pass" on routine noise.',
    mechanism: 'When an analytical mind treats every incoming ping and minor chore with 100% perfectionist depth, all 4 working-memory slots saturate before noon. Separating work into one Crown Jewel and shipping a clean, good-enough 3-minute reply on routine items frees hours of prime energy.',
    ritual: 'Name your single Crown Jewel for the day, and on the next two routine messages or errands, take three minutes to ship a clean, simple answer and close the tab.',
    cur_q: '🔮 Systems Throughput: Why does a good-enough answer shipped in 3 minutes on a routine node beat a 99% answer shipped 3 days late?',
    cur_a: '✨ Because in distributed systems and human teams, unblocking downstream flow matters ten times more on routine nodes than local over-polishing!'
  },
  {
    id: 'd2_g4',
    title: 'Floor-Up Orthopedic Reset: Left Arch Dome & 30-Second Hang',
    principle: 'Postural ease starts from the ground up: gently doming the inner arch of your left foot aligns the knee and hip, while a 30-second passive hang opens the ribcage and decompresses the spine.',
    mechanism: 'Lifting the medial arch of the left foot while keeping the big toe mound grounded rotates the tibia externally by a few degrees, leveling the pelvis and relaxing the lower back. Pairing that with a passive bar hang or wide chest opener floods proprioceptive nerves with calm feedback.',
    ritual: 'Stand barefoot for 60 seconds feeling the tripod of your foot (big toe mound, little toe mound, center heel), let your shoulders drop wide, and soften your jaw and upper belly.',
    cur_q: '🔮 Biomechanics Question: How does doming the foot arch influence neck and jaw tension six feet higher up the body?',
    cur_a: '✨ Through the Deep Front Line myofascial chain connecting the posterior tibialis, psoas, diaphragm, and deep neck flexors!'
  },
  {
    id: 'd3_g4',
    title: 'The 15-Second "# NEXT:" Breadcrumb Before Standing Up',
    principle: 'Re-entry friction after a break happens only when you walk away from your desk on a fuzzy problem. Leaving a tiny `# NEXT:` note right at the cursor makes sitting back down effortless.',
    mechanism: 'Every time you leave your workstation without saving your mental program counter, your brain has to spend 15 minutes of fresh glucose reconstructing the call stack when you return. Typing a single concrete next action (`# NEXT: check tensor shape on line 88`) reduces reload time to 5 seconds.',
    ritual: 'Before closing your laptop or stepping away for coffee, type one `# NEXT:` line with a simple 10-second physical action so your returning self slides straight into flow.',
    cur_q: '🔮 Computer Architecture Analogy: What is the exact CPU equivalent of leaving a `# NEXT:` cursor breadcrumb?',
    cur_a: '✨ Saving the Program Counter (PC) and register state to the stack frame before an interrupt, so resuming execution is $O(1)$ instead of a cold reboot!'
  },
  {
    id: 'd4_g4',
    title: 'Counting Doors & Counters: Unhurried Transition Physics',
    principle: 'A top-down mind often estimates travel time as "home to destination = 10 minutes," erasing elevators, parking basements, security gates, and corridors. Counting the physical doors and counters in between keeps every transition unhurried.',
    mechanism: 'Rushing through doorways because of compressed time estimates triggers low-grade sympathetic stress before you even arrive. Adding 4 to 5 minutes for each physical transition boundary (elevator + parking + reception) lets you walk in early with a cool head.',
    ritual: 'Before heading out to any appointment, count the physical doors and counters along the way and drop your walking pace by 15% as you cross each doorway.',
    cur_q: '🔮 Spatial Hippocampus Question: Why do people often forget why they walked into a room ("the Doorway Effect")?',
    cur_a: '✨ Walking through a doorway triggers an event-boundary flush in the hippocampus—which you can use intentionally to leave the previous room’s stress behind!'
  },
  {
    id: 'd6_g4',
    title: 'The 2-Minute "Ugly Sketch" Starter-Motor Trick',
    principle: 'A perfectionist brain freezes on a blank page, yet loves improving a rough draft. Lowering the bar to a 2-minute messy 4-bullet sketch bypasses starting friction completely.',
    mechanism: 'The basal ganglia’s initiation gate stalls when the prefrontal cortex demands "Write a polished architecture document." Giving yourself permission to write the roughest 4-line caveman outline possible breaks static inertia; once the cursor is moving, your architectural instinct takes over naturally.',
    ritual: 'Whenever a document or task feels sticky to start, race a 120-second timer to jot down four rough, unpolished bullet points.',
    cur_q: '🔮 Mechanics & Brain Analogy: Why is static friction ($\\mu_s$) always higher than kinetic friction ($\\mu_k$)?',
    cur_a: '✨ Starting requires breaking resting default-mode inertia; once motor and striatal circuits are firing, sustaining motion takes less than half the energy!'
  },
  {
    id: 'd7_g4',
    title: 'Warm-to-Cool Gear-Shift Shower Between Work and Evening',
    principle: 'Deep analytical focus can leave your mind revving in daytime work gear even after your workday is done. Water is the fastest physical clutch pedal to shift into evening freedom.',
    mechanism: 'Starting a shower warm relaxes tight upper-back and neck muscles through vasodilation, and finishing with 20–30 seconds of cool water over the neck and chest triggers a clean, sustained lift in baseline dopamine and parasympathetic calm without any screen scrolling.',
    ritual: 'Use an unhurried evening shower—warm first, finishing with a 20-second cool rinse—as the physical boundary where work ends and free evening play begins.',
    cur_q: '🔮 Physiology Question: What happens to baseline dopamine after brief cool-water immersion in human clinical studies?',
    cur_a: '✨ Studies in the European Journal of Applied Physiology measured a smooth, sustained lift in plasma dopamine and alertness with zero cortisol spike!'
  },
  {
    id: 'd8_g4',
    title: 'Single-Arm Suitcase Carry & Grounded Upright Presence',
    principle: 'Carrying a moderate weight in one hand at a time wakes up the deep lateral core stabilizers automatically, leveling the pelvis and giving your walk an effortless, grounded posture.',
    mechanism: 'When you hold a dumbbell, kettlebell, or loaded bag in one hand (a suitcase carry), the opposite quadratus lumborum (QL), obliques, and hip stabilizers fire reflexively to keep your spine tall and vertical—fixing asymmetrical waist tension without conscious effort.',
    ritual: 'Carry a moderate weight in one hand for 30 seconds per side while keeping your shoulders level, chest open, and breathing smoothly.',
    cur_q: '🔮 Spine Biomechanics: Why did spine researcher Stuart McGill rank the single-arm suitcase carry above sit-ups for core health?',
    cur_a: '✨ Because it trains the core’s true anatomical job—stabilizing the pelvis and spine against lateral tilt while keeping the discs in a neutral position!'
  },
  {
    id: 'd9_g4',
    title: 'The 10-Second 5-Need Interoception Sightline Check',
    principle: 'Deep concentration mutes physical signals like thirst, hunger, eye strain, and breath holding until late-afternoon fatigue hits. A 10-second check keeps the physical battery full.',
    mechanism: 'The anterior insula translates internal body signals (hydration, blood glucose, muscle tension) into conscious mood. When you are absorbed in code or research, checking five simple gauges prevents physical thirst or shallow breathing from masquerading as mental exhaustion.',
    ritual: 'Take 10 seconds to check five physical gauges: (1) Water within reach, (2) Protein fuel, (3) Soft jaw and belly, (4) Eyes looking 20 feet out a window, and (5) Comfortable posture.',
    cur_q: '🔮 Interoception Question: Which brain region translates internal body signals like hydration and heart rate into subjective mood?',
    cur_a: '✨ The anterior insula—so a sip of water and a deep breath often clear "bad mood" signals in under a minute!'
  },
  {
    id: 'd11_g4',
    title: 'Bouldering & Swimming: 3D Tactile Meditation',
    principle: 'On a bouldering wall or in a swimming lane, your 4 working-memory slots cannot ruminate about yesterday or tomorrow because grip, foot placement, buoyancy, and breath fill 100% of present awareness.',
    mechanism: 'Beginner climbers burn out their forearms by pulling with bent arms; experienced climbers hang on straight-arm skeletal frames, twist a hip into the wall to place their center of mass over their big toe, and push upward with their legs. Complex 3D coordination recruits the cerebellum, resetting prefrontal attention.',
    ritual: 'During your next climbing, swimming, or movement session, put 100% of your attention inside the tactile feel of your hands, feet, and exhale for five minutes.',
    cur_q: '🔮 Climbing Physics: Why does turning your hip into an overhanging wall save half your finger strength?',
    cur_a: '✨ Bringing your center of mass closer to the wall reduces the outward rotational torque trying to peel your fingers off the hold!'
  },
  {
    id: 'd14_g4',
    title: 'Golden-Hour Panoramic Walk: Optic Flow & Amygdala Calm',
    principle: 'Staring at a screen 18 inches away locks your eyes in narrow foveal focus, which is wired to daytime alertness. Stepping outside for an unhurried walk with wide horizon vision physically engages the nervous system’s evening brake.',
    mechanism: 'When you walk outdoors and let your gaze rest softly on distant trees, clouds, and buildings, the lateral movement of the world across your peripheral retina ("optic flow") activates circuits in the superior colliculus and thalamus that directly quiet amygdala activity.',
    ritual: 'Enjoy a 15-to-20-minute golden-hour walk without looking at a phone screen—letting your eyes take in the widest horizon available.',
    cur_q: '🔮 Visual Neuroscience: Why does outdoor walking quiet mental chatter faster than sitting indoors?',
    cur_a: '✨ Forward self-motion combined with wide peripheral optic flow sends a direct safety signal that quiets threat circuits in the brainstem!'
  },
  {
    id: 'd16_g4',
    title: 'Tech Lead Calm: Keeping the Monkey on Its Rightful Owner',
    principle: 'In William Oncken’s classic leadership rule ("Who’s Got the Monkey?"), when someone brings a problem and you say "Let me look into that and get back to you," the monkey jumps from their back onto yours.',
    mechanism: 'A helpful senior engineer can easily accumulate ten other people’s monkeys by 3 PM. Guiding a colleague with two calm architectural questions and agreeing on their next step helps them grow faster while keeping your own working memory completely clear.',
    ritual: 'When someone brings an ambiguous blocker, offer a warm 2-sentence architectural pointer on the spot so ownership stays cleanly in their hands.',
    cur_q: '🔮 Engineering Mentorship: Why do teammates grow three times faster when you coach the interface rather than taking over the task?',
    cur_a: '✨ Because solving the step inside a clear frame builds their own engineering confidence while preserving your high-leverage focus!'
  },
  {
    id: 'd18_g4',
    title: 'Satyajit Ray’s Chiaroscuro Light & Freehand Paper Sketching',
    principle: 'From Leonardo da Vinci’s notebooks to Satyajit Ray and Subrata Mitra inventing bounce-cloth lighting for the Apu Trilogy, great visual art uses the interplay of light and shadow (*chiaroscuro*) rather than harsh flat light.',
    mechanism: 'Digital screens snap every line to a rigid grid. Drawing loose lines, cartoons, or light-and-shadow studies with a real pen on paper—or framing a portrait near a single window where light falls off with distance ($I \\propto 1/r^2$)—engages visuomotor flow with zero perfectionism.',
    ritual: 'Take three minutes with a pen on blank paper to sketch a loose contour or shadow study without erasing a single line.',
    cur_q: '🔮 Optical Physics: Why does placing a subject close to a window make the background fall into rich dark shadow without a black backdrop?',
    cur_a: '✨ Because light intensity follows the inverse-square law ($1/r^2$): a subject 2 feet from the window receives $16\\times$ more light than a wall 8 feet behind them!'
  }
];

function buildAllZorbaReels() {
  const list = [];

  function pushSongGroup(songs, vibeId, badgeText) {
    songs.forEach(sv => {
      const audioRel = `reels/${sv.id}.mp3`;
      list.push({
        id: sv.id,
        vibe: vibeId,
        badge_bn: badgeText,
        title_bn: sv.title,
        title_spoken: true,
        sections: [
          {
            heading_bn: '🎵 Musical Backstory & Sonic Landscape',
            body_bn: sv.story,
            tone: 'story',
            spoken: true
          },
          {
            heading_bn: '📜 Verified Lyrics, Meaning & Baritone Guide',
            body_bn: sv.bhaavna,
            tone: 'hitch',
            spoken: true
          },
          {
            heading_bn: '💡 The Right Question Hook',
            body_bn: `${sv.hook_q}\n\n${sv.hook_a}`,
            tone: 'extra',
            spoken: true
          }
        ],
        curiosity_q_bn: sv.cur_q,
        curiosity_q_spoken: true,
        curiosity_a_bn: sv.cur_a,
        curiosity_a_spoken: true,
        yt_query: sv.yt_query,
        yt_label_bn: `Listen to "${sv.title}" on YouTube`,
        audio_url: ZORBA_AUDIO_BASE + sv.id + '.mp3',
        audio_rel: audioRel,
        story_end: 0
      });
    });
  }

  // 1. 🎸 English Songs (8), 🎶 Hindi Songs (8), 🪷 Bengali Songs (8)
  pushSongGroup(ZORBA_ENGLISH_SONGS, 'songs_en', '🎸 English Songs');
  pushSongGroup(ZORBA_HINDI_SONGS, 'songs_hi', '🎶 Hindi Songs');
  pushSongGroup(ZORBA_BENGALI_SONGS, 'songs_bn', '🪷 Bengali Songs');

  // 2. 🔭 Frontier Science (16)
  ZORBA_SCIENCE_CARDS.forEach(sc => {
    const audioRel = `reels/${sc.id}.mp3`;
    list.push({
      id: sc.id,
      vibe: 'science',
      badge_bn: '🔭 Frontier Science',
      title_bn: sc.title,
      title_spoken: true,
      sections: [
        {
          heading_bn: '🔭 The Core Phenomenon',
          body_bn: sc.phenomenon,
          tone: 'story',
          spoken: true
        },
        {
          heading_bn: '🧮 First-Principles Intuition & Mechanism',
          body_bn: sc.mechanism,
          tone: 'hitch',
          spoken: true
        },
        {
          heading_bn: '🌐 Why It Matters for Mind & Systems',
          body_bn: sc.bridge,
          tone: 'extra',
          spoken: true
        }
      ],
      curiosity_q_bn: sc.cur_q,
      curiosity_q_spoken: true,
      curiosity_a_bn: sc.cur_a,
      curiosity_a_spoken: true,
      yt_query: sc.yt_query,
      yt_label_bn: `Explore "${sc.title}" on YouTube`,
      audio_url: ZORBA_AUDIO_BASE + sc.id + '.mp3',
      audio_rel: audioRel,
      story_end: 0
    });
  });

  // 3. 🌿 Inner Clarity (12)
  ZORBA_CLARITY_CARDS.forEach(cl => {
    const audioRel = `reels/${cl.id}.mp3`;
    list.push({
      id: cl.id,
      vibe: 'clarity',
      badge_bn: '🌿 Inner Clarity',
      title_bn: cl.title,
      title_spoken: true,
      sections: [
        {
          heading_bn: '🌿 The Core Insight',
          body_bn: cl.insight,
          tone: 'story',
          spoken: true
        },
        {
          heading_bn: '🧭 Psychological & Life Reframe',
          body_bn: cl.reframe,
          tone: 'hitch',
          spoken: true
        },
        {
          heading_bn: '⚡ Simple Everyday Practice',
          body_bn: cl.practice,
          tone: 'extra',
          spoken: true
        }
      ],
      curiosity_q_bn: cl.cur_q,
      curiosity_q_spoken: true,
      curiosity_a_bn: cl.cur_a,
      curiosity_a_spoken: true,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + cl.id + '.mp3',
      audio_rel: audioRel,
      story_end: 0
    });
  });

  // 4. 🎧 Active Listening (12)
  ZORBA_LISTENING_CARDS.forEach(lv => {
    const audioRel = `reels/${lv.id}.mp3`;
    list.push({
      id: lv.id,
      vibe: 'listening',
      badge_bn: '🎧 Active Listening',
      title_bn: lv.title,
      title_spoken: true,
      sections: [
        {
          heading_bn: '🎧 The Listening Lens',
          body_bn: lv.lens,
          tone: 'story',
          spoken: true
        },
        {
          heading_bn: '🎙️ Spoken Passage (Catch the Main Idea)',
          body_bn: lv.monologue,
          tone: 'hitch',
          spoken: true
        },
        {
          heading_bn: '🎯 1-Sentence Headline & Key Anchors',
          body_bn: lv.synthesis,
          tone: 'extra',
          spoken: true
        }
      ],
      curiosity_q_bn: lv.cur_q,
      curiosity_q_spoken: true,
      curiosity_a_bn: lv.cur_a,
      curiosity_a_spoken: true,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + lv.id + '.mp3',
      audio_rel: audioRel,
      story_end: 0
    });
  });

  // 5. 🦁 Embodied Flow (12)
  ZORBA_FLOW_CARDS.forEach(fv => {
    const audioRel = `reels/${fv.id}.mp3`;
    list.push({
      id: fv.id,
      vibe: 'zorba',
      badge_bn: '🦁 Embodied Flow',
      title_bn: fv.title,
      title_spoken: true,
      sections: [
        {
          heading_bn: '🦁 The Core Principle',
          body_bn: fv.principle,
          tone: 'story',
          spoken: true
        },
        {
          heading_bn: '🧬 How It Works in the Body & Brain',
          body_bn: fv.mechanism,
          tone: 'hitch',
          spoken: true
        },
        {
          heading_bn: '⚡ 60-Second Reset',
          body_bn: fv.ritual,
          tone: 'extra',
          spoken: true
        }
      ],
      curiosity_q_bn: fv.cur_q,
      curiosity_q_spoken: true,
      curiosity_a_bn: fv.cur_a,
      curiosity_a_spoken: true,
      yt_query: '',
      yt_label_bn: '',
      audio_url: ZORBA_AUDIO_BASE + fv.id + '.mp3',
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
