import os
import pprint

from internal.database.services import determine_firmware_type

from internal.db_app import BaseTab, error_handler

class AddTab(BaseTab):
    def create_widgets(self):
        self.create_block("company", {"name": None}, ("SUBMIT", self.submit_company))
        self.create_block("family", {"name": None}, ("SUBMIT", self.submit_family))
        self.create_block("firmware", {"folder": ('./firmwares',)}, ("SUBMIT", self.submit_firmwares_from_folder))
        self.create_block("protocol", {"name": None}, ("SUBMIT", self.submit_protocol))
        self.create_block(
            "device",
            {
                "name": None,
                "company": self.app.entity_collections['company'],
                "family": self.app.entity_collections['family'],
                "dev_type": ("switch", "router"),
            },
            ("SUBMIT", self.submit_device)
        )
        self.create_block(
            "template",
            {
                "name": None,
                "family": self.app.entity_collections['family'],
                "type": self.app.entity_collections['template_type'],
                "role": self.app.entity_collections['role'],
                'text': None
            },
            ('SUBMIT', self.submit_template)
        )
        self.create_block(
            "preset",
            {
                "name": None,
                "device": self.app.entity_collections['device'],
                "role": self.app.entity_collections['role'],
            },
            ('SUBMIT', self.submit_preset)
        )
        self.create_feedback_area()

    @error_handler
    def submit_preset(self):
        device = self.check_device_name(self.fields['preset']['device'].get())
        preset_name = self.fields['preset']['name'].get().strip()
        if not preset_name:
            raise ValueError("Preset name cannot be empty.")
        role = self.fields['template']['role'].get().strip()
        if role not in self.entity_collections['role'] or role == 'common':
            raise ValueError("Invalid role.")

        self.app.entity_services['preset'].create(
            {
                'name': preset_name,
                'role': role,
                'device_id': device.id
            }
        )

    @error_handler
    def submit_template(self):
        template_name = self.fields['template']['name'].get().strip()
        template_type = self.fields['template']['type'].get().strip()
        role = self.fields['template']['role'].get().strip()
        text = self.fields['template']['text'].get().strip()

        if not template_name:
            raise ValueError("Template name cannot be empty.")
        if not template_type:
            raise ValueError("Select template type")
        if not role:
            raise ValueError("Select template role")
        if not text:
            raise ValueError("Template text cannot be empty.")

        family = self.check_family_name(self.fields['template']['family'].get())

        self.app.entity_services['template'].create(
            {
                'name': template_name,
                'family_id': family.id,
                'type': template_type,
                'role': role,
                'text': text
            }
        )

        self.display_feedback("Successfully added to the templates table.")
    @error_handler
    def submit_protocol(self):
        protocol_name = self.fields['protocol']['name'].get().strip()
        if not protocol_name:
            raise ValueError("Protocol name cannot be empty.")

        self.app.entity_services["protocol"].create({"name": protocol_name})
        self.display_feedback("Successfully added to the protocols table.")

    @error_handler
    def submit_family(self):
        family_name = self.fields['family']['name'].get().strip()
        if not family_name:
            raise ValueError("Family name cannot be empty.")

        self.app.entity_services["family"].create({"name": family_name})
        self.display_feedback("Successfully added to the families table.")

    @error_handler
    def submit_device(self):
        device_name = self.fields["device"]["name"].get().strip()
        dev_type = self.fields["device"]["dev_type"].get().strip()

        if not device_name:
            raise ValueError("Device name cannot be empty.")
        if not dev_type:
            raise ValueError("Select device type")

        company = self.check_company_name(self.fields["device"]["company"].get())
        family = self.check_family_name(self.fields["device"]["family"].get())
        new_device = {
            "name": device_name,
            "company_id": company.id,
            "family_id": family.id,
            "dev_type": dev_type,
        }

        device = self.app.entity_services["device"].create(new_device)

        self.display_feedback("Successfully added to the devices table.")

    @error_handler
    def submit_company(self):
        company_name = self.fields['company']['name'].get().strip()
        if not company_name:
            raise ValueError("Company name cannot be empty.")

        self.app.entity_services["company"].create({"name": company_name})
        self.display_feedback("Successfully added to the companies table.")

    @error_handler
    def submit_firmwares_from_folder(self):
        folder_name = self.fields['firmware']['folder'].get().strip()
        if not folder_name:
            raise ValueError("Folder name cannot be empty.")
        if not os.path.isdir(folder_name):
            raise ValueError("Folder '{folder_name}' does not exist.")

        folder_name = folder_name if os.path.isabs(folder_name) else os.path.abspath(folder_name)
        existing_firmwares = [firmware.name for firmware in self.app.entity_services["firmware"].get_all()]
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
            self.app.entity_services["firmware"].create(new_firmware)

        self.display_feedback("Successfully added new firmwares from the folder.")
