/* ==========================================================================
   Dead-Noun -> Visual Action Movie Converter (`src/dead-noun-converter.js`)
   Built for Visual-Spatial / 3D Movie-Simulation Brains (Koushik).
   Replaces lifeless corporate/bureaucratic "dead nouns" (nominalizations like
   "Supervision of a rollout includes oversight of...") with concrete, living
   "Who-Does-What" actors and action verbs so the mental movie projector plays
   automatically with zero cortisol.
   ========================================================================== */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  if (root) {
    root.DeadNounConverter = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : window, function () {
  "use strict";

  // 1. High-Impact Multi-Word Corporate & Engineering Phrase Replacements
  //    Ordered longest/most-specific first so whole clauses flip into visual scenes.
  const PHRASE_RULES = [
    [
      /\bsupervision of a rollout includes the following\b/gi,
      "When you watch new code go live, you do these things"
    ],
    [
      /\bsupervision of a rollout\b/gi,
      "watching new code go live"
    ],
    [
      /\bmust detect material changes in the behavior of the service,\s*including performance,\s*resource consumption,\s*and error rates\b/gi,
      "You must spot any big changes in how the server behaves—like slowing down, eating too much CPU/RAM, or throwing errors"
    ],
    [
      /\bmust include oversight of a service['’]s critical metrics and those of its most important clients\/customers\b/gi,
      "You must watch your service's main health graphs and check that your biggest customers aren't breaking"
    ],
    [
      /\bmust be a manual effort\b/gi,
      "A human must do all the watching by hand"
    ],
    [
      /\bmay be accomplished by some combination of manual and automation effort\b/gi,
      "You can do this using a mix of human checks and automatic bots/alarms"
    ],
    [
      /\bdetect material changes in the behavior of\b/gi,
      "spot any big changes in how"
    ],
    [
      /\bmaterial changes in the behavior of the (\w+)\b/gi,
      "big changes in how the $1 behaves"
    ],
    [
      /\bmaterial changes in the behavior of\b/gi,
      "big changes in how it behaves in"
    ],
    [
      /\bmaterial changes in\b/gi,
      "big noticeable changes in"
    ],
    [
      /\bresource consumption\b/gi,
      "how much CPU/RAM it eats"
    ],
    [
      /\binclude oversight of\b/gi,
      "watch over"
    ],
    [
      /\boversight of\b/gi,
      "watching over"
    ],
    [
      /\bmay be accomplished by\b/gi,
      "you can do this with"
    ],
    [
      /\bcan be accomplished by\b/gi,
      "you can do this with"
    ],
    [
      /\bcan be achieved through\b/gi,
      "you can do this by"
    ],
    [
      /\bincludes the following\b/gi,
      "means doing these things"
    ],
    [
      /\bis comprised of\b/gi,
      "is made of"
    ],
    [
      /\bin accordance with\b/gi,
      "following"
    ],
    [
      /\bin compliance with\b/gi,
      "following"
    ],
    [
      /\bin the event of\b/gi,
      "if there is"
    ],
    [
      /\bin the event that\b/gi,
      "if"
    ],
    [
      /\bfor the purpose of\b/gi,
      "to"
    ],
    [
      /\bwith the objective of\b/gi,
      "to"
    ],
    [
      /\bin order to\b/gi,
      "to"
    ],
    [
      /\bdue to the fact that\b/gi,
      "because"
    ],
    [
      /\bon account of the fact that\b/gi,
      "because"
    ],
    [
      /\bwith regard to\b/gi,
      "about"
    ],
    [
      /\bwith respect to\b/gi,
      "about"
    ],
    [
      /\bpertaining to\b/gi,
      "about"
    ],
    [
      /\bprior to\b/gi,
      "before"
    ],
    [
      /\bsubsequent to\b/gi,
      "after"
    ],
    [
      /\bat this point in time\b/gi,
      "right now"
    ],
    [
      /\bon a regular basis\b/gi,
      "regularly"
    ],
    [
      /\ba sufficient number of\b/gi,
      "enough"
    ],
    [
      /\bhas the ability to\b/gi,
      "can"
    ],
    [
      /\bhave the ability to\b/gi,
      "can"
    ],
    [
      /\bis capable of (\w+ing)\b/gi,
      "can $1"
    ],
    [
      /\bit is imperative that\b/gi,
      "you must make sure"
    ],
    [
      /\bit is essential that\b/gi,
      "you must make sure"
    ],
    [
      /\btake into consideration\b/gi,
      "consider"
    ],
    [
      /\bmake a determination\b/gi,
      "decide"
    ],
    [
      /\bconduct an investigation into\b/gi,
      "dig into"
    ],
    [
      /\bconduct an investigation\b/gi,
      "investigate"
    ],
    [
      /\bperform an assessment of\b/gi,
      "check"
    ],
    [
      /\bprovide assistance to\b/gi,
      "help"
    ],
    [
      /\bprovide assistance\b/gi,
      "help"
    ]
  ];

  // 2. Dead-Noun ("<Nominalization> of") -> Living Action Verb Map
  //    Transforms "(The) <DeadNoun> of X" into "<LivingActionVerb> X"
  const DEAD_NOUN_OF_MAP = {
    supervision: "watching",
    oversight: "watching over",
    implementation: "building and turning on",
    utilization: "using",
    verification: "checking",
    validation: "testing and checking",
    mitigation: "stopping the damage of",
    remediation: "fixing",
    escalation: "paging the next team for",
    provisioning: "spinning up",
    deprecation: "phasing out",
    decommissioning: "shutting down",
    authorization: "approving",
    authentication: "verifying who logs into",
    prioritization: "ranking what comes first in",
    optimization: "speeding up",
    initiation: "starting",
    termination: "stopping",
    modification: "changing",
    configuration: "setting up",
    investigation: "digging into",
    determination: "deciding",
    assessment: "checking",
    evaluation: "testing and scoring",
    deployment: "pushing live",
    rollout: "pushing out",
    monitoring: "watching the health of",
    execution: "running",
    documentation: "writing down",
    notification: "alerting",
    identification: "spotting",
    detection: "spotting",
    resolution: "solving",
    prevention: "blocking",
    allocation: "handing out",
    acquisition: "getting",
    distribution: "sending out",
    maintenance: "keeping up",
    restoration: "bringing back online",
    recovery: "recovering",
    integration: "connecting",
    migration: "moving",
    replication: "copying",
    synchronization: "syncing",
    elimination: "removing",
    removal: "removing",
    reduction: "cutting down",
    submission: "sending in",
    completion: "finishing",
    review: "checking",
    administration: "managing",
    facilitation: "helping run",
    enforcement: "enforcing",
    observation: "watching",
    measurement: "measuring",
    transmission: "sending",
    retrieval: "fetching",
    ingestion: "loading in",
    extraction: "pulling out",
    transformation: "converting",
    aggregation: "combining",
    orchestration: "coordinating",
    consolidation: "merging"
  };

  let DEAD_NOUN_KEYS = Object.keys(DEAD_NOUN_OF_MAP).join("|");
  let DEAD_NOUN_OF_REGEX = new RegExp(
    `\\b(?:the\\s+)?(${DEAD_NOUN_KEYS})\\s+of\\b`,
    "gi"
  );
  let dynamicPhraseRules = [];

  /**
   * Merges cloud-synced rules (`cloud-rules.json` from GitHub / KORTEX Cloud)
   * into the live in-memory converter without needing an extension reinstall.
   */
  function applyCloudRules(cloudPayload) {
    if (!cloudPayload || typeof cloudPayload !== "object") return false;
    let updated = false;

    if (Array.isArray(cloudPayload.phraseRules)) {
      const compiled = [];
      for (let i = 0; i < cloudPayload.phraseRules.length; i++) {
        const pair = cloudPayload.phraseRules[i];
        if (Array.isArray(pair) && pair.length >= 2 && typeof pair[0] === "string" && typeof pair[1] === "string") {
          try {
            compiled.push([new RegExp(pair[0], "gi"), pair[1]]);
          } catch (_e) {}
        }
      }
      if (compiled.length > 0) {
        dynamicPhraseRules = compiled;
        updated = true;
      }
    }

    if (cloudPayload.deadNounOfMap && typeof cloudPayload.deadNounOfMap === "object") {
      const keys = Object.keys(cloudPayload.deadNounOfMap);
      for (let i = 0; i < keys.length; i++) {
        const k = String(keys[i] || "").toLowerCase().trim();
        const v = String(cloudPayload.deadNounOfMap[keys[i]] || "").trim();
        if (k && v) {
          DEAD_NOUN_OF_MAP[k] = v;
          updated = true;
        }
      }
      DEAD_NOUN_KEYS = Object.keys(DEAD_NOUN_OF_MAP).join("|");
      DEAD_NOUN_OF_REGEX = new RegExp(
        `\\b(?:the\\s+)?(${DEAD_NOUN_KEYS})\\s+of\\b`,
        "gi"
      );
    }

    return updated;
  }

  // 3. Single-Word Bureaucratic Verb/Noun Replacements
  const WORD_RULES = [
    [/\butilize\b/gi, "use"],
    [/\butilizes\b/gi, "uses"],
    [/\butilized\b/gi, "used"],
    [/\butilizing\b/gi, "using"],
    [/\butilization\b/gi, "use"],
    [/\bfacilitate\b/gi, "help run"],
    [/\bfacilitates\b/gi, "helps run"],
    [/\bcommence\b/gi, "start"],
    [/\bcommences\b/gi, "starts"],
    [/\bterminate\b/gi, "stop"],
    [/\bterminates\b/gi, "stops"],
    [/\bascertain\b/gi, "find out"],
    [/\bendeavor\b/gi, "try"],
    [/\bmitigate\b/gi, "reduce and fix"],
    [/\bremediate\b/gi, "fix"],
    [/\bameliorate\b/gi, "improve"]
  ];

  function matchCase(sourceWord, replacement) {
    if (!sourceWord || !replacement) return replacement;
    const firstChar = sourceWord.charAt(0);
    if (firstChar === firstChar.toUpperCase() && firstChar !== firstChar.toLowerCase()) {
      return replacement.charAt(0).toUpperCase() + replacement.slice(1);
    }
    return replacement;
  }

  /**
   * Converts a single sentence or paragraph of corporate "dead nouns" into
   * vivid, effortless "Who-Does-What" visual action prose.
   */
  function convertTextToActionMovie(rawText) {
    const input = String(rawText || "");
    if (!input.trim()) {
      return { text: input, changed: false, changeCount: 0 };
    }

    let out = input;
    let changeCount = 0;

    // Step 0: Cloud-synced dynamic phrase rules take top priority
    for (let i = 0; i < dynamicPhraseRules.length; i++) {
      const [pattern, replacement] = dynamicPhraseRules[i];
      out = out.replace(pattern, match => {
        changeCount++;
        return matchCase(match, replacement);
      });
    }

    // Step 1: Multi-word phrase rules
    for (let i = 0; i < PHRASE_RULES.length; i++) {
      const [pattern, replacement] = PHRASE_RULES[i];
      out = out.replace(pattern, match => {
        changeCount++;
        return matchCase(match, replacement);
      });
    }

    // Step 2: "<DeadNoun> of X" -> "<LivingActionVerb> X"
    out = out.replace(DEAD_NOUN_OF_REGEX, (fullMatch, nounKey) => {
      const actionVerb = DEAD_NOUN_OF_MAP[String(nounKey || "").toLowerCase()];
      if (!actionVerb) return fullMatch;
      changeCount++;
      return matchCase(fullMatch, actionVerb);
    });

    // Step 3: Single-word corporate verbs
    for (let i = 0; i < WORD_RULES.length; i++) {
      const [pattern, replacement] = WORD_RULES[i];
      out = out.replace(pattern, match => {
        changeCount++;
        return matchCase(match, replacement);
      });
    }

    return {
      text: out,
      changed: out !== input,
      changeCount
    };
  }

  /**
   * Walks text nodes inside a DOM element and converts dead nouns in-place
   * while preserving all child elements (checkboxes, links, buttons, inputs).
   * Stores original text on a WeakMap / property so it can be restored cleanly.
   */
  function convertElementInPlace(el, originalTextStore) {
    if (!el) return 0;
    let totalChanges = 0;

    function walk(node) {
      if (!node) return;
      if (node.nodeType === 3) {
        // Text node
        const raw = node.nodeValue || "";
        if (!raw.trim()) return;
        const res = convertTextToActionMovie(raw);
        if (res.changed) {
          if (originalTextStore && typeof originalTextStore.set === "function" && !originalTextStore.has(node)) {
            originalTextStore.set(node, raw);
          }
          node.nodeValue = res.text;
          totalChanges += res.changeCount;
        }
        return;
      }
      if (node.nodeType === 1) {
        const tag = (node.tagName || "").toUpperCase();
        if (tag === "SCRIPT" || tag === "STYLE" || tag === "NOSCRIPT" || tag === "CODE" || tag === "PRE" || tag === "TEXTAREA" || tag === "INPUT") {
          return;
        }
        const children = node.childNodes || [];
        for (let i = 0; i < children.length; i++) {
          walk(children[i]);
        }
      }
    }

    walk(el);
    if (totalChanges > 0 && el.classList) {
      el.classList.add("mac-speak-movie-active");
    }
    return totalChanges;
  }

  function restoreElementOriginalText(el, originalTextStore) {
    if (!el || !originalTextStore) return 0;
    let restored = 0;

    function walk(node) {
      if (!node) return;
      if (node.nodeType === 3) {
        if (originalTextStore.has(node)) {
          node.nodeValue = originalTextStore.get(node);
          originalTextStore.delete(node);
          restored++;
        }
        return;
      }
      if (node.nodeType === 1) {
        const children = node.childNodes || [];
        for (let i = 0; i < children.length; i++) {
          walk(children[i]);
        }
      }
    }

    walk(el);
    if (el.classList) {
      el.classList.remove("mac-speak-movie-active");
    }
    return restored;
  }

  return {
    PHRASE_RULES,
    DEAD_NOUN_OF_MAP,
    applyCloudRules,
    convertTextToActionMovie,
    convertElementInPlace,
    restoreElementOriginalText
  };
});
