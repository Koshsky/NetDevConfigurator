import tkinter as tk
from tkinter import ttk

from database.models.models import Companies, Devices, Firmwares
from database.services.device_service import DeviceService
from database.services.firmware_service import FirmwareService
from database.services.device_firmwares_service import DeviceFirmwaresService

from .base_tab import BaseTab

class UpdateTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app, "")

    def create_widgets(self):
        self.create_block("device", ["name"], lambda : 1)
        self.create_block("firmware", ["name"], lambda : 1)
        self.create_button_in_line("LINK", self.link_device_with_firmware)
        self.create_feedback_area()

    def link_device_with_firmware(self):
        device_name = self.fields["device"]["name"].get().strip()
        firmware_name = self.fields["firmware"]["name"].get().strip()

        if not device_name:
            self.display_feedback("Please enter a device name.")
            return
        
        if not firmware_name:
            self.display_feedback("Please enter a firmware name.")
            return

        device = self.app.device_service.get_by_name(device_name)
        if not device:
            self.display_feedback("Device not found.")
            return

        firmware = self.app.firmware_service.get_by_name(firmware_name)
        if not firmware:
            self.display_feedback("Firmware not found.")
            return

        result = self.app.device_firmware_service.link_device_firmware(device.id, firmware.id)

        if result:
            self.display_feedback(f"Linked device '{device.name}' with firmware '{firmware.name}' successfully.")
        else:
            self.display_feedback("Failed to link device with firmware.")