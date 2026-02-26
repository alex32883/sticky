"""
TaskItem model - Represents a single checklist item within a note.
"""


class TaskItem:
    """A checklist item with text and completion state."""

    def __init__(self, text: str = "", checked: bool = False, task_id: str | None = None):
        self.id = task_id or self._generate_id()
        self.text = text
        self.checked = checked

    def _generate_id(self) -> str:
        """Generate a unique ID for the task."""
        import uuid
        return str(uuid.uuid4())[:8]

    def to_dict(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        return {
            "id": self.id,
            "text": self.text,
            "checked": self.checked,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TaskItem":
        """Deserialize from dictionary."""
        return cls(
            text=data.get("text", ""),
            checked=data.get("checked", False),
            task_id=data.get("id"),
        )
