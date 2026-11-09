/* ==========================================================================
   MacBook Smart Read Aloud & Auto-Select — Background Service Worker
   (`src/background.js`)
   - Wires Chrome keyboard commands (`Alt+Space`, `Alt+R`, `Alt+A`, `Alt+M`)
     and Right-Click Context Menu items to the active tab's content script.
   - Automatically syncs the latest `cloud-rules.json` Dead-Noun -> Action-Movie
     dictionary from GitHub Cloud (`kouSeek/portfolio@mac-speak-chrome-ext`)
     into `chrome.storage.local` on startup, every 30 minutes, and on demand.
   ========================================================================== */
"use strict";

const CLOUD_RULES_URLS = [
  "https://raw.githubusercontent.com/kouSeek/portfolio/mac-speak-chrome-ext/cloud-rules.json",
  "http://koushikchak.c.googlers.com:9500/api/mac-speak/cloud-rules.json"
];

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

function sendToActiveTab(tabId, payload) {
  if (!tabId || !chrome.tabs || typeof chrome.tabs.sendMessage !== "function") return;
  chrome.tabs.sendMessage(tabId, payload, () => {
    if (chrome.runtime && chrome.runtime.lastError) {
      // If content script wasn't injected yet (e.g., tab was open before extension install), inject on the fly
      if (chrome.scripting && typeof chrome.scripting.executeScript === "function") {
        chrome.scripting.executeScript(
          {
            target: { tabId },
            files: ["src/article-detector.js", "src/dead-noun-converter.js", "src/content.js"]
          },
          () => {
            if (!chrome.runtime.lastError) {
              chrome.tabs.sendMessage(tabId, payload);
            }
          }
        );
      }
    }
  });
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
  chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
    if (msg && msg.action === "sync-cloud-rules") {
      syncCloudRulesNow().then(res => {
        if (typeof sendResponse === "function") sendResponse(res);
      });
      return true;
    }
    return false;
  });
}

// Periodic background cloud sync every 30 minutes
setInterval(() => {
  syncCloudRulesNow();
}, 30 * 60 * 1000);

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
