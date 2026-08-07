WORK = "Work"
SHORT_BREAK = "Short Break"
LONG_BREAK = "Long Break"


def format_mm_ss(seconds: int) -> str:
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes:02d}:{sec:02d}"


def format_hh_mm_ss(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    sec = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{sec:02d}"


def next_phase(current_phase: str, completed_work_sessions: int) -> tuple[str, int]:
    if current_phase == WORK:
        completed_work_sessions += 1
        if completed_work_sessions % 4 == 0:
            return LONG_BREAK, completed_work_sessions
        return SHORT_BREAK, completed_work_sessions

    return WORK, completed_work_sessions
