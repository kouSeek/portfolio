#!/usr/bin/env python3
"""Unit tests for MacBook Smart Read Aloud & Auto-Select Chrome Extension."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import unittest

EXT_ROOT = Path(__file__).resolve().parent.parent


def find_node_binary() -> str:
    """Locate a working Node.js binary on PATH or standard developer directories."""
    from_path = shutil.which("node") or shutil.which("nodejs")
    if from_path:
        return from_path
    home = Path.home()
    candidates = [
        *sorted(home.glob(".vscode/cli/serve-web/*/node")),
        *sorted(home.glob(".jetski-server/bin/*/node")),
        *sorted(home.glob(".nvm/versions/node/*/bin/node")),
        Path("/usr/local/bin/node"),
        Path("/usr/bin/node"),
    ]
    for cand in candidates:
        if cand.is_file():
            return str(cand)
    raise FileNotFoundError("Could not locate node binary")


class TestMacSpeakChromeExtension(unittest.TestCase):
    """Verify manifest V3 structure, article detection, DOM range selection, and keyboard shortcuts."""

    def test_manifest_and_files_exist(self) -> None:
        manifest_path = EXT_ROOT / "manifest.json"
        self.assertTrue(manifest_path.is_file())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["manifest_version"], 3)
        self.assertIn("commands", manifest)
        self.assertIn("select-from-here", manifest["commands"])
        self.assertEqual(
            manifest["commands"]["select-from-here"]["suggested_key"]["mac"],
            "Alt+Space",
        )
        self.assertIn("speak-from-here", manifest["commands"])
        self.assertIn("select-full-article", manifest["commands"])
        self.assertIn("toggle-movie-mode", manifest["commands"])

        for rel in (
            "src/article-detector.js",
            "src/dead-noun-converter.js",
            "src/content.js",
            "src/content.css",
            "src/background.js",
            "src/popup.html",
            "src/popup.js",
            "macos/install_mac_onekey_speech.sh",
        ):
            self.assertTrue((EXT_ROOT / rel).is_file(), f"Missing {rel}")

    def test_dead_noun_converter_and_movie_mode_in_node_vm(self) -> None:
        js_test = r"""
const converter = require("./src/dead-noun-converter.js");

const q1 = converter.convertTextToActionMovie(
  "Supervision of a rollout includes the following:"
);
const opt1 = converter.convertTextToActionMovie(
  "Must detect material changes in the behavior of the service, including performance, resource consumption, and error rates."
);
const opt2 = converter.convertTextToActionMovie(
  "Must include oversight of a service's critical metrics and those of its most important clients/customers."
);
const opt3 = converter.convertTextToActionMovie("Must be a manual effort.");
const opt4 = converter.convertTextToActionMovie(
  "May be accomplished by some combination of manual and automation effort."
);
const gen = converter.convertTextToActionMovie(
  "The implementation of the pipeline requires verification of credentials prior to the execution of the job."
);

process.stdout.write(JSON.stringify({
  q1: q1.text,
  opt1: opt1.text,
  opt2: opt2.text,
  opt3: opt3.text,
  opt4: opt4.text,
  gen: gen.text,
  genChanged: gen.changed
}));
"""
        proc = subprocess.run(
            [find_node_binary(), "-e", js_test],
            cwd=str(EXT_ROOT),
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        out = json.loads(proc.stdout)
        self.assertEqual(out["q1"], "When you watch new code go live, you do these things:")
        self.assertIn("You must spot any big changes in how the server behaves", out["opt1"])
        self.assertIn("You must watch your service's main health graphs", out["opt2"])
        self.assertEqual(out["opt3"], "A human must do all the watching by hand.")
        self.assertIn("You can do this using a mix of human checks and automatic bots/alarms", out["opt4"])
        self.assertTrue(out["genChanged"])
        self.assertIn("Building and turning on the pipeline", out["gen"])
        self.assertIn("before running the job", out["gen"])

    def test_article_detector_and_keyboard_controller_in_node_vm(self) -> None:
        js_test = r"""
const detector = require("./src/article-detector.js");
const controllerMod = require("./src/content.js");

