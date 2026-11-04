/* ============================================================================
   MODULE 4: HEIRLOOM LETTER & MORNING INSPIRATION (💌 চিঠি — src/js/letter-view.js)
   ============================================================================ */
function pickNewRandomQuote(autoPlayAudio) {
  if (MORNING_QUOTES.length > 1) {
    let nextIdx = curQuoteIdx;
    for (let tries = 0; tries < 10 && nextIdx === curQuoteIdx; tries++) {
      nextIdx = Math.floor(Math.random() * MORNING_QUOTES.length);
    }
    if (nextIdx === curQuoteIdx) {
      nextIdx = (curQuoteIdx + 1) % MORNING_QUOTES.length;
    }
    curQuoteIdx = nextIdx;
  }
  const qEl = document.getElementById('dailyQuoteText');
  if (qEl) qEl.textContent = MORNING_QUOTES[curQuoteIdx];
  if (autoPlayAudio) {
    stopAllAudio();
    toggleMorningQuoteAudio();
  }
  return curQuoteIdx;
}

function renderSlideDots() {
  const dotsRow = document.getElementById('slideDotsRow');
  if (!dotsRow) return;
  dotsRow.innerHTML = '';
  SLIDES.forEach((s, idx) => {
    const dot = document.createElement('button');
    dot.className = 'slide-dot' + (idx === curSlideIdx ? ' active' : '');
    dot.textContent = toBnDigits(idx + 1);
    dot.setAttribute('aria-label', 'চিঠির পাতা ' + (idx + 1));
    dot.onclick = () => goToSlide(idx, true);
    dotsRow.appendChild(dot);
  });
}

function renderSlide() {
  const s = SLIDES[curSlideIdx];
  const vLink = document.getElementById('btnWatchMovieLetter');
  if (vLink && typeof LETTER_VIDEO_URL === 'string') vLink.href = LETTER_VIDEO_URL;
  const imgEl = document.getElementById('slideImg');
  if (imgEl) imgEl.src = s.img_b64;
  document.getElementById('slideBadge').textContent = s.badge;
  document.getElementById('slideTitleBn').textContent = s.title_bn;
  document.getElementById('slideHighlight').textContent = s.highlight_bn;
  document.getElementById('slideBodyBn').textContent = s.text_bn;
  document.getElementById('prevBtn').disabled = (curSlideIdx === 0);
  document.getElementById('nextBtn').disabled = (curSlideIdx === SLIDES.length - 1);
  renderSlideDots();
  syncAllAudioButtonsUI(!audioEl.paused);
}

function goToSlide(idx, autoPlay) {
  curSlideIdx = Math.max(0, Math.min(SLIDES.length - 1, idx));
  stopAllAudio();
  renderSlide();
  if (autoPlay) toggleSlideAudio();
}

function prevSlide() {
  if (curSlideIdx > 0) goToSlide(curSlideIdx - 1, true);
}

function nextSlide() {
  if (curSlideIdx < SLIDES.length - 1) goToSlide(curSlideIdx + 1, true);
}

function toggleAutoPlayAll() {
  autoAdvance = !autoAdvance;
  document.getElementById('autoAdvanceBtn').textContent = autoAdvance ? '🔁 পরপর: চালু' : '🔁 পরপর: বন্ধ';
}

/* ============================================================================
   MODULE 4B: KOUSHIK'S PROTECTED ADMIN SETTINGS & OBSIDIAN-STYLE MA WIKI
   (Bottom of 💌 চিঠি — Maintained by Koushik, Hidden from Ma's Daily Flow)
   ============================================================================ */
function resolveWikiPageByLinkTitle(linkText) {
  const pages = kalyaniWikiVault.pages || [];
  const t = String(linkText || '').trim();
  for (let i = 0; i < pages.length; i++) {
    if (pages[i].title_bn === t || pages[i].id === t || t.includes(pages[i].title_bn)) {
      return pages[i].id;
    }
  }
  if (t.includes('গোপাল') || t.includes('বালগোপাল') || t.includes('ভোলানাথ') || t.includes('জগন্নাথ') || t.includes('সারদা') || t.includes('পশুপাখি')) {
    return 'joy_gods_and_stories';
  }
  if (t.includes('রেডিও') || t.includes('মন')) return 'mind_and_mood';
  if (t.includes('খাবার')) return 'food_and_preferences';
  if (t.includes('রানাঘাট')) return 'ranaghat_and_memories';
  if (t.includes('কথাবার্তা') || t.includes('ভাষা')) return 'language_and_voice';
  return 'agent_pattern_log';
}

function formatObsidianWikilinksHtml(rawText) {
  return String(rawText || '').replace(/\[\[([^\]]+)\]\]/g, (_, inner) => {
    const targetId = resolveWikiPageByLinkTitle(inner);
    return `<button type="button" class="wiki-link-pill" onclick="selectMaWikiPage('${targetId}')">[[${inner}]]</button>`;
  });
}

