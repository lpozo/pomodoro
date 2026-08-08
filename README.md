# Pomodoro app

[![Tests](https://img.shields.io/github/actions/workflow/status/lpozo/pomodoro/tests.yml)](https://github.com/lpozo/pomodoro/actions/workflows/tests.yml)
[![Lint](https://img.shields.io/github/actions/workflow/status/lpozo/pomodoro/lint.yml)](https://github.com/lpozo/pomodoro/actions/workflows/lint.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/github/license/lpozo/pomodoro)](LICENSE)

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
