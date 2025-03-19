"""Custom entry widget."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, Optional

from gui.styles import (
    ENTRY_BACKGROUND,
    FONT,
    PADDING,
    BORDER_WIDTH,
)


class CustomEntry(ttk.Entry):
    """Custom entry widget with additional functionality."""

    def __init__(
        self,
        parent: Any,
        **kwargs: Dict[str, Any],
    ) -> None:
        """Initialize the CustomEntry.

        Args:
            parent: The parent widget.
            **kwargs: Additional keyword arguments.
        """
        # Создаем стиль для поля ввода
        style = ttk.Style()
        style.configure(
            "Light.TEntry",
            fieldbackground=ENTRY_BACKGROUND,
            background=ENTRY_BACKGROUND,
            foreground="black",
            insertcolor="black",
            relief="flat",
            borderwidth=BORDER_WIDTH,
            padding=PADDING,
            font=FONT,
        )

        super().__init__(parent, style="Light.TEntry", **kwargs)

    def set_text(self, text: str) -> None:
        """Set the entry text.

        Args:
            text: The new text to set.
        """
        self.delete(0, tk.END)
        self.insert(0, text)

    def get_text(self) -> str:
        """Get the entry text.

        Returns:
            str: The current text.
        """
        return self.get()

    def clear(self) -> None:
        """Clear the entry text."""
        self.delete(0, tk.END)

    def set_style(self, style: str) -> None:
        """Set the entry style.

        Args:
            style: The style to apply.
        """
        self.configure(style=style)
