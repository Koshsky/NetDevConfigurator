"""Custom text widget."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict

from gui.styles import (
    BORDER_WIDTH,
    ENTRY_BACKGROUND,
    FONT,
    PADDING,
)


class CustomText(tk.Text):
    """Custom text widget with additional functionality."""

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
        # Создаем стиль для текстового поля
        style = ttk.Style()
        style.configure(
            "Light.TText",
            background=ENTRY_BACKGROUND,
            foreground="black",
            insertbackground="black",
            relief="flat",
            borderwidth=BORDER_WIDTH,
            font=FONT,
            padding=PADDING,
        )

        super().__init__(
            parent,
            width=width,
            height=height,
            wrap=wrap,
            bg=ENTRY_BACKGROUND,
            fg="black",
            insertbackground="black",
            relief="flat",
            borderwidth=BORDER_WIDTH,
            font=FONT,
            padx=PADDING[0],
            pady=PADDING[1],
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
