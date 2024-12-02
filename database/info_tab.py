import tkinter as tk
from tkinter import ttk
from .models.models import Companies, Devices, Firmwares
from .services.device_service import DeviceService  # Assuming you have a DeviceService
from .services.firmware_service import FirmwareService

firmware_folder = "./firmwares/"

class InfoTab:
    def __init__(self, parent, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.cur_row = 0  # Use self.cur_row to keep track of rows
        self.create_widgets()
        self.frame.pack(padx=10, pady=10)

    def create_widgets(self):
        ttk.Label(self.frame, text="Device:").grid(row=self.cur_row, column=0, padx=5, pady=5)

        ttk.Label(self.frame, text="Name:").grid(row=self.cur_row, column=1, padx=5, pady=5)
        self.field_3_1 = ttk.Entry(self.frame)
        self.field_3_1.grid(row=self.cur_row, column=2, padx=5, pady=5)

        delete_button = tk.Button(self.frame, text="SHOW", command=self.show_information)
        delete_button.grid(row=self.cur_row, column=3, padx=5, pady=5)

        self.cur_row += 1

        # Feedback text area
        self.feedback_text = tk.Text(self.frame, wrap='word', width=50, height=10)
        self.feedback_text.grid(row=self.cur_row, column=0, columnspan=4, padx=5, pady=5)
        self.feedback_text.insert(tk.END, "Feedback will be here...\n")
        self.feedback_text.config(state=tk.DISABLED)

    def display_feedback(self, message):
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, message)
        self.feedback_text.config(state=tk.DISABLED)
        print(message)

    def show_information(self):
        name = self.field_3_1.get()
        if not name:
            self.display_feedback("Please enter a device name.")
            return
        
        try:
            # Get the device by name
            device = self.app.device_service.get_by_name(name)  # Assuming you have a method to get device by name
            if not device:
                self.display_feedback("Device not found.")
                return
            
            # Fetch associated firmwares from device_firmwares
            associated_firmwares = self.app.device_service.get_firmwares_by_device_id(device.id)  # Assuming this method exists

            # Fetch the company name using the company_id
            company = self.app.company_service.get_by_id(device.company_id)  # Assuming you have a method to get company by ID
            company_name = company.name if company else "Unknown Company"

            # Prepare the output message
            firmware_list = "\n\t".join(firmware.name for firmware in associated_firmwares) if associated_firmwares else "No associated firmwares."
            
            output_message = (
                f"Device Information:\n"
                f"Name: {device.name}\n"
                f"ID: {device.id}\n"
                f"Company: {company_name}\n"
                f"Device Type: {['', 'router', 'switch'][device.dev_type]}\n"
                f"Primary Configuration: {['', 'COM port + SSH', 'SSH', 'COM port + SNMP'][device.primary_conf]}\n"
                f"Port Number: {device.port_num}\n"
                f"Associated Firmwares:\n\t{firmware_list}\n"
            )
            
            self.display_feedback(output_message)
        except Exception as e:
            self.display_feedback(f"Error retrieving device information: {e}")