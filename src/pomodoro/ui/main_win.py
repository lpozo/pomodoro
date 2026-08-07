import tkinter as tk
from tkinter import ttk

from pomodoro.constants import (
    DEFAULT_LONG_BREAK_MINUTES,
    DEFAULT_SHORT_BREAK_MINUTES,
    DEFAULT_WORK_MINUTES,
    LONG_BREAK,
    REST_COMPLETE_SOUND,
    SECONDS_PER_MINUTE,
    SHORT_BREAK,
    TICK_INTERVAL_MS,
    WORK,
    WORK_COMPLETE_SOUND,
)
from pomodoro.model.formatters import format_hh_mm_ss, format_mm_ss
from pomodoro.model.sound import play_sound
from pomodoro.model.timer import next_phase
from pomodoro.ui.about_dlg import show_about_dialog
from pomodoro.ui.setting_dlg import show_settings_dialog


class PomodoroApp:
    """Tkinter controller and view for the Pomodoro timer application.

    Args:
        root: Tk root window used to render the UI.
    """

    def __init__(self, root: tk.Tk):
        """Initialize application state and build the UI.

        Args:
            root: Tk root window used by the app.
        """
        self.root = root
        self.root.title("Pomodoro")
        self.root.resizable(False, False)

        self.durations_min = {
            WORK: DEFAULT_WORK_MINUTES,
            SHORT_BREAK: DEFAULT_SHORT_BREAK_MINUTES,
            LONG_BREAK: DEFAULT_LONG_BREAK_MINUTES,
        }
        self.current_phase = WORK
        self.remaining_seconds = self.durations_min[WORK] * SECONDS_PER_MINUTE
        self.is_running = False
        self.completed_work_sessions = 0
        self.total_work_seconds = 0
        self.timer_job: str | None = None

        self.phase_var = tk.StringVar(value="Phase: Work")
        self.timer_var = tk.StringVar(
            value=format_mm_ss(DEFAULT_WORK_MINUTES * SECONDS_PER_MINUTE)
        )
        self.total_work_var = tk.StringVar(value="Total Work Time: 00:00:00")
        self.sessions_var = tk.StringVar(value="Completed Work Sessions: 0")
        self.error_var = tk.StringVar(value="")

        self._build_menu()
        self._build_ui()
        self._refresh_ui()

    def _build_menu(self) -> None:
        """Create the application menu bar."""
        menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(menu_bar, tearoff=False)
        self.file_menu.add_command(
            label="Preferences...",
            command=self._open_config_dialog,
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.destroy)
        menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.help_menu = tk.Menu(menu_bar, tearoff=False)
        self.help_menu.add_command(label="About", command=self._open_about_dialog)
        menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.root.configure(menu=menu_bar)

    def _build_ui(self) -> None:
        """Create and place all widgets for the main window."""
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

        self.start_button = ttk.Button(frame, text="▶", command=self.start_timer)
        self.pause_button = ttk.Button(frame, text="⏸", command=self.pause_timer)
        self.stop_button = ttk.Button(frame, text="⏹", command=self.stop_timer)

        self.start_button.grid(column=0, row=4, padx=4, pady=(0, 10), sticky="ew")
        self.pause_button.grid(column=1, row=4, padx=4, pady=(0, 10), sticky="ew")
        self.stop_button.grid(column=2, row=4, padx=4, pady=(0, 10), sticky="ew")

        ttk.Label(frame, textvariable=self.error_var, foreground="red").grid(
            column=0,
            row=5,
            columnspan=3,
            pady=(2, 0),
        )

    def _open_config_dialog(self) -> None:
        """Open a modal dialog to configure interval durations."""
        updated_durations = show_settings_dialog(self.root, self.durations_min)
        if updated_durations is None:
            return

        self.error_var.set("")
        self.durations_min = updated_durations

        if not self.is_running:
            self.load_phase(self.current_phase)
            self._refresh_ui()

    def _open_about_dialog(self) -> None:
        """Open the About dialog."""
        show_about_dialog(self.root)

    def _refresh_ui(self) -> None:
        """Refresh labels and button states from current app state."""
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
            self.stop_button.state(["!disabled"])
            self.file_menu.entryconfigure("Preferences...", state=tk.DISABLED)
        else:
            self.start_button.state(["!disabled"])
            self.pause_button.state(["disabled"])
            self.stop_button.state(["disabled"])
            self.file_menu.entryconfigure("Preferences...", state=tk.NORMAL)

    def load_phase(self, phase: str) -> None:
        """Set active phase and reset remaining time for that phase.

        Args:
            phase: Phase label to load.
        """
        self.current_phase = phase
        self.remaining_seconds = self.durations_min[phase] * SECONDS_PER_MINUTE

    def handle_phase_completion(self) -> None:
        """Advance to the next phase and trigger completion sound."""
        previous_phase = self.current_phase
        if previous_phase == WORK:
            self.completed_work_sessions += 1

        next_phase_name, _ = next_phase(
            self.current_phase,
            self.completed_work_sessions,
        )

        if previous_phase == WORK:
            play_sound(WORK_COMPLETE_SOUND)
        else:
            play_sound(REST_COMPLETE_SOUND)

        self.load_phase(next_phase_name)

    def schedule_tick(self) -> None:
        """Schedule the next timer tick in one second."""
        self.timer_job = self.root.after(TICK_INTERVAL_MS, self.tick)

    def tick(self) -> None:
        """Advance the timer by one second and update phase when needed."""
        if not self.is_running:
            return

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            if self.current_phase == WORK:
                self.total_work_seconds += 1

        if self.remaining_seconds <= 0:
            self.handle_phase_completion()

        self._refresh_ui()
        self.schedule_tick()

    def start_timer(self) -> None:
        """Start the timer if inputs are valid and not already running."""
        if self.is_running:
            return

        self.is_running = True
        self._refresh_ui()
        self.schedule_tick()

    def pause_timer(self) -> None:
        """Pause the timer and cancel any scheduled tick."""
        if not self.is_running:
            return

        self.is_running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self._refresh_ui()

    def stop_timer(self) -> None:
        """Stop the timer and reset to the work phase.

        Keeps the accumulated total work time and completed work sessions.
        """
        self.is_running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        self.load_phase(WORK)
        self._refresh_ui()
