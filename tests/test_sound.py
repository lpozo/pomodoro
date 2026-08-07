from pathlib import Path
from uuid import uuid4

import pytest

import pomodoro.constants as constants
import pomodoro.model.sound as sound


@pytest.mark.parametrize(
    "player_path,sound_name",
    [
        (None, "focus"),
        ("/usr/bin/afplay", f"missing_{uuid4().hex}"),
    ],
)
def test_play_sound_noops_when_cannot_play(
    monkeypatch,
    tmp_path: Path,
    player_path: str | None,
    sound_name: str,
):
    popen_calls = []

    monkeypatch.setattr(sound.shutil, "which", lambda _: player_path)
    monkeypatch.delenv(constants.SOUND_DIR_ENV, raising=False)
    # Keep search isolated to tmp_path when no custom sound dir is configured.
    monkeypatch.setattr(sound.Path, "home", lambda: tmp_path)
    monkeypatch.setattr(
        sound.subprocess,
        "Popen",
        lambda *args, **kwargs: popen_calls.append((args, kwargs)),
    )

    sound.play_sound(sound_name)

    assert popen_calls == []


def test_play_sound_invokes_popen_with_direct_path(monkeypatch, tmp_path: Path):
    popen_calls = []
    sound_file = tmp_path / "focus.aiff"
    sound_file.write_text("data")

    monkeypatch.setattr(sound.shutil, "which", lambda _: "/usr/bin/afplay")

    def fake_popen(*args, **kwargs):
        popen_calls.append((args, kwargs))

    monkeypatch.setattr(sound.subprocess, "Popen", fake_popen)

    sound.play_sound(str(sound_file))

    assert len(popen_calls) == 1
    args, kwargs = popen_calls[0]
    assert args[0] == ["/usr/bin/afplay", str(sound_file)]
    assert kwargs["stdout"] is sound.subprocess.DEVNULL
    assert kwargs["stderr"] is sound.subprocess.DEVNULL


@pytest.mark.parametrize("extension", constants.SOUND_EXTENSIONS)
def test_play_sound_resolves_from_custom_sound_dir_with_any_supported_extension(
    monkeypatch,
    tmp_path: Path,
    extension: str,
):
    popen_calls = []
    custom_dir = tmp_path / "custom_sounds"
    custom_dir.mkdir()
    sound_file = custom_dir / f"focus{extension}"
    sound_file.write_text("data")

    monkeypatch.setenv(constants.SOUND_DIR_ENV, str(custom_dir))
    monkeypatch.setattr(sound.shutil, "which", lambda _: "/usr/bin/afplay")

    def fake_popen(*args, **kwargs):
        popen_calls.append((args, kwargs))

    monkeypatch.setattr(sound.subprocess, "Popen", fake_popen)

    sound.play_sound("focus")

    assert len(popen_calls) == 1
    args, _ = popen_calls[0]
    assert args[0] == ["/usr/bin/afplay", str(sound_file)]


def test_play_sound_resolves_custom_sound_dir_with_tilde(monkeypatch, tmp_path: Path):
    popen_calls = []
    fake_home = tmp_path / "fake_home"
    custom_dir = fake_home / "my_sounds"
    custom_dir.mkdir(parents=True)
    sound_file = custom_dir / "focus.aiff"
    sound_file.write_text("data")

    monkeypatch.setenv("HOME", str(fake_home))
    monkeypatch.setenv(constants.SOUND_DIR_ENV, "~/my_sounds")
    monkeypatch.setattr(sound.shutil, "which", lambda _: "/usr/bin/afplay")

    def fake_popen(*args, **kwargs):
        popen_calls.append((args, kwargs))

    monkeypatch.setattr(sound.subprocess, "Popen", fake_popen)

    sound.play_sound("focus")

    assert len(popen_calls) == 1
    args, _ = popen_calls[0]
    assert args[0] == ["/usr/bin/afplay", str(sound_file)]


@pytest.mark.parametrize("error", [OSError("boom"), FileNotFoundError("missing")])
def test_play_sound_swallows_oserror_variants(
    monkeypatch,
    tmp_path: Path,
    error: OSError,
):
    sound_file = tmp_path / "focus.aiff"
    sound_file.write_text("data")

    monkeypatch.setattr(sound.shutil, "which", lambda _: "/usr/bin/afplay")

    def raise_oserror(*args, **kwargs):
        raise error

    monkeypatch.setattr(sound.subprocess, "Popen", raise_oserror)

    # Should not raise.
    sound.play_sound(str(sound_file))
