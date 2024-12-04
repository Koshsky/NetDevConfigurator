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
        self.create_block("device", {"name":None}, None)
        self.create_block("firmware", {"name":None}, None)
        self.create_button_in_line("LINK", self.link)
        self.create_block("devicе", {"name":None}, None)     # not ASKII symbol to avoid conflict
        self.create_block("firmwarе", {"name":None}, None)
        self.create_button_in_line("UNLINK", self.unlink)
        self.create_feedback_area()

    def link(self):
        try:
            device_id = self.check_device_name(self.fields["device"]["name"].get().strip())
            firmware_id = self.check_firmware_name(self.fields["firmware"]["name"].get().strip())

            self.app.device_firmware_service.link(device_id, firmware_id)
            self.display_feedback(f"Linked device with firmware successfully.")
        except ValueError as e:
            self.display_feedback(f"Error: {e}")
        except Exception as e:
            self.display_feedback(f"Error adding to database: {e}")
            self.app.session.rollback()


    def unlink(self):
        try:
            device_id = self.check_device_name(self.fields["devicе"]["name"].get().strip())
            firmware_id = self.check_firmware_name(self.fields["firmwarе"]["name"].get().strip())

            self.app.device_firmware_service.unlink(device_id, firmware_id)
            self.display_feedback(f"Unlinked device with firmware successfully.")
        except ValueError as e:
            self.display_feedback(f"Error: {e}")
        except Exception as e:
            self.display_feedback(f"Error adding to database: {e}")
            self.app.session.rollback()

    def check_device_name(self, device_name: str) -> int:
        if not device_name:
            raise ValueError("Device name cannot be empty")

        device = self.app.device_service.get_by_name(device_name)
        if not device:
            raise ValueError("Device not found.")

        return device.id

    def check_firmware_name(self, firmware_name: str) -> int:
        if not firmware_name:
            raise ValueError("Firmware name cannot be empty")

        firmware = self.app.firmware_service.get_by_name(firmware_name)
        if not firmware:
            raise ValueError("firmware not found.")

        return firmware.id