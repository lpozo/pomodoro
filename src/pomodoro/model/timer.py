from .constants import LONG_BREAK, SHORT_BREAK, WORK, WORK_SESSIONS_PER_LONG_BREAK


def next_phase(current_phase: str, completed_work_sessions: int) -> tuple[str, int]:
    """Compute the next timer phase and session count.

    Args:
        current_phase: The current phase label.
        completed_work_sessions: Number of completed work sessions.

    Returns:
        A tuple containing the next phase label and the updated number
        of completed work sessions.
    """
    if current_phase == WORK:
        if completed_work_sessions % WORK_SESSIONS_PER_LONG_BREAK == 0:
            return LONG_BREAK, completed_work_sessions
        return SHORT_BREAK, completed_work_sessions

    return WORK, completed_work_sessions
