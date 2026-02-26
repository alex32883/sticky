"""
MainWindow - Dashboard displaying all sticky notes in a grid layout (tkinter).
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from views.note_card import NoteCard
from views.calendar_widget import CalendarWidget


class MainWindow:
    """Main dashboard window with notes grid and floating add button."""

    def __init__(self, viewmodel):
        self.viewmodel = viewmodel
        self._note_cards: dict[str, NoteCard] = {}
        self._root = tk.Tk()
        self._root.title("Sticky Notes")
        self._root.minsize(500, 400)
        self._root.configure(bg="#f5f5f5")

        self._setup_ui()
        self._populate_notes()
        viewmodel.on_notes_changed(self._on_notes_changed)
        viewmodel.on_calendar_refresh(self._on_calendar_refresh)
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._root.geometry("900x600")
        self._center_on_screen()

    def _setup_ui(self) -> None:
        # Toolbar: Save, Export, Load
        toolbar = tk.Frame(self._root, bg="#f5f5f5", pady=8, padx=16)
        toolbar.pack(fill=tk.X)

        save_btn = tk.Button(toolbar, text="Save", command=self._on_save,
                             relief=tk.FLAT, bg="#2196F3", fg="white", padx=12, pady=4, cursor="hand2")
        save_btn.pack(side=tk.LEFT, padx=4)

        export_btn = tk.Button(toolbar, text="Export", command=self._on_export,
                               relief=tk.FLAT, bg="#4CAF50", fg="white", padx=12, pady=4, cursor="hand2")
        export_btn.pack(side=tk.LEFT, padx=4)

        load_btn = tk.Button(toolbar, text="Load", command=self._on_load,
                             relief=tk.FLAT, bg="#FF9800", fg="white", padx=12, pady=4, cursor="hand2")
        load_btn.pack(side=tk.LEFT, padx=4)

        main_frame = tk.Frame(self._root, padx=16, pady=8, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left: calendar sidebar
        calendar_panel = tk.Frame(main_frame, width=200, bg="#f5f5f5")
        calendar_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 16))
        calendar_panel.pack_propagate(False)
        self._calendar = CalendarWidget(
            calendar_panel,
            get_notes_with_due=lambda: self.viewmodel.notes,
        )
        self._calendar.pack(fill=tk.BOTH, expand=True)

        # Right: Canvas + scrollbar for notes
        canvas_frame = tk.Frame(main_frame, bg="#f5f5f5")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(canvas_frame, bg="#f5f5f5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)

        self._notes_container = tk.Frame(canvas, bg="#f5f5f5")
        self._canvas_window_id = canvas.create_window((0, 0), window=self._notes_container, anchor=tk.NW)
        self._notes_container.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: self._on_canvas_configure(e, canvas))

        self._canvas = canvas

        # FAB - Floating Add Button
        self._fab = tk.Button(self._root, text="+", font=("Segoe UI", 24, "bold"),
                              bg="#2196F3", fg="white", relief=tk.FLAT, cursor="hand2",
                              activebackground="#1976D2", activeforeground="white",
                              width=3, height=1, command=self._on_add_note)
        self._fab.place(relx=1.0, rely=1.0, anchor=tk.SE, x=-24, y=-24)

    def _on_canvas_configure(self, event, canvas: tk.Canvas) -> None:
        """Update scroll region and reposition notes on resize."""
        canvas.itemconfig(self._canvas_window_id, width=event.width)
        self._relayout_cards()

    def _center_on_screen(self) -> None:
        self._root.update_idletasks()
        w, h = self._root.winfo_width(), self._root.winfo_height()
        x = (self._root.winfo_screenwidth() - w) // 2
        y = (self._root.winfo_screenheight() - h) // 2
        self._root.geometry(f"+{x}+{y}")

    def _populate_notes(self) -> None:
        self._clear_cards()
        for note in self.viewmodel.notes:
            self._add_card(note)
        self._relayout_cards()

    def _clear_cards(self) -> None:
        for card in self._note_cards.values():
            card.destroy()
        self._note_cards.clear()

    def _relayout_cards(self) -> None:
        """Arrange cards in a flow grid."""
        for w in self._notes_container.winfo_children():
            w.grid_forget()
        cards = list(self._note_cards.values())
        if not cards:
            return
        cols = max(1, self._root.winfo_width() // 340)
        for i, card in enumerate(cards):
            row, col = i // cols, i % cols
            card.grid(row=row, column=col, padx=8, pady=8, sticky=tk.NW)

    def _add_card(self, note) -> None:
        card = NoteCard(self._notes_container, note, self.viewmodel, on_delete=self._on_delete_note)
        self._note_cards[note.id] = card

    def _on_add_note(self) -> None:
        self.viewmodel.add_note()

    def _on_delete_note(self, note) -> None:
        self.viewmodel.delete_note(note)

    def _on_notes_changed(self) -> None:
        self._populate_notes()
        self._on_calendar_refresh()

    def _on_calendar_refresh(self) -> None:
        if hasattr(self, "_calendar") and self._calendar.winfo_exists():
            self._calendar.refresh()

    def _sync_all_cards(self) -> None:
        """Sync UI values from all note cards to the model."""
        for card in self._note_cards.values():
            card.sync_from_ui()

    def _on_save(self) -> None:
        """Save all notes to default location."""
        self._sync_all_cards()
        self.viewmodel.save_all()
        if hasattr(self, "_calendar") and self._calendar.winfo_exists():
            self._calendar.refresh()
        messagebox.showinfo("Saved", "Notes saved successfully.")

    def _on_export(self) -> None:
        """Export all notes to a user-chosen file."""
        self._sync_all_cards()
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export notes"
        )
        if path and self.viewmodel.export_to_file(path):
            messagebox.showinfo("Exported", f"Notes exported to:\n{path}")
        elif path:
            messagebox.showerror("Export failed", "Could not export notes.")

    def _on_load(self) -> None:
        """Load notes: first try local directory (notes.json next to exe), else file dialog."""
        self._sync_all_cards()
        # Try loading from local directory (exe dir when frozen, AppData when script)
        if self.viewmodel.load_from_local_directory():
            self._populate_notes()
            messagebox.showinfo("Loaded", "Notes loaded from local directory.")
            return
        # Fall back to file dialog
        path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load notes"
        )
        if path:
            if self.viewmodel.load_from_file(path):
                self._populate_notes()
                messagebox.showinfo("Loaded", "Notes loaded successfully.")
            else:
                messagebox.showerror("Load failed", "Could not load notes from file.")

    def _on_close(self) -> None:
        """Save all notes and close the app."""
        self._sync_all_cards()
        self.viewmodel.save_all()
        self._root.destroy()

    def run(self) -> None:
        self._root.mainloop()
