import tkinter as tk
from tkinter import IntVar, ttk

class BaseTab:
    def __init__(self, parent, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.cur_row = 0
        self.fields = {}
        self.create_widgets()
        self.frame.pack(padx=10, pady=10)
        
    def create_block(self, block_name, list_params, button = None, width=None, button_in_line=False):
        # sourcery skip: class-extract-method
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
            if presets is None or len(presets) == 0:
                field = ttk.Entry(self.frame)
                field.grid(row=self.cur_row, column=cur_col+1, padx=5, pady=5)

                self.fields[block_name][param] = field
                self.cur_row += 1
            elif isinstance(presets, list):
                field = ttk.Combobox(self.frame, values=presets)
                field.grid(row=self.cur_row, column=cur_col+1, padx=5, pady=5)
                field.current(0)

                self.fields[block_name][param] = field
                self.cur_row += 1
            elif isinstance(presets, tuple):
                if space is not None:
                    raise ValueError(f"cannot create checkbutton group: space is not None (space={space})")
                self.fields[block_name][param] = {}
                for box in presets:
                    checkbox_var = IntVar()
                    checkbox = tk.Checkbutton(self.frame, text=box, variable=checkbox_var)
                    checkbox.grid(row=self.cur_row, column=cur_col+1, padx=5)

                    self.fields[block_name][param][box] = checkbox_var
                    self.cur_row += 1
            if space is not None:
                if space:
                    space -= 1
                else:
                    self.cur_row = first_row
                    cur_col += 2
                    space = width
                
        if width is not None and len(list_params) > width:
            self.cur_row = first_row + width

        if button is not None:
            if button_in_line:
                self.create_button_in_line(button)
            else:
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
        """
        Generic method to validate and retrieve an entity by name.

        Args:
            entity_type (str): Type of entity to validate (e.g., 'protocol', 'device')
            entity_name (str): Name of the entity to validate

        Returns:
            int: ID of the validated entity

        Raises:
            ValueError: If entity name is empty or entity is not found
        """
        if not (entity_name := entity_name.strip()):
            raise ValueError(f"{entity_type.capitalize()} name cannot be empty")

        service = self.app.entity_services.get(entity_type)
        if not service:
            raise ValueError(f"Invalid entity type: {entity_type}")

        if entity := service.get_by_name(entity_name):
            return entity
        else:
            raise ValueError(f"{entity_type.capitalize()} not found")

    # Replace individual check methods with this generic method
    def check_protocol_name(self, protocol_name: str) -> int:
        return self.validate_entity('protocol', protocol_name)

    def check_family_name(self, family_name: str) -> int:
        return self.validate_entity('family', family_name)

    def check_device_name(self, device_name: str) -> int:
        return self.validate_entity('device', device_name)

    def check_firmware_name(self, firmware_name: str) -> int:
        return self.validate_entity('firmware', firmware_name)

    def check_company_name(self, company_name: str) -> int:
        return self.validate_entity('company', company_name)
    