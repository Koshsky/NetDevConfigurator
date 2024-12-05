import tkinter as tk
from tkinter import ttk

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
        for param, presets in list_params.items():
            label = ttk.Label(self.frame, text=f"{param}")
            label.grid(row=self.cur_row, column=1, padx=5, pady=5)
            if presets is None or len(presets) == 0:
                field = ttk.Entry(self.frame)
                field.grid(row=self.cur_row, column=2, padx=5, pady=5)

                self.fields[block_name][param] = field
                self.cur_row += 1
            elif isinstance(presets, list):
                field = ttk.Combobox(self.frame, values=presets)
                field.grid(row=self.cur_row, column=2, padx=5, pady=5)
                field.current(0)

                self.fields[block_name][param] = field
                self.cur_row += 1
            elif isinstance(presets, tuple):
                self.fields[block_name][param] = dict()
                for box in presets:
                    checkbox = tk.Checkbutton(self.frame, text=box)
                    checkbox.grid(row=self.cur_row, column=2, padx=5, pady=5)

                    self.fields[block_name][param][box] = checkbox
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

    def check_device_name(self, device_name: str) -> int:  # TODO: изменить аннотацию, возвращаемый тип 
        device_name = device_name.strip()
        if not device_name:
            raise ValueError("Device name cannot be empty")

        device = self.app.device_service.get_by_name(device_name)
        if not device:
            raise ValueError("Device not found.")

        return device

    def check_firmware_name(self, firmware_name: str) -> int:  # TODO: изменить аннотацию, возвращаемый тип
        firmware_name = firmware_name.strip()
        if not firmware_name:
            raise ValueError("Firmware name cannot be empty")

        firmware = self.app.firmware_service.get_by_name(firmware_name)
        if not firmware:
            raise ValueError("firmware not found.")

        return firmware

    def check_company_name(self, company_name: str) -> int:  # TODO: изменить аннотацию, возвращаемый тип
        company_name = company_name.strip()
        if not company_name:
            raise ValueError("Company name cannot be empty")

        company = self.app.company_service.get_by_name(company_name)
        if not company:
            raise ValueError("company not found.")

        return company
