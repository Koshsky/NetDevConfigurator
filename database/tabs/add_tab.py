import tkinter as tk
from tkinter import ttk
import os

from database.models.models import Companies, DeviceFirmwares, Devices, Firmwares
from database.services.company_service import CompanyService
from database.services.firmware_service import FirmwareService, determine_firmware_type

from .base_tab import BaseTab

class AddTab(BaseTab):
    def __init__(self, parent, app):
        self.companies = ["Eltex", "Zyxel"]
        super().__init__(parent, app, button_text="SUBMIT")

    def create_widgets(self):
        self.create_block(
            "company", 
            {"name": None}, 
            self.submit_company
        )

        self.create_block(
            "firmware", 
            {"folder": ['./firmwares']}, 
            self.submit_firmwares_from_folder
        )
        # TODO: добавить УДОБНЫЕ пресеты для port_num
        # TODO: добавить пресеты для company........... 
        self.create_block(
            "device", 
            {
                "name": None,
                "protocols": ('ssh', 'http', 'COM', 'SNMP'),
                "company": self.companies,
                "dev_type": ["switch", "router"],
                "port_num": [24, 48]
            }, 
            self.submit_device
        )
        self.create_feedback_area()
    
    def submit_device(self):
        device_name = self.fields["device"]["name"].get().strip()
        dev_type = self.fields["device"]["dev_type"].get().strip()
        port_num = self.fields["device"]["port_num"].get().strip()

        if not device_name:
            self.display_feedback("Error: Device name cannot be empty.")
            return
        if not dev_type:
            self.display_feedback("Error: Select device type")
            return
        if not port_num.isdigit():
            self.display_feedback("Error: Port number must be a valid integer.")
            return

        try:
            company = self.check_company_name(self.fields["device"]["company"].get())

            new_device = {
                "name": device_name,
                "company_id": company.id,
                "dev_type": dev_type,
                "port_num": int(port_num)
            }
            
            self.app.device_service.create(new_device)
            self.display_feedback("Successfully added to the devices table.")

        except Exception as e:
            self.display_feedback(f"Error adding to devices table: {e}")
            self.app.session.rollback()

    def submit_company(self):
        company_name = self.fields['company']['name'].get().strip()
        if not company_name:
            self.display_feedback("Error: Company name cannot be empty.")
            return

        try:
            self.app.company_service.create({"name": company_name})
            self.display_feedback("Successfully added to the companies table.")
        except Exception as e:
            self.display_feedback(f"Error adding to companies table: {e}")
            self.app.session.rollback()

    def submit_firmwares_from_folder(self):
        folder_name = self.fields['firmware']['folder'].get().strip()
        if not folder_name:
            self.display_feedback("Error: Folder name cannot be empty.")
            return
            
        if not os.path.isdir(folder_name):
            self.display_feedback(f"Error: Folder '{folder_name}' does not exist.")
            return  

        folder_name = os.path.abspath(folder_name) if not os.path.isabs(folder_name) else folder_name

        try:
            existing_firmwares = [firmware.name for firmware in self.app.firmware_service.get_all()]
            for filename in os.listdir(folder_name):
                firmware_name = filename
                if firmware_name in existing_firmwares:
                    print(f"Firmware '{firmware_name}' already exists in the table. Skipping.")  # TODO: replace with logger
                    continue
                
                new_firmware = Firmwares(
                        name=firmware_name,
                        full_path=f'{folder_name}/{firmware_name}',
                        type=determine_firmware_type(firmware_name)
                )
                self.app.firmware_service.create(new_firmware)

            self.display_feedback("Successfully added new firmwares from the folder.")
        except Exception as e:
            self.display_feedback(f"Error adding firmwares from folder: {e}")
            self.app.session.rollback()
