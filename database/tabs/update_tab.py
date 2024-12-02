import tkinter as tk
from tkinter import ttk
from database.models.models import Companies, Devices, Firmwares
from database.services.device_service import DeviceService
from database.services.firmware_service import FirmwareService
from database.services.device_firmwares_service import DeviceFirmwaresService  # Importing the DeviceFirmwareService

firmware_folder = "./firmwares/"

class UpdateTab:
    def __init__(self, parent, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.create_widgets()
        self.frame.pack(padx=10, pady=10)

    def create_widgets(self):
        cur_row = 0

        # DEVICE BLOCK
        self.entity_3 = ttk.Label(self.frame, text="device:")
        self.entity_3.grid(row=cur_row, column=0, padx=5, pady=5)

        self.param_3_1 = ttk.Label(self.frame, text="name:")
        self.param_3_1.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_3_1 = ttk.Entry(self.frame)
        self.field_3_1.grid(row=cur_row, column=2, padx=5, pady=5)

        cur_row += 1

        # FIRMWARE BLOCK
        self.entity_2 = ttk.Label(self.frame, text="firmware:")
        self.entity_2.grid(row=cur_row, column=0, padx=5, pady=5)

        self.param_2_1 = ttk.Label(self.frame, text="name:")
        self.param_2_1.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_2_1 = ttk.Entry(self.frame)
        self.field_2_1.grid(row=cur_row, column=2, padx=5, pady=5)

        cur_row += 1

        self.button_2_1 = tk.Button(self.frame, text="LINK", command=self.link_device_with_firmware)
        self.button_2_1.grid(row=cur_row, column=2, padx=5, pady=5)

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

    def link_device_with_firmware(self):
        device_name = self.field_3_1.get()
        firmware_name = self.field_2_1.get()

        if not device_name:
            self.display_feedback("Please enter a device name.")
            return
        
        if not firmware_name:
            self.display_feedback("Please enter a firmware name.")
            return

        # Check if the device exists
        device = self.app.device_service.get_by_name(device_name)
        if not device:
            self.display_feedback("Device not found.")
            return

        # Check if the firmware exists
        firmware = self.app.firmware_service.get_by_name(firmware_name)
        if not firmware:
            self.display_feedback("Firmware not found.")
            return

        # Link the device with the firmware using DeviceFirmwareService
        result = self.app.device_firmware_service.link_device_firmware(device.id, firmware.id)  # Assuming this method exists

        if result:
            self.display_feedback(f"Linked device '{device.name}' with firmware '{firmware.name}' successfully.")
        else:
            self.display_feedback("Failed to link device with firmware.")