"""Custom label widget."""

from tkinter import ttk
from typing import Any, Dict

from gui.styles import (
    BACKGROUND_COLOR,
    FONT,
    PADDING,
)


class CustomLabel(ttk.Label):
    """Custom label widget with additional functionality."""

    def __init__(
        self,
        parent: Any,
        text: str = "",
        **kwargs: Dict[str, Any],
    ) -> None:
        """Initialize the CustomLabel.

        Args:
            parent: The parent widget.
            text: The text to display.
            **kwargs: Additional keyword arguments.
        """
        # Создаем стиль для метки
        style = ttk.Style()
        style.configure(
            "Light.TLabel",
            background=BACKGROUND_COLOR,
            foreground="black",
            padding=PADDING,
            font=FONT,
        )

        super().__init__(parent, text=text, style="Light.TLabel", **kwargs)

    def set_text(self, text: str) -> None:
        """Set the label text.

        Args:
            text: The new text to display.
        """
        self.configure(text=text)

    def set_style(self, style: str) -> None:
        """Set the label style.

        Args:
            style: The style to apply.
        """
        self.configure(style=style)