function selectMaWikiPage(pageId) {
  kalyaniWikiVault.activePageId = pageId;
  saveKalyaniWikiVault();
  renderKoushikAdminPanel();
}

function saveAdminGeminiKey() {
  const inp = document.getElementById('adminGeminiKeyInput');
  if (inp && inp.value) {
    saveGeminiApiKey(inp.value);
    showCelebrationToast('🔑 কৌশিক: জেমিনি এআই চাবি (API Key) সফলভাবে সেভ হয়েছে!');
    renderKoushikAdminPanel();
  }
}

function clearAdminGeminiKey() {
  clearGeminiApiKey();
  showCelebrationToast('🗑️ জেমিনি এআই চাবি মুছে ফেলা হয়েছে।');
  renderKoushikAdminPanel();
}

function addAdminWikiNoteFromInput() {
  const inp = document.getElementById('adminNewWikiEntryInput');
  if (!inp || !inp.value || !inp.value.trim()) return;
  const pageId = kalyaniWikiVault.activePageId || 'mind_and_mood';
  appendMaWikiEntry(pageId, inp.value.trim(), '');
  inp.value = '';
  showCelebrationToast('🧠 মায়ের স্মৃতি-উইকিতে নতুন নোট যুক্ত হয়েছে!');
  renderKoushikAdminPanel();
}

function copyMaWikiMarkdown() {
  const md = buildMaWikiContextMarkdown();
  try {
    if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
      navigator.clipboard.writeText(md);
    }
  } catch (e) {}
  showCelebrationToast('📋 মায়ের সম্পূর্ণ Obsidian স্মৃতি-উইকি কপি হয়েছে!');
}

function copyKalyaniSystemPrompt() {
  const txt = typeof KALYANI_SYSTEM_PROMPT === 'string' ? KALYANI_SYSTEM_PROMPT : '';
  try {
    if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
      navigator.clipboard.writeText(txt);
    }
  } catch (e) {}
  showCelebrationToast('📋 অ্যান্ড্রয়েড জেমিনি মাস্টার প্রম্পট কপি হয়েছে!');
}

function clearKalyaniThreadsAndMemory() {
  kalyaniThreads = {};
  saveKalyaniThreads();
  renderPlanView();
  renderKoushikAdminPanel();
  showCelebrationToast('🧹 ভয়েস মেসেজ চ্যাট ইতিহাস পরিষ্কার করা হয়েছে।');
}

