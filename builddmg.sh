#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg

# Empty the dmg folder.
rm -r dist/dmg/*

# Copy the app bundle to the dmg folder.
cp -r "dist/SmartVisionAI.app" dist/dmg

# If the DMG already exists, delete it.
test -f "dist/SmartVisionAI.dmg" && rm "dist/SmartVisionAI.dmg"

# Create the DMG with the appropriate settings
create-dmg \
  --volname "SmartVisionAI" \  # Volume name
  --volicon "src/app_icons/smartvisionaiapp.ico" \  # Icon for the DMG volume
  --window-pos 200 120 \  # Window position of the DMG
  --window-size 600 300 \  # Window size of the DMG
  --icon-size 100 \  # Icon size in the DMG window
  --icon "SmartVisionAI.app" 175 120 \  # Position of the app icon inside the DMG
  --hide-extension "SmartVisionAI.app" \  # Hide the extension of the app bundle in the DMG
  --app-drop-link 425 120 \  # Position of the "drag to Applications" link
  "dist/SmartVisionAI.dmg" \  # Output DMG file path
  "dist/dmg/"  # Directory where the app is located before DMG creation
