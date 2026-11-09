# Chrome Web Store (Internal `@google.com`) Listing & Metadata

Use the ready-to-paste fields below when uploading `mac-speak-chrome-ext.zip` to the **[Chrome Web Store Developer Console](https://chrome.google.com/webstore/devconsole)** for internal `@google.com` distribution (`https://chrome.google.com/webstore/a/google.com/`).

---

## 1. Store Listing Fields

- **Title:** `MacBook Smart Read Aloud & Movie Mode (Dead-Noun Converter)`
- **Summary (132 chars max):**
  `Zero-drag article selection (⌥Space), 1.0x Read Aloud (⌥R), and Movie Mode (⌥M) converting corporate dead nouns into visual actions.`
- **Category:** `Productivity` / `Workflow & Planning`
- **Language:** `English`

### Detailed Description (Copy-Paste)
```text
MacBook Smart Read Aloud & Movie Mode (Dead-Noun Converter) is a neuro-inclusive reading and comprehension assistant designed for visual-spatial thinkers and MacBook readers.

KEY FEATURES:
1. 🎬 Movie Mode (Option + M / Alt+M):
   Converts lifeless corporate and bureaucratic "dead nouns" (nominalizations like "Supervision of a rollout includes oversight of...", "implementation of", "utilization of", "mitigation of") in-place into vivid "Who-Does-What" visual action verbs ("When you watch new code go live...") while preserving all checkboxes, links, and interactive controls. Press Option + M again to restore the original text.

2. 📖 Zero-Drag Smart Article Selection (Option + Space or Option + Click):
   Automatically detects the main article container (filtering out navigation bars, sidebars, and footers) and selects from your hovered paragraph—or the first visible paragraph at the top of your screen—all the way to the end of the article so macOS Accessibility "Speak Selection" (Option + Esc) works without manual dragging.

3. 🔊 1-Key Read Aloud (Option + R or Shift + Option + Click):
   Auto-selects and immediately reads aloud from the hovered/visible paragraph to the end of the article at a natural 1.0x comprehension pace using macOS native voices, automatically converting dead corporate nouns into living action verbs before speaking. Press Space to Play/Pause, click any paragraph to skip directly to it, or press Esc to stop.

4. ☁️ Over-The-Air (OTA) Cloud Rule Sync:
   Automatically syncs the latest Dead-Noun -> Action-Movie dictionary from the cloud repository into chrome.storage.local.
```

---

## 2. Privacy Tab — Permission Justifications (Copy-Paste)

- **Single Purpose Description:**
  `Helps users read web articles, documentation, and quizzes by auto-selecting clean article text from the hovered paragraph to the end of the page, reading text aloud at 1.0x pace, and converting abstract nominalizations ("dead nouns") into active verbs in-place.`
- **`activeTab` Justification:**
  `Required to trigger smart paragraph selection, Read Aloud, or Movie Mode when the user clicks the extension popup or invokes a keyboard shortcut on the active tab.`
- **`contextMenus` Justification:**
  `Provides Right-Click context menu shortcuts ("Select from Here to End", "Read Aloud from Here", and "Movie Mode: Flip Dead Nouns into Visual Action Verbs").`
- **`scripting` Justification:**
  `Injects the article detector and dead-noun converter into already-open tabs when invoked via the context menu or keyboard shortcut.`
- **`storage` Justification:**
  `Caches the latest cloud-synced Dead-Noun -> Action-Verb dictionary locally in chrome.storage.local.`
- **Remote Code:**
  `No, I am not using Remote code.` *(Only declarative JSON dictionary rules are fetched via `cloud-rules.json`; all executable JS is bundled inside the extension package.)*

---

## 3. Distribution Tab

- **Visibility:** `Private` $\rightarrow$ **`All users in my domain (google.com)`** *(or `Only trusted testers`)*
