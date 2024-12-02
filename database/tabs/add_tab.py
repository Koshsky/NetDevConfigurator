import tkinter as tk
from tkinter import ttk
import os


from database.models.models import Companies, DeviceFirmwares, Devices, Firmwares
from database.services.company_service import CompanyService
from database.services.firmware_service import FirmwareService
from .base_tab import BaseTab

firmware_folder = "./firmwares/"

class AddTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app, button_text="SUBMIT")

    def create_widgets(self):
        cur_row = 0
        cur_row = self.create_block(cur_row, "company", ["name"], self.submit_company)
        cur_row = self.create_block(cur_row, "firmware", ["folder"], self.submit_firmwares_from_folder)
        cur_row = self.create_block(cur_row, "device", ["name", "company", "dev_type", "primary_conf", "port_num"], self.submit_device)
        cur_row = self.create_feedback_area(cur_row)
        return cur_row + 1
    
    def submit_device(self):
        device_name = self.fields["device"]["name"].get().strip()
        company_name = self.fields["device"]["company"].get().strip()
        dev_type = self.fields["device"]["dev_type"].get().strip()
        primary_conf = self.fields["device"]["primary_conf"].get().strip()
        port_num = self.fields["device"]["port_num"].get().strip()

        if not device_name:
            self.display_feedback("Error: Device name cannot be empty.")
            return
        if not company_name:
            self.display_feedback("Error: Company name cannot be empty.")
            return
        if dev_type == "":
            self.display_feedback("Error: Select device type")
            return
        else:
            if dev_type not in ("router", "switch"):
                self.display_feedback("Error: Invalid device type. Please select 'router' or 'switch'.")
                return
            dev_type = 1 if dev_type == "router" else 2

        if primary_conf == "":
            self.display_feedback("Error: select primary configuration")
            return
        else:
            if primary_conf == "COM port + SSH":
                primary_conf = 1
            elif primary_conf == "SSH":
                primary_conf = 2
            elif primary_conf == "COM port + SNMP":
                if dev_type == 1:
                    self.display_feedback("Error: COM port + SNMP is not supported for router.")
                primary_conf = 3
            else:
                self.display_feedback("Error: Invalid primary configuration.")
                return

        if not port_num.isdigit():
            self.display_feedback("Error: Port number must be a valid integer.")
            return

        try:
            # Assuming you have a CompanyService method to get a company by name
            company_service = self.app.company_service
            existing_company = company_service.get_by_name(company_name)

            if not existing_company:
                self.display_feedback(f"Error: Company '{company_name}' does not exist.")
                return


            # Create a new device entry
            new_device = Devices(
                name=device_name,
                company_id=existing_company.id,  # Use the ID of the existing company
                dev_type=int(dev_type),
                primary_conf=int(primary_conf),
                port_num=int(port_num)
            )
            
            # Use the DeviceService to create the new device
            self.app.device_service.create(new_device)
            self.display_feedback("Successfully added to the devices table.")

        except Exception as e:
            self.display_feedback(f"Error adding to devices table: {e}")

    def submit_company(self):
        company_name = self.fields['company']['name'].get().strip()
        if not company_name:
            self.display_feedback("Error: Company name cannot be empty.")
            return

        try:
            # Use the CompanyService to create a new company
            new_company = Companies(name=company_name)
            created_company = self.app.company_service.create(new_company)
            self.display_feedback("Successfully added to the companies table.")
        except Exception as e:
            self.display_feedback(f"Error adding to companies table: {e}")

    def submit_firmwares_from_folder(self):
        company_name = self.fields['firmware']['folder'].get().strip()
        if not company_name:
            self.display_feedback("Error: Folder name cannot be empty.")
            return

        # Check if the folder exists
        if not os.path.isdir(company_name):
            self.display_feedback(f"Error: Folder '{company_name}' does not exist.")
            return

        try:
            # Iterate through all files in the folder
            for filename in os.listdir(company_name):
                firmware_name = filename.strip()  # Remove extra spaces

                if not firmware_name:
                    continue  # Skip empty file names

                # Check if firmware_name exists in the database
                existing_firmwares = self.app.firmware_service.get_all()
                if any(firmware.name == firmware_name for firmware in existing_firmwares):
                    self.display_feedback(f"Firmware '{firmware_name}' already exists in the table. Skipping.")
                    continue  # Skip if firmware already exists

                # Create a new firmware entry
                new_firmware = Firmwares(name=firmware_name)  # Assuming name is the only field needed
                self.app.firmware_service.create(new_firmware)

            self.display_feedback("Successfully added new firmwares from the folder.")
        except Exception as e:
            self.display_feedback(f"Error adding firmwares from folder: {e}")
