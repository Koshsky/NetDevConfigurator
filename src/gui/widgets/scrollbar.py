"""Custom scrollbar widget."""

from tkinter import ttk

from config import config


class CustomScrollbar(ttk.Scrollbar):
    """Custom scrollbar widget with improved styling."""

    def __init__(self, master, **kwargs):
        """Initialize the custom scrollbar.

        Args:
            master: The parent widget.
            **kwargs: Additional keyword arguments.
        """
        style = ttk.Style()
        style.configure(
            "Custom.Vertical.TScrollbar",
            gripcount=1,
            background=config.app.color3,
            troughcolor=config.app.color3,
            bordercolor="blue",
            arrowcolor="white",
        )
        super().__init__(master, style="Custom.Vertical.TScrollbar", **kwargs)

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
