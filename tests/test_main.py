import runpy
import tkinter as tk
from pathlib import Path

import pomodoro.ui as pomodoro_ui


class FakeRoot:
    def __init__(self):
        self.mainloop_called = False
        self.tk = self

    def call(self, *args):
        return None

    def mainloop(self):
        self.mainloop_called = True


def test_module_execution_starts_tk_mainloop(monkeypatch):
    fake_root = FakeRoot()
    app_roots = []

    monkeypatch.setattr(tk, "Tk", lambda: fake_root)
    monkeypatch.setattr(pomodoro_ui, "PomodoroApp", app_roots.append)

    entrypoint = Path(__file__).parents[1] / "src" / "pomodoro" / "__main__.py"
    runpy.run_path(str(entrypoint), run_name="__main__")

    assert app_roots == [fake_root]
    assert fake_root.mainloop_called
