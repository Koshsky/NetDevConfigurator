from internal.db_app.base_tab import BaseTab

class DeviceInfoTab(BaseTab):
    def create_widgets(self):
        self.create_block("device", {"name":None}, ("SHOW", self.show_information))  # TODO: тут должен быть нормальный список девайсов...
        self.create_feedback_area()

    def show_information(self):
        try:
            device = self.check_device_name(self.fields["device"]["name"].get())
            associated_firmwares = self.app.device_firmware_service.get_firmwares_by_device_id(device.id)
            associated_protocols = self.app.device_protocol_service.get_protocols_by_device_id(device.id)

            company = self.app.company_service.get_by_id(device.company_id)
            family = self.app.family_service.get_by_id(device.family_id)
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