function makeBlock(tag, text, topPx, heightPx = 40, insideNoise = false) {
  return {
    nodeType: 1,
    tagName: tag.toUpperCase(),
    textContent: text,
    hidden: false,
    children: [],
    classList: {
      _set: new Set(),
      add(c) { this._set.add(c); },
      remove(c) { this._set.delete(c); },
      contains(c) { return this._set.has(c); }
    },
    getAttribute() { return null; },
    getBoundingClientRect() {
      return { top: topPx, bottom: topPx + heightPx, left: 0, right: 600, width: 600, height: heightPx };
    },
    closest(sel) {
      if (sel.includes("aside")) {
        return insideNoise ? { tagName: "NAV" } : null;
      }
      return this;
    },
    contains(other) { return other === this; },
    querySelectorAll() { return []; }
  };
}

const navLink = makeBlock("p", "Home About Contact Subscribe Login Sidebar Link", 10, 30, true);
const h1 = makeBlock("h1", "Deep Brain Architecture and Cognitive Flow", -120, 45, false);
const p1 = makeBlock("p", "First intro paragraph that was already scrolled above the top of the screen.", -40, 40, false);
const p2 = makeBlock("p", "Second paragraph currently visible right at the top of the user screen viewport.", 90, 50, false);
const p3 = makeBlock("p", "Third paragraph hovering under the user cursor right now in the middle of the page.", 220, 55, false);
const h2 = makeBlock("h2", "Section Two: Next Major Heading", 320, 40, false);
const p4 = makeBlock("p", "Fourth paragraph at the very bottom of the long article body.", 980, 60, false);

const allBlocks = [navLink, h1, p1, p2, p3, h2, p4];
const articleEl = {
  nodeType: 1,
  tagName: "ARTICLE",
  textContent: allBlocks.slice(1).map(b => b.textContent).join("\n\n"),
  hidden: false,
  getAttribute() { return null; },
  getBoundingClientRect() { return { top: -120, bottom: 1040, width: 700, height: 1160 }; },
  querySelectorAll(sel) {
    if (sel === "a") return [];
    return allBlocks;
  }
};

let lastRange = null;
const mockSelection = {
  isCollapsed: true,
  anchorNode: null,
  removeAllRanges() { lastRange = null; },
  addRange(r) { lastRange = r; },
  toString() {
    if (!lastRange) return "";
    const sIdx = allBlocks.indexOf(lastRange.startNode);
    const eIdx = allBlocks.indexOf(lastRange.endNode);
    return allBlocks.slice(sIdx, eIdx + 1).map(b => b.textContent).join("\n\n");
  }
};

const spokenUtterances = [];
let speechPaused = false;
let speechCanceled = false;

const mockWin = {
  innerHeight: 800,
  getComputedStyle() { return { display: "block", visibility: "visible", opacity: "1" }; },
  getSelection() { return mockSelection; },
  scrollBy() {},
  SpeechSynthesisUtterance: function(text) {
    this.text = text;
    this.rate = 1.0;
  },
  speechSynthesis: {
    getVoices() { return [{ name: "Daniel (Enhanced)", lang: "en-GB", default: true }]; },
    speak(u) { spokenUtterances.push({ text: u.text, rate: u.rate }); },
    pause() { speechPaused = true; },
    resume() { speechPaused = false; },
    cancel() { speechCanceled = true; }
  }
};

const listeners = {};
const mockDoc = {
  defaultView: mockWin,
  body: {
    appendChild() {}
  },
  getElementById() { return null; },
  createElement() {
    return { id: "", innerHTML: "", classList: { add() {}, remove() {} } };
  },
  createRange() {
    return {
      startNode: null,
      endNode: null,
      setStartBefore(n) { this.startNode = n; },
      setEndAfter(n) { this.endNode = n; }
    };
  },
  querySelectorAll(sel) {
    if (sel === "article") return [articleEl];
    return [];
  },
  addEventListener(type, fn) {
    listeners[type] = fn;
  }
};

// 1. Test Viewport-Top Auto-Detection (no hover -> starts from p2 which is first visible in viewport, skipping scrolled-past h1 & p1 and navLink)
const viewportRes = detector.selectArticleContent(mockDoc, { mode: "to-end", doc: mockDoc, win: mockWin });

// 2. Test Hovered Paragraph Auto-Select (Option+Space while hovering p3 -> selects from p3 through p4)
const ctrl = controllerMod.createController({ document: mockDoc, window: mockWin });
ctrl.init();
ctrl.handleMouseOver({ target: p3 });
let preventedKey = false;
ctrl.handleKeyDown({
  altKey: true,
  metaKey: false,
  ctrlKey: false,
  code: "Space",
  key: "\u00a0",
  target: { tagName: "DIV" },
  preventDefault() { preventedKey = true; }
});
const hoveredSelectionText = mockSelection.toString();

