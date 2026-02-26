"""
Storage Service - Handles JSON persistence for notes.
Uses exe/script directory when running as executable for reliable save/load.
"""

import json
import os
import sys
from pathlib import Path

from models.note import Note


class StorageService:
    """Manages loading and saving notes to a local JSON file."""

    FILENAME = "notes.json"
    APP_FOLDER = "StickyNotes"

    def _get_storage_path(self) -> Path:
        """Get the full path to the notes JSON file.
        When frozen (exe): use same folder as executable.
        When script: use %AppData%\\StickyNotes for consistency.
        """
        if getattr(sys, "frozen", False):
            # Running as PyInstaller executable - store next to exe
            base = Path(sys.executable).resolve().parent
        else:
            # Running as script - use AppData
            app_data = os.environ.get("APPDATA", os.path.expanduser("~"))
            base = Path(app_data) / self.APP_FOLDER
        base.mkdir(parents=True, exist_ok=True)
        return base / self.FILENAME

    def get_local_notes_path(self) -> Path:
        """Get the path to notes.json in the local directory (exe dir when frozen)."""
        return self._get_storage_path()

    def local_notes_exists(self) -> bool:
        """Check if notes.json exists in the local directory."""
        return self.get_local_notes_path().exists()

    def load_notes(self) -> list[Note]:
        """Load notes from JSON file. Returns empty list if file doesn't exist."""
        path = self._get_storage_path()
        if not path.exists():
            return []

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            notes_data = data.get("notes", [])
            return [Note.from_dict(n) for n in notes_data]
        except (json.JSONDecodeError, IOError):
            return []

    def save_notes(self, notes: list[Note]) -> None:
        """Save notes to default JSON file."""
        self.save_notes_to_path(self._get_storage_path(), notes)

    def save_notes_to_path(self, path: str | Path, notes: list[Note]) -> None:
        """Save notes to a specific file path."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {"notes": [n.to_dict() for n in notes]}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_notes_from_path(self, path: str | Path) -> list[Note]:
        """Load notes from a specific file path."""
        path = Path(path)
        if not path.exists():
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Note.from_dict(n) for n in data.get("notes", [])]
        except (json.JSONDecodeError, IOError):
            return []
