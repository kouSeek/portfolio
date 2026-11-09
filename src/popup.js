"use strict";

function sendActionToCurrentTab(action) {
  chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
    const tab = tabs && tabs[0];
    if (!tab || !tab.id) return;
    chrome.tabs.sendMessage(tab.id, { action }, () => {
      window.close();
    });
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
