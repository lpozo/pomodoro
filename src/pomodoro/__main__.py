import tkinter as tk

from pomodoro.ui import PomodoroApp


def main() -> None:
    """Run the Pomodoro desktop application.

    Creates the Tk root window, initializes the UI controller,
    and starts the Tkinter event loop.
    """
    root = tk.Tk()
    PomodoroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
