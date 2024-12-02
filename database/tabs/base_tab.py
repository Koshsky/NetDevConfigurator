import tkinter as tk
from tkinter import ttk
import os


from database.models.models import Companies, DeviceFirmwares, Devices, Firmwares
from database.services.company_service import CompanyService
from database.services.firmware_service import FirmwareService

class BaseTab:
    def __init__(self, parent, app, button_text):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.button_text = button_text
        self.fields = dict()
        self.create_widgets()
        self.frame.pack(padx=10, pady=10)

    def create_block(self, cur_row: int, block_name: str, list_params: list[str], function) -> int:
        self.fields[block_name] = dict()
        ttk.Label(self.frame, text=f"{block_name}:").grid(row=cur_row, column=0, padx=5, pady=5)
        for param in list_params:
            label = ttk.Label(self.frame, text=f"{param}")
            label.grid(row=cur_row, column=1, padx=5, pady=5)
            field = ttk.Entry(self.frame)
            field.grid(row=cur_row, column=2, padx=5, pady=5)
            self.fields[block_name][param] = field
            cur_row += 1

        self.button = tk.Button(self.frame, text=self.button_text, command=function)
        self.button.grid(row=cur_row-1, column=3, padx=5, pady=5)

        return cur_row

    def create_button_in_line(self, cur_row: int, text: str, function) -> int:
        button = tk.Button(self.frame, text=text, command=function)
        button.grid(row=cur_row, column=0, pady=10)

        return cur_row + 1

    def create_feedback_area(self, cur_row: int) -> int:
        self.feedback_text = tk.Text(self.frame, wrap='word', width=100, height=20)
        self.feedback_text.grid(row=cur_row, column=0, columnspan=4, padx=5, pady=5)
        self.feedback_text.insert(tk.END, "Feedback will be here...\n")
        self.feedback_text.config(state=tk.DISABLED)

        return cur_row + 1

    def display_feedback(self, message):
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, message)
        self.feedback_text.config(state=tk.DISABLED)

    def create_widgets(self):
        raise NotImplementedError
