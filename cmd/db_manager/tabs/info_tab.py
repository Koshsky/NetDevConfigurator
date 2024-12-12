from internal.db_app.base_tab import BaseTab

class InfoTab(BaseTab):
    def create_widgets(self):
        self.create_block("company", {"name":None}, ("SHOW", self.show_company_info))
        self.create_block("family", {"name":None}, ("SHOW", self.show_family_info))
        self.create_block("device", {"name":None}, ("SHOW", self.show_device_info))
        self.create_block("firmare", {"name":None}, ("SHOW", self.show_firmware_info))
        self.create_feedback_area()

    def show_device_info(self):
        try:
            device = self.check_device_name(self.fields["device"]["name"].get())
            associated_firmwares = self.app.entity_services["device_firmware"].get_firmwares_by_device_id(device.id)
            associated_protocols = self.app.entity_services["device_protocol"].get_protocols_by_device_id(device.id)

            company = self.app.entity_services["company"].get_by_id(device.company_id)
            family = self.app.entity_services["family"].get_by_id(device.family_id)
            company_name = company.name if company else "Unknown Company"  # UNREACHABLE по идее...
            family_name = family.name if family else "Unknown Family"  # UNREACHABLE по идее...

            firmware_list = "\n\t".join(firmware.name for firmware in associated_firmwares) if associated_firmwares else "No associated firmwares."
            protocol_list = "\n\t".join(protocol.name for protocol in associated_protocols) if associated_protocols else "No associated firmwares."
            
            output_message = (
                f"Device Information:\n"
                f"Name: {device.name}\n"
                f"ID: {device.id}\n"
                f"Company: {company_name}\n"
                f"Family: {family_name}\n"
                f"Device Type: {device.dev_type}\n"
                f"Number of ports\n"
                f"\tgigabit: {device.num_gigabit_ports}\n"
                f"\t10gigabit: {device.num_10gigabit_ports}\n"
                f"Associated Protocols:\n\t{protocol_list}\n"
                f"Associated Firmwares:\n\t{firmware_list}\n"
            )
            
            self.display_feedback(output_message)
        except Exception as e:
            self.display_feedback(f"Error retrieving device information:\n{e}")

    def show_family_info(self):  # sourcery skip: class-extract-method
        try:
            family = self.check_family_name(self.fields["family"]["name"].get())
            associated_devices = self.app.entity_services["device"].get_devices_by_family_id(family.id)

            device_list = "\n\t".join(device.name for device in associated_devices) if associated_devices else "No associated devices."
            
            output_message = (
                f"Family Information:\n"
                f"Name: {family.name}\n"
                f"ID: {family.id}\n"
                f"Associated devices:\n\t{device_list}\n"
            )
            
            self.display_feedback(output_message)
        except Exception as e:
            self.display_feedback(f"Error retrieving family information:\n{e}")

    def show_company_info(self):
        try:
            company = self.check_company_name(self.fields["company"]["name"].get())
            associated_devices = self.app.entity_services["device"].get_devices_by_company_id(company.id)

            device_list = "\n\t".join(device.name for device in associated_devices) if associated_devices else "No associated devices."
            
            output_message = (
                f"Company Information:\n"
                f"Name: {company.name}\n"
                f"ID: {company.id}\n"
                f"Associated devices:\n\t{device_list}\n"
            )
            
            self.display_feedback(output_message)
        except Exception as e:
            self.display_feedback(f"Error retrieving company information:\n{e}")

    def show_firmware_info(self):
        try:
            firmware = self.check_firmware_name(self.fields["firmware"]["name"].get())
            associated_devices = self.app.entity_services["device_firmware"].get_devices_by_firmware_id(firmware.id)\

            device_list = "\n\t".join(device.name for device in associated_devices) if associated_devices else "No associated device."
            
            output_message = (
                f"Firmware Information:\n"
                f"Name: {firmware.name}\n"
                f"Full_path: {firmware.full_path}\n"
                f"Type: {firmware.type}\n"
                f"ID: {firmware.id}\n"\
                f"Associated Devices:\n\t{device_list}\n"
            )
            
            self.display_feedback(output_message)
        except Exception as e:
            self.display_feedback(f"Error retrieving firmware information:\n{e}")
