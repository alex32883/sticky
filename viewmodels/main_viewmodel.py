"""
MainViewModel - Handles logic for notes: add, delete, save, load.
Implements observable pattern via callbacks (no external GUI framework).
"""

from models.note import Note
from models.task_item import TaskItem
from services.storage import StorageService


class MainViewModel:
    """ViewModel for the main window. Manages notes collection and persistence."""

    def __init__(self):
        self._notes: list[Note] = []
        self._storage = StorageService()
        self._on_notes_changed_callbacks: list[callable] = []
        self.load_notes()  # Load from local directory (exe dir when frozen) on start

    def on_notes_changed(self, callback: callable) -> None:
        """Register a callback to run when notes change."""
        self._on_notes_changed_callbacks.append(callback)

    def _notify_notes_changed(self) -> None:
        for cb in self._on_notes_changed_callbacks:
            cb()

    @property
    def notes(self) -> list[Note]:
        """Get list of notes."""
        return self._notes

    def add_note(self) -> Note:
        """Create and add a new note, save, and notify UI."""
        note = Note()
        self._notes.append(note)
        self._save_and_notify()
        return note

    def delete_note(self, note: Note) -> None:
        """Remove a note, save, and notify UI."""
        if note in self._notes:
            self._notes.remove(note)
            self._save_and_notify()

    def add_task_to_note(self, note: Note, text: str = "") -> TaskItem:
        """Add a checklist item to a note."""
        task = TaskItem(text=text)
        note.tasks.append(task)
        self._save_only()
        return task

    def remove_task_from_note(self, note: Note, task: TaskItem) -> None:
        """Remove a checklist item from a note."""
        if task in note.tasks:
            note.tasks.remove(task)
            self._save_only()

    def update_note(self, note: Note) -> None:
        """Mark note as updated and save (title, content, task checkboxes)."""
        self._save_only()

    def cycle_note_color(self, note: Note) -> str:
        """Cycle note color and save."""
        color = note.cycle_color()
        self._save_only()
        return color

    def load_notes(self) -> None:
        """Load notes from storage."""
        self._notes = self._storage.load_notes()
        if not self._notes:
            self._notes.append(Note(title="Welcome!", content="Add more notes with the + button."))
            self._save_and_notify()
        else:
            self._notify_notes_changed()

    def _save_only(self) -> None:
        """Save to storage without notifying (avoids repopulating UI on each keystroke)."""
        self._storage.save_notes(self._notes)

    def save_all(self) -> None:
        """Force save all notes to default storage."""
        self._storage.save_notes(self._notes)

    def export_to_file(self, path: str) -> bool:
        """Export notes to a file. Returns True on success."""
        try:
            self._storage.save_notes_to_path(path, self._notes)
            return True
        except (IOError, OSError):
            return False

    def load_from_file(self, path: str) -> bool:
        """Load notes from a file, replacing current notes. Saves to default location."""
        try:
            notes = self._storage.load_notes_from_path(path)
            if notes:
                self._notes = notes
                self._storage.save_notes(self._notes)  # Persist to default location
                self._notify_notes_changed()
                return True
            return False
        except (IOError, OSError):
            return False

    def load_from_local_directory(self) -> bool:
        """Load notes from notes.json in the local directory (exe dir when frozen).
        Returns True if the file existed and was loaded, False otherwise.
        """
        if not self._storage.local_notes_exists():
            return False
        path = str(self._storage.get_local_notes_path())
        return self.load_from_file(path)

    def load_from_default(self) -> None:
        """Reload notes from default storage location."""
        self.load_notes()

    def _save_and_notify(self) -> None:
        """Save to storage and notify listeners (repopulate notes list)."""
        self._storage.save_notes(self._notes)
        self._notify_notes_changed()
