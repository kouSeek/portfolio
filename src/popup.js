"use strict";

const statusEl = document.getElementById("popup-status");
const apiKeyInput = document.getElementById("gemini-api-key-input");

function setStatus(text) {
  if (statusEl) statusEl.textContent = text;
}

// Load saved Gemini API key from chrome.storage.local
if (typeof chrome !== "undefined" && chrome.storage && chrome.storage.local && apiKeyInput) {
  chrome.storage.local.get(["geminiApiKey"], items => {
    if (items && items.geminiApiKey) {
      apiKeyInput.value = items.geminiApiKey;
      setStatus("AI Ready ✨");
    }
  });
}

/**
 * Dispatches the action through `background.js` (`popup-dispatch`) so that
 * even if the current tab was already open before the extension loaded/updated,
 * `background.js` automatically injects the content scripts on the fly!
 */
function sendActionToCurrentTab(targetAction) {
  setStatus("Running...");
  chrome.runtime.sendMessage({ action: "popup-dispatch", targetAction }, res => {
    if (chrome.runtime && chrome.runtime.lastError) {
      setStatus("Reload tab");
      return;
    }
    if (res && res.ok === false && res.reason) {
      setStatus("Open a webpage");
      return;
    }
    setStatus("Done ✓");
    setTimeout(() => {
      window.close();
    }, 180);
  });
}

document.getElementById("btn-select-from-here")?.addEventListener("click", () => {
  sendActionToCurrentTab("select-from-here");
});

document.getElementById("btn-select-full")?.addEventListener("click", () => {
  sendActionToCurrentTab("select-full-article");
});

document.getElementById("btn-speak-from-here")?.addEventListener("click", () => {
  sendActionToCurrentTab("speak-from-here");
});

document.getElementById("btn-movie-mode")?.addEventListener("click", () => {
  sendActionToCurrentTab("toggle-movie-mode");
});

document.getElementById("btn-sync-cloud")?.addEventListener("click", () => {
  const label = document.getElementById("sync-cloud-label");
  if (label) label.textContent = "⏳ Syncing from Cloud...";
  chrome.runtime.sendMessage({ action: "sync-cloud-rules" }, res => {
    if (label) {
      label.textContent = (res && res.ok)
        ? `✅ Synced Cloud v${res.version}`
        : "✓ Using Built-in Rules";
    }
  });
});

document.getElementById("btn-save-api-key")?.addEventListener("click", () => {
  const val = String((apiKeyInput && apiKeyInput.value) || "").trim();
  if (typeof chrome !== "undefined" && chrome.storage && chrome.storage.local) {
    chrome.storage.local.set({ geminiApiKey: val }, () => {
      setStatus(val ? "Key Saved ✓" : "Key Cleared");
    });
  }
});
