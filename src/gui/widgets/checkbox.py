"""Custom checkbox widget."""

import tkinter as tk
from typing import Any, Dict, Optional

from gui.styles import (
    BACKGROUND_COLOR,
    ENTRY_BACKGROUND,
    FONT,
    PADDING,
)


class CustomCheckbox(tk.Checkbutton):
    """Custom checkbox widget with additional functionality."""

    def __init__(
        self,
        parent: Any,
        text: str = "",
        style: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        """Initialize the CustomCheckbox.

        Args:
            parent: The parent widget.
            text: The text to display next to the checkbox.
            style: The style to apply to the checkbox (ignored for tk.Checkbutton).
            **kwargs: Additional keyword arguments.
        """
        self._var = tk.BooleanVar()
        super().__init__(
            parent,
            text=text,
            variable=self._var,
            bg=BACKGROUND_COLOR,
            fg="black",
            font=FONT,
            padx=PADDING[0],
            pady=PADDING[1],
            selectcolor=ENTRY_BACKGROUND,
            **kwargs,
        )

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
        self._var.set(checked)

    def is_checked(self) -> bool:
        """Get the checkbox checked state.

        Returns:
            bool: Whether the checkbox is checked.
        """
        return self._var.get()

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
