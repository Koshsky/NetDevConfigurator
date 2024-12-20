from internal.db_app import BaseTab, error_handler
from pprint import pformat

class InfoTab(BaseTab):
    def create_widgets(self):
        entities = ['company', 'family', 'device', 'firmware']
        for entity in entities:
            self.create_block(entity, {"name":None}, ("SHOW", getattr(self, f'show_{entity}_info')))
        self.create_block('template',
        {
            'name': None,
            'type': list(self.app.entity_collections['template_types']),
            'role': list(self.app.entity_collections['roles']),
        },
        ("SHOW", self.show_template_info))
        self.create_feedback_area()

    @error_handler
    def show_template_info(self):
        name = self.fields['template']['name'].get()
        type_ = self.fields['template']['type'].get()
        role = self.fields['template']['role'].get()
        template = self.app.entity_services['template'].get_by_name_type_role(name, type_, role)
        self.display_feedback(
            pformat(self.app.entity_services['template'].get_info_by_id(template.id))
        )

    @error_handler
    def show_device_info(self):
        device_name = self.fields["device"]["name"].get().strip()
        self.display_feedback(
            pformat(self.app.entity_services['device'].get_info_by_name(device_name))
        )


    @error_handler
    def show_family_info(self):  # sourcery skip: class-extract-method
        family = self.check_family_name(self.fields["family"]["name"].get())

        device_list = self._stringify_list(self.app.entity_services["device"].get_devices_by_family_id(family.id))

        self.display_feedback(
            f"Family Information:\n"
            f"Name: {family.name}\n"
            f"ID: {family.id}\n"
            f"Associated devices:\n\t{device_list}\n"
        )

    @error_handler
    def show_company_info(self):
        company = self.check_company_name(self.fields["company"]["name"].get())

        device_list = self._stringify_list(self.app.entity_services["device"].get_devices_by_company_id(company.id))

        self.display_feedback(
            f"Company Information:\n"
            f"Name: {company.name}\n"
            f"ID: {company.id}\n"
            f"Associated devices:\n\t{device_list}\n"
            )


    @error_handler
    def show_firmware_info(self):
        firmware = self.check_firmware_name(self.fields["firmware"]["name"].get())

        device_list = self._stringify_list(self.app.entity_services["device_firmware"].get_devices_by_firmware_id(firmware.id))

        self.display_feedback(
            f"Firmware Information:\n"
            f"Name: {firmware.name}\n"
            f"Full_path: {firmware.full_path}\n"
            f"Type: {firmware.type}\n"
            f"ID: {firmware.id}\n"\
            f"Associated Devices:\n\t{device_list}\n"
        )

    def _stringify_list(self, associated):
        return "\n\t".join(i.name for i in associated) if associated else "No associated"
