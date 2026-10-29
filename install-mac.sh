#!/usr/bin/env bash
set -e

echo "🎨 Installing PickHex for macOS..."

TMP_DIR="$(mktemp -d)"
ZIP_PATH="$TMP_DIR/PickHex-macOS.zip"

echo "⬇️  Downloading latest PickHex release..."
curl -fsSL "https://github.com/murrer33/PickHex/releases/latest/download/PickHex-macOS.zip" -o "$ZIP_PATH"

echo "📦 Extracting PickHex.app..."
ditto -x -k "$ZIP_PATH" "$TMP_DIR/extracted"

APP_FOUND="$(find "$TMP_DIR/extracted" -name "PickHex.app" -maxdepth 3 | head -n 1)"

if [ -z "$APP_FOUND" ]; then
    echo "❌ Could not find PickHex.app in archive."
    rm -rf "$TMP_DIR"
    exit 1
fi

rm -rf "/Applications/PickHex.app"
cp -R "$APP_FOUND" "/Applications/PickHex.app"

# Remove macOS Gatekeeper quarantine flag so it opens without any warning popup
xattr -cr "/Applications/PickHex.app" 2>/dev/null || true

rm -rf "$TMP_DIR"

echo "✅ PickHex installed to /Applications/PickHex.app!"
echo "🚀 Launching PickHex (check your top Menu Bar)..."
open "/Applications/PickHex.app"
