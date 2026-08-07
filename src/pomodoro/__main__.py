import sys
import tkinter as tk

from .ui import PomodoroApp


def main() -> None:
    """Run the Pomodoro desktop application.

    Creates the Tk root window, initializes the UI controller,
    and starts the Tkinter event loop.
    """
    root = tk.Tk()
    if sys.platform == "darwin":
        # Best-effort app name for macOS menu integration when run from Python.
        root.tk.call("set", "::tk::mac::appName", "Pomodoro")
        root.tk.call("tk", "appname", "Pomodoro")
    PomodoroApp(root)
    root.mainloop()
