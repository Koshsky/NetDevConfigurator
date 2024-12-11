import os
import pprint

from internal.database.services import determine_firmware_type

from internal.db_app.base_tab import BaseTab

class AddTab(BaseTab):
    def __init__(self, parent, app):
        # TODO: или убрать вовсе в поля self.app чтобы можно было получить доступ из любой вкладки.
        super().__init__(parent, app)

    def create_widgets(self):
        self.create_block(
            "family", 
            {"name": None}, 
            ("SUBMIT", self.submit_family)
        )
        self.create_block(
            "company", 
            {"name": None}, 
            ("SUBMIT", self.submit_company)
        )
        self.create_block(
            "protocol",
            {"name": None},
            ("SUBMIT", self.submit_protocol)
        )
        self.create_block(
            "firmware", 
            {"folder": ['./firmwares']}, 
            ("SUBMIT", self.submit_firmwares_from_folder)
        )
        self.create_block(
            "device", 
            {
                "name": None,
                "protocols": self.app.protocols,                 
                "company": list(self.app.companies),
                "family": list(self.app.families),
                "dev_type": ["switch", "router"],
                "num_gigabit_ports": [24, 48],
                "num_10gigabit_ports": [4, 6]
            }, 
            ("SUBMIT", self.submit_device)
        )
        self.create_feedback_area()
        
    def submit_protocol(self):
        protocol_name = self.fields['protocol']['name'].get().strip()
        if not protocol_name:
            self.display_feedback("Error: Protocol name cannot be empty.")
            return

        try:
            self.app.protocol_service.create({"name": protocol_name})
            self.display_feedback("Successfully added to the protocols table.")
        except Exception as e:
            self.display_feedback(f"Error adding to protocols table: {e}")
            self.app.session.rollback()
        
    def submit_family(self):
        family_name = self.fields['family']['name'].get().strip()
        if not family_name:
            self.display_feedback("Error: Family name cannot be empty.")
            return

        try:
            self.app.family_service.create({"name": family_name})
            self.display_feedback("Successfully added to the families table.")
        except Exception as e:
            self.display_feedback(f"Error adding to families table: {e}")
            self.app.session.rollback()
        
    
    def submit_device(self):  # sourcery skip: extract-method
        device_name = self.fields["device"]["name"].get().strip()
        dev_type = self.fields["device"]["dev_type"].get().strip()
        num_gigabit_ports = self.fields["device"]["num_gigabit_ports"].get().strip()
        num_10gigabit_ports = self.fields["device"]["num_10gigabit_ports"].get().strip()

        if not device_name:
            self.display_feedback("Error: Device name cannot be empty.")
            return
        if not dev_type:
            self.display_feedback("Error: Select device type")
            return
        if not num_gigabit_ports.isdigit() or not num_10gigabit_ports.isdigit():
            self.display_feedback("Error: Port number must be a valid integer.")
            return

        try:
            company = self.check_company_name(self.fields["device"]["company"].get())
            family = self.check_family_name(self.fields["device"]["family"].get())
            new_device = {
                "name": device_name,
                "company_id": company.id,
                "family_id": family.id,
                "dev_type": dev_type,
                "num_gigabit_ports": int(num_gigabit_ports),
                "num_10gigabit_ports": int(num_10gigabit_ports),
            }
            
            device = self.app.device_service.create(new_device)
            for protocol_name, checkbox in self.fields["device"]["protocols"].items():
                if checkbox.get() == 1:
                    protocol = self.check_protocol_name(protocol_name)
                    self.app.device_protocol_service.link(device.id, protocol.id)

            self.display_feedback("Successfully added to the devices table.")

        except Exception as e:
            self.display_feedback(f"Error adding to devices table: {e}")
            self.app.session.rollback()

    def link(self):
        try:
            device = self.check_device_name(self.fields["device"]["name"].get().strip())
            firmware = self.check_firmware_name(self.fields["firmware"]["name"].get().strip())

            self.app.device_firmware_service.link(device.id, firmware.id)
            self.display_feedback("Linked device with firmware successfully.")
        except ValueError as e:
            self.display_feedback(f"Error: {e}")
        except Exception as e:
            self.display_feedback(f"Error adding to database:\n{e}")
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

        folder_name = folder_name if os.path.isabs(folder_name) else os.path.abspath(folder_name)

        try:
            existing_firmwares = [firmware.name for firmware in self.app.firmware_service.get_all()]
            for filename in os.listdir(folder_name):
                firmware_name = filename
                if firmware_name in existing_firmwares:
                    print(f"Firmware '{firmware_name}' already exists in the table. Skipping.")
                    continue
                
                new_firmware = {
                        "name": firmware_name,
                        "full_path": f'{folder_name}/{firmware_name}',
                        "type": determine_firmware_type(firmware_name)
                }
                self.app.firmware_service.create(new_firmware)

            self.display_feedback("Successfully added new firmwares from the folder.")
        except Exception as e:
            self.display_feedback(f"Error adding firmwares from folder: {e}")
            self.app.session.rollback()
