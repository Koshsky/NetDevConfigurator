from internal.db_app.base_tab import BaseTab

class InfoTab(BaseTab):
    def create_widgets(self):
        entities = ['company', 'family', 'device', 'firmware', 'template_piece']
        for entity in entities:
            self.create_block(entity, {"name":None}, ("SHOW", getattr(self, f'show_{entity}_info')))
        self.create_feedback_area()
        
    def show_template_piece_info(self):
        try:
            template_piece = self.check_template_piece_name(self.fields['template_piece']['name'].get())
        except Exception as e:
            self.show_error("Retrieval Error", e)
            return
        
        self.display_feedback(
            f"Template Piece Information:\n"
            f"id: {template_piece.id}\n"
            f"name: {template_piece.name}\n"
            f"type: {template_piece.type}\n"
            f"role: {template_piece.role}\n"
            f"text:\n{template_piece.text}\n"
        )

            
    def show_device_info(self):
        try:
            device = self.check_device_name(self.fields["device"]["name"].get())
        except Exception as e:
            self.show_error("Retrieval Error", e)
            return
        
        company_name = self.app.entity_services["company"].get_by_id(device.company_id).name
        family_name = self.app.entity_services["family"].get_by_id(device.family_id).name
        protocol_list = self._stringify_list(self.app.entity_services["device_protocol"].get_protocols_by_device_id(device.id))
        firmware_list = self._stringify_list(self.app.entity_services["device_firmware"].get_firmwares_by_device_id(device.id))
                
        self.display_feedback(
            f"{device.name}(id={device.id}) Information:\n"
            f"Company: {company_name}\n"
            f"Family: {family_name}\n"
            f"Device Type: {device.dev_type}\n"
            f"Associated Protocols:\n\t{protocol_list}\n"
            f"Associated Firmwares:\n\t{firmware_list}\n"
        )

    def show_family_info(self):  # sourcery skip: class-extract-method
        try:
            family = self.check_family_name(self.fields["family"]["name"].get())
        except Exception as e:
            self.show_error("Retrieval Error", e)
            return
            
        device_list = self._stringify_list(self.app.entity_services["device"].get_devices_by_family_id(family.id))
                
        self.display_feedback(
            f"Family Information:\n"
            f"Name: {family.name}\n"
            f"ID: {family.id}\n"
            f"Associated devices:\n\t{device_list}\n"
        )
            
    def show_company_info(self):
        try:
            company = self.check_company_name(self.fields["company"]["name"].get())
        except Exception as e:
            self.show_error("Retrieval Error", e)
            return

        device_list = self._stringify_list(self.app.entity_services["device"].get_devices_by_company_id(company.id))
        
        self.display_feedback(
            f"Company Information:\n"
            f"Name: {company.name}\n"
            f"ID: {company.id}\n"
            f"Associated devices:\n\t{device_list}\n"
            )

    def show_firmware_info(self):
        try:
            firmware = self.check_firmware_name(self.fields["firmware"]["name"].get())
        except Exception as e:
            self.show_error("Retrieval Error", e)
            return
            
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
