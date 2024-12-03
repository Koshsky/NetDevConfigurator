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
        self.cur_row = 0
        self.button_text = button_text  # TODO: убрать этот параметр в create_block. последний аргумент - {"text": text, "func": func}
        self.fields = dict()
        self.create_widgets()
        self.frame.pack(padx=10, pady=10)

    def create_block(self, block_name: str, list_params: dict, function):
        self.fields[block_name] = dict()
        ttk.Label(self.frame, text=f"{block_name}:").grid(row=self.cur_row, column=0, padx=5, pady=5)
        for param, presets in list_params.items():  # TODO: реализовать list_params как словарь {"label":str, "presets":list[str]}
            label = ttk.Label(self.frame, text=f"{param}")
            label.grid(row=self.cur_row, column=1, padx=5, pady=5)
            if presets is None:
                field = ttk.Entry(self.frame)
                field.grid(row=self.cur_row, column=2, padx=5, pady=5)
            else:
                field = ttk.Combobox(self.frame, values=presets)
                field.grid(row=self.cur_row, column=2, padx=5, pady=5)

            self.fields[block_name][param] = field
            self.cur_row += 1


        if function is not None:
            self.button = tk.Button(self.frame, text=self.button_text, command=function)
            self.button.grid(row=self.cur_row-1, column=3, padx=5, pady=5)


    def create_button_in_line(self, text: str, function):
        button = tk.Button(self.frame, text=text, command=function)
        button.grid(row=self.cur_row, column=0, pady=5, columnspan=5, sticky="ew")

        self.cur_row += 1

    def create_feedback_area(self):
        self.feedback_text = tk.Text(self.frame, wrap='word', width=100, height=20)
        self.feedback_text.grid(row=self.cur_row, column=0, columnspan=4, padx=5, pady=5)
        self.feedback_text.insert(tk.END, "Feedback will be here...\n")
        self.feedback_text.config(state=tk.DISABLED)

        self.cur_row += 1

    def display_feedback(self, message):
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, message)
        self.feedback_text.config(state=tk.DISABLED)
        print(message)  # TODO: replace with logger

    def create_widgets(self):
        raise NotImplementedError
