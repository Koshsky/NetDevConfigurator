"""Custom scrollbar widget."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, Optional

from gui.styles import (
    ENTRY_BACKGROUND,
    FONT,
    PADDING,
    BORDER_WIDTH,
)


class CustomScrollbar(ttk.Scrollbar):
    """Custom scrollbar widget with additional functionality."""

    def __init__(
        self,
        parent: Any,
        orient: str = "vertical",
        **kwargs: Dict[str, Any],
    ) -> None:
        """Initialize the CustomScrollbar.

        Args:
            parent: The parent widget.
            orient: The orientation of the scrollbar ("vertical" or "horizontal").
            **kwargs: Additional keyword arguments.
        """
        # Создаем стиль для полосы прокрутки
        style = ttk.Style()
        style.configure(
            "Light.Vertical.TScrollbar",
            background=ENTRY_BACKGROUND,
            troughcolor=ENTRY_BACKGROUND,
            width=10,
            arrowsize=13,
            relief="flat",
            borderwidth=BORDER_WIDTH,
        )
        style.configure(
            "Light.Horizontal.TScrollbar",
            background=ENTRY_BACKGROUND,
            troughcolor=ENTRY_BACKGROUND,
            width=10,
            arrowsize=13,
            relief="flat",
            borderwidth=BORDER_WIDTH,
        )

        # Выбираем стиль в зависимости от ориентации
        scrollbar_style = (
            "Light.Vertical.TScrollbar"
            if orient == "vertical"
            else "Light.Horizontal.TScrollbar"
        )

        super().__init__(parent, orient=orient, style=scrollbar_style, **kwargs)

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
