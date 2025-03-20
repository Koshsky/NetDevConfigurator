"""Custom entry widget."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict

from config import config


class CustomEntry(ttk.Entry):
    """Custom entry widget with improved styling."""

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
        super().__init__(parent, **kwargs)
        self._setup_style()

    def _setup_style(self):
        """Setup the entry style."""
        style = ttk.Style()
        style.configure(
            "Custom.TEntry",
            background=config.app.background_color,
            foreground=config.app.foreground_color,
            font=config.app.font,
            padding=config.app.padding,
        )
        self.configure(style="Custom.TEntry")

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
