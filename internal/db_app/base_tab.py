import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple, Callable

class BaseTab:
    def __init__(self, parent, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.cur_row = 0
        self.fields = {}
        self.create_widgets()
        self.frame.pack(padx=10, pady=10)

    def create_block(self, block_name: str, list_params: dict, button: Optional[Tuple[str, Callable]] = None):
        if button is not None and not (isinstance(button, tuple) and len(button) == 2 
                                     and isinstance(button[0], str) and callable(button[1])):
            raise TypeError("button parameter must be a tuple of (str, callable) or None")
        
        self.fields[block_name] = {}
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
                self.fields[block_name][param] = {}
                for box in presets:
                    checkbox = tk.Checkbutton(self.frame, text=box)
                    checkbox.grid(row=self.cur_row, column=2, padx=5)

                    self.fields[block_name][param][box] = checkbox
                    self.cur_row += 1
        
        if button is not None:
            self.button = tk.Button(self.frame, text=button[0], command=button[1])
            self.button.grid(row=self.cur_row-1, column=3, padx=5, pady=5)
        
    def create_grid_combobox(self,  width: int, block_name: str, list_params: dict, button: Optional[Tuple[str, Callable]] = None):
        if button is not None and not (isinstance(button, tuple) and len(button) == 2 
                                     and isinstance(button[0], str) and callable(button[1])):
            raise TypeError("button parameter must be a tuple of (str, callable) or None")
        
        self.fields[block_name] = {}
        ttk.Label(self.frame, text=f"{block_name}:").grid(row=self.cur_row, column=0, padx=5, pady=5)
        cur_col = 1
        space = width
        first_row = self.cur_row
        for param, presets in list_params.items():
            label = ttk.Label(self.frame, text=f"{param}")
            label.grid(row=self.cur_row, column=cur_col, padx=5, pady=5)
            field = ttk.Combobox(self.frame, values=presets)
            field.grid(row=self.cur_row, column=cur_col+1, padx=5, pady=5)
            field.current(0)

            self.fields[block_name][param] = field
            self.cur_row += 1
            space -= 1
            if not space:
                self.cur_row = first_row
                cur_col += 2
                space = width
                
        if len(list_params) > width:
            self.cur_row = first_row + width

        if button is not None:
            self.create_button_in_line(button)

    def create_button_in_line(self, button: Tuple[str, Callable]):
        if not (isinstance(button, tuple) and len(button) == 2 
                                     and isinstance(button[0], str) and callable(button[1])):
            raise TypeError("button parameter must be a tuple of (str, callable)")
        button = tk.Button(self.frame, text=button[0], command=button[1])
        button.grid(row=self.cur_row, column=0, pady=5, columnspan=5, sticky="ew")

        self.cur_row += 1

    def create_feedback_area(self, width=100, height=20):
        self.feedback_text = tk.Text(self.frame, wrap='word', width=width, height=height)
        self.feedback_text.grid(row=self.cur_row, column=0, columnspan=5, padx=5, pady=5)
        self.feedback_text.insert(tk.END, "Feedback will be here...\n")
        self.feedback_text.config(state=tk.DISABLED)

        self.cur_row += 1

    def display_feedback(self, message):
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, message)
        self.feedback_text.config(state=tk.DISABLED)
        
    def create_widgets(self):
        raise NotImplementedError

    def check_protocol_name(self, protocol_name: str) -> int:  # TODO: изменить аннотацию, возвращаемый тип 
        if protocol_name := protocol_name.strip():
            protocol = self.app.protocol_service.get_by_name(protocol_name)
        else:
            raise ValueError("Device name cannot be empty")

        if not protocol:
            raise ValueError("Protocol not found.")

        return protocol

    def check_device_name(self, device_name: str) -> int:  # TODO: изменить аннотацию, возвращаемый тип 
        if device_name := device_name.strip():
            device = self.app.device_service.get_by_name(device_name)
        else:
            raise ValueError("Device name cannot be empty")
        if not device:
            raise ValueError("Device not found.")

        return device

    def check_firmware_name(self, firmware_name: str) -> int:  # TODO: изменить аннотацию, возвращаемый тип
        if firmware_name := firmware_name.strip():
            firmware = self.app.firmware_service.get_by_name(firmware_name)
        else:
            raise ValueError("Firmware name cannot be empty")
        if not firmware:
            raise ValueError("firmware not found.")

        return firmware

    def check_company_name(self, company_name: str) -> int:  # TODO: изменить аннотацию, возвращаемый тип
        if company_name := company_name.strip():
            company = self.app.company_service.get_by_name(company_name)
        else:
            raise ValueError("Company name cannot be empty")
        if not company:
            raise ValueError("company not found.")

        return company
