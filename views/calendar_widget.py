"""
CalendarWidget - Month calendar with prev/next navigation for the dashboard (tkinter).
Highlights days that have notes due.
"""

import calendar
import tkinter as tk
from datetime import datetime
from typing import Callable


class CalendarWidget(tk.Frame):
    """Shows one month with prev/next and optional highlight for days with due notes."""

    def __init__(self, parent, get_notes_with_due: Callable[[], list], **kwargs):
        super().__init__(parent, **kwargs)
        self.get_notes_with_due = get_notes_with_due
        self._year = datetime.now().year
        self._month = datetime.now().month
        self._day_buttons: list[tk.Button] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.configure(bg="#fff", relief=tk.GROOVE, bd=1, padx=8, pady=8)
        # Month / Year nav
        nav = tk.Frame(self, bg="#fff")
        nav.pack(fill=tk.X, pady=(0, 6))
        tk.Button(nav, text="\u2190", width=2, command=self._prev_month, bg="#fff", relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT)
        self._month_label = tk.Label(nav, text="", font=("Segoe UI", 12, "bold"), bg="#fff")
        self._month_label.pack(side=tk.LEFT, expand=True)
        tk.Button(nav, text="\u2192", width=2, command=self._next_month, bg="#fff", relief=tk.FLAT, cursor="hand2").pack(side=tk.RIGHT)

        # Weekday headers
        week_frame = tk.Frame(self, bg="#fff")
        week_frame.pack(fill=tk.X)
        for w in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            tk.Label(week_frame, text=w, font=("Segoe UI", 8), fg="#666", bg="#fff", width=3).pack(side=tk.LEFT)

        # Days grid
        self._days_frame = tk.Frame(self, bg="#fff", pady=4)
        self._days_frame.pack(fill=tk.BOTH, expand=True)
        self._refresh_calendar()

    def _refresh_calendar(self) -> None:
        self._month_label.config(text=datetime(self._year, self._month, 1).strftime("%B %Y"))
        for w in self._days_frame.winfo_children():
            w.destroy()
        self._day_buttons.clear()
        cal = calendar.Calendar(calendar.MONDAY)
        weeks = cal.monthdayscalendar(self._year, self._month)
        today = datetime.now()
        due_days = set()
        for note in self.get_notes_with_due():
            if note.due_date:
                try:
                    parts = note.due_date.split("-")
                    if len(parts) == 3:
                        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
                        if y == self._year and m == self._month:
                            due_days.add(d)
                except (ValueError, IndexError):
                    pass
        for row, week in enumerate(weeks):
            for col, d in enumerate(week):
                if d == 0:
                    tk.Frame(self._days_frame, bg="#fff", width=28, height=24).grid(row=row, column=col, padx=1, pady=1)
                    continue
                btn = tk.Label(
                    self._days_frame, text=str(d), width=3, font=("Segoe UI", 9),
                    bg="#fff", fg="#333"
                )
                btn.grid(row=row, column=col, padx=1, pady=1)
                if self._year == today.year and self._month == today.month and d == today.day:
                    btn.configure(bg="#E3F2FD", fg="#1976D2")
                if d in due_days:
                    btn.configure(bg="#C8E6C9", fg="#2E7D32")  # Green for days with due notes
                self._day_buttons.append(btn)

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

    def refresh(self) -> None:
        """Call when notes change to update due-date highlights."""
        self._refresh_calendar()
