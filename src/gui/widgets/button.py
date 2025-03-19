"""Custom button widget."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict, Optional


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
            "Green.TButton",
            background="#4CAF50",  # Основной зеленый
            foreground="white",  # Белый текст
            padding=(10, 5),  # Отступы
            relief="flat",  # Плоский стиль
            borderwidth=0,  # Без границ
            font=("Helvetica", 10),  # Шрифт
        )

        # Настраиваем эффекты при наведении и нажатии
        style.map(
            "Green.TButton",
            background=[("active", "#45a049"), ("pressed", "#3d8b40")],
            foreground=[("active", "white"), ("pressed", "white")],
            relief=[("pressed", "flat"), ("!pressed", "flat")],
        )

        super().__init__(
            parent, text=text, command=command, style="Green.TButton", **kwargs
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
