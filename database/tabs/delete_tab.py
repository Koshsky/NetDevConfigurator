import tkinter as tk
from tkinter import ttk

from database.models.models import Companies, Devices, Firmwares
from database.services.company_service import CompanyService
from database.services.device_service import DeviceService
from database.services.firmware_service import FirmwareService

from .base_tab import BaseTab


class DeleteTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app, "DELETE")

    def create_widgets(self):
        self.create_block("company", {"name":None}, self.delete_company)
        self.create_block("firmware", {"name":None}, self.delete_firmware)
        self.create_block("device", {"name":None}, self.delete_device)
        self.create_feedback_area()

    def delete_company(self):
        name = self.fields["company"]["name"].get()
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
            self.app.session.rollback()

    def delete_firmware(self):
        name = self.fields["firmware"]["name"].get()
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
            self.app.session.rollback()

    def delete_device(self):
        name = self.fields["device"]["name"].get()
        if not name:
            self.display_feedback("Please enter a device name.")
            return
        
        try:
            deleted_device = self.app.device_service.delete_by_name(name)
            if deleted_device:
                self.display_feedback(f"Deleted device: {deleted_device.name}")
            else:
                self.display_feedback("Device not found for deletion.")
        except Exception as e:
            self.display_feedback(f"Error deleting device: {e}")
            self.app.session.rollback()
