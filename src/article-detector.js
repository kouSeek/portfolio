/* ==========================================================================
   MacBook Smart Read Aloud & Auto-Select — Article & Viewport Detector
   (`src/article-detector.js`)
   Finds the clean main article container on any webpage, filters out navbars,
   sidebars, ads, and code-syntax dumps, and builds a native DOM Selection
   Range (`window.getSelection()`) from the hovered or top-of-screen paragraph
   all the way to the end of the article for macOS "Speak Selection".
   ========================================================================== */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  if (root) {
    root.MacSpeakArticleDetector = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : window, function () {
  "use strict";

  const PRIMARY_ARTICLE_SELECTORS = [
    "article",
    "[role='main'] article",
    "main article",
    "#mw-content-text .mw-parser-output",
    "#mw-content-text",
    ".markdown-body",
    ".post-content",
    ".entry-content",
    ".article-body",
    ".article-content",
    ".story-body",
    ".ltx_page_main",
    ".g3doc-content",
    "[role='main']",
    "main"
  ];

  const NOISE_ANCESTOR_SELECTOR = [
    "nav",
    "header:not(article header)",
    "footer",
    "aside",
    "[role='navigation']",
    "[role='banner']",
    "[role='contentinfo']",
    "[aria-hidden='true']",
    ".sidebar",
    ".nav",
    ".navbar",
    ".menu",
    ".toc",
    "#toc",
    ".table-of-contents",
    ".ad",
    ".ads",
    ".advertisement",
    ".promo",
    ".related-posts",
    ".recommended",
    ".comments",
    "#comments",
    ".cookie-banner",
    ".modal",
    ".popup",
    "script",
    "style",
    "noscript",
    "svg"
  ].join(", ");

  const READABLE_BLOCK_SELECTOR = "h1, h2, h3, h4, h5, h6, p, li, blockquote, dd, figcaption, label, td";

  function normalizeText(raw) {
    return String(raw || "").replace(/\s+/g, " ").trim();
  }

  function isElementVisible(el, win) {
    if (!el || el.nodeType !== 1) return false;
    if (el.hidden || el.getAttribute("aria-hidden") === "true") return false;
    const w = win || (el.ownerDocument && el.ownerDocument.defaultView) || (typeof window !== "undefined" ? window : null);
    if (w && typeof w.getComputedStyle === "function") {
      try {
        const style = w.getComputedStyle(el);
        if (style && (style.display === "none" || style.visibility === "hidden" || parseFloat(style.opacity) === 0)) {
          return false;
        }
      } catch (_e) {}
    }
    if (typeof el.getBoundingClientRect === "function") {
      const rect = el.getBoundingClientRect();
      if (rect && rect.width === 0 && rect.height === 0 && !el.children?.length) {
        return false;
      }
    }
    return true;
  }

  function isInsideNoiseContainer(el, articleRoot) {
    if (!el || typeof el.closest !== "function") return false;
    const hit = el.closest(NOISE_ANCESTOR_SELECTOR);
    if (!hit) return false;
    if (articleRoot && hit === articleRoot) return false;
    return true;
  }

  function countLinkDensity(el) {
    if (!el || typeof el.querySelectorAll !== "function") return 0;
    const totalLen = normalizeText(el.textContent).length;
    if (totalLen === 0) return 1;
    const links = el.querySelectorAll("a");
    let linkChars = 0;
    for (let i = 0; i < links.length; i++) {
      linkChars += normalizeText(links[i].textContent).length;
    }
    return linkChars / totalLen;
  }

  /**
   * Finds the best main article container in `doc` using semantic selectors
   * first, then falling back to a Readability-style paragraph text-density score.
   */
  function findMainArticleContainer(doc) {
    if (!doc || !doc.body) return null;
    const win = doc.defaultView || (typeof window !== "undefined" ? window : null);

    // 1. Check semantic article/main selectors with substantial prose
    let bestSemantic = null;
    let bestSemanticScore = 0;
    for (let i = 0; i < PRIMARY_ARTICLE_SELECTORS.length; i++) {
      const sel = PRIMARY_ARTICLE_SELECTORS[i];
      let nodes = [];
      try {
        nodes = doc.querySelectorAll(sel);
      } catch (_e) {
        nodes = [];
      }
      for (let j = 0; j < nodes.length; j++) {
        const cand = nodes[j];
        if (!isElementVisible(cand, win)) continue;
        const textLen = normalizeText(cand.textContent).length;
        if (textLen < 160) continue;
        const linkDensity = countLinkDensity(cand);
        if (linkDensity > 0.65) continue;
        const pCount = cand.querySelectorAll ? cand.querySelectorAll("p, li, blockquote").length : 1;
        const priorityBonus = (PRIMARY_ARTICLE_SELECTORS.length - i) * 120;
        const score = textLen * (1 - linkDensity * 0.5) + pCount * 85 + priorityBonus;
        if (score > bestSemanticScore) {
          bestSemanticScore = score;
          bestSemantic = cand;
        }
      }
    }
    if (bestSemantic) return bestSemantic;

    // 2. Fallback: score parent containers of all <p> elements
    const paragraphs = doc.querySelectorAll ? doc.querySelectorAll("p") : [];
    const scoreMap = new Map();
    for (let i = 0; i < paragraphs.length; i++) {
      const p = paragraphs[i];
      if (!isElementVisible(p, win) || isInsideNoiseContainer(p, null)) continue;
      const t = normalizeText(p.textContent);
      if (t.length < 25) continue;
      const parent = p.parentElement;
      const grandParent = parent ? parent.parentElement : null;
      if (parent) {
        scoreMap.set(parent, (scoreMap.get(parent) || 0) + t.length + 60);
      }
      if (grandParent && grandParent !== doc.body) {
        scoreMap.set(grandParent, (scoreMap.get(grandParent) || 0) + (t.length + 60) * 0.6);
      }
    }

    let bestFallback = doc.body;
    let bestFallbackScore = 0;
    for (const [cand, rawScore] of scoreMap.entries()) {
      const ld = countLinkDensity(cand);
      const adj = rawScore * (1 - ld * 0.6);
      if (adj > bestFallbackScore) {
        bestFallbackScore = adj;
        bestFallback = cand;
      }
    }
    return bestFallback || doc.body;
  }

  /**
   * Collects ordered, leaf-level readable prose blocks (`h1..h6, p, li, blockquote`)
   * inside `rootContainer`, skipping nested duplicates and navigation chrome.
   */
  function collectReadableBlocks(doc, rootContainer) {
    const container = rootContainer || findMainArticleContainer(doc) || (doc && doc.body);
    if (!container || typeof container.querySelectorAll !== "function") return [];
    const win = (doc && doc.defaultView) || (typeof window !== "undefined" ? window : null);

    const rawNodes = Array.from(container.querySelectorAll(READABLE_BLOCK_SELECTOR));
    const filtered = [];

    for (let i = 0; i < rawNodes.length; i++) {
      const node = rawNodes[i];
      if (!isElementVisible(node, win)) continue;
      if (isInsideNoiseContainer(node, container)) continue;

      // Skip a block if it contains another readable block child (e.g., <li> wrapping <p> or <blockquote> wrapping <p>)
      const hasInnerBlock = rawNodes.some(other => other !== node && node.contains && node.contains(other));
      if (hasInnerBlock) continue;

      const text = normalizeText(node.textContent);
      const tag = (node.tagName || "").toUpperCase();
      const isHeading = /^H[1-6]$/.test(tag);

      if (!text) continue;
      if (!isHeading && text.length < 8) continue;
      if (!isHeading && countLinkDensity(node) > 0.78 && text.length < 140) continue;

      filtered.push(node);
    }

    // Fallback for web apps / quiz pages where prose sits inside leaf <div> elements
    if (filtered.length < 2 && typeof container.querySelectorAll === "function") {
      const divNodes = Array.from(container.querySelectorAll("div"));
      for (let i = 0; i < divNodes.length; i++) {
        const d = divNodes[i];
        if (!isElementVisible(d, win) || isInsideNoiseContainer(d, container)) continue;
        // Only pick leaf-like divs that don't wrap other block divs/p/li
        if (d.querySelector && d.querySelector("div, p, li, h1, h2, h3, h4, h5, h6, table")) continue;
        const t = normalizeText(d.textContent);
        if (t.length >= 15 && countLinkDensity(d) <= 0.75 && !filtered.includes(d)) {
          filtered.push(d);
        }
      }
    }

    if (filtered.length === 0 && normalizeText(container.textContent).length > 0) {
      return [container];
    }
    return filtered;
  }

  /**
   * Resolves which block in `blocks` corresponds to the user's current context:
   * 1. Explicit clicked or hovered DOM element (`hoveredEl`)
   * 2. Existing non-empty user selection start node (`window.getSelection()`)
   * 3. First block visible in the current viewport (`rect.bottom > topMargin && rect.top < viewportHeight`)
   * 4. Fallback to `blocks[0]`
   */
  function resolveStartingBlockIndex(blocks, opts = {}) {
    if (!Array.isArray(blocks) || blocks.length === 0) return -1;
    const { hoveredEl, doc, win, topHeaderMarginPx = 56 } = opts;

    // 1. Check hovered or clicked element
    if (hoveredEl) {
      for (let i = 0; i < blocks.length; i++) {
        if (blocks[i] === hoveredEl || (blocks[i].contains && blocks[i].contains(hoveredEl)) || (hoveredEl.contains && hoveredEl.contains(blocks[i]))) {
          return i;
        }
      }
      if (typeof hoveredEl.closest === "function") {
        const closestBlock = hoveredEl.closest(READABLE_BLOCK_SELECTOR);
        if (closestBlock) {
          const idx = blocks.indexOf(closestBlock);
          if (idx !== -1) return idx;
        }
      }
    }

    // 2. If the user highlighted a few words as an anchor, start from that block
    const w = win || (doc && doc.defaultView) || (typeof window !== "undefined" ? window : null);
    if (w && typeof w.getSelection === "function") {
      const sel = w.getSelection();
      if (sel && !sel.isCollapsed && sel.anchorNode) {
        const anchorEl = sel.anchorNode.nodeType === 1 ? sel.anchorNode : sel.anchorNode.parentElement;
        if (anchorEl) {
          for (let i = 0; i < blocks.length; i++) {
            if (blocks[i] === anchorEl || (blocks[i].contains && blocks[i].contains(anchorEl))) {
              // Only use selection anchor if it wasn't already a multi-block full-article selection
              const selTextLen = normalizeText(sel.toString()).length;
              const blockTextLen = normalizeText(blocks[i].textContent).length;
              if (selTextLen <= blockTextLen * 1.25) {
                return i;
              }
              break;
            }
          }
        }
      }
    }

    // 3. First readable block currently visible near the top of the screen
    const vh = (w && Number.isFinite(w.innerHeight) && w.innerHeight > 0) ? w.innerHeight : 800;
    for (let i = 0; i < blocks.length; i++) {
      const b = blocks[i];
      if (typeof b.getBoundingClientRect !== "function") continue;
      const r = b.getBoundingClientRect();
      if (!r) continue;
      if (r.bottom > topHeaderMarginPx && r.top < vh * 0.85) {
        return i;
      }
    }

    return 0;
  }

  /**
   * Resolves the end block index for a given selection scope:
   * - `"to-end"` (default): from `startIndex` through `blocks.length - 1`
   * - `"full-article"`: from `0` through `blocks.length - 1`
   * - `"section"`: from `startIndex` through the end of the current heading section
   * - `"paragraph"`: just `startIndex`
   */
  function resolveEndingBlockIndex(blocks, startIndex, mode = "to-end") {
    if (!Array.isArray(blocks) || blocks.length === 0) return -1;
    const safeStart = Math.max(0, Math.min(blocks.length - 1, Number(startIndex) || 0));
    if (mode === "paragraph") {
      return safeStart;
    }
    if (mode === "section") {
      const startTag = (blocks[safeStart].tagName || "").toUpperCase();
      const startLevel = /^H([1-6])$/.test(startTag) ? parseInt(startTag.slice(1), 10) : 6;
      for (let i = safeStart + 1; i < blocks.length; i++) {
        const tag = (blocks[i].tagName || "").toUpperCase();
        const m = tag.match(/^H([1-6])$/);
        if (m) {
          const lvl = parseInt(m[1], 10);
          if (lvl <= startLevel) {
            return Math.max(safeStart, i - 1);
          }
        }
      }
      return blocks.length - 1;
    }
    return blocks.length - 1;
  }

  /**
   * Programmatically creates a native DOM `Selection` (`window.getSelection()`)
   * spanning from `blocks[startIdx]` through `blocks[endIdx]`.
   * This allows macOS "Speak Selection" (`Option + Esc` or Right-Click → Speech → Start Speaking)
   * to immediately read the selected range without manual dragging.
   */
  function applyDomSelectionRange(doc, startNode, endNode) {
    if (!doc || !startNode || !endNode) return null;
    const win = doc.defaultView || (typeof window !== "undefined" ? window : null);
    if (!win || typeof win.getSelection !== "function" || typeof doc.createRange !== "function") {
      return null;
    }
    const sel = win.getSelection();
    if (!sel) return null;
    const range = doc.createRange();
    try {
      range.setStartBefore(startNode);
      range.setEndAfter(endNode);
      sel.removeAllRanges();
      sel.addRange(range);
      return {
        selection: sel,
        range,
        selectedText: normalizeText(sel.toString())
      };
    } catch (_e) {
      return null;
    }
  }

  /**
   * High-level entry point: detects the article, resolves start & end blocks,
   * applies the native browser selection, and returns metadata + block list.
   */
  function selectArticleContent(doc, opts = {}) {
    const mode = opts.mode || "to-end";
    const articleRoot = findMainArticleContainer(doc);
    const blocks = collectReadableBlocks(doc, articleRoot);
    if (blocks.length === 0) {
      return {
        ok: false,
        reason: "no-readable-blocks",
        blocks: [],
        startIndex: -1,
        endIndex: -1,
        selectedText: ""
      };
    }

    const startIndex = mode === "full-article"
      ? 0
      : resolveStartingBlockIndex(blocks, opts);
    const endIndex = resolveEndingBlockIndex(blocks, startIndex, mode);
    const selectedBlocks = blocks.slice(startIndex, endIndex + 1);
    const domSel = applyDomSelectionRange(doc, blocks[startIndex], blocks[endIndex]);
    const cleanParagraphs = selectedBlocks.map(b => normalizeText(b.textContent)).filter(Boolean);

    return {
      ok: true,
      mode,
      articleRoot,
      blocks,
      selectedBlocks,
      startIndex,
      endIndex,
      blockCount: selectedBlocks.length,
      totalBlocks: blocks.length,
      cleanParagraphs,
      selectedText: (domSel && domSel.selectedText) || cleanParagraphs.join("\n\n")
    };
  }

  return {
    normalizeText,
    isElementVisible,
    isInsideNoiseContainer,
    countLinkDensity,
    findMainArticleContainer,
    collectReadableBlocks,
    resolveStartingBlockIndex,
    resolveEndingBlockIndex,
    applyDomSelectionRange,
    selectArticleContent
  };
});
