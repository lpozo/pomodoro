import tkinter as tk

from pomodoro.ui.main_win import PomodoroApp


def test_pause_and_stop_buttons_share_running_state():
    root = tk.Tk()
    root.withdraw()
    try:
        app = PomodoroApp(root)

        assert app.pause_button.instate(["disabled"])
        assert app.stop_button.instate(["disabled"])

        app.start_timer()

        assert app.pause_button.instate(["!disabled"])
        assert app.stop_button.instate(["!disabled"])

        app.pause_timer()

        assert app.pause_button.instate(["disabled"])
        assert app.stop_button.instate(["disabled"])

        app.start_timer()
        app.stop_timer()

        assert app.pause_button.instate(["disabled"])
        assert app.stop_button.instate(["disabled"])
    finally:
        root.destroy()
