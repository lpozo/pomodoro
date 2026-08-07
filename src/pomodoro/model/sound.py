import os
import shutil
import subprocess
from pathlib import Path

from .constants import SOUND_DIR_ENV, SOUND_EXTENSIONS


def _resolve_sound_file(sound: str) -> str | None:
    sound_path = Path(sound).expanduser()
    if sound_path.is_file():
        return str(sound_path)

    # Allow custom sound directory through environment configuration.
    search_dirs: list[Path] = []
    custom_sound_dir = os.getenv(SOUND_DIR_ENV)
    if custom_sound_dir:
        search_dirs.append(Path(custom_sound_dir).expanduser())

    search_dirs.extend(
        [
            Path.home() / "Library" / "Sounds",
            Path("/System/Library/Sounds"),
        ]
    )

    for base_dir in search_dirs:
        for extension in SOUND_EXTENSIONS:
            candidate = base_dir / f"{sound}{extension}"
            if candidate.is_file():
                return str(candidate)

    return None


def play_sound(file_path: str) -> None:
    """Play a sound if the system player and file are available.

    The sound can be an absolute path, a relative path, or a sound name
    that is resolved against configured search directories.

    Args:
        file_path: Sound identifier or file path to play.
    """
    player = shutil.which("afplay")
    if not player:
        return

    resolved_file = _resolve_sound_file(file_path)
    if resolved_file is None:
        return

    try:
        subprocess.Popen(
            [player, resolved_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        pass
