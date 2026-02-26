"""
Note model - Represents a single sticky note with title, content, tasks, and color.
"""

from .task_item import TaskItem


class Note:
    """A sticky note containing title, content, color, and checklist items."""

    # Available colors for notes (hex values)
    COLORS = [
        "#FFF9C4",  # Yellow
        "#F8BBD9",  # Pink
        "#BBDEFB",  # Blue
        "#C8E6C9",  # Green
        "#E1BEE7",  # Purple
    ]

    DEFAULT_WIDTH = 280
    DEFAULT_HEIGHT = 280

    def __init__(
        self,
        title: str = "New Note",
        content: str = "",
        color: str | None = None,
        note_id: str | None = None,
        tasks: list[TaskItem] | None = None,
        width: int | None = None,
        height: int | None = None,
    ):
        self.id = note_id or self._generate_id()
        self.title = title
        self.content = content
        self.color = color or self.COLORS[0]
        self.tasks = tasks or []
        self.width = width if width is not None else self.DEFAULT_WIDTH
        self.height = height if height is not None else self.DEFAULT_HEIGHT

    def _generate_id(self) -> str:
        """Generate a unique ID for the note."""
        import uuid
        return str(uuid.uuid4())[:8]

    def cycle_color(self) -> str:
        """Cycle to the next color and return it."""
        idx = self.COLORS.index(self.color) if self.color in self.COLORS else 0
        self.color = self.COLORS[(idx + 1) % len(self.COLORS)]
        return self.color

    def to_dict(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "color": self.color,
            "tasks": [t.to_dict() for t in self.tasks],
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        """Deserialize from dictionary."""
        tasks_data = data.get("tasks", [])
        tasks = [TaskItem.from_dict(t) for t in tasks_data]
        w = data.get("width", cls.DEFAULT_WIDTH)
        h = data.get("height", cls.DEFAULT_HEIGHT)
        size = max(w or cls.DEFAULT_WIDTH, h or cls.DEFAULT_HEIGHT)
        return cls(
            title=data.get("title", "New Note"),
            content=data.get("content", ""),
            color=data.get("color", cls.COLORS[0]),
            note_id=data.get("id"),
            tasks=tasks,
            width=size,
            height=size,
        )
