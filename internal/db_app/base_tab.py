import tkinter as tk
from tkinter import IntVar, ttk

class BaseTab:
    def __init__(self, parent, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.cur_row = 0
        self.cur_col = 0
        self.fields = {}
        self.create_widgets()
        self.frame.pack(padx=10, pady=10)
        
    def _create_entry_field(self, entity_name, param_name):
        field = ttk.Entry(self.frame)
        field.grid(row=self.cur_row, column=self.cur_col+1, padx=5, pady=5)
        self.fields[entity_name][param_name] = field
        self.cur_row += 1

    def _create_combobox_field(self, entity_name, param_name, param_presets):
        field = ttk.Combobox(self.frame, values=param_presets)
        field.grid(row=self.cur_row, column=self.cur_col+1, padx=5, pady=5)
        field.current(0)
        self.fields[entity_name][param_name] = field
        self.cur_row += 1

    def _create_checkbox_group(self, entity_name, param_name, param_presets, width=None):
        self.fields[entity_name][param_name] = {}
        space = width
        first_row = self.cur_row
        first_col = self.cur_col
        for box in param_presets:
            checkbox_var = IntVar()
            checkbox = tk.Checkbutton(self.frame, text=box, variable=checkbox_var)
            checkbox.grid(row=self.cur_row, column=self.cur_col+1, padx=5)
            self.fields[entity_name][param_name][box] = checkbox_var
            self.cur_row += 1
            if space is not None:
                space -= 1
                if not space:
                    self.cur_row = first_row
                    self.cur_col += 1
                    space = width
        if width is not None and len(param_presets) > width:
                self.cur_row = first_row + width
                self.cur_col = first_col

    def _create_combobox_group(self, entity_name, param_name, param_presets, width=None):
        self.fields[entity_name][param_name] = {}
        space = width
        first_row = self.cur_row
        first_col = self.cur_col
        for sub_param, preset in param_presets.items():
            label = ttk.Label(self.frame, text=f"{sub_param}")
            label.grid(row=self.cur_row, column=self.cur_col+1, padx=5, pady=5)
            field = ttk.Combobox(self.frame, values=preset)
            field.grid(row=self.cur_row, column=self.cur_col+2, padx=5, pady=5)
            field.current(0)
            self.fields[entity_name][param_name][sub_param] = field
            self.cur_row += 1
            if space is not None:
                space -= 1
                if not space:
                    self.cur_row = first_row
                    self.cur_col += 2
                    space = width
        if width is not None and len(param_presets) > width:
                self.cur_row = first_row + width
                self.cur_col = first_col
            

    def create_block(self, entity_name, parameters, button=None, width=None):
        if entity_name not in self.fields:
            self.fields[entity_name] = {}

        ttk.Label(self.frame, text=f"{entity_name}:").grid(row=self.cur_row, column=0, padx=5, pady=5)
        self.cur_col = 1

        for param_name, param_presets in parameters.items():
            ttk.Label(self.frame, text=f"{param_name}").grid(row=self.cur_row, column=self.cur_col, padx=5, pady=5)
            
            if param_presets is None or len(param_presets) == 0:
                self._create_entry_field(entity_name, param_name)
            elif isinstance(param_presets, list):
                self._create_combobox_field(entity_name, param_name, param_presets)
            elif isinstance(param_presets, tuple):
                self._create_checkbox_group(entity_name, param_name, param_presets, width)
            elif isinstance(param_presets, dict):
                self._create_combobox_group(entity_name, param_name, param_presets, width)

        if button is not None:
            self.button = tk.Button(self.frame, text=button[0], command=button[1])
            self.button.grid(row=self.cur_row-1, column=3, padx=5, pady=5)

        
    
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
            
    def create_button_in_line(self, button):
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

    def validate_entity(self, entity_type: str, entity_name: str) -> int:
        if not (entity_name := entity_name.strip()):
            raise ValueError(f"{entity_type.capitalize()} name cannot be empty")

        service = self.app.entity_services.get(entity_type)
        if not service:
            raise ValueError(f"Invalid entity type: {entity_type}")

        if entity := service.get_by_name(entity_name):
            return entity
        else:
            raise ValueError(f"{entity_type.capitalize()} not found")

    def check_protocol_name(self, protocol_name: str) -> int:
        return self.validate_entity('protocol', protocol_name)

    def check_port_name(self, port_name: str) -> int:
        return self.validate_entity('port', port_name)

    def check_family_name(self, family_name: str) -> int:
        return self.validate_entity('family', family_name)

    def check_device_name(self, device_name: str) -> int:
        return self.validate_entity('device', device_name)

    def check_firmware_name(self, firmware_name: str) -> int:
        return self.validate_entity('firmware', firmware_name)

    def check_company_name(self, company_name: str) -> int:
        return self.validate_entity('company', company_name)
    