// 3. Test Option+R (Built-in Read Aloud from hovered p3) + Space (Pause/Resume) + Click p4 to skip + Esc (Stop)
ctrl.handleKeyDown({
  altKey: true,
  metaKey: false,
  ctrlKey: false,
  code: "KeyR",
  key: "r",
  target: { tagName: "DIV" },
  preventDefault() {}
});
const firstSpokenText = spokenUtterances[spokenUtterances.length - 1]?.text || "";
const firstSpokenRate = spokenUtterances[spokenUtterances.length - 1]?.rate || 0;

// Press Space to pause
ctrl.handleKeyDown({
  altKey: false,
  metaKey: false,
  ctrlKey: false,
  key: " ",
  target: { tagName: "DIV" },
  preventDefault() {}
});
const pausedAfterSpace = ctrl.state.paused && speechPaused;

// Press Space again to resume
ctrl.handleKeyDown({
  altKey: false,
  metaKey: false,
  ctrlKey: false,
  key: " ",
  target: { tagName: "DIV" },
  preventDefault() {}
});
const resumedAfterSecondSpace = !ctrl.state.paused && !speechPaused;

// Click p4 while speaking -> skips directly to p4
ctrl.handleClick({
  altKey: false,
  metaKey: false,
  ctrlKey: false,
  target: p4,
  preventDefault() {},
  stopPropagation() {}
});
const spokenAfterClickSkip = spokenUtterances[spokenUtterances.length - 1]?.text || "";

// Press Escape to stop
ctrl.handleKeyDown({
  altKey: false,
  metaKey: false,
  ctrlKey: false,
  key: "Escape",
  target: { tagName: "DIV" },
  preventDefault() {}
});
const stoppedAfterEsc = !ctrl.state.speaking;

process.stdout.write(JSON.stringify({
  viewportTotalBlocks: viewportRes.totalBlocks,
  viewportStartIndex: viewportRes.startIndex,
  viewportFirstBlockText: viewportRes.selectedBlocks[0].textContent,
  viewportLastBlockText: viewportRes.selectedBlocks[viewportRes.selectedBlocks.length - 1].textContent,
  preventedKey,
  hoveredSelectionText,
  firstSpokenText,
  firstSpokenRate,
  pausedAfterSpace,
  resumedAfterSecondSpace,
  spokenAfterClickSkip,
  stoppedAfterEsc
}));
"""
        proc = subprocess.run(
            [find_node_binary(), "-e", js_test],
            cwd=str(EXT_ROOT),
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        out = json.loads(proc.stdout)

        # Filtered out navLink (only 6 real blocks: h1, p1, p2, p3, h2, p4)
        self.assertEqual(out["viewportTotalBlocks"], 6)
        # Viewport-aware start: skips h1 (-120px) and p1 (-40px) and starts right at p2 (+90px)!
        self.assertEqual(out["viewportStartIndex"], 2)
        self.assertIn("Second paragraph currently visible right at the top", out["viewportFirstBlockText"])
        self.assertIn("Fourth paragraph at the very bottom", out["viewportLastBlockText"])

        # Hovered paragraph Option+S: selects from p3 through p4 (excludes p2)
        self.assertTrue(out["preventedKey"])
        self.assertTrue(out["hoveredSelectionText"].startswith("Third paragraph hovering under the user cursor"))
        self.assertTrue(out["hoveredSelectionText"].endswith("Fourth paragraph at the very bottom of the long article body."))
        self.assertNotIn("Second paragraph", out["hoveredSelectionText"])

        # Option+R speaks from p3 at 1.0x rate, Space pauses/resumes, Click skips to p4, Esc stops
        self.assertEqual(out["firstSpokenText"], "Third paragraph hovering under the user cursor right now in the middle of the page.")
        self.assertEqual(out["firstSpokenRate"], 1.0)
        self.assertTrue(out["pausedAfterSpace"])
        self.assertTrue(out["resumedAfterSecondSpace"])
        self.assertEqual(out["spokenAfterClickSkip"], "Fourth paragraph at the very bottom of the long article body.")
        self.assertTrue(out["stoppedAfterEsc"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
