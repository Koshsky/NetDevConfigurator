import logging
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import IntVar, ttk
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from ttkwidgets.autocomplete import AutocompleteCombobox
from config import config

logger = logging.getLogger("gui")


class BaseTab:
    """Base class for creating tabs in the application."""

    def __init__(self, parent: tk.Tk, app: Any, log_name: str = "Unknown tab") -> None:
        """Initializes a new instance of the BaseTab class."""
        self.__log_name: str = log_name
        self.frame: ttk.Frame = ttk.Frame(parent)
        self.frame.columnconfigure(
            list(range(config["app"]["grid_columns"])), minsize=40, weight=1
        )
        self.frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False, padx=5, pady=5)
        self.app: Any = app
        self._cur_row: int = 0
        self.cur_col: int = 0
        self.fields: Dict[str, Any] = {}

    def refresh_widgets(self) -> None:
        """Refreshes the widgets on the tab."""
        logger.debug("%s tab refreshed", self.__log_name)
        self._remove_widgets()
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Creates the widgets for the tab. Must be implemented by subclasses."""
        raise NotImplementedError("tab._create_widgets not implemented!")

    def hide(self) -> None:
        """Hides the tab."""
        logger.debug("%s tab is hidden", self.__log_name)
        self.app.notebook.hide(self.frame)

    def show(self) -> None:
        """Shows the tab."""
        logger.debug("%s tab is shown", self.__log_name)
        self.refresh_widgets()
        self.app.notebook.add(self.frame, text=self.__log_name)

    def show_if(self, condition: bool) -> None:
        """Shows the tab if the condition is true, hides it otherwise."""
        if condition:
            self.show()
        else:
            self.hide()

    def _remove_widgets(self) -> None:
        """Removes all widgets from the tab."""
        logger.debug("%s tab cleared", self.__log_name)
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.fields = {}

    def create_large_input_field(
        self, field_name: str, width: int = 75, height: int = 12
    ) -> None:
        """Creates a large text input field."""
        if field_name in self.fields:
            raise ValueError(f"Field '{field_name}' already exists.")

        text_field = tk.Text(self.frame, wrap="word", width=width, height=height)
        text_field.grid(
            row=self._cur_row, column=0, columnspan=100, padx=5, pady=5, sticky="w"
        )

        self.fields[field_name] = text_field
        self._cur_row += 1

    def create_block(
        self,
        entity_name: str,
        parameters: Dict[str, Union[Tuple[str, ...], List[str], Dict[str, List[str]]]],
        button: Optional[Tuple[str, Callable[[], None]]] = None,
        width: Optional[int] = None,
    ) -> None:
        """Creates a block of input fields."""

        if entity_name not in self.fields:
            self.fields[entity_name] = {}

        ttk.Label(self.frame, text=entity_name).grid(
            row=self._cur_row, column=0, padx=5, pady=5
        )
        self.cur_col = 1

        for param_name, param_presets in parameters.items():
            ttk.Label(self.frame, text=param_name).grid(
                row=self._cur_row, column=self.cur_col, padx=5, pady=5
            )

            if param_presets is None or len(param_presets) == 0:
                self.__create_entry_field(entity_name, param_name)
            elif isinstance(param_presets, tuple):
                self.__create_combobox_field(entity_name, param_name, param_presets)
            elif isinstance(param_presets, list):
                self.__create_checkbox_group(
                    entity_name, param_name, param_presets, width
                )
            elif isinstance(param_presets, dict):
                self.__create_combobox_group(
                    entity_name, param_name, param_presets, width
                )
            else:
                raise TypeError(
                    "Invalid parameter preset type"
                )  # Handle unexpected types

            self._cur_row += 1  # Move to the next row after each parameter

        if button is not None:
            if not (
                isinstance(button, tuple)
                and len(button) == 2
                and isinstance(button[0], str)
                and callable(button[1])
            ):
                raise TypeError("button parameter must be a tuple of (str, callable)")

            tk.Button(self.frame, text=button[0], command=button[1]).grid(
                row=self._cur_row - len(parameters),
                column=self.cur_col + 2,
                padx=5,
                pady=5,
                rowspan=len(parameters),
            )

        ttk.Label(self.frame, text="").grid(row=self._cur_row, column=0, pady=0)
        self._cur_row += 1

    def create_button_in_line(self, button: Tuple[str, Callable[[], None]]) -> None:
        """Creates a button that occupies the full width of the tab."""
        if not (
            isinstance(button, tuple)
            and len(button) == 2
            and isinstance(button[0], str)
            and callable(button[1])
        ):
            raise TypeError("button parameter must be a tuple of (str, callable)")

        button_widget = tk.Button(self.frame, text=button[0], command=button[1])
        button_widget.grid(
            row=self._cur_row,
            column=0,
            pady=5,
            columnspan=config["app"]["grid_columns"],
            sticky="ew",
        )
        self._cur_row += 1

    def create_feedback_area(
        self, message: str = "DATABASE STORAGE", width: int = 150, height: int = 25
    ) -> None:
        """Creates a text area for displaying feedback messages."""
        self.feedback_text = tk.Text(
            self.frame, wrap="word", width=width, height=height, state=tk.DISABLED
        )
        self.feedback_text.grid(
            row=self._cur_row,
            column=0,
            columnspan=config["app"]["grid_columns"],
            padx=5,
            pady=5,
            sticky="nsew",
        )

        scrollbar = ttk.Scrollbar(
            self.frame, orient="vertical", command=self.feedback_text.yview
        )
        scrollbar.grid(
            row=self._cur_row, column=config["app"]["grid_columns"], sticky="ns"
        )
        self.feedback_text.config(yscrollcommand=scrollbar.set)

        self.display_feedback(message)  # Use display_feedback to set initial message
        self._cur_row += 1

    def show_error(self, title: str, error: str) -> None:
        """Shows an error message box."""
        messagebox.showerror(title, error)

    def display_feedback(self, message: str) -> None:
        """Displays a feedback message in the feedback area."""
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, message)
        self.feedback_text.config(state=tk.DISABLED)

    def __create_entry_field(self, entity_name: str, param_name: str) -> None:
        """Creates a single entry field."""
        field = ttk.Entry(self.frame)
        field.grid(row=self._cur_row, column=self.cur_col + 1, padx=5, pady=5)
        self.fields[entity_name][param_name] = field

    def __create_combobox_field(
        self, entity_name: str, param_name: str, param_presets: Tuple[str, ...]
    ) -> None:
        """Creates a single combobox field."""
        field = AutocompleteCombobox(self.frame, completevalues=param_presets)
        field.grid(row=self._cur_row, column=self.cur_col + 1, padx=5, pady=5)
        field.current(0)
        self.fields[entity_name][param_name] = field

    def __create_checkbox_group(
        self,
        entity_name: str,
        param_name: str,
        param_presets: List[str],
        width: Optional[int] = None,
    ) -> None:
        """Creates a group of checkboxes."""
        self.fields[entity_name][param_name] = {}
        space = width
        first_row = self._cur_row
        first_col = self.cur_col
        for box in param_presets:
            checkbox_var = IntVar()
            checkbox = tk.Checkbutton(self.frame, text=box, variable=checkbox_var)
            checkbox.grid(row=self._cur_row, column=self.cur_col + 1, padx=5)
            self.fields[entity_name][param_name][box] = checkbox_var
            self._cur_row += 1
            if space is not None:
                space -= 1
                if not space:
                    self._cur_row = first_row
                    self.cur_col += 1
                    space = width
        if width is not None and len(param_presets) == width:
            self._cur_row = first_row + width
            self.cur_col = first_col

    def __create_combobox_group(
        self,
        entity_name: str,
        param_name: str,
        param_presets: Dict[str, List[str]],
        width: Optional[int] = None,
    ) -> None:
        """Creates a group of comboboxes."""
        self.fields[entity_name][param_name] = {}
        space = width
        first_row = self._cur_row
        first_col = self.cur_col
        for sub_param, preset in param_presets.items():
            label = ttk.Label(self.frame, text=sub_param)
            label.grid(
                row=self._cur_row, column=self.cur_col + 1, padx=5, pady=5, sticky="e"
            )
            field = AutocompleteCombobox(self.frame, completevalues=preset)
            field.grid(row=self._cur_row, column=self.cur_col + 2, padx=5, pady=5)
            field.current(0)
            self.fields[entity_name][param_name][sub_param] = field
            self._cur_row += 1
            if space is not None:
                space -= 1
                if not space:
                    self._cur_row = first_row
                    self.cur_col += 2
                    space = width
        if width is not None and len(param_presets) > width:
            self._cur_row = first_row + width
            self.cur_col = first_col