function renderKoushikAdminPanel() {
  const host = document.getElementById('koushikAdminBody');
  if (!host) return;

  const hasKey = !!getGeminiApiKey();
  const pages = kalyaniWikiVault.pages || [];
  const activePage = pages.find(p => p.id === kalyaniWikiVault.activePageId) || pages[0];
  const sc = kalyaniWikiVault.patternScores || {};

  const wikiTabsHtml = pages.map(p => {
    const isAct = activePage && p.id === activePage.id;
    return `
      <button type="button" id="wikiTab_${p.id}" class="wiki-tab-btn ${isAct ? 'active' : ''}" onclick="selectMaWikiPage('${p.id}')">
        ${p.icon} ${p.title_bn} <span class="wiki-count-badge">${toBnDigits((p.entries || []).length)}</span>
      </button>
    `;
  }).join('');

  const activeEntriesHtml = (activePage && Array.isArray(activePage.entries))
    ? activePage.entries.map(e => `<li class="wiki-entry-item">${formatObsidianWikilinksHtml(e)}</li>`).join('')
    : '';

  const tagsHtml = (activePage && Array.isArray(activePage.tags))
    ? activePage.tags.map(t => `<span class="wiki-tag-chip">${t}</span>`).join(' ')
    : '';

  host.innerHTML = `
    <div class="admin-block">
      <div class="admin-block-title">🔑 ১. গুগল জেমিনি এআই চাবি (API Key — কৌশিকের কনফিগারেশন)</div>
      <div class="admin-status-line">
        স্ট্যাটাস: <strong>${hasKey ? '✅ এআই চাবি সংযুক্ত আছে (ভয়েস উত্তর ও স্মার্ট এজেন্ট সক্রিয়)' : '⚠️ এআই চাবি এখনো দেওয়া হয়নি (অফলাইন ফলব্যাক সক্রিয়)'}</strong>
      </div>
      <div class="vn-key-row">
        <input id="adminGeminiKeyInput" type="password" class="vn-key-input" placeholder="AIza..." value="${getGeminiApiKey()}" />
        <button id="btnSaveAdminKey" class="ag-btn check checked" onclick="saveAdminGeminiKey()">💾 সেভ করো</button>
        <button id="btnClearAdminKey" class="ag-btn" onclick="clearAdminGeminiKey()">🗑️ মুছে ফেলো</button>
      </div>
    </div>

    <div class="admin-block">
      <div class="admin-block-title">🎛️ ২. অ্যাপের আচরণ ও মোড কন্ট্রোল (App Behavior Controls)</div>
      <div class="admin-toggles-grid">
        <button id="btnAdminRadioMode" class="ag-btn ${radioAutoPlay ? 'check checked' : ''}" onclick="toggleRadioMode()">
          ${radioAutoPlay ? '📻 রেডিও অটো-প্লে (পরপর গল্প): চালু ✅' : '⏸️ রেডিও অটো-প্লে: বন্ধ'}
        </button>
        <button id="btnAdminStoryOnly" class="ag-btn ${storyOnlyAudio ? 'check checked' : ''}" onclick="toggleStoryOnlyAudio()">
          ${storyOnlyAudio ? '✂️ শুধু গল্পটুকু শোনানো (হোমওয়ার্ক ছাড়া): চালু ✅' : '🔊 পুরো অডিও: চালু'}
        </button>
        <button id="btnAdminUnlockAll" class="ag-btn ${unlockAllDaysMode ? 'check checked' : ''}" onclick="toggleUnlockAllDaysMode()">
          ${unlockAllDaysMode ? '🔓 সব ২১ দিন খোলা রাখা: চালু ✅' : '🔒 ক্রমানুসারে দিন খোলা: চালু'}
        </button>
      </div>
    </div>

    <div id="maObsidianWikiPanel" class="admin-block wiki-vault-block">
      <div class="admin-block-title">🧠 ৩. মায়ের জীবন্ত স্মৃতি-উইকি (Obsidian-Style LLM Wiki & Pattern Graph)</div>
      <div class="wiki-pattern-bar">
        <span>📊 এজেন্ট প্যাটার্ন স্কোর:</span>
        <span class="wiki-score-pill">😂 হাসি: ${toBnDigits(sc.comedy || 5)}</span>
        <span class="wiki-score-pill">🪷 ভগবান: ${toBnDigits(sc.gods || 5)}</span>
        <span class="wiki-score-pill">🐘 পশুপাখি: ${toBnDigits(sc.animals || 5)}</span>
        <span class="wiki-score-pill">🎵 গান: ${toBnDigits(sc.music || 4)}</span>
        <span class="wiki-score-pill">🏡 স্মৃতি: ${toBnDigits(sc.reminiscence || 4)}</span>
      </div>
      <div class="wiki-tabs-row">${wikiTabsHtml}</div>
      <div class="wiki-active-page">
        <div class="wiki-page-header">
          <div class="wiki-page-title">${activePage ? (activePage.icon + ' [[' + activePage.title_bn + ']]') : ''}</div>
          <div class="wiki-page-tags">${tagsHtml}</div>
        </div>
        <ul class="wiki-entries-list">${activeEntriesHtml}</ul>
        <div class="vn-key-row" style="margin-top:10px;">
          <input id="adminNewWikiEntryInput" type="text" class="vn-key-input" placeholder="মায়ের সম্পর্কে নতুন নোট বা [[উইকিলিঙ্ক]] যোগ করো..." />
          <button id="btnAddAdminWikiNote" class="ag-btn check checked" onclick="addAdminWikiNoteFromInput()">+ যোগ করো</button>
        </div>
      </div>
    </div>

    <div class="admin-block">
      <div class="admin-block-title">📋 ৪. জেমিনি মাস্টার প্রম্পট, উইকি এক্সপোর্ট ও সিস্টেম টুলস</div>
      <div class="admin-toggles-grid">
        <button id="btnCopyMaWikiMarkdown" class="ag-btn" onclick="copyMaWikiMarkdown()">📥 মায়ের উইকি (Markdown) কপি করো</button>
        <button id="btnCopySystemPrompt" class="ag-btn" onclick="copyKalyaniSystemPrompt()">📋 জেমিনি মাস্টার প্রম্পট কপি করো</button>
        <button id="btnAdminNotifPerm" class="ag-btn" onclick="requestMicAndNotificationPermission()">🔔 সকালের নোটিফিকেশন টেস্ট</button>
        <button id="btnAdminClearThreads" class="ag-btn" onclick="clearKalyaniThreadsAndMemory()">🧹 ভয়েস মেসেজ ইতিহাস পরিষ্কার</button>
      </div>
    </div>
  `;
}

/* Gentle Touch Swipe Support on Letter Card */
(function attachLetterSwipe() {
  const card = document.getElementById('letterSlideCard');
  if (!card || !card.addEventListener) return;
  let touchStartX = 0;
  let touchStartY = 0;
  card.addEventListener('touchstart', ev => {
    if (!ev.touches || !ev.touches.length) return;
    touchStartX = ev.touches[0].clientX;
    touchStartY = ev.touches[0].clientY;
  }, { passive: true });
  card.addEventListener('touchend', ev => {
    if (!ev.changedTouches || !ev.changedTouches.length) return;
    const dx = ev.changedTouches[0].clientX - touchStartX;
    const dy = ev.changedTouches[0].clientY - touchStartY;
    if (Math.abs(dx) > 56 && Math.abs(dx) > Math.abs(dy) * 1.4) {
      if (dx < 0) nextSlide();
      else prevSlide();
    }
  }, { passive: true });
})();
