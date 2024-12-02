import tkinter as tk
from tkinter import ttk
from .models.models import Companies, Devices, Firmwares
from .services.company_service import CompanyService
from .services.device_service import DeviceService  # Assuming you have a DeviceService
from .services.firmware_service import FirmwareService

firmware_folder = "./firmwares/"

class DeleteTab:
    def __init__(self, parent, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.create_widgets()
        self.frame.pack(padx=10, pady=10)

    def create_widgets(self):
        # COMPANY BLOCK
        cur_row = 0
        self.entity_1 = ttk.Label(self.frame, text="company:")
        self.entity_1.grid(row=cur_row, column=0, padx=5, pady=5)

        self.param_1_1 = ttk.Label(self.frame, text="name:")
        self.param_1_1.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_1_1 = ttk.Entry(self.frame)
        self.field_1_1.grid(row=cur_row, column=2, padx=5, pady=5)

        self.button_1 = tk.Button(self.frame, text="DELETE", command=self.delete_company)
        self.button_1.grid(row=cur_row, column=3, padx=5, pady=5)

        cur_row += 1

        # FIRMWARE BLOCK
        self.entity_2 = ttk.Label(self.frame, text="firmware:")
        self.entity_2.grid(row=cur_row, column=0, padx=5, pady=5)

        self.param_2_1 = ttk.Label(self.frame, text="name:")
        self.param_2_1.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_2_1 = ttk.Entry(self.frame)
        self.field_2_1.grid(row=cur_row, column=2, padx=5, pady=5)

        self.button_2_1 = tk.Button(self.frame, text="DELETE", command=self.delete_firmware)
        self.button_2_1.grid(row=cur_row, column=3, padx=5, pady=5)

        cur_row += 1

        # DEVICE BLOCK
        self.entity_3 = ttk.Label(self.frame, text="device:")
        self.entity_3.grid(row=cur_row, column=0, padx=5, pady=5)

        self.param_3_1 = ttk.Label(self.frame, text="name:")
        self.param_3_1.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_3_1 = ttk.Entry(self.frame)
        self.field_3_1.grid(row=cur_row, column=2, padx=5, pady=5)

        self.button_3 = tk.Button(self.frame, text="DELETE", command=self.delete_device)
        self.button_3.grid(row=cur_row, column=3, padx=5, pady=5)

        cur_row += 1

        # Feedback text area
        self.feedback_text = tk.Text(self.frame, wrap='word', width=50, height=10)
        self.feedback_text.grid(row=cur_row, column=0, columnspan=4, padx=5, pady=5)
        self.feedback_text.insert(tk.END, "Feedback will be here...\n")
        self.feedback_text.config(state=tk.DISABLED)

    def display_feedback(self, message):
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, message)
        self.feedback_text.config(state=tk.DISABLED)
        print(message)

    def delete_company(self):
        name = self.field_1_1.get()
        if not name:
            self.display_feedback("Please enter a company name.")
            return
        
        deleted_company = self.app.company_service.delete_by_name(name)
        if deleted_company:
            self.display_feedback(f"Deleted company: {deleted_company.name}")
        else:
            self.display_feedback("Company not found for deletion.")

    def delete_firmware(self):
        name = self.field_2_1.get()
        if not name:
            self.display_feedback("Please enter a firmware name.")
            return
        
        deleted_firmware = self.app.firmware_service.delete_by_name(name)
        if deleted_firmware:
            self.display_feedback(f"Deleted firmware: {deleted_firmware.name}")
        else:
            self.display_feedback("Firmware not found for deletion.")

    def delete_device(self):
        name = self.field_3_1.get()
        if not name:
            self.display_feedback("Please enter a device name.")
            return
        
        deleted_device = self.app.device_service.delete_by_name(name)  # Assuming a delete_by_name method exists
        if deleted_device:
            self.display_feedback(f"Deleted device: {deleted_device.name}")
        else:
            self.display_feedback("Device not found for deletion.")