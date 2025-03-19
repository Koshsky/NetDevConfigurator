"""Custom frame widget."""

from tkinter import ttk
from typing import Any, Dict

from gui.styles import (
    BACKGROUND_COLOR,
    BORDER_WIDTH,
    PADDING,
)


class CustomFrame(ttk.Frame):
    """Custom frame widget with additional functionality."""

    def __init__(
        self,
        parent: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        """Initialize the CustomFrame.

        Args:
            parent: The parent widget.
            **kwargs: Additional keyword arguments.
        """
        # Создаем стиль для фрейма
        style = ttk.Style()
        style.configure(
            "Light.TFrame",
            background=BACKGROUND_COLOR,
            relief="flat",
            borderwidth=BORDER_WIDTH,
            padding=PADDING,
        )

        super().__init__(parent, style="Light.TFrame", **kwargs)
        self.current_row = 0
        self.current_column = 0

    def get_current_position(self) -> tuple[int, int]:
        """Get the current position in the frame.

        Returns:
            tuple[int, int]: The current row and column.
        """
        return self.current_row, self.current_column

    def set_current_position(self, row: int, column: int) -> None:
        """Set the current position in the frame.

        Args:
            row: The row to set.
            column: The column to set.
        """
        self.current_row = row
        self.current_column = column

    def increment_row(self) -> None:
        """Increment the current row."""
        self.current_row += 1

    def increment_column(self) -> None:
        """Increment the current column."""
        self.current_column += 1

    def reset_position(self) -> None:
        """Reset the current position to (0, 0)."""
        self.current_row = 0
        self.current_column = 0
