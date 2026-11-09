/* ==========================================================================
   MacBook Smart Read Aloud & Auto-Select — Content Script Controller
   (`src/content.js`)
   - Tracks hovered paragraph / heading in real time.
   - `Option + Space` (`Alt+Space`): Auto-selects from the hovered or top-of-screen
     paragraph to the end of the article in `window.getSelection()` so macOS
     "Speak Selection" (`Option + Esc` or Right-Click → Speech → Start Speaking)
     reads it immediately without manual dragging.
     (Pressing `Option + Space` a second time within 2.5s cycles to Full Article,
      then Current Section Only.)
   - `Option + A` (`Alt+A`): Auto-selects the entire clean article from start to finish.
   - `Option + R` (`Alt+R`) or `Option + Click` on any paragraph: Auto-selects
     and immediately starts reading aloud from that paragraph to the end of the
     article using MacBook's native voices (`window.speechSynthesis`) at 1.0x pace.
   - During Read Aloud:
     - `Space`: Play / Pause
     - Click any paragraph: Jump directly to that paragraph
     - `Esc`: Stop speaking
   ========================================================================== */
(function (root, factory) {
  const api = factory(root);
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  if (root) {
    root.MacSpeakContentController = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : window, function (root) {
  "use strict";

  const detector = (root && root.MacSpeakArticleDetector) ||
    (typeof require === "function" ? require("./article-detector.js") : null);
  const deadNounConverter = (root && root.DeadNounConverter) ||
    (typeof require === "function" ? require("./dead-noun-converter.js") : null);

  function createController(env = {}) {
    const doc = env.document || (root && root.document) || null;
    const win = env.window || (root && root.window) || root || null;

    const state = {
      hoveredElement: null,
      altKeyPressed: false,
      lastSelectTimestamp: 0,
      lastSelectMode: "",
      speaking: false,
      paused: false,
      activeBlocks: [],
      currentBlockIdx: 0,
      sessionId: 0,
      toastTimer: null,
      movieModeActive: false,
      originalTextStore: typeof Map === "function" ? new Map() : null
    };

    function showToast(title, subtitle, durationMs = 2600) {
      if (!doc || !doc.body || typeof doc.createElement !== "function") return;
      let toast = doc.getElementById("mac-speak-status-toast");
      if (!toast) {
        toast = doc.createElement("div");
        toast.id = "mac-speak-status-toast";
        doc.body.appendChild(toast);
      }
      toast.innerHTML =
        `<div class="mac-speak-toast-title">${escapeHtml(title)}</div>` +
        (subtitle ? `<div class="mac-speak-toast-sub">${escapeHtml(subtitle)}</div>` : "");
      if (toast.classList) toast.classList.add("visible");
      if (state.toastTimer) clearTimeout(state.toastTimer);
      state.toastTimer = setTimeout(() => {
        if (toast && toast.classList) toast.classList.remove("visible");
      }, durationMs);
    }

    function escapeHtml(str) {
      return String(str || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }

    function clearHoverIndicator() {
      if (!doc || typeof doc.querySelectorAll !== "function") return;
      doc.querySelectorAll(".mac-speak-hover-anchor").forEach(el => {
        if (el.classList) el.classList.remove("mac-speak-hover-anchor");
      });
    }

    function clearActiveParagraphHighlight() {
      if (!doc || typeof doc.querySelectorAll !== "function") return;
      doc.querySelectorAll(".mac-speak-active-paragraph").forEach(el => {
        if (el.classList) el.classList.remove("mac-speak-active-paragraph");
      });
    }

    function pickPreferredMacVoice() {
      if (!win || !win.speechSynthesis || typeof win.speechSynthesis.getVoices !== "function") {
        return null;
      }
      const voices = win.speechSynthesis.getVoices() || [];
      if (voices.length === 0) return null;
      const preferredOrder = [
        "siri",
        "personal",
        "ava (premium)",
        "ava (enhanced)",
        "daniel (enhanced)",
        "serena (premium)",
        "oliver (enhanced)",
        "samantha (enhanced)",
        "alex",
        "daniel",
        "samantha"
      ];
      const enVoices = voices.filter(v => !v.lang || v.lang.toLowerCase().startsWith("en"));
      const pool = enVoices.length > 0 ? enVoices : voices;
      for (let i = 0; i < preferredOrder.length; i++) {
        const key = preferredOrder[i];
        const hit = pool.find(v => String(v.name || "").toLowerCase().includes(key));
        if (hit) return hit;
      }
      return pool.find(v => v.default) || pool[0];
    }

    /**
     * Auto-selects readable article text in Chrome's native `window.getSelection()`
     * so macOS "Speak Selection" (`Option + Esc` or Right-Click → Speech → Start Speaking)
     * can speak the entire range without manual click-and-drag.
     */
    function triggerSmartSelect(explicitMode, explicitTargetEl) {
      if (!detector || !doc) return { ok: false, reason: "no-detector" };

      const now = Date.now();
      let mode = explicitMode || "to-end";
      if (!explicitMode && now - state.lastSelectTimestamp < 2500) {
        if (state.lastSelectMode === "to-end") mode = "full-article";
        else if (state.lastSelectMode === "full-article") mode = "section";
        else mode = "to-end";
      }
      state.lastSelectTimestamp = now;
      state.lastSelectMode = mode;

      const res = detector.selectArticleContent(doc, {
        mode,
        hoveredEl: explicitTargetEl || state.hoveredElement,
        doc,
        win
      });

      if (!res.ok) {
        showToast("No readable article text found on this page", "");
        return res;
      }

      const modeLabel = mode === "full-article"
        ? `Selected Full Article (${res.blockCount} paragraphs)`
        : (mode === "section"
          ? `Selected Current Section (${res.blockCount} paragraphs)`
          : `Selected from Paragraph #${res.startIndex + 1} to End (${res.blockCount} paragraphs)`);

      showToast(
        `✓ ${modeLabel}`,
        "Press Option+Esc (or Right-Click → Speech → Start Speaking) • Press Option+Space again to cycle scope"
      );
      return res;
    }

    function stopSpeaking(showNotification = false) {
      state.sessionId++;
      state.speaking = false;
      state.paused = false;
      state.activeBlocks = [];
      state.currentBlockIdx = 0;
      clearActiveParagraphHighlight();
      if (win && win.speechSynthesis) {
        try {
          win.speechSynthesis.cancel();
        } catch (_e) {}
      }
      if (showNotification) {
        showToast("⏹ Stopped Read Aloud", "", 1400);
      }
    }

    function togglePauseSpeaking() {
      if (!state.speaking || !win || !win.speechSynthesis) return false;
      if (!state.paused) {
        state.paused = true;
        try {
          win.speechSynthesis.pause();
        } catch (_e) {}
        showToast("⏸ Paused Read Aloud", "Press Space to resume • Click any paragraph to skip • Esc to stop", 2000);
        return true;
      }
      state.paused = false;
      try {
        win.speechSynthesis.resume();
      } catch (_e) {}
      showToast("▶️ Resumed Read Aloud", "Space = Pause • Click any paragraph to skip", 1600);
      return false;
    }

    function scrollBlockSafelyIntoView(blockEl) {
      if (!blockEl || typeof blockEl.getBoundingClientRect !== "function" || !win) return;
      const r = blockEl.getBoundingClientRect();
      const vh = Number(win.innerHeight) || 800;
      if (r.top < 72 || r.bottom > vh - 80) {
        if (typeof win.scrollBy === "function") {
          win.scrollBy({ top: r.top - 96, behavior: "smooth" });
        } else if (typeof blockEl.scrollIntoView === "function") {
          blockEl.scrollIntoView({ block: "center", behavior: "smooth" });
        }
      }
    }

    function speakFromBlockIndex(startIdx, blocksToRead) {
      if (!win || !win.speechSynthesis || typeof win.SpeechSynthesisUtterance !== "function") {
        // Fallback: if speechSynthesis is unavailable, select the range for macOS Option+Esc
        if (blocksToRead && blocksToRead.length > 0) {
          detector.applyDomSelectionRange(doc, blocksToRead[startIdx], blocksToRead[blocksToRead.length - 1]);
        }
        return false;
      }

      const mySession = ++state.sessionId;
      state.activeBlocks = blocksToRead;
      state.currentBlockIdx = Math.max(0, Math.min(blocksToRead.length - 1, Number(startIdx) || 0));
      state.speaking = true;
      state.paused = false;

      try {
        win.speechSynthesis.cancel();
      } catch (_e) {}

      const voice = pickPreferredMacVoice();

      function speakStep() {
        if (mySession !== state.sessionId || !state.speaking) return;
        if (state.currentBlockIdx >= state.activeBlocks.length) {
          stopSpeaking(false);
          showToast("✓ Finished reading article", "", 1800);
          return;
        }

        const block = state.activeBlocks[state.currentBlockIdx];
        clearActiveParagraphHighlight();
        if (block && block.classList) {
          block.classList.add("mac-speak-active-paragraph");
        }
        // Also select the active paragraph through the end of the article in native DOM Selection
        // so the user always sees where they are and can use macOS native controls at any moment
        detector.applyDomSelectionRange(doc, block, state.activeBlocks[state.activeBlocks.length - 1]);
        scrollBlockSafelyIntoView(block);

        const rawText = detector.normalizeText(block ? block.textContent : "");
        const text = deadNounConverter
          ? deadNounConverter.convertTextToActionMovie(rawText).text
          : rawText;
        if (!text) {
          state.currentBlockIdx++;
          speakStep();
          return;
        }

        const utter = new win.SpeechSynthesisUtterance(text);
        if (voice) utter.voice = voice;
        utter.rate = 1.0;

        utter.onend = () => {
          if (mySession !== state.sessionId || !state.speaking) return;
          state.currentBlockIdx++;
          speakStep();
        };

        utter.onerror = (ev) => {
          if (mySession !== state.sessionId || !state.speaking) return;
          if (ev && (ev.error === "canceled" || ev.error === "interrupted")) return;
          state.currentBlockIdx++;
          speakStep();
        };

        win.speechSynthesis.speak(utter);
      }

      speakStep();
      return true;
    }

    /**
     * Auto-selects from the hovered/visible paragraph to the end of the article
     * AND starts reading aloud immediately at 1.0x natural comprehension pace.
     */
    function triggerSmartSpeak(explicitTargetEl) {
      if (!detector || !doc) return { ok: false, reason: "no-detector" };
      const articleRoot = detector.findMainArticleContainer(doc);
      const blocks = detector.collectReadableBlocks(doc, articleRoot);
      if (blocks.length === 0) {
        showToast("No readable article text found on this page", "");
        return { ok: false, reason: "no-readable-blocks" };
      }

      const startIdx = detector.resolveStartingBlockIndex(blocks, {
        hoveredEl: explicitTargetEl || state.hoveredElement,
        doc,
        win
      });

      showToast(
        `🔊 Reading from Paragraph #${startIdx + 1} of ${blocks.length}`,
        "Space = Play/Pause • Click any paragraph to skip • Esc = Stop"
      );
      speakFromBlockIndex(startIdx, blocks);
      return {
        ok: true,
        startIndex: startIdx,
        totalBlocks: blocks.length
      };
    }

    /**
     * Toggles "Movie Mode" (`Option + M` / `Alt+M`): converts lifeless corporate
     * "dead nouns" (nominalizations) across the page into vivid "Who-Does-What"
     * visual action verbs in-place, or restores the original page text.
     */
    function toggleMovieMode() {
      if (!deadNounConverter || !doc || !doc.body) {
        return { ok: false, reason: "no-converter" };
      }
      if (!state.movieModeActive) {
        const count = deadNounConverter.convertElementInPlace(doc.body, state.originalTextStore);
        state.movieModeActive = true;
        showToast(
          `🎬 Movie Mode ON (${count} dead-noun phrase${count === 1 ? "" : "s"} flipped to visual actions)`,
          "Press ⌥M again to restore original corporate text",
          3200
        );
        return { ok: true, active: true, convertedCount: count };
      } else {
        const restored = deadNounConverter.restoreElementOriginalText(doc.body, state.originalTextStore);
        state.movieModeActive = false;
        showToast(
          "📄 Original Corporate Text Restored",
          "Press ⌥M anytime for 🎬 Visual Action Movie Mode",
          2200
        );
        return { ok: true, active: false, restoredCount: restored };
      }
    }

    function handleMouseOver(e) {
      if (!e || !e.target || typeof e.target.closest !== "function") return;
      const block = e.target.closest("h1, h2, h3, h4, h5, h6, p, li, blockquote");
      if (!block) return;
      state.hoveredElement = block;
      if (state.altKeyPressed) {
        clearHoverIndicator();
        if (block.classList) block.classList.add("mac-speak-hover-anchor");
      }
    }

    function handleClick(e) {
      if (!e || !e.target || typeof e.target.closest !== "function") return;
      const clickedBlock = e.target.closest("h1, h2, h3, h4, h5, h6, p, li, blockquote");
      if (!clickedBlock) return;

      // 1. Option + Click (`e.altKey`): Select from clicked paragraph to end of article!
      //    If Shift+Option+Click: also start Built-in Read Aloud immediately.
      if (e.altKey && !e.metaKey && !e.ctrlKey) {
        e.preventDefault();
        e.stopPropagation();
        state.hoveredElement = clickedBlock;
        if (e.shiftKey) {
          triggerSmartSpeak(clickedBlock);
        } else {
          triggerSmartSelect("to-end", clickedBlock);
        }
        return;
      }

      // 2. While built-in Read Aloud is active, clicking any paragraph inside the article jumps directly to it!
      if (state.speaking && state.activeBlocks.length > 0) {
        const hitIdx = state.activeBlocks.findIndex(
          b => b === clickedBlock || (b.contains && b.contains(clickedBlock))
        );
        if (hitIdx !== -1) {
          e.preventDefault();
          e.stopPropagation();
          speakFromBlockIndex(hitIdx, state.activeBlocks);
        }
      }
    }

    function handleKeyDown(e) {
      if (!e) return;
      const tag = (e.target && e.target.tagName) ? e.target.tagName.toUpperCase() : "";
      const inEditable =
        tag === "INPUT" ||
        tag === "TEXTAREA" ||
        tag === "SELECT" ||
        Boolean(e.target && e.target.isContentEditable);

      if (e.key === "Alt") {
        state.altKeyPressed = true;
        if (state.hoveredElement && state.hoveredElement.classList) {
          state.hoveredElement.classList.add("mac-speak-hover-anchor");
        }
      }

      if (inEditable) return;

      // Option + Space (`Alt+Space` / `Space`): Smart Select from Hovered/Visible Paragraph to End of Article
      if (e.altKey && !e.metaKey && !e.ctrlKey && (e.code === "Space" || e.key === " " || e.key === "\u00a0")) {
        e.preventDefault();
        triggerSmartSelect();
        return;
      }

      // Option + A (`Alt+A` / `KeyA`): Smart Select Entire Clean Article
      if (e.altKey && !e.metaKey && !e.ctrlKey && (e.code === "KeyA" || e.key === "a" || e.key === "A" || e.key === "å")) {
        e.preventDefault();
        triggerSmartSelect("full-article");
        return;
      }

      // Option + R (`Alt+R` / `KeyR`): Smart Select & Read Aloud Immediately
      if (e.altKey && !e.metaKey && !e.ctrlKey && (e.code === "KeyR" || e.key === "r" || e.key === "R" || e.key === "®")) {
        e.preventDefault();
        if (state.speaking) {
          stopSpeaking(true);
        } else {
          triggerSmartSpeak();
        }
        return;
      }

      // Option + M (`Alt+M` / `KeyM`): Toggle Movie Mode (Dead Nouns -> Visual Action Verbs)
      if (e.altKey && !e.metaKey && !e.ctrlKey && (e.code === "KeyM" || e.key === "m" || e.key === "M" || e.key === "µ")) {
        e.preventDefault();
        toggleMovieMode();
        return;
      }

      // While built-in Read Aloud is active: Space = Play/Pause, Esc = Stop
      if (state.speaking) {
        if (e.key === " " && !e.altKey && !e.metaKey && !e.ctrlKey && tag !== "BUTTON" && tag !== "A") {
          e.preventDefault();
          togglePauseSpeaking();
          return;
        }
        if (e.key === "Escape") {
          e.preventDefault();
          stopSpeaking(true);
        }
      }
    }

    function handleKeyUp(e) {
      if (e && e.key === "Alt") {
        state.altKeyPressed = false;
        clearHoverIndicator();
      }
    }

    function handleRuntimeMessage(msg, _sender, sendResponse) {
      if (!msg || typeof msg !== "object") return;
      if (msg.action === "select-from-here") {
        const r = triggerSmartSelect("to-end");
        if (typeof sendResponse === "function") sendResponse(r);
      } else if (msg.action === "select-full-article") {
        const r = triggerSmartSelect("full-article");
        if (typeof sendResponse === "function") sendResponse(r);
      } else if (msg.action === "select-section") {
        const r = triggerSmartSelect("section");
        if (typeof sendResponse === "function") sendResponse(r);
      } else if (msg.action === "speak-from-here") {
        if (state.speaking) {
          stopSpeaking(true);
          if (typeof sendResponse === "function") sendResponse({ ok: true, stopped: true });
        } else {
          const r = triggerSmartSpeak();
          if (typeof sendResponse === "function") sendResponse(r);
        }
      } else if (msg.action === "toggle-pause") {
        const paused = togglePauseSpeaking();
        if (typeof sendResponse === "function") sendResponse({ ok: true, paused });
      } else if (msg.action === "stop-speaking") {
        stopSpeaking(true);
        if (typeof sendResponse === "function") sendResponse({ ok: true });
      } else if (msg.action === "toggle-movie-mode") {
        const r = toggleMovieMode();
        if (typeof sendResponse === "function") sendResponse(r);
      }
    }

    function init() {
      if (!doc || typeof doc.addEventListener !== "function") return;
      doc.addEventListener("mouseover", handleMouseOver, { passive: true });
      doc.addEventListener("click", handleClick, true);
      doc.addEventListener("keydown", handleKeyDown, true);
      doc.addEventListener("keyup", handleKeyUp, true);

      if (root && root.chrome && root.chrome.runtime && root.chrome.runtime.onMessage) {
        root.chrome.runtime.onMessage.addListener(handleRuntimeMessage);
      }

      // Load latest OTA cloud-synced Dead-Noun rules from chrome.storage.local
      if (deadNounConverter && typeof deadNounConverter.applyCloudRules === "function" && root && root.chrome && root.chrome.storage && root.chrome.storage.local) {
        try {
          root.chrome.storage.local.get(["cloudRules"], items => {
            if (items && items.cloudRules) {
              deadNounConverter.applyCloudRules(items.cloudRules);
            }
          });
          if (root.chrome.storage.onChanged) {
            root.chrome.storage.onChanged.addListener((changes, area) => {
              if (area === "local" && changes.cloudRules && changes.cloudRules.newValue) {
                deadNounConverter.applyCloudRules(changes.cloudRules.newValue);
              }
            });
          }
        } catch (_e) {}
      }
    }

    return {
      state,
      triggerSmartSelect,
      triggerSmartSpeak,
      toggleMovieMode,
      togglePauseSpeaking,
      stopSpeaking,
      handleMouseOver,
      handleClick,
      handleKeyDown,
      handleKeyUp,
      handleRuntimeMessage,
      init
    };
  }

  let defaultInstance = null;
  if (typeof document !== "undefined" && !root.__MAC_SPEAK_SKIP_AUTO_INIT__) {
    defaultInstance = createController({ document, window: root });
    defaultInstance.init();
  }

  return {
    createController,
    getDefaultInstance: () => defaultInstance
  };
});
