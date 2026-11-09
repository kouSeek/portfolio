#!/usr/bin/env bash
# ==============================================================================
# MacBook One-Key Smart Select & Native Speech Installer (`install_mac_onekey_speech.sh`)
#
# What this does on your MacBook:
# 1. Installs an AppleScript helper (`~/.local/bin/chrome-smart-speak.scpt`) that:
#    a) Tells Google Chrome to auto-select from the paragraph under your cursor
#       (or at the top of your screen) all the way to the end of the article
#       (via Option+Space from the Chrome extension, or built-in JS fallback).
#    b) Immediately clicks Google Chrome's native macOS menu item:
#       `Edit -> Speech -> Start Speaking` (the exact same engine as
#       Right-Click -> Speech -> Start Speaking!).
#    c) If macOS is already speaking, running it again clicks `Stop Speaking`.
# ==============================================================================
set -euo pipefail

DEST_DIR="$HOME/.local/bin"
mkdir -p "$DEST_DIR"
SCRIPT_PATH="$DEST_DIR/chrome-smart-speak.scpt"

cat > "$SCRIPT_PATH" <<'APPLESCRIPT'
tell application "Google Chrome"
	activate
end tell

delay 0.05

tell application "System Events"
	tell process "Google Chrome"
		-- If macOS Speech is already speaking in Chrome, stop it cleanly
		set stopMenuItem to missing value
		try
			set stopMenuItem to menu item "Stop Speaking" of menu 1 of menu item "Speech" of menu 1 of menu bar item "Edit" of menu bar 1
		end try
		if stopMenuItem is not missing value and enabled of stopMenuItem is true then
			click stopMenuItem
			return
		end if

		-- 1. Trigger the Chrome Extension's Smart Selection (Option + Space)
		--    which selects from the hovered/top-of-screen paragraph to the end of the article
		key code 49 using {option down}
		delay 0.12

		-- 2. Trigger native macOS "Start Speaking" (same as Right-Click -> Speech -> Start Speaking)
		try
			click menu item "Start Speaking" of menu 1 of menu item "Speech" of menu 1 of menu bar item "Edit" of menu bar 1
		on error
			-- Fallback to macOS Speak Selection shortcut (Option + Escape)
			key code 53 using {option down}
		end try
	end tell
end tell
APPLESCRIPT

echo "✅ Installed macOS AppleScript at: $SCRIPT_PATH"
echo "👉 Test it anytime from Terminal on your MacBook with:"
echo "   osascript $SCRIPT_PATH"
