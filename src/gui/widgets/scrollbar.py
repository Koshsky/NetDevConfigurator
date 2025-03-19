"""Custom scrollbar widget."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, Optional


class CustomScrollbar(ttk.Scrollbar):
    """Custom scrollbar widget with additional functionality."""

    def __init__(
        self,
        parent: Any,
        orient: str = "vertical",
        style: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        """Initialize the CustomScrollbar.

        Args:
            parent: The parent widget.
            orient: The orientation of the scrollbar ("vertical" or "horizontal").
            style: The style to apply to the scrollbar.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(parent, orient=orient, **kwargs)

        # Применяем стиль если указан
        if style:
            self.configure(style=style)

    def set_style(self, style: str) -> None:
        """Set the scrollbar style.

        Args:
            style: The style to apply.
        """
        self.configure(style=style)

    def set_orientation(self, orient: str) -> None:
        """Set the scrollbar orientation.

        Args:
            orient: The new orientation ("vertical" or "horizontal").
        """
        self.configure(orient=orient)
