import pytest

from src.pomodoro.model.formatters import format_hh_mm_ss, format_mm_ss


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0, "00:00"),
        (5, "00:05"),
        (59, "00:59"),
        (60, "01:00"),
        (65, "01:05"),
        (3599, "59:59"),
    ],
)
def test_format_mm_ss(seconds: int, expected: str):
    assert format_mm_ss(seconds) == expected


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0, "00:00:00"),
        (5, "00:00:05"),
        (59, "00:00:59"),
        (60, "00:01:00"),
        (3661, "01:01:01"),
        (86399, "23:59:59"),
        (86400, "24:00:00"),
    ],
)
def test_format_hh_mm_ss(seconds: int, expected: str):
    assert format_hh_mm_ss(seconds) == expected
