/* ==========================================================================
   MacBook Smart Read Aloud & Movie Mode — Background Service Worker
   (`src/background.js`)
   - Auto-injects content scripts (`article-detector.js`, `dead-noun-converter.js`,
     `content.js`, `content.css`) into already-open tabs when clicked from Popup,
     Context Menu, or Keyboard Shortcut (`Alt+Space`, `Alt+R`, `Alt+A`, `Alt+M`).
   - Speaks audio reliably via Chrome's native `chrome.tts` engine (never blocked
     by webpage autoplay policies or popup closing).
   - Calls `gemini-2.5-flash` (`https://generativelanguage.googleapis.com/...`)
     directly from the user's MacBook over HTTPS (zero Cloudtop needed!) to
     rewrite complex corporate "dead nouns" into vivid 3D visual-action sentences.
   - Syncs `cloud-rules.json` Over-The-Air (`OTA`) from GitHub Cloud.
   ========================================================================== */
"use strict";

const CLOUD_RULES_URLS = [
  "https://raw.githubusercontent.com/kouSeek/portfolio/mac-speak-chrome-ext/cloud-rules.json",
  "http://koushikchak.c.googlers.com:9500/api/mac-speak/cloud-rules.json"
];

const GEMINI_FLASH_MODELS = [
  "gemini-3.8-flash",
  "gemini-3-flash-preview"
];
const GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models";

async function syncCloudRulesNow() {
  for (let i = 0; i < CLOUD_RULES_URLS.length; i++) {
    const url = `${CLOUD_RULES_URLS[i]}?t=${Date.now()}`;
    try {
      const resp = await fetch(url, { cache: "no-store" });
      if (!resp.ok) continue;
      const data = await resp.json();
      if (data && typeof data === "object" && (data.deadNounOfMap || data.phraseRules)) {
        const meta = {
          cloudRules: data,
          cloudRulesSyncedAt: new Date().toISOString(),
          cloudRulesSource: CLOUD_RULES_URLS[i]
        };
        if (typeof chrome !== "undefined" && chrome.storage && chrome.storage.local) {
          chrome.storage.local.set(meta);
        }
        return { ok: true, version: data.version || "latest", syncedAt: meta.cloudRulesSyncedAt };
      }
    } catch (_e) {}
  }
  return { ok: false, reason: "offline-or-unreachable" };
}

function getStoredGeminiApiKey() {
  return new Promise(resolve => {
    if (typeof chrome === "undefined" || !chrome.storage || !chrome.storage.local) {
      resolve("");
      return;
    }
    chrome.storage.local.get(["geminiApiKey"], items => {
      resolve(String((items && items.geminiApiKey) || "").trim());
    });
  });
}

/**
 * Calls Google's public Cloud Gemini 2.5 Flash API directly from the user's
 * MacBook over HTTPS (`generativelanguage.googleapis.com`) to convert an array
 * of corporate/abstract sentences into vivid "Who-Does-What" visual actions.
 */
async function rewriteSentencesWithGeminiFlash(sentences, explicitApiKey) {
  const apiKey = String(explicitApiKey || (await getStoredGeminiApiKey()) || "").trim();
  if (!apiKey) {
    return { ok: false, reason: "missing-api-key" };
  }
  if (!Array.isArray(sentences) || sentences.length === 0) {
    return { ok: false, reason: "empty-input" };
  }

  const prompt = [
    "You are a Dead-Noun -> 3D Visual Action Movie translator for a visual-spatial engineer.",
    "Corporate English uses frozen abstract nouns (nominalizations like 'Supervision of a rollout includes oversight of...') which have no actor and no motion.",
    "Rewrite each numbered item in the JSON array below into plain, vivid, effortless 'Who-Does-What' everyday English using living actors ('you', 'your server', 'a human', 'auto-alarms') and moving action verbs ('watch', 'spot', 'push live', 'check').",
    "Rules:",
    "1. Preserve the exact meaning and keep each item concise (1 sentence).",
    "2. Return ONLY a valid JSON array of strings with the exact same length and order as the input array. Do not wrap in markdown fences.",
    "",
    "Input JSON array:",
    JSON.stringify(sentences)
  ].join("\n");

  let lastReason = "network-error";
  for (let i = 0; i < GEMINI_FLASH_MODELS.length; i++) {
    const modelId = GEMINI_FLASH_MODELS[i];
    const url = `${GEMINI_API_BASE}/${modelId}:generateContent?key=${encodeURIComponent(apiKey)}`;
    try {
      const resp = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: {
            temperature: 0.2,
            responseMimeType: "application/json"
          }
        })
      });
      if (!resp.ok) {
        lastReason = `http-${resp.status}`;
        continue;
      }
      const data = await resp.json();
      const rawText =
        data?.candidates?.[0]?.content?.parts?.[0]?.text || "";
      const cleaned = String(rawText).replace(/^```(?:json)?\s*|\s*```$/gi, "").trim();
      const parsed = JSON.parse(cleaned);
      if (Array.isArray(parsed) && parsed.length === sentences.length) {
        return { ok: true, model: modelId, rewritten: parsed };
      }
      lastReason = "length-mismatch";
    } catch (err) {
      lastReason = String((err && err.message) || "network-error");
    }
  }
  return { ok: false, reason: lastReason };
}

