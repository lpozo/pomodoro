# Pomodoro app (Tkinter)

Simple desktop Pomodoro timer built with Tkinter.

## Run the app

```bash
uv run pomodoro
```

## Run tests

```bash
uv run pytest
```

## Build macOS app bundle

Run the build script and find the `.app` bundle in `dist/`:

```bash
bash packaging/macos/build_app.sh
```

Output: `dist/Pomodoro.app`

See [packaging/macos/README.md](packaging/macos/README.md) for more PyInstaller-based build details.
