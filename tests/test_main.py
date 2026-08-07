from src.pomodoro.logic import (
    LONG_BREAK,
    SHORT_BREAK,
    WORK,
    format_hh_mm_ss,
    format_mm_ss,
    next_phase,
)


def test_format_mm_ss():
    assert format_mm_ss(0) == "00:00"
    assert format_mm_ss(65) == "01:05"


def test_format_hh_mm_ss():
    assert format_hh_mm_ss(0) == "00:00:00"
    assert format_hh_mm_ss(3661) == "01:01:01"


def test_next_phase_from_work_to_short_break():
    phase, completed = next_phase(WORK, 0)
    assert phase == SHORT_BREAK
    assert completed == 1


def test_next_phase_from_work_to_long_break_on_fourth_session():
    phase, completed = next_phase(WORK, 3)
    assert phase == LONG_BREAK
    assert completed == 4


def test_next_phase_from_break_to_work():
    phase, completed = next_phase(SHORT_BREAK, 2)
    assert phase == WORK
    assert completed == 2
