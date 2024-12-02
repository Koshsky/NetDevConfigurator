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
        self.cur_row = 0  # Use self.cur_row to keep track of rows
        self.create_widgets()
        self.frame.pack(padx=10, pady=10)

    def create_widgets(self):
        # COMPANY BLOCK
        self.add_company_widgets()

        # FIRMWARE BLOCK
        self.add_firmware_widgets()

        # DEVICE BLOCK
        self.add_device_widgets()

        # Feedback text area
        self.feedback_text = tk.Text(self.frame, wrap='word', width=50, height=10)
        self.feedback_text.grid(row=self.cur_row, column=0, columnspan=4, padx=5, pady=5)
        self.feedback_text.insert(tk.END, "Feedback will be here...\n")
        self.feedback_text.config(state=tk.DISABLED)

    def add_company_widgets(self):
        ttk.Label(self.frame, text="Company:").grid(row=self.cur_row, column=0, padx=5, pady=5)

        ttk.Label(self.frame, text="Name:").grid(row=self.cur_row, column=1, padx=5, pady=5)
        self.field_1_1 = ttk.Entry(self.frame)
        self.field_1_1.grid(row=self.cur_row, column=2, padx=5, pady=5)

        delete_button = tk.Button(self.frame, text="DELETE", command=self.delete_company)
        delete_button.grid(row=self.cur_row, column=3, padx=5, pady=5)

        self.cur_row += 1

    def add_firmware_widgets(self):
        ttk.Label(self.frame, text="Firmware:").grid(row=self.cur_row, column=0, padx=5, pady=5)

        ttk.Label(self.frame, text="Name:").grid(row=self.cur_row, column=1, padx=5, pady=5)
        self.field_2_1 = ttk.Entry(self.frame)
        self.field_2_1.grid(row=self.cur_row, column=2, padx=5, pady=5)

        delete_button = tk.Button(self.frame, text="DELETE", command=self.delete_firmware)
        delete_button.grid(row=self.cur_row, column=3, padx=5, pady=5)

        self.cur_row += 1

    def add_device_widgets(self):
        ttk.Label(self.frame, text="Device:").grid(row=self.cur_row, column=0, padx=5, pady=5)

        ttk.Label(self.frame, text="Name:").grid(row=self.cur_row, column=1, padx=5, pady=5)
        self.field_3_1 = ttk.Entry(self.frame)
        self.field_3_1.grid(row=self.cur_row, column=2, padx=5, pady=5)

        delete_button = tk.Button(self.frame, text="DELETE", command=self.delete_device)
        delete_button.grid(row=self.cur_row, column=3, padx=5, pady=5)

        self.cur_row += 1

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
        
        try:
            deleted_company = self.app.company_service.delete_by_name(name)
            if deleted_company:
                self.display_feedback(f"Deleted company: {deleted_company.name}")
            else:
                self.display_feedback("Company not found for deletion.")
        except Exception as e:
            self.display_feedback(f"Error deleting company: {e}")

    def delete_firmware(self):
        name = self.field_2_1.get()
        if not name:
            self.display_feedback("Please enter a firmware name.")
            return
        
        try:
            deleted_firmware = self.app.firmware_service.delete_by_name(name)
            if deleted_firmware:
                self.display_feedback(f"Deleted firmware: {deleted_firmware.name}")
            else:
                self.display_feedback("Firmware not found for deletion.")
        except Exception as e:
            self.display_feedback(f"Error deleting firmware: {e}")

    def delete_device(self):
        name = self.field_3_1.get()
        if not name:
            self.display_feedback("Please enter a device name.")
            return
        
        try:
            deleted_device = self.app.device_service.delete_by_name(name)  # Assuming a delete_by_name method exists
            if deleted_device:
                self.display_feedback(f"Deleted device: {deleted_device.name}")
            else:
                self.display_feedback("Device not found for deletion.")
        except Exception as e:
            self.display_feedback(f"Error deleting device: {e}")