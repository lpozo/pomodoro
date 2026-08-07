import pytest

from pomodoro.constants import LONG_BREAK, SHORT_BREAK, WORK
from pomodoro.model.timer import next_phase


@pytest.mark.parametrize(
    (
        "current_phase",
        "completed_work_sessions",
        "expected_phase",
        "expected_completed",
    ),
    [
        (WORK, 1, SHORT_BREAK, 1),
        (WORK, 2, SHORT_BREAK, 2),
        (WORK, 3, SHORT_BREAK, 3),
        (WORK, 4, LONG_BREAK, 4),
        (WORK, 8, LONG_BREAK, 8),
        (SHORT_BREAK, 2, WORK, 2),
        (LONG_BREAK, 4, WORK, 4),
    ],
)
def test_next_phase(
    current_phase: str,
    completed_work_sessions: int,
    expected_phase: str,
    expected_completed: int,
):
    phase, completed = next_phase(current_phase, completed_work_sessions)
    assert phase == expected_phase
    assert completed == expected_completed
