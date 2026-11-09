#!/usr/bin/env bash
# ==============================================================================
# MacBook Smart Read Aloud & Movie Mode (Dead-Noun Converter) — One-Shot Installer
# Downloads the latest extension into ~/Downloads/mac-speak-chrome-ext with
# ZERO background runners, ZERO LaunchAgents, and ZERO auto-git sync jobs.
# ==============================================================================
set -euo pipefail

TARBALL_URL="https://github.com/kouSeek/portfolio/archive/refs/heads/mac-speak-chrome-ext.tar.gz"
INSTALL_DIR="${1:-${HOME}/Downloads/mac-speak-chrome-ext}"
OLD_PLIST="${HOME}/Library/LaunchAgents/com.koushik.macspeak.cloudsync.plist"

# 1. Remove any old background LaunchAgent if previously installed
if [ -f "${OLD_PLIST}" ]; then
  launchctl unload "${OLD_PLIST}" 2>/dev/null || true
  rm -f "${OLD_PLIST}"
  echo "🧹 Removed old background LaunchAgent (${OLD_PLIST})."
fi

# 2. Download and extract latest extension files (one-shot, no git daemon)
echo "📦 Installing latest MacBook Smart Read Aloud & Movie Mode into ${INSTALL_DIR}..."
mkdir -p "${INSTALL_DIR}"
curl -fsSL "${TARBALL_URL}" | tar -xz -C "${INSTALL_DIR}" --strip-components=1

# 3. If CORP_EXT_KEY is provided, inject it into manifest.json for Corp Chrome allowlisting
if [ -n "${CORP_EXT_KEY:-}" ]; then
  INSTALL_DIR="${INSTALL_DIR}" CORP_EXT_KEY="${CORP_EXT_KEY}" python3 - <<'PY'
import json, os
from pathlib import Path
p = Path(os.environ["INSTALL_DIR"]) / "manifest.json"
m = json.loads(p.read_text(encoding="utf-8"))
m["key"] = os.environ["CORP_EXT_KEY"]
p.write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
PY
  echo "🔑 Applied Google Corp Chrome developer key (ID: pbnaomcgbfiofkfobmlhmdobjchjkphi)."
fi

echo ""
echo "======================================================================"
echo "✅ Installed at: ${INSTALL_DIR} (zero background jobs)"
echo "----------------------------------------------------------------------"
echo "In Chrome (chrome://extensions):"
echo "  1. Enable 'Developer mode' (top-right)."
echo "  2. Click 'Load unpacked' -> select ${INSTALL_DIR}"
echo "     (or click 🔄 Reload on the card if already added)."
echo "======================================================================"
