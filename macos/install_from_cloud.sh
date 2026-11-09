#!/usr/bin/env bash
# ==============================================================================
# MacBook Smart Read Aloud & Movie Mode (Dead-Noun Converter) — Cloud Installer
# Clones the cloud repository into `~/.mac-speak-chrome-ext` and installs a
# background macOS LaunchAgent (`com.koushik.macspeak.cloudsync`) that keeps
# the local extension folder 100% synced with the cloud repo automatically.
#
# Run once on MacBook:
#   curl -fsSL https://raw.githubusercontent.com/kouSeek/portfolio/mac-speak-chrome-ext/macos/install_from_cloud.sh | bash
# ==============================================================================
set -euo pipefail

REPO_URL="https://github.com/kouSeek/portfolio.git"
BRANCH="mac-speak-chrome-ext"
INSTALL_DIR="${HOME}/.mac-speak-chrome-ext"
PLIST_DIR="${HOME}/Library/LaunchAgents"
PLIST_PATH="${PLIST_DIR}/com.koushik.macspeak.cloudsync.plist"

echo "☁️ Installing MacBook Smart Read Aloud & Movie Mode from Cloud..."

if [ -d "${INSTALL_DIR}/.git" ]; then
  echo "🔄 Updating existing installation at ${INSTALL_DIR}..."
  git -C "${INSTALL_DIR}" fetch origin "${BRANCH}" --depth=1
  git -C "${INSTALL_DIR}" reset --hard "origin/${BRANCH}"
else
  rm -rf "${INSTALL_DIR}"
  git clone --branch "${BRANCH}" --single-branch --depth=1 "${REPO_URL}" "${INSTALL_DIR}"
fi

# Set up macOS LaunchAgent to auto-pull cloud updates every 15 minutes
if [ "$(uname -s)" = "Darwin" ]; then
  mkdir -p "${PLIST_DIR}"
  cat > "${PLIST_PATH}" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.koushik.macspeak.cloudsync</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-c</string>
    <string>cd "${INSTALL_DIR}" &amp;&amp; /usr/bin/git fetch origin "${BRANCH}" --depth=1 &amp;&amp; /usr/bin/git reset --hard "origin/${BRANCH}"</string>
  </array>
  <key>StartInterval</key>
  <integer>900</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/tmp/macspeak-cloudsync.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/macspeak-cloudsync.err</string>
</dict>
</plist>
EOF
  launchctl unload "${PLIST_PATH}" 2>/dev/null || true
  launchctl load "${PLIST_PATH}" 2>/dev/null || true
  echo "✅ Installed background macOS Cloud Auto-Sync daemon (pulls cloud updates every 15m + OTA rule sync)."
  open -a "Google Chrome" "chrome://extensions" 2>/dev/null || true
fi

echo ""
echo "======================================================================"
echo "✅ Cloud Installation Ready at: ${INSTALL_DIR}"
echo "----------------------------------------------------------------------"
echo "One-time Chrome setup:"
echo "  1. In Chrome (chrome://extensions), turn ON 'Developer mode' (top-right)."
echo "  2. Click 'Load unpacked' and select: ${INSTALL_DIR}"
echo "     (Press Cmd + Shift + . in the Mac file picker to show hidden dot-folders!)"
echo "======================================================================"
