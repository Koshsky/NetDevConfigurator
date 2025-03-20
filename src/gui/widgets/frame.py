"""Custom frame widget."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict

from config import config

from gui.styles import (
    BACKGROUND_COLOR,
    BORDER_WIDTH,
    PADDING,
)


class CustomFrame(ttk.Frame):
    """Custom frame widget with improved styling."""

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
        super().__init__(parent, **kwargs)
        self._setup_style()
        self.current_row = 0
        self.current_column = 0

    def _setup_style(self):
        """Setup the frame style."""
        style = ttk.Style()
        style.configure(
            "Custom.TFrame",
            background=config.app.background_color,
            relief="flat",
            borderwidth=config.app.border_width,
            padding=config.app.padding,
        )
        self.configure(style="Custom.TFrame")

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
