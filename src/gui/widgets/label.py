"""Custom label widget."""

from tkinter import ttk
from typing import Any, Dict

from config import config


class CustomLabel(ttk.Label):
    """Custom label widget with improved styling."""

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
        super().__init__(parent, text=text, **kwargs)
        self._setup_style()

    def _setup_style(self):
        """Setup the label style."""
        style = ttk.Style()
        style.configure(
            "Custom.TLabel",
            background=config.app.background_color,
            foreground="black",
            font=config.app.font,
            padding=config.app.padding,
        )
        self.configure(style="Custom.TLabel")

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
