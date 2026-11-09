# 🔊🎬 MacBook Smart Read Aloud & Movie Mode (Dead-Noun Converter)

**Cloud Repository:** [`https://github.com/kouSeek/portfolio/tree/mac-speak-chrome-ext`](https://github.com/kouSeek/portfolio/tree/mac-speak-chrome-ext)  
**Manifest Version:** Chrome Manifest V3 (`v1.2.0`)  
**Architecture:** Zero-Drag Smart Article Selection + 1.0x MacBook Read Aloud + **3D Visual-Action Movie Mode (`Dead-Noun De-Nominalizer`)** + **Over-The-Air (`OTA`) Cloud Auto-Sync**

---

## 🌟 Overview & Purpose

Built specifically for **Visual-Spatial / 3D Movie-Simulator thinkers** and MacBook readers who want effortless, zero-cortisol reading on any webpage, engineering doc, or compliance quiz:

1. **🎬 Movie Mode (`Option + M` / `⌥ M` — Dead-Noun to Visual-Action Converter):**
   - Corporate and bureaucratic writing replaces living people and action verbs with frozen abstract nouns (**nominalizations** like *"Supervision of a rollout includes oversight of..."*). While verbal/word-token readers process abstract nouns like algebra, a **3D Visual-Movie brain** stalls when there is no actor or moving verb to render on its mental screen.
   - Pressing **`Option + M`** (`Alt+M`) on any webpage, Google Doc, or training quiz rewrites **100+ corporate dead-noun constructions in-place (`<2ms`)** into vivid **"Who-Does-What" visual action verbs** while preserving all checkboxes, links, and inputs. Press **`Option + M`** again anytime to restore the original text.
2. **📖 Zero-Drag Smart Selection (`Option + Space` / `⌥ Space` or `Option + Click`):**
   - Eliminates the tedious task of manually clicking and dragging from the top to the bottom of long articles before triggering macOS Accessibility **Speak Selection** (`Option + Esc` or `Right-Click → Speech → Start Speaking`).
   - Automatically detects the main article body (ignoring navbars, sidebars, ads, and footers) and highlights a native DOM selection from your **hovered paragraph** (or the **first visible paragraph at the top of your viewport**) all the way to the end of the article.
   - Pressing **`Option + Space`** a second time within `2.5s` cycles through **From Here to End** $\rightarrow$ **Entire Article** $\rightarrow$ **Current Section Only**.
3. **🔊 1-Key Read Aloud (`Option + R` / `⌥ R` or `Shift + Option + Click`):**
   - Auto-selects from the hovered/visible paragraph to the end of the article and immediately reads it aloud at a natural **`1.0x` comprehension pace** using macOS native voices (`Siri` / `Ava` / `Daniel`).
   - **Automatic Movie-Mode Speech:** Even if you didn't press `Option + M` first, `Option + R` automatically passes every paragraph through the **Dead-Noun Converter** before speaking so your ears always hear living visual actions!
   - **Interactive Controls While Reading:** Press **`Space`** to Play/Pause, **click any paragraph** to jump directly to it, or press **`Esc`** to stop.
4. **☁️ Over-The-Air (`OTA`) Cloud Auto-Sync (`cloud-rules.json` + LaunchAgent):**
   - The background service worker (`src/background.js`) automatically fetches the latest `cloud-rules.json` from [`https://raw.githubusercontent.com/kouSeek/portfolio/mac-speak-chrome-ext/cloud-rules.json`](https://raw.githubusercontent.com/kouSeek/portfolio/mac-speak-chrome-ext/cloud-rules.json) on browser startup, every 30 minutes, and when clicking **`☁️ Sync Latest Cloud Rules`** in the popup.

---

## ⌨️ Keyboard Shortcuts & Controls

| Shortcut / Action | Function |
| :--- | :--- |
| **`Option + M`** (`⌥ M`) | **Toggle 🎬 Movie Mode:** Flips corporate "Dead Nouns" into living "Who-Does-What" visual action verbs in-place across the page (press again to restore original). |
| **`Option + Space`** (`⌥ Space`) or **`Option + Click`** | **Smart Auto-Select to End:** Highlights from the hovered/top-visible paragraph to the end of the article for macOS `Option + Esc` Speak Selection. |
| **`Option + R`** (`⌥ R`) or **`Shift + Option + Click`** | **Smart Read Aloud from Here (`1.0x`):** Reads from the hovered/visible paragraph to the end of the article with automatic Dead-Noun conversion. |
| **`Option + A`** (`⌥ A`) | **Select Entire Article:** Selects the entire clean article from start to finish. |
| **`Space`** *(while reading)* | **Play / Pause** active Read Aloud. |
| **Click any paragraph** *(while reading)* | **Skip / Jump** directly to that paragraph. |
| **`Esc`** *(while reading)* | **Stop** Read Aloud and clear paragraph highlight. |

---

## 🎬 Example Dead-Noun $\rightarrow$ Visual Action Movie Conversions

| ❌ Original Corporate "Dead Nouns" | 🎬 **`Option + M` (`Movie Mode`)** Visual Action Output |
| :--- | :--- |
| *"Supervision of a rollout includes the following:"* | ***"When you watch new code go live, you do these things:"*** |
| *"Must detect material changes in the behavior of the service, including performance, resource consumption, and error rates."* | ***"You must spot any big changes in how the server behaves—like slowing down, eating too much CPU/RAM, or throwing errors."*** |
| *"Must include oversight of a service's critical metrics and those of its most important clients/customers."* | ***"You must watch your service's main health graphs and check that your biggest customers aren't breaking."*** |
| *"Must be a manual effort."* | ***"A human must do all the watching by hand."*** |
| *"May be accomplished by some combination of manual and automation effort."* | ***"You can do this using a mix of human checks and automatic bots/alarms."*** |
| *"The implementation of the pipeline requires verification of credentials prior to the execution of the job."* | ***"Building and turning on the pipeline requires checking credentials before running the job."*** |

---

## ☁️ Installation & Cloud Auto-Sync Options

## 📦 One-Shot Installation & Update on MacBook (Zero Background Jobs)

Run this single command in your MacBook Terminal whenever you want to install or update `~/Downloads/mac-speak-chrome-ext`:
```bash
curl -fsSL https://raw.githubusercontent.com/kouSeek/portfolio/mac-speak-chrome-ext/macos/install_from_cloud.sh | bash
```
1. Downloads and extracts the latest extension directly into `~/Downloads/mac-speak-chrome-ext` (no background daemon, no `launchd` runner, and no auto-git sync).
2. In `chrome://extensions`, enable **Developer mode** (top-right) and click **Load unpacked** -> select `~/Downloads/mac-speak-chrome-ext` (or click **🔄 Reload** if already loaded).

### Option 2: Publishing to Google's Internal Chrome Web Store (`@google.com` Domain)
Google provides an internal Chrome Web Store for Googlers (`https://chrome.google.com/webstore/a/google.com/` — see `go/publish-extensions-as-a-googler` and `go/cws-vebs`). To publish this extension to the internal `@google.com` store for 1-click cloud installation across all your corp machines:
1. Open the **[Chrome Web Store Developer Console](https://chrome.google.com/webstore/devconsole)**.
2. Click **+ New item** (top-right) and upload [`mac-speak-chrome-ext.zip`](mac-speak-chrome-ext.zip).
3. Copy-paste the store listing fields from [`CHROMEWEBSTORE.md`](CHROMEWEBSTORE.md).
4. Under the **Distribution** tab, select:
   - **Visibility:** `Private — All users in my domain (google.com)` *(or `Only trusted testers` if restricting to yourself)*.
5. Click **Submit for review**. Because this extension only requests narrow, low-risk permissions (`activeTab`, `contextMenus`, `scripting`, `storage`), internal domain reviews typically complete within `<24 hours`, after which Chrome auto-updates it across all your signed-in browsers!

---

## 🧪 Running the Test Suite
```bash
python3 tests/test_extension.py
```
