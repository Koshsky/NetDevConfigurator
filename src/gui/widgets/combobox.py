"""Custom combobox widget."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List, Optional, Tuple


from ttkwidgets.autocomplete import AutocompleteCombobox

# с AutocompleteCombobox существует ОЧЕНЬ неприятный баг.
from config import config


class CustomCombobox(ttk.Combobox):
    """Custom combobox widget with additional functionality."""

    def __init__(
        self,
        parent: Any,
        completevalues: Optional[Tuple[str, ...]] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        """Initialize the CustomCombobox.

        Args:
            parent: The parent widget.
            completevalues: The values to use for autocomplete.
            **kwargs: Additional keyword arguments.
        """
        # Create a light style for combobox
        style = ttk.Style()
        style.configure(
            "Light.TCombobox",
            fieldbackground=config.app.second_color,
            background=config.app.second_color,
            selectbackground=config.app.second_color,
            selectforeground=config.app.foreground_color,
            arrowcolor=config.app.foreground_color,
        )

        super().__init__(
            parent,
            # completevalues=completevalues or (),
            style="Light.TCombobox",
            **kwargs,
        )

    def set_values(self, values: List[str]) -> None:
        """Set the combobox values.

        Args:
            values: The new values to use for autocomplete.
        """
        pass
        # self.configure(completevalues=tuple(values))

    def set_text(self, text: Optional[str]) -> None:
        """Set the combobox text.

        Args:
            text: The new text to set. Can be None.
        """
        if text is None:
            self.clear()
        else:
            self.set(text)

    def get_text(self) -> str:
        """Get the combobox text.

        Returns:
            str: The current text.
        """
        return self.get()

    def clear(self) -> None:
        """Clear the combobox text."""
        self.delete(0, tk.END)

    def set_style(self, style: str) -> None:
        """Set the combobox style.

        Args:
            style: The style to apply.
        """
        self.configure(style=style)

    def set_enabled(self, enabled: bool = True) -> None:
        """Set the combobox enabled state.

        Args:
            enabled: Whether to enable the combobox.
        """
        self.configure(state=tk.NORMAL if enabled else tk.DISABLED)
