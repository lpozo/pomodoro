import tkinter as tk
from tkinter import ttk


def show_about_dialog(parent: tk.Tk) -> None:
    """Show the About dialog.

    Args:
        parent: Parent Tk window.
    """
    dialog = tk.Toplevel(parent)
    dialog.title("About Pomodoro")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()

    frame = ttk.Frame(dialog, padding=16)
    frame.grid(column=0, row=0, sticky="nsew")

    ttk.Label(frame, text="Pomodoro", font=("Helvetica", 14, "bold")).grid(
        column=0,
        row=0,
        pady=(0, 8),
    )
    ttk.Label(frame, text="Simple desktop Pomodoro timer.").grid(
        column=0,
        row=1,
        pady=(0, 4),
    )
    ttk.Label(frame, text="Built with Python and Tkinter.").grid(
        column=0,
        row=2,
        pady=(0, 12),
    )

    ttk.Button(frame, text="OK", command=dialog.destroy).grid(column=0, row=3)

    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
    dialog.bind("<Return>", lambda _event: dialog.destroy())
    dialog.bind("<Escape>", lambda _event: dialog.destroy())

    parent.wait_window(dialog)
