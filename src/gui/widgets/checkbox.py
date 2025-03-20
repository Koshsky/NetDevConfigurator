"""Custom checkbox widget."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, Optional

from config import config


class CustomCheckbox(ttk.Checkbutton):
    """Custom checkbox widget with improved styling."""

    def __init__(self, master, **kwargs):
        """Initialize the custom checkbox.

        Args:
            master: The parent widget.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(master, **kwargs)
        self._setup_style()

    def _setup_style(self):
        """Setup the checkbox style."""
        style = ttk.Style()
        style.configure(
            "Custom.TCheckbutton",
            background=config.app.background_color,
            foreground="black",
            font=config.app.font,
            padding=config.app.padding,
        )
        style.map(
            "Custom.TCheckbutton",
            background=[("selected", config.app.background_color)],
            foreground=[("selected", "black")],
        )
        self.configure(style="Custom.TCheckbutton")

    def set_text(self, text: str) -> None:
        """Set the checkbox text.

        Args:
            text: The new text to display.
        """
        self.configure(text=text)

    def set_checked(self, checked: bool) -> None:
        """Set the checkbox checked state.

        Args:
            checked: Whether to check the checkbox.
        """
        self.select() if checked else self.deselect()

    def is_checked(self) -> bool:
        """Get the checkbox checked state.

        Returns:
            bool: Whether the checkbox is checked.
        """
        return self.instate(['selected'])

    def set_style(self, style: str) -> None:
        """Set the checkbox style (ignored for tk.Checkbutton).

        Args:
            style: The style to apply (ignored).
        """
        pass

    def set_enabled(self, enabled: bool = True) -> None:
        """Set the checkbox enabled state.

        Args:
            enabled: Whether to enable the checkbox.
        """
        self.configure(state=tk.NORMAL if enabled else tk.DISABLED)
