"""
DatePickerDialog - Simple calendar popup to pick a date (tkinter).
"""

import calendar
import tkinter as tk
from datetime import datetime


class DatePickerDialog:
    """Modal dialog showing a month calendar with prev/next navigation."""

    def __init__(self, parent, year: int, month: int, day: int):
        self.result: str | None = None
        self._year, self._month, self._day = year, month, day
        self._win = tk.Toplevel(parent)
        self._win.title("Pick due date")
        self._win.transient(parent)
        self._win.grab_set()
        self._win.geometry("260x240")
        self._win.resizable(False, False)
        self._build_ui()
        self._win.wait_window()

    def _build_ui(self) -> None:
        # Month / Year nav
        nav = tk.Frame(self._win, pady=6)
        nav.pack(fill=tk.X)
        tk.Button(nav, text="\u2190", width=3, command=self._prev_month).pack(side=tk.LEFT, padx=4)
        self._month_label = tk.Label(nav, text="", font=("Segoe UI", 11, "bold"))
        self._month_label.pack(side=tk.LEFT, expand=True)
        tk.Button(nav, text="\u2192", width=3, command=self._next_month).pack(side=tk.RIGHT, padx=4)

        # Weekday headers
        week_frame = tk.Frame(self._win)
        week_frame.pack(fill=tk.X, padx=8)
        for w in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            tk.Label(week_frame, text=w, font=("Segoe UI", 9), width=4).pack(side=tk.LEFT)

        # Days grid
        self._days_frame = tk.Frame(self._win, padx=8, pady=4)
        self._days_frame.pack(fill=tk.BOTH, expand=True)
        self._refresh_calendar()

    def _refresh_calendar(self) -> None:
        month_name = datetime(self._year, self._month, 1).strftime("%B %Y")
        self._month_label.config(text=month_name)
        for w in self._days_frame.winfo_children():
            w.destroy()
        cal = calendar.Calendar(calendar.MONDAY)
        weeks = cal.monthdayscalendar(self._year, self._month)
        today = datetime.now()
        for row, week in enumerate(weeks):
            for col, d in enumerate(week):
                if d == 0:
                    tk.Label(self._days_frame, text="", width=4).grid(row=row, column=col, padx=1, pady=1)
                    continue
                btn = tk.Button(
                    self._days_frame, text=str(d), width=4,
                    command=lambda day=d: self._pick(day)
                )
                btn.grid(row=row, column=col, padx=1, pady=1)
                if self._year == today.year and self._month == today.month and d == today.day:
                    btn.configure(bg="#E3F2FD")

    def _prev_month(self) -> None:
        if self._month == 1:
            self._year -= 1
            self._month = 12
        else:
            self._month -= 1
        self._refresh_calendar()

    def _next_month(self) -> None:
        if self._month == 12:
            self._year += 1
            self._month = 1
        else:
            self._month += 1
        self._refresh_calendar()

    def _pick(self, day: int) -> None:
        self.result = f"{self._year:04d}-{self._month:02d}-{day:02d}"
        self._win.destroy()
