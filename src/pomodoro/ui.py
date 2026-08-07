import shutil
import subprocess
import tkinter as tk
from tkinter import ttk

from .logic import (
    LONG_BREAK,
    SHORT_BREAK,
    WORK,
    format_hh_mm_ss,
    format_mm_ss,
    next_phase,
)

WORK_COMPLETE_SOUND = "/System/Library/Sounds/Glass.aiff"
REST_COMPLETE_SOUND = "/System/Library/Sounds/Hero.aiff"


def play_sound(file_path: str) -> None:
    player = shutil.which("afplay")
    if not player:
        return

    try:
        subprocess.Popen(
            [player, file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        pass


class PomodoroApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Pomodoro")
        self.root.resizable(False, False)

        self.durations_min = {
            WORK: 25,
            SHORT_BREAK: 5,
            LONG_BREAK: 15,
        }
        self.current_phase = WORK
        self.remaining_seconds = self.durations_min[WORK] * 60
        self.is_running = False
        self.completed_work_sessions = 0
        self.total_work_seconds = 0
        self.timer_job: str | None = None

        self.phase_var = tk.StringVar(value="Phase: Work")
        self.timer_var = tk.StringVar(value="25:00")
        self.total_work_var = tk.StringVar(value="Total Work Time: 00:00:00")
        self.sessions_var = tk.StringVar(value="Completed Work Sessions: 0")
        self.error_var = tk.StringVar(value="")

        self.work_var = tk.StringVar(value="25")
        self.short_break_var = tk.StringVar(value="5")
        self.long_break_var = tk.StringVar(value="15")

        self.build_ui()
        self.refresh_ui()

    def build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.grid(column=0, row=0, sticky="nsew")

        ttk.Label(
            frame,
            textvariable=self.phase_var,
            font=("Helvetica", 16, "bold"),
        ).grid(column=0, row=0, columnspan=3, pady=(0, 8))
        ttk.Label(
            frame,
            textvariable=self.timer_var,
            font=("Courier", 42, "bold"),
        ).grid(column=0, row=1, columnspan=3, pady=(0, 8))
        ttk.Label(frame, textvariable=self.total_work_var).grid(
            column=0,
            row=2,
            columnspan=3,
        )
        ttk.Label(frame, textvariable=self.sessions_var).grid(
            column=0,
            row=3,
            columnspan=3,
            pady=(0, 10),
        )

        self.start_button = ttk.Button(frame, text="Start", command=self.start_timer)
        self.pause_button = ttk.Button(frame, text="Pause", command=self.pause_timer)
        self.stop_button = ttk.Button(frame, text="Stop", command=self.stop_timer)

        self.start_button.grid(column=0, row=4, padx=4, pady=(0, 10), sticky="ew")
        self.pause_button.grid(column=1, row=4, padx=4, pady=(0, 10), sticky="ew")
        self.stop_button.grid(column=2, row=4, padx=4, pady=(0, 10), sticky="ew")

        ttk.Label(frame, text="Work (min)").grid(column=0, row=5)
        ttk.Label(frame, text="Short Break (min)").grid(column=1, row=5)
        ttk.Label(frame, text="Long Break (min)").grid(column=2, row=5)

        self.work_entry = ttk.Entry(
            frame,
            textvariable=self.work_var,
            width=10,
            justify="center",
        )
        self.short_break_entry = ttk.Entry(
            frame,
            textvariable=self.short_break_var,
            width=10,
            justify="center",
        )
        self.long_break_entry = ttk.Entry(
            frame,
            textvariable=self.long_break_var,
            width=10,
            justify="center",
        )

        self.work_entry.grid(column=0, row=6, padx=4, pady=(4, 8))
        self.short_break_entry.grid(column=1, row=6, padx=4, pady=(4, 8))
        self.long_break_entry.grid(column=2, row=6, padx=4, pady=(4, 8))

        ttk.Label(frame, textvariable=self.error_var, foreground="red").grid(
            column=0,
            row=7,
            columnspan=3,
            pady=(2, 0),
        )

    def set_entries_state(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.work_entry.configure(state=state)
        self.short_break_entry.configure(state=state)
        self.long_break_entry.configure(state=state)

    def apply_input_durations(self) -> bool:
        try:
            work_val = int(self.work_var.get())
            short_val = int(self.short_break_var.get())
            long_val = int(self.long_break_var.get())
        except ValueError:
            self.error_var.set("Intervals must be integer values.")
            return False

        if work_val < 1 or short_val < 1 or long_val < 1:
            self.error_var.set("Intervals must be at least 1 minute.")
            return False

        self.error_var.set("")
        self.durations_min = {
            WORK: work_val,
            SHORT_BREAK: short_val,
            LONG_BREAK: long_val,
        }
        return True

    def refresh_ui(self) -> None:
        self.phase_var.set(f"Phase: {self.current_phase}")
        self.timer_var.set(format_mm_ss(self.remaining_seconds))
        self.total_work_var.set(
            f"Total Work Time: {format_hh_mm_ss(self.total_work_seconds)}"
        )
        self.sessions_var.set(
            f"Completed Work Sessions: {self.completed_work_sessions}"
        )

        if self.is_running:
            self.start_button.state(["disabled"])
            self.pause_button.state(["!disabled"])
            self.set_entries_state(False)
        else:
            self.start_button.state(["!disabled"])
            self.pause_button.state(["disabled"])
            self.set_entries_state(True)

    def load_phase(self, phase: str) -> None:
        self.current_phase = phase
        self.remaining_seconds = self.durations_min[phase] * 60

    def handle_phase_completion(self) -> None:
        previous_phase = self.current_phase
        next_phase_name, self.completed_work_sessions = next_phase(
            self.current_phase,
            self.completed_work_sessions,
        )

        if previous_phase == WORK:
            play_sound(WORK_COMPLETE_SOUND)
        else:
            play_sound(REST_COMPLETE_SOUND)

        self.load_phase(next_phase_name)

    def schedule_tick(self) -> None:
        self.timer_job = self.root.after(1000, self.tick)

    def tick(self) -> None:
        if not self.is_running:
            return

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            if self.current_phase == WORK:
                self.total_work_seconds += 1

        if self.remaining_seconds <= 0:
            self.handle_phase_completion()

        self.refresh_ui()
        self.schedule_tick()

    def start_timer(self) -> None:
        if self.is_running:
            return

        if not self.apply_input_durations():
            self.refresh_ui()
            return

        self.is_running = True
        self.refresh_ui()
        self.schedule_tick()

    def pause_timer(self) -> None:
        if not self.is_running:
            return

        self.is_running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.refresh_ui()

    def stop_timer(self) -> None:
        if not self.apply_input_durations():
            self.refresh_ui()
            return

        self.is_running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        self.load_phase(WORK)
        self.refresh_ui()