const MENU_ITEMS = [
  {
    id: "mac-speak-select-to-end",
    title: "📖 Select from Here to End of Article (for Mac Speech)",
    contexts: ["page", "selection"]
  },
  {
    id: "mac-speak-select-full",
    title: "📄 Select Entire Clean Article (for Mac Speech)",
    contexts: ["page", "selection"]
  },
  {
    id: "mac-speak-read-aloud",
    title: "🔊 Auto-Select & Read Aloud from Here (Space = Pause)",
    contexts: ["page", "selection"]
  },
  {
    id: "mac-speak-movie-mode",
    title: "🎬 Movie Mode: Flip 'Dead Nouns' into Visual Action Verbs (⌥M)",
    contexts: ["page", "selection"]
  }
];

function sendToActiveTab(tabId, payload, doneCallback) {
  if (!tabId || !chrome.tabs || typeof chrome.tabs.sendMessage !== "function") {
    if (typeof doneCallback === "function") doneCallback({ ok: false, reason: "no-tab" });
    return;
  }
  chrome.tabs.sendMessage(tabId, payload, response => {
    if (chrome.runtime && chrome.runtime.lastError) {
      // Tab was already open before extension loaded/updated -> inject CSS + JS on the fly!
      if (chrome.scripting && typeof chrome.scripting.executeScript === "function") {
        if (typeof chrome.scripting.insertCSS === "function") {
          chrome.scripting.insertCSS({ target: { tabId }, files: ["src/content.css"] }, () => {});
        }
        chrome.scripting.executeScript(
          {
            target: { tabId },
            files: ["src/article-detector.js", "src/dead-noun-converter.js", "src/content.js"]
          },
          () => {
            if (chrome.runtime && chrome.runtime.lastError) {
              if (typeof doneCallback === "function") {
                doneCallback({
                  ok: false,
                  reason: chrome.runtime.lastError.message || "cannot-inject"
                });
              }
              return;
            }
            chrome.tabs.sendMessage(tabId, payload, retryResp => {
              if (typeof doneCallback === "function") doneCallback(retryResp || { ok: true });
            });
          }
        );
      } else if (typeof doneCallback === "function") {
        doneCallback({ ok: false, reason: "no-scripting-api" });
      }
    } else if (typeof doneCallback === "function") {
      doneCallback(response || { ok: true });
    }
  });
}

function speakViaChromeTts(tabId, text, rate, sessionId) {
  if (typeof chrome === "undefined" || !chrome.tts || typeof chrome.tts.speak !== "function") {
    return false;
  }
  try {
    chrome.tts.stop();
  } catch (_e) {}

  chrome.tts.speak(String(text || ""), {
    rate: Number(rate) || 1.0,
    enqueue: false,
    onEvent(event) {
      if (!event || !tabId) return;
      if (
        event.type === "end" ||
        event.type === "error" ||
        event.type === "cancelled" ||
        event.type === "interrupted"
      ) {
        chrome.tabs.sendMessage(
          tabId,
          {
            action: "tts-bg-event",
            eventType: event.type,
            sessionId
          },
          () => {
            // Ignore lastError if tab closed
            void (chrome.runtime && chrome.runtime.lastError);
          }
        );
      }
    }
  });
  return true;
}

