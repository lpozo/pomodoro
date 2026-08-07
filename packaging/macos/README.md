# macOS packaging

This folder contains a PyInstaller setup for building `Pomodoro.app` on macOS.

## Why PyInstaller

- Good default for a Python desktop app.
- Generates a native `.app` bundle.
- Easy to run from `uv` without modifying runtime dependencies.

## Build the app

From the repository root:

```bash
bash packaging/macos/build_app.sh
```

Output:

- `dist/Pomodoro.app`

## Optional: create a DMG installer

If you have `create-dmg` installed:

```bash
create-dmg \
  --volname "Pomodoro" \
  --window-size 600 400 \
  --app-drop-link 450 185 \
  dist/Pomodoro.dmg \
  dist/Pomodoro.app
```

## Notes

- To distribute outside your machine, you'll typically need code signing and notarization.
- If you want a custom Dock icon, set `icon=` in `packaging/macos/pomodoro.spec`.
