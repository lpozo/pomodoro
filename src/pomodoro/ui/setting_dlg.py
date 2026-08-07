import tkinter as tk
from tkinter import ttk

from ..model.constants import (
    LONG_BREAK,
    MAX_INTERVAL_MINUTES,
    MIN_INTERVAL_MINUTES,
    SHORT_BREAK,
    WORK,
)


def show_settings_dialog(
    parent: tk.Tk,
    current_durations: dict[str, int],
) -> dict[str, int] | None:
    """Show the settings dialog and return updated intervals if accepted.

    Args:
        parent: Parent Tk window.
        current_durations: Current durations in minutes by phase.

    Returns:
        Updated duration mapping when Apply is pressed, otherwise None.
    """
    result: dict[str, int] | None = None

    dialog = tk.Toplevel(parent)
    dialog.title("Configure Intervals")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()

    work_var = tk.StringVar(value=str(current_durations[WORK]))
    short_break_var = tk.StringVar(value=str(current_durations[SHORT_BREAK]))
    long_break_var = tk.StringVar(value=str(current_durations[LONG_BREAK]))
    dialog_error_var = tk.StringVar(value="")

    dialog_frame = ttk.Frame(dialog, padding=16)
    dialog_frame.grid(column=0, row=0, sticky="nsew")

    ttk.Label(dialog_frame, text="Work (min)").grid(column=0, row=0, sticky="w")
    ttk.Label(dialog_frame, text="Short Break (min)").grid(column=0, row=1, sticky="w")
    ttk.Label(dialog_frame, text="Long Break (min)").grid(column=0, row=2, sticky="w")

    ttk.Spinbox(
        dialog_frame,
        textvariable=work_var,
        from_=MIN_INTERVAL_MINUTES,
        to=MAX_INTERVAL_MINUTES,
        increment=1,
        width=10,
        justify="center",
    ).grid(column=1, row=0, padx=(8, 0), pady=2)
    ttk.Spinbox(
        dialog_frame,
        textvariable=short_break_var,
        from_=MIN_INTERVAL_MINUTES,
        to=MAX_INTERVAL_MINUTES,
        increment=1,
        width=10,
        justify="center",
    ).grid(column=1, row=1, padx=(8, 0), pady=2)
    ttk.Spinbox(
        dialog_frame,
        textvariable=long_break_var,
        from_=MIN_INTERVAL_MINUTES,
        to=MAX_INTERVAL_MINUTES,
        increment=1,
        width=10,
        justify="center",
    ).grid(column=1, row=2, padx=(8, 0), pady=2)

    ttk.Label(dialog_frame, textvariable=dialog_error_var, foreground="red").grid(
        column=0,
        row=3,
        columnspan=2,
        pady=(6, 2),
    )

    def close_dialog() -> None:
        dialog.destroy()

    def accept_dialog() -> None:
        nonlocal result
        try:
            work_val = int(work_var.get())
            short_val = int(short_break_var.get())
            long_val = int(long_break_var.get())
        except ValueError:
            dialog_error_var.set("Intervals must be integer values.")
            return

        if (
            work_val < MIN_INTERVAL_MINUTES
            or short_val < MIN_INTERVAL_MINUTES
            or long_val < MIN_INTERVAL_MINUTES
        ):
            dialog_error_var.set("Intervals must be at least 1 minute.")
            return

        result = {
            WORK: work_val,
            SHORT_BREAK: short_val,
            LONG_BREAK: long_val,
        }
        close_dialog()

    ttk.Button(dialog_frame, text="Cancel", command=close_dialog).grid(
        column=0,
        row=4,
        pady=(8, 0),
        sticky="ew",
    )
    ttk.Button(dialog_frame, text="Apply", command=accept_dialog).grid(
        column=1,
        row=4,
        padx=(8, 0),
        pady=(8, 0),
        sticky="ew",
    )

    dialog.protocol("WM_DELETE_WINDOW", close_dialog)
    dialog.bind("<Return>", lambda _event: accept_dialog())
    dialog.bind("<Escape>", lambda _event: close_dialog())

    parent.wait_window(dialog)
    return result
