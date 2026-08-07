def format_mm_ss(seconds: int) -> str:
    """Format seconds as MM:SS.

    Args:
        seconds: Duration in seconds.

    Returns:
        A zero-padded string in MM:SS format.
    """
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes:02d}:{sec:02d}"


def format_hh_mm_ss(seconds: int) -> str:
    """Format seconds as HH:MM:SS.

    Args:
        seconds: Duration in seconds.

    Returns:
        A zero-padded string in HH:MM:SS format.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    sec = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{sec:02d}"
