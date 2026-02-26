"""
NoteCard - A reusable widget representing a single sticky note (tkinter).
"""

import tkinter as tk
from tkinter import ttk

from models.note import Note
from models.task_item import TaskItem


class NoteCard(tk.Frame):
    """Sticky note card with title, content, task list, color picker, and delete."""

    MIN_WIDTH = 220
    MIN_HEIGHT = 180
    MAX_WIDTH = 500
    MAX_HEIGHT = 600

    def __init__(self, parent, note: Note, viewmodel, on_delete=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.note = note
        self.viewmodel = viewmodel
        self.on_delete = on_delete
        self._task_widgets: list[tuple[tk.Checkbutton, tk.Entry]] = []
        self._task_vars: list[tk.BooleanVar] = []
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

        # Content
        content_frame = tk.Frame(inner, bg=self.note.color)
        content_frame.pack(fill=tk.BOTH, expand=True)
        self.content_edit = tk.Text(content_frame, height=4, font=("Segoe UI", 10), relief=tk.FLAT,
                                    wrap=tk.WORD, bg=self.note.color, padx=2, pady=2)
        self.content_edit.pack(fill=tk.BOTH, expand=True)
        self.content_edit.insert("1.0", self.note.content)
        self.content_edit.bind("<KeyRelease>", lambda e: self._on_content_changed())

        # Tasks
        self.tasks_frame = tk.Frame(inner, bg=self.note.color)
        self.tasks_frame.pack(fill=tk.X, pady=(6, 0))

        add_btn = tk.Button(self.tasks_frame, text="+ Add task", relief=tk.FLAT, cursor="hand2",
                            bg=self.note.color, fg="#666", font=("Segoe UI", 10),
                            command=self._add_task)
        add_btn.pack(anchor=tk.W)

        self._rebuild_tasks()

        # Resize grip - bottom-right corner
        self._resize_grip = tk.Frame(inner, bg=self.note.color, width=16, height=16, cursor="size")
        self._resize_grip.place(relx=1.0, rely=1.0, anchor=tk.SE)
        self._resize_grip.bind("<Button-1>", self._on_resize_start)
        self._resize_grip.bind("<B1-Motion>", self._on_resize_drag)
        self._resize_grip.bind("<ButtonRelease-1>", self._on_resize_end)

    def sync_from_ui(self) -> None:
        """Sync current UI values to the note model (call before save on close)."""
        self.note.title = self.title_var.get()
        self.note.content = self.content_edit.get("1.0", tk.END).strip()
        for i, (cb, entry) in enumerate(self._task_widgets):
            if i < len(self.note.tasks):
                self.note.tasks[i].text = entry.get()
                self.note.tasks[i].checked = self._task_vars[i].get()

    def _on_title_changed(self) -> None:
        self.note.title = self.title_var.get()
        self.viewmodel.update_note(self.note)

    def _on_content_changed(self) -> None:
        self.note.content = self.content_edit.get("1.0", tk.END).strip()
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
        if hasattr(self, "tasks_frame"):
            self.tasks_frame.configure(bg=color)
        if hasattr(self, "color_btn"):
            self.color_btn.configure(bg=color)
        if hasattr(self, "delete_btn"):
            self.delete_btn.configure(bg=color)
        if hasattr(self, "_resize_grip"):
            self._resize_grip.configure(bg=color)
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

    def _add_task(self) -> None:
        self.viewmodel.add_task_to_note(self.note, "New task")
        self._rebuild_tasks()

    def _rebuild_tasks(self) -> None:
        for row in self._task_widgets:
            cb, entry = row
            cb.destroy()
            entry.destroy()
        self._task_widgets.clear()
        self._task_vars.clear()

        for task in self.note.tasks:
            var = tk.BooleanVar(value=task.checked)
            self._task_vars.append(var)

            row_frame = tk.Frame(self.tasks_frame, bg=self.note.color)
            row_frame.pack(anchor=tk.W, pady=1, fill=tk.X)

            def make_cb_cmd(t, v, e):
                def cmd():
                    t.checked = v.get()
                    self.viewmodel.update_note(self.note)
                    self._update_task_entry_style(e, t.checked)
                return cmd

            entry_var = tk.StringVar(value=task.text)
            entry = tk.Entry(row_frame, textvariable=entry_var, font=("Segoe UI", 10),
                             relief=tk.FLAT, bg=self.note.color)

            cb = tk.Checkbutton(row_frame, variable=var, command=make_cb_cmd(task, var, entry),
                                bg=self.note.color, relief=tk.FLAT)
            cb.pack(side=tk.LEFT)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0), ipady=1)

            def on_task_text_changed(*_):
                task.text = entry_var.get()
                self.viewmodel.update_note(self.note)
            entry_var.trace_add("write", on_task_text_changed)
            self._update_task_entry_style(entry, task.checked)
            self._task_widgets.append((cb, entry))

    def _update_task_entry_style(self, entry: tk.Entry, checked: bool) -> None:
        if checked:
            entry.configure(fg="#666")
            try:
                entry.configure(font=("Segoe UI", 10, "overstrike"))
            except tk.TclError:
                entry.configure(font=("Segoe UI", 10))
        else:
            entry.configure(fg="#000", font=("Segoe UI", 10))
