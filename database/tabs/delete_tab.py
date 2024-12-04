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
        try:
            company = self.check_company_name(self.fields["company"]["name"].get())
            self.app.company_service.delete(company)
        except Exception as e:
            self.display_feedback(f"Error deleting company: {e}")
            self.app.session.rollback()

    def delete_firmware(self):
        try:
            firmware = self.check_firmware_name(self.fields["firmware"]["name"].get())
            self.app.firmware_service.delete(firmware)
        except Exception as e:
            self.display_feedback(f"Error deleting firmware: {e}")
            self.app.session.rollback()

    def delete_device(self):
        try:
            device = self.check_device_name(self.fields["device"]["name"].get())
            self.app.device_service.delete(device)
        except Exception as e:
            self.display_feedback(f"Error deleting device: {e}")
            self.app.session.rollback()
