"""Custom button widget."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict, Optional
from config import config


class CustomButton(ttk.Button):
    """Custom button widget with additional functionality."""

    def __init__(
        self,
        parent: Any,
        text: str = "",
        command: Optional[Callable] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        """Initialize the CustomButton.

        Args:
            parent: The parent widget.
            text: The text to display on the button.
            command: The command to execute when clicked.
            **kwargs: Additional keyword arguments.
        """
        # Создаем стиль для кнопки
        style = ttk.Style()
        style.configure(
            "Custom.TButton",
            background=config.app.color3,
            foreground=config.app.text_color,
            padding=config.app.padding,
            relief="flat",
            borderwidth=1,
            font=config.app.font,
        )

        # Настраиваем эффекты при наведении и нажатии
        style.map(
            "Custom.TButton",
            background=[
                ("active", config.app.color4),
                ("pressed", config.app.color4),
                ("disabled", config.app.color4),
            ],
            foreground=[
                ("active", config.app.text_color),
                ("pressed", config.app.text_color),
                ("disabled", config.app.color3),
            ],
            relief=[("pressed", "sunken")],
            borderwidth=[("active", 2)],
        )

        super().__init__(
            parent, text=text, command=command, style="Custom.TButton", **kwargs
        )

    def set_text(self, text: str) -> None:
        """Set the button text.

        Args:
            text: The new text to display.
        """
        self.configure(text=text)

    def set_command(self, command: Callable) -> None:
        """Set the button command.

        Args:
            command: The new command to execute.
        """
        self.configure(command=command)

    def set_enabled(self, enabled: bool = True) -> None:
        """Set the button enabled state.

        Args:
            enabled: Whether to enable the button.
        """
        self.configure(state=tk.NORMAL if enabled else tk.DISABLED)