if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.onInstalled) {
  chrome.runtime.onInstalled.addListener(() => {
    syncCloudRulesNow();
    if (!chrome.contextMenus) return;
    chrome.contextMenus.removeAll(() => {
      MENU_ITEMS.forEach(item => {
        chrome.contextMenus.create(item);
      });
    });
  });
}

if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.onStartup) {
  chrome.runtime.onStartup.addListener(() => {
    syncCloudRulesNow();
  });
}

if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.onMessage) {
  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (!msg || typeof msg !== "object") return false;

    // 1. Popup button dispatch -> finds active tab, auto-injects if needed, and runs action
    if (msg.action === "popup-dispatch" && msg.targetAction) {
      chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
        const activeTab = tabs && tabs[0];
        if (!activeTab || !activeTab.id) {
          if (typeof sendResponse === "function") sendResponse({ ok: false, reason: "no-active-tab" });
          return;
        }
        sendToActiveTab(activeTab.id, { action: msg.targetAction }, res => {
          if (typeof sendResponse === "function") sendResponse(res);
        });
      });
      return true;
    }

    // 2. Native Chrome TTS engine commands from content script
    if (msg.action === "tts-speak") {
      const tabId = sender && sender.tab && sender.tab.id;
      const ok = speakViaChromeTts(tabId, msg.text, msg.rate || 1.0, msg.sessionId);
      if (typeof sendResponse === "function") sendResponse({ ok });
      return false;
    }
    if (msg.action === "tts-pause") {
      if (chrome.tts && typeof chrome.tts.pause === "function") {
        try { chrome.tts.pause(); } catch (_e) {}
      }
      if (typeof sendResponse === "function") sendResponse({ ok: true });
      return false;
    }
    if (msg.action === "tts-resume") {
      if (chrome.tts && typeof chrome.tts.resume === "function") {
        try { chrome.tts.resume(); } catch (_e) {}
      }
      if (typeof sendResponse === "function") sendResponse({ ok: true });
      return false;
    }
    if (msg.action === "tts-stop") {
      if (chrome.tts && typeof chrome.tts.stop === "function") {
        try { chrome.tts.stop(); } catch (_e) {}
      }
      if (typeof sendResponse === "function") sendResponse({ ok: true });
      return false;
    }

    // 3. Direct Gemini 2.5 Flash Movie Rewrite from MacBook over HTTPS
    if (msg.action === "gemini-movie-rewrite") {
      rewriteSentencesWithGeminiFlash(msg.sentences, msg.apiKey).then(res => {
        if (typeof sendResponse === "function") sendResponse(res);
      });
      return true;
    }

    // 4. OTA Cloud Rule Sync
    if (msg.action === "sync-cloud-rules") {
      syncCloudRulesNow().then(res => {
        if (typeof sendResponse === "function") sendResponse(res);
      });
      return true;
    }

    return false;
  });
}

if (typeof chrome !== "undefined" && chrome.contextMenus && chrome.contextMenus.onClicked) {
  chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (!tab || !tab.id) return;
    if (info.menuItemId === "mac-speak-select-to-end") {
      sendToActiveTab(tab.id, { action: "select-from-here" });
    } else if (info.menuItemId === "mac-speak-select-full") {
      sendToActiveTab(tab.id, { action: "select-full-article" });
    } else if (info.menuItemId === "mac-speak-read-aloud") {
      sendToActiveTab(tab.id, { action: "speak-from-here" });
    } else if (info.menuItemId === "mac-speak-movie-mode") {
      sendToActiveTab(tab.id, { action: "toggle-movie-mode" });
    }
  });
}

if (typeof chrome !== "undefined" && chrome.commands && chrome.commands.onCommand) {
  chrome.commands.onCommand.addListener(command => {
    chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
      const activeTab = tabs && tabs[0];
      if (!activeTab || !activeTab.id) return;
      if (command === "select-from-here") {
        sendToActiveTab(activeTab.id, { action: "select-from-here" });
      } else if (command === "speak-from-here") {
        sendToActiveTab(activeTab.id, { action: "speak-from-here" });
      } else if (command === "select-full-article") {
        sendToActiveTab(activeTab.id, { action: "select-full-article" });
      } else if (command === "toggle-movie-mode") {
        sendToActiveTab(activeTab.id, { action: "toggle-movie-mode" });
      }
    });
  });
}

// Periodic background cloud sync every 30 minutes
setInterval(() => {
  syncCloudRulesNow();
}, 30 * 60 * 1000);
