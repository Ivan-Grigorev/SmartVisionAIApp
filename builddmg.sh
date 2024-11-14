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
  --volname "SmartVisionAI" \
  --volicon "src/app_icons/smartvisionaiapp.ico" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "SmartVisionAI.app" 175 120 \
  --hide-extension "SmartVisionAI.app" \
  --app-drop-link 425 120 \
  "dist/SmartVisionAI.dmg" \
  "dist/dmg/"
