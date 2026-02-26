"""
NoteCard - A reusable widget representing a single sticky note (tkinter).
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime

from models.note import Note


class NoteCard(tk.Frame):
    """Sticky note card with title, content, status dropdown, color picker, and delete."""

    MIN_WIDTH = 220
    MIN_HEIGHT = 180
    MAX_WIDTH = 500
    MAX_HEIGHT = 600

    def __init__(self, parent, note: Note, viewmodel, on_delete=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.note = note
        self.viewmodel = viewmodel
        self.on_delete = on_delete
        self._resize_start: tuple[int, int, int, int] | None = None

        self._setup_ui()
        self._apply_color(note.color)
        self._apply_size()

    def _setup_ui(self) -> None:
        self.configure(bg="#f5f5f5")
        self.grid_propagate(False)
        self.pack_propagate(False)
        # Card frame with relief
        inner = tk.Frame(self, bg=self.note.color, relief=tk.RAISED, bd=1, highlightthickness=0)
        inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Header
        header = tk.Frame(inner, bg=self.note.color)
        header.pack(fill=tk.X, pady=(0, 6))

        self.title_var = tk.StringVar(value=self.note.title)
        self.title_edit = tk.Entry(header, textvariable=self.title_var, font=("Segoe UI", 12, "bold"),
                                   relief=tk.FLAT, bg=self.note.color)
        self.title_edit.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)
        self.title_var.trace_add("write", lambda *_: self._on_title_changed())

        btn_frame = tk.Frame(header, bg=self.note.color)
        btn_frame.pack(side=tk.RIGHT)

        self.color_btn = tk.Button(btn_frame, text="\u2699", width=2, relief=tk.FLAT, cursor="hand2",
                                   command=self._on_color_click)
        self.color_btn.pack(side=tk.LEFT, padx=2)

        self.delete_btn = tk.Button(btn_frame, text="\u00D7", width=2, relief=tk.FLAT, cursor="hand2",
                                    fg="#c00", command=lambda: self.on_delete and self.on_delete(self.note))
        self.delete_btn.pack(side=tk.LEFT)

        # Due date row
        self.meta_frame = tk.Frame(inner, bg=self.note.color)
        self.meta_frame.pack(fill=tk.X, pady=(0, 4))

        tk.Label(self.meta_frame, text="Due:", font=("Segoe UI", 9), bg=self.note.color, fg="#555").pack(side=tk.LEFT, padx=(0, 4))
        self.due_var = tk.StringVar(value=self.note.due_date or "")
        self.due_entry = tk.Entry(self.meta_frame, textvariable=self.due_var, font=("Segoe UI", 9),
                                  width=12, relief=tk.FLAT, bg=self.note.color)
        self.due_entry.pack(side=tk.LEFT, padx=(0, 2))
        self.due_var.trace_add("write", lambda *_: self._on_due_changed())
        tk.Button(self.meta_frame, text="...", relief=tk.FLAT, cursor="hand2", bg=self.note.color,
                 font=("Segoe UI", 9), command=self._pick_due_date).pack(side=tk.LEFT)

        # Status dropdown
        tk.Label(self.meta_frame, text="Status:", font=("Segoe UI", 9), bg=self.note.color, fg="#555").pack(side=tk.LEFT, padx=(12, 4))
        self._status_values = [label for _, label in Note.STATUS_CHOICES]
        self._status_var = tk.StringVar(value=self._label_for_status(self.note.status))
        self._status_dropdown = ttk.Combobox(
            self.meta_frame, textvariable=self._status_var, values=self._status_values,
            state="readonly", width=12, font=("Segoe UI", 9)
        )
        self._status_dropdown.pack(side=tk.LEFT, padx=(0, 4))
        self._status_dropdown.bind("<<ComboboxSelected>>", self._on_status_changed)

        # Content
        content_frame = tk.Frame(inner, bg=self.note.color)
        content_frame.pack(fill=tk.BOTH, expand=True)
        self.content_edit = tk.Text(content_frame, height=4, font=("Segoe UI", 10), relief=tk.FLAT,
                                    wrap=tk.WORD, bg=self.note.color, padx=2, pady=2)
        self.content_edit.pack(fill=tk.BOTH, expand=True)
        self.content_edit.insert("1.0", self.note.content)
        self.content_edit.bind("<KeyRelease>", lambda e: self._on_content_changed())

        # Resize grip - bottom-right corner
        self._resize_grip = tk.Frame(inner, bg=self.note.color, width=16, height=16, cursor="size")
        self._resize_grip.place(relx=1.0, rely=1.0, anchor=tk.SE)
        self._resize_grip.bind("<Button-1>", self._on_resize_start)
        self._resize_grip.bind("<B1-Motion>", self._on_resize_drag)
        self._resize_grip.bind("<ButtonRelease-1>", self._on_resize_end)

        self._apply_status_style()

    def _label_for_status(self, status: str) -> str:
        for value, label in Note.STATUS_CHOICES:
            if value == status:
                return label
        return "New"

    def _status_from_label(self, label: str) -> str:
        for value, lbl in Note.STATUS_CHOICES:
            if lbl == label:
                return value
        return Note.STATUS_NEW

    def sync_from_ui(self) -> None:
        """Sync current UI values to the note model (call before save on close)."""
        self.note.title = self.title_var.get()
        self.note.content = self.content_edit.get("1.0", tk.END).strip()
        self.note.due_date = self.due_var.get().strip() or None
        self.note.status = self._status_from_label(self._status_var.get())
        self.note.completed = self.note.status == Note.STATUS_COMPLETED

    def _on_title_changed(self) -> None:
        self.note.title = self.title_var.get()
        self.viewmodel.update_note(self.note)

    def _on_content_changed(self) -> None:
        self.note.content = self.content_edit.get("1.0", tk.END).strip()
        self.viewmodel.update_note(self.note)

    def _on_due_changed(self) -> None:
        self.note.due_date = self.due_var.get().strip() or None
        self.viewmodel.update_note(self.note)

    def _on_status_changed(self, event=None) -> None:
        self.note.status = self._status_from_label(self._status_var.get())
        self.note.completed = self.note.status == Note.STATUS_COMPLETED
        self.viewmodel.update_note(self.note)
        self._apply_status_style()

    def _apply_status_style(self) -> None:
        """Dim and strikethrough title when status is Completed."""
        if self.note.status != Note.STATUS_COMPLETED:
            if hasattr(self, "title_edit"):
                self.title_edit.configure(fg="#000", font=("Segoe UI", 12, "bold"))
            return
        # Completed: grey out and strikethrough title
        for w in self.winfo_children():
            self._set_fg_recursive(w, "#666")
        if hasattr(self, "title_edit"):
            self.title_edit.configure(fg="#666")
        try:
            self.title_edit.configure(font=("Segoe UI", 12, "bold overstrike"))
        except tk.TclError:
            self.title_edit.configure(font=("Segoe UI", 12, "bold"))

    def _set_fg_recursive(self, w, color: str) -> None:
        try:
            w.configure(fg=color)
        except (tk.TclError, AttributeError):
            pass
        for c in w.winfo_children():
            self._set_fg_recursive(c, color)

    def _pick_due_date(self) -> None:
        """Open a simple calendar popup to pick due date."""
        from views.date_picker import DatePickerDialog
        current = self.note.due_date
        try:
            if current:
                year, month, day = map(int, current.split("-"))
            else:
                t = datetime.now()
                year, month, day = t.year, t.month, t.day
        except (ValueError, AttributeError):
            t = datetime.now()
            year, month, day = t.year, t.month, t.day
        result = DatePickerDialog(self, year, month, day).result
        if result:
            self.due_var.set(result)
            self.note.due_date = result
            self.viewmodel.update_note(self.note)

    def _on_color_click(self) -> None:
        color = self.viewmodel.cycle_note_color(self.note)
        self._apply_color(color)

    def _apply_size(self) -> None:
        """Apply note width/height to the card."""
        w = max(self.MIN_WIDTH, min(self.MAX_WIDTH, self.note.width))
        h = max(self.MIN_HEIGHT, min(self.MAX_HEIGHT, self.note.height))
        self.note.width, self.note.height = w, h
        self.configure(width=w, height=h)

    def _on_resize_start(self, event) -> None:
        self._resize_start = (event.x_root, event.y_root, self.note.width, self.note.height)

    def _on_resize_drag(self, event) -> None:
        if self._resize_start is None:
            return
        dx = event.x_root - self._resize_start[0]
        dy = event.y_root - self._resize_start[1]
        w = max(self.MIN_WIDTH, min(self.MAX_WIDTH, self._resize_start[2] + dx))
        h = max(self.MIN_HEIGHT, min(self.MAX_HEIGHT, self._resize_start[3] + dy))
        self.note.width, self.note.height = int(w), int(h)
        self.configure(width=self.note.width, height=self.note.height)
        self.viewmodel.update_note(self.note)

    def _on_resize_end(self, event) -> None:
        self._resize_start = None

    def _apply_color(self, color: str) -> None:
        self.note.color = color
        for w in self.winfo_children():
            self._set_bg_recursive(w, color)
        if hasattr(self, "content_edit"):
            self.content_edit.configure(bg=color)
        if hasattr(self, "title_edit"):
            self.title_edit.configure(bg=color)
        if hasattr(self, "color_btn"):
            self.color_btn.configure(bg=color)
        if hasattr(self, "delete_btn"):
            self.delete_btn.configure(bg=color)
        if hasattr(self, "_resize_grip"):
            self._resize_grip.configure(bg=color)
        if hasattr(self, "due_entry"):
            self.due_entry.configure(bg=color)
        if hasattr(self, "meta_frame"):
            self.meta_frame.configure(bg=color)
        # Update inner frame
        for c in self.winfo_children():
            if isinstance(c, tk.Frame):
                c.configure(bg=color)
                for cc in c.winfo_children():
                    self._set_bg_recursive(cc, color)

    def _set_bg_recursive(self, w, color: str) -> None:
        try:
            w.configure(bg=color)
        except tk.TclError:
            pass
        for c in w.winfo_children():
            self._set_bg_recursive(c, color)
