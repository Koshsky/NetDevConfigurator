import logging
import tkinter as tk
import tkinter.messagebox as messagebox
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from config import config
from gui.widgets import (
    CustomButton,
    CustomCheckbox,
    CustomCombobox,
    CustomEntry,
    CustomFrame,
    CustomLabel,
    CustomScrollbar,
    CustomText,
)

logger = logging.getLogger("gui")


class BaseTab:
    """Base class for creating tabs in the application."""

    def __init__(self, parent: tk.Tk, app: Any, log_name: str = "Unknown tab") -> None:
        """Initializes a new instance of the BaseTab class."""
        self.__log_name: str = log_name
        # Основной фрейм, который будет расширяться
        self.frame: CustomFrame = CustomFrame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Внутренний контейнер для центрирования виджетов
        self.content_frame = CustomFrame(self.frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

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
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.fields = {}
        self.frame.reset_position()

    def create_large_input_field(
        self, field_name: str, width: int = 75, height: int = 12
    ) -> None:
        """Creates a large text input field."""
        if field_name in self.fields:
            raise ValueError(f"Field '{field_name}' already exists.")

        text_field = CustomText(self.content_frame, width=width, height=height)
        text_field.pack(fill=tk.X, padx=5, pady=5)

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
        # Создаем основной фрейм и центрируем его
        block_frame = CustomFrame(self.content_frame)
        block_frame.pack(fill=tk.X, padx=5, pady=5)

        if entity_name not in self.fields:
            self.fields[entity_name] = {}

        # Создаем фрейм для заголовка
        header_frame = CustomFrame(block_frame)
        header_frame.pack(fill=tk.X, pady=2)

        # Заголовок блока
        CustomLabel(header_frame, text=entity_name).pack(side=tk.LEFT)

        self.cur_col = 1

        # Создаем фрейм для параметров
        params_frame = CustomFrame(block_frame)
        params_frame.pack(fill=tk.X, padx=5, pady=5)

        for param_name, param_presets in parameters.items():
            # Создаем фрейм для строки параметра
            param_frame = CustomFrame(params_frame)
            param_frame.pack(fill=tk.X, pady=2)

            # Метка параметра
            CustomLabel(param_frame, text=param_name).pack(side=tk.LEFT, padx=5)

            # Фрейм для поля ввода и кнопки
            input_frame = CustomFrame(param_frame)
            input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

            if param_presets is None or len(param_presets) == 0:
                self.__create_entry_field(entity_name, param_name, input_frame)
            elif isinstance(param_presets, tuple):
                self.__create_combobox_field(entity_name, param_name, param_presets, input_frame)
            elif isinstance(param_presets, list):
                self.__create_checkbox_group(
                    entity_name, param_name, param_presets, width, input_frame
                )
            elif isinstance(param_presets, dict):
                self.__create_combobox_group(
                    entity_name, param_name, param_presets, width, input_frame
                )
            else:
                raise TypeError("Invalid parameter preset type")

            # Добавляем кнопку, если она есть
            if button is not None:
                if not (
                    isinstance(button, tuple)
                    and len(button) == 2
                    and isinstance(button[0], str)
                    and callable(button[1])
                ):
                    raise TypeError("button parameter must be a tuple of (str, callable)")

                CustomButton(input_frame, text=button[0], command=button[1]).pack(side=tk.LEFT, padx=5)

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

        button_widget = CustomButton(self.content_frame, text=button[0], command=button[1])
        button_widget.pack(fill=tk.X, padx=5, pady=5)
        self._cur_row += 1

    def create_feedback_area(
        self, message: str = "DATABASE STORAGE", width: int = 150, height: int = 25
    ) -> None:
        """Creates a text area for displaying feedback messages."""
        feedback_frame = CustomFrame(self.content_frame)
        feedback_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.feedback_text = CustomText(
            feedback_frame, wrap="word", width=width, height=height, state=tk.DISABLED
        )
        self.feedback_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = CustomScrollbar(
            feedback_frame, orient="vertical", command=self.feedback_text.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.feedback_text.config(yscrollcommand=scrollbar.set)

        self.display_feedback(message)
        self._cur_row += 1

    def show_error(self, title: str, error: str) -> None:
        """Shows an error message box."""
        messagebox.showerror(title, error)

    def display_feedback(self, message: str) -> None:
        """Displays a feedback message in the feedback area."""
        self.feedback_text.set_readonly(False)
        self.feedback_text.set_text(message)
        self.feedback_text.set_readonly(True)

    def __create_entry_field(self, entity_name: str, param_name: str, parent_frame: CustomFrame) -> None:
        """Creates a single entry field."""
        field = CustomEntry(parent_frame, width=30)  # Ограничиваем ширину
        field.pack(side=tk.LEFT, padx=5)
        self.fields[entity_name][param_name] = field

    def __create_combobox_field(
        self, entity_name: str, param_name: str, param_presets: Tuple[str, ...], parent_frame: CustomFrame
    ) -> None:
        """Creates a single combobox field."""
        field = CustomCombobox(parent_frame, completevalues=param_presets, width=30)  # Ограничиваем ширину
        field.pack(side=tk.LEFT, padx=5)
        field.set_values(list(param_presets))
        field.set_text(param_presets[0] if param_presets else "")
        self.fields[entity_name][param_name] = field

    def __create_checkbox_group(
        self,
        entity_name: str,
        param_name: str,
        param_presets: List[str],
        width: Optional[int] = None,
        parent_frame: CustomFrame = None,
    ) -> None:
        """Creates a group of checkboxes."""
        self.fields[entity_name][param_name] = {}

        if width is not None:
            # Создаем сетку чекбоксов
            for i in range(0, len(param_presets), width):
                row_frame = CustomFrame(parent_frame)
                row_frame.pack(fill=tk.X, pady=2)

                for box in param_presets[i:i + width]:
                    checkbox = CustomCheckbox(row_frame, text=box)
                    checkbox.pack(side=tk.LEFT, padx=5)
                    self.fields[entity_name][param_name][box] = checkbox
        else:
            # Размещаем чекбоксы в столбец
            for box in param_presets:
                checkbox = CustomCheckbox(parent_frame, text=box)
                checkbox.pack(anchor=tk.W, pady=2)
                self.fields[entity_name][param_name][box] = checkbox

    def __create_combobox_group(
        self,
        entity_name: str,
        param_name: str,
        param_presets: Dict[str, List[str]],
        width: Optional[int] = None,
        parent_frame: CustomFrame = None,
    ) -> None:
        """Creates a group of comboboxes in a grid layout.

        Args:
            entity_name: The name of the entity.
            param_name: The name of the parameter.
            param_presets: Dictionary of parameter presets.
            width: The width of the grid (number of columns).
            parent_frame: The parent frame to create comboboxes in.
        """
        self.fields[entity_name][param_name] = {}

        # Если width не указан, используем значение по умолчанию из конфига
        if width is None:
            width = config.app.grid_columns

        # Создаем фрейм для сетки
        grid_frame = CustomFrame(parent_frame)
        grid_frame.pack(fill=tk.X, pady=2)

        # Создаем комбобоксы в сетке
        for i, (sub_param, preset) in enumerate(param_presets.items()):
            row = i % width
            col = i // width

            # Создаем фрейм для метки и комбобокса
            cell_frame = CustomFrame(grid_frame)
            cell_frame.grid(row=row, column=col, padx=5, pady=2, sticky="ew")

            # Настраиваем веса колонок для равномерного распределения
            grid_frame.grid_columnconfigure(col, weight=1)

            # Создаем метку и комбобокс
            CustomLabel(cell_frame, text=sub_param).pack(side=tk.LEFT, padx=2)
            field = CustomCombobox(cell_frame, completevalues=preset, width=30)  # Ограничиваем ширину
            field.pack(side=tk.LEFT, padx=2)
            field.set_values(preset)
            field.set_text(preset[0] if preset else "")
            self.fields[entity_name][param_name][sub_param] = field
