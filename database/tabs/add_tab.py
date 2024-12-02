import tkinter as tk
from tkinter import ttk
import os
from database.models.models import Companies, DeviceFirmwares, Devices, Firmwares
from database.services.company_service import CompanyService
from database.services.firmware_service import FirmwareService

firmware_folder = "./firmwares/"

class AddTab:
    def __init__(self, parent, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.create_widgets()
        self.frame.pack(padx=10, pady=10)

    def create_company_block(self, cur_row: int) -> int:
        self.entity_1 = ttk.Label(self.frame, text="company:")
        self.entity_1.grid(row=cur_row, column=0, padx=5, pady=5)

        self.param_1_1 = ttk.Label(self.frame, text="name:")
        self.param_1_1.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_1_1 = ttk.Entry(self.frame)
        self.field_1_1.grid(row=cur_row, column=2, padx=5, pady=5)

        self.button_1 = tk.Button(self.frame, text="SUBMIT", command=self.submit_company)
        self.button_1.grid(row=cur_row, column=3, padx=5, pady=5)

        return cur_row + 1

    def create_firmware_block(self, cur_row: int) -> int:
        self.entity_2 = ttk.Label(self.frame, text="firmware:")
        self.entity_2.grid(row=cur_row, column=0, padx=5, pady=5)

        self.param_2_1 = ttk.Label(self.frame, text="name:")
        self.param_2_1.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_2_1 = ttk.Entry(self.frame)
        self.field_2_1.grid(row=cur_row, column=2, padx=5, pady=5)

        self.button_2_1 = tk.Button(self.frame, text="SUBMIT", command=self.submit_firmware)
        self.button_2_1.grid(row=cur_row, column=3, padx=5, pady=5)

        cur_row += 1
        
        self.param_2_2 = ttk.Label(self.frame, text="folder:")
        self.param_2_2.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_2_2 = ttk.Entry(self.frame)
        self.field_2_2.grid(row=cur_row, column=2, padx=5, pady=5)

        self.button_2_2 = tk.Button(self.frame, text="SEARCH", command=self.submit_firmwares_from_folder)
        self.button_2_2.grid(row=cur_row, column=3, padx=5, pady=5)

        return cur_row + 1

    def create_device_block(self, cur_row: int) -> int:
        self.entity_3 = ttk.Label(self.frame, text="device:")
        self.entity_3.grid(row=cur_row, column=0, padx=5, pady=5)

        self.param_3_1 = ttk.Label(self.frame, text="name:")
        self.param_3_1.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_3_1 = ttk.Entry(self.frame)
        self.field_3_1.grid(row=cur_row, column=2, padx=5, pady=5)

        cur_row += 1

        self.param_3_2 = ttk.Label(self.frame, text="company:")
        self.param_3_2.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_3_2 = ttk.Combobox(self.frame, values=["Eltex", "Zyxel"])
        self.field_3_2.grid(row=cur_row, column=2, padx=5, pady=5)

        cur_row += 1

        self.param_3_3 = ttk.Label(self.frame, text="dev_type:")
        self.param_3_3.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_3_3 = ttk.Combobox(self.frame, values=["router", "switch"])
        self.field_3_3.grid(row=cur_row, column=2, padx=5, pady=5)

        cur_row += 1

        self.param_3_4 = ttk.Label(self.frame, text="primary_conf:")
        self.param_3_4.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_3_4 = ttk.Combobox(self.frame, values=["COM port + SSH", "SSH", "COM port + SNMP"])
        self.field_3_4.grid(row=cur_row, column=2, padx=5, pady=5)

        cur_row += 1

        self.param_3_5 = ttk.Label(self.frame, text="port_num:")
        self.param_3_5.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_3_5 = ttk.Entry(self.frame)
        self.field_3_5.grid(row=cur_row, column=2, padx=5, pady=5)

        self.button_3 = tk.Button(self.frame, text="SUBMIT", command=self.submit_device)
        self.button_3.grid(row=cur_row, column=3, padx=5, pady=5)

        return cur_row + 1

    def create_feedback_area(self, cur_row: int) -> int:
        self.feedback_text = tk.Text(self.frame, wrap='word', width=50, height=10)
        self.feedback_text.grid(row=cur_row, column=0, columnspan=4, padx=5, pady=5)
        self.feedback_text.insert(tk.END, "Feedback will be here...\n")
        self.feedback_text.config(state=tk.DISABLED)
        return cur_row + 1

    def create_widgets(self):
        cur_row = 0
        cur_row = self.create_company_block(cur_row)
        cur_row = self.create_firmware_block(cur_row)
        cur_row = self.create_device_block(cur_row)
        cur_row = self.create_feedback_area(cur_row)

    def display_feedback(self, message):
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, message)
        self.feedback_text.config(state=tk.DISABLED)
        print(message)

    
    def submit_device(self):
        # Retrieve the values from the input fields
        device_name = self.field_3_1.get().strip()
        company_name = self.field_3_2.get().strip()  # This should be a company name
        dev_type = self.field_3_3.get().strip()
        primary_conf = self.field_3_4.get().strip()
        port_num = self.field_3_5.get().strip()

        # Validate input fields
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
        company_name = self.field_1_1.get().strip()  # Get the name and remove extra spaces

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
        folder_name = self.field_2_2.get().strip()  # Get the folder name and remove extra spaces

        if not folder_name:
            self.display_feedback("Error: Folder name cannot be empty.")
            return

        # Check if the folder exists
        if not os.path.isdir(folder_name):
            self.display_feedback(f"Error: Folder '{folder_name}' does not exist.")
            return

        try:
            # Iterate through all files in the folder
            for filename in os.listdir(folder_name):
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

    def submit_firmware(self):
        firmware_name = self.field_2_1.get().strip()  # Get the name and remove extra spaces

        if not firmware_name:
            self.display_feedback("Error: Firmware name cannot be empty.")
            return

        # firmware_path = os.path.join(firmware_folder, firmware_name)
        # if not os.path.isfile(firmware_path):
        #     self.display_feedback(f"Error: file '{firmware_name}' not found in firmwares folder.")
        #     return

        try:
            # Check if firmware_name exists in the database
            existing_firmwares = self.app.firmware_service.get_all()
            if any(firmware.name == firmware_name for firmware in existing_firmwares):
                self.display_feedback(f"Error: firmware '{firmware_name}' already exists in the table.")
                return

            # Create a new firmware entry
            new_firmware = Firmwares(name=firmware_name)  # Assuming name is the only field needed
            self.app.firmware_service.create(new_firmware)
            self.display_feedback("Successfully added to the firmwares table.")
        except Exception as e:
            self.display_feedback(f"Error when adding firmware to the table: {e}")

    