# AGENTS.md

Simple desktop Pomodoro timer: Python 3.10+ / Tkinter, `uv`-managed, MIT. No runtime dependencies.

## Commands

```bash
uv run pomodoro            # run the app (entrypoint: pomodoro.__main__:main)
uv run pytest              # run tests (testpaths = tests)
uv run ruff check .        # lint: E/F/W/I incl. import sorting (I001)
uv run ruff format --check .  # format check (line-length 88)
bash packaging/macos/build_app.sh  # build dist/Pomodoro.app via PyInstaller
```

Run ruff and tests before committing. Import order is enforced (ruff `I`).

## Layout

- `src/pomodoro/` — src-layout package (`package-dir = {"": "src"}` in pyproject)
- `src/pomodoro/model/` — pure, tk-free logic: phase transitions (`timer.py`), time formatting (`formatters.py`), macOS sound via `afplay` (`sound.py`)
- `src/pomodoro/ui/` — Tkinter: `main_win.py` (controller: after-scheduled ticks), `setting_dlg.py`, `about_dlg.py`
- `src/pomodoro/constants.py` — central place for durations, sound names, labels
- `tests/` — plain pytest; UI tests instantiate a real `tk.Tk()` (withdrawn)

## Gotchas

- Tkinter is a stdlib build dependency, not a pip package. CI's system Python lacks it, so `.github/workflows/tests.yml` installs `python3-tk` via apt and runs tests under `xvfb-run` (the `tk.Tk()` UI test needs a virtual display on Linux).
- PyInstaller is intentionally NOT in `pyproject.toml` — `build_app.sh` uses `uv run --with pyinstaller`. Don't add it as a dependency.
- App icon lives at `packaging/macos/Pomodoro.icns`, wired into `pomodoro.spec`. Regeneration is manual (render PNG → iconset → `iconutil -c icns`).
- `dist/` and `build/` are gitignored build artifacts.

## Conventions

- Conventional Commit messages (`feat:`, `fix:`, `docs:`, `ci:`, `chore:`).
- Work on a feature branch, push, and open a PR with `gh pr create`. Do not commit directly to `main`.
