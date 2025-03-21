"""Custom text widget."""

import tkinter as tk
from typing import Any, Dict

from config import config


class CustomText(tk.Text):
    """Custom text widget with improved styling."""

    def __init__(
        self,
        parent: Any,
        width: int = 40,
        height: int = 10,
        wrap: str = "word",
        **kwargs: Dict[str, Any],
    ) -> None:
        """Initialize the CustomText.

        Args:
            parent: The parent widget.
            width: The width of the text widget.
            height: The height of the text widget.
            wrap: The wrap mode for text.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            parent,
            width=width,
            height=height,
            wrap=wrap,
            bg=config.app.color4,
            fg=config.app.text_color,
            font=config.app.font,
            padx=config.app.padding[0],
            pady=config.app.padding[1],
            relief="flat",
            borderwidth=config.app.border_width,
            **kwargs,
        )

    def set_text(self, text: str) -> None:
        """Set the text widget content.

        Args:
            text: The new text to set.
        """
        self.delete(1.0, tk.END)
        self.insert(1.0, text)

    def get_text(self) -> str:
        """Get the text widget content.

        Returns:
            str: The current text.
        """
        return self.get(1.0, tk.END).strip()

    def clear(self) -> None:
        """Clear the text widget content."""
        self.delete(1.0, tk.END)

    def set_readonly(self, readonly: bool = True) -> None:
        """Set the text widget to readonly mode.

        Args:
            readonly: Whether to make the widget readonly.
        """
        self.configure(state=tk.DISABLED if readonly else tk.NORMAL)
