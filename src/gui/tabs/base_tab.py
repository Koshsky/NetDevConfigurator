import logging
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import IntVar, ttk

from ttkwidgets.autocomplete import AutocompleteCombobox

logger = logging.getLogger("gui")


class BaseTab:
    def __init__(self, parent, app, log_name="Unknown tab"):
        self.__log_name = log_name
        self.frame = ttk.Frame(parent)
        self.frame.pack(padx=10, pady=10)
        self.app = app
        self._cur_row = self.cur_col = 0
        self.fields = {}

    def refresh_widgets(self):
        self._remove_widgets()
        self._create_widgets()
        logger.debug("%s tab refreshed", self.__log_name)

    def _create_widgets(self):
        raise NotImplementedError("tab._create_widgets not implemented!")

    def hide(self):
        self.app.notebook.hide(self.frame)
        logger.debug("%s tab is hidden", self.__log_name)

    def show(self):
        self.refresh_widgets()
        self.app.notebook.add(self.frame)
        logger.debug("%s tab is normal", self.__log_name)

    def show_if(self, condition: bool):
        if condition:
            self.show()
        else:
            self.hide()

    def _remove_widgets(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.fields = {}
        logger.debug("%s tab cleared", self.__log_name)

    def create_large_input_field(self, field_name, width=75, height=12):
        if field_name in self.fields:
            raise ValueError(f"Field '{field_name}' already exists.")

        text_field = tk.Text(self.frame, wrap="word", width=width, height=height)
        text_field.grid(
            row=self._cur_row, column=0, columnspan=100, padx=5, pady=5, sticky="w"
        )

        self.fields[field_name] = text_field

        self._cur_row += 1

    def create_block(self, entity_name, parameters, button=None, width=None):
        if entity_name not in self.fields:
            self.fields[entity_name] = {}

        ttk.Label(self.frame, text=f"{entity_name}").grid(
            row=self._cur_row, column=0, padx=5, pady=5
        )
        self.cur_col = 1

        for param_name, param_presets in parameters.items():
            ttk.Label(self.frame, text=f"{param_name}").grid(
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

        if button is not None:
            self.button = tk.Button(self.frame, text=button[0], command=button[1])
            self.button.grid(row=self._cur_row - 1, column=3, padx=5, pady=5)

        ttk.Label(self.frame, text="").grid(row=self._cur_row, column=0, pady=0)
        self._cur_row += 1

    def create_button_in_line(self, button):
        if not (
            isinstance(button, tuple)
            and len(button) == 2
            and isinstance(button[0], str)
            and callable(button[1])
        ):
            raise TypeError("button parameter must be a tuple of (str, callable)")
        button = tk.Button(self.frame, text=button[0], command=button[1])
        button.grid(row=self._cur_row, column=0, pady=5, columnspan=100, sticky="ew")

        self._cur_row += 1

    def create_feedback_area(self, message="DATABASE STORAGE", width=150, height=25):
        self.feedback_text = tk.Text(
            self.frame, wrap="word", width=width, height=height
        )
        self.feedback_text.grid(
            row=self._cur_row, column=0, columnspan=15, padx=5, pady=5, sticky="nsew"
        )

        scrollbar = ttk.Scrollbar(
            self.frame, orient="vertical", command=self.feedback_text.yview
        )
        scrollbar.grid(row=self._cur_row, column=15, sticky="ns")
        self.feedback_text.config(yscrollcommand=scrollbar.set)

        self.feedback_text.insert(tk.END, message)
        self.feedback_text.config(state=tk.DISABLED)

        self._cur_row += 1

    def show_error(self, title, error):
        messagebox.showerror(title, error)

    def display_feedback(self, message):
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, message)
        self.feedback_text.config(state=tk.DISABLED)

    def __create_entry_field(self, entity_name, param_name):
        field = ttk.Entry(self.frame)
        field.grid(row=self._cur_row, column=self.cur_col + 1, padx=5, pady=5)
        self.fields[entity_name][param_name] = field
        self._cur_row += 1

    def __create_combobox_field(self, entity_name, param_name, param_presets):
        field = AutocompleteCombobox(self.frame, completevalues=param_presets)
        field.grid(row=self._cur_row, column=self.cur_col + 1, padx=5, pady=5)
        field.current(0)
        self.fields[entity_name][param_name] = field
        self._cur_row += 1

    def __create_checkbox_group(
        self, entity_name, param_name, param_presets, width=None
    ):
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
        self, entity_name, param_name, param_presets, width=None
    ):
        self.fields[entity_name][param_name] = {}
        space = width
        first_row = self._cur_row
        first_col = self.cur_col
        for sub_param, preset in param_presets.items():
            label = ttk.Label(self.frame, text=f"{sub_param}")
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
