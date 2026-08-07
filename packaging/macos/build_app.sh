#!/usr/bin/env bash
set -euo pipefail

# Build a macOS .app bundle with PyInstaller without adding dependencies
# to pyproject.toml. Artifacts are written to dist/ and build/.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

uv run --with pyinstaller pyinstaller --clean --noconfirm packaging/macos/pomodoro.spec

echo "Build complete: dist/Pomodoro.app"
