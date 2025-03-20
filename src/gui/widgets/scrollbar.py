"""Custom scrollbar widget."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict

from config import config


class CustomScrollbar(ttk.Scrollbar):
    """Custom scrollbar widget with improved styling."""

    def __init__(self, master, **kwargs):
        """Initialize the custom scrollbar.

        Args:
            master: The parent widget.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(master, **kwargs)
        self._setup_style()

    def _setup_style(self):
        """Setup the scrollbar style."""
        style = ttk.Style()
        style.configure(
            "Custom.Vertical.TScrollbar",
            background=config.app.second_color,
            troughcolor=config.app.second_color,
            width=10,
            arrowsize=13,
        )
        self.configure(style="Custom.Vertical.TScrollbar")

    def set_orientation(self, orient: str) -> None:
        """Set the scrollbar orientation.

        Args:
            orient: The new orientation ("vertical" or "horizontal").
        """
        # Обновляем стиль при изменении ориентации
        scrollbar_style = (
            "Light.Vertical.TScrollbar"
            if orient == "vertical"
            else "Light.Horizontal.TScrollbar"
        )
        self.configure(orient=orient, style=scrollbar_style)
