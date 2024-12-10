from internal.db_app.base_tab import BaseTab

class DeviceInfoTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app, "SHOW")

    def create_widgets(self):
        self.create_block("device", {"name":None}, self.show_information)  # TODO: тут должен быть нормальный список девайсов...
        self.create_feedback_area()

    def show_information(self):
        try:
            device = self.check_device_name(self.fields["device"]["name"].get())
            associated_firmwares = self.app.device_firmware_service.get_firmwares_by_device_id(device.id)

            company = self.app.company_service.get_by_id(device.company_id)
            company_name = company.name if company else "Unknown Company"  # UNREACHABLE по идее...

            firmware_list = "\n\t".join(firmware.name for firmware in associated_firmwares) if associated_firmwares else "No associated firmwares."
            
            output_message = (
                f"Device Information:\n"
                f"Name: {device.name}\n"
                f"ID: {device.id}\n"
                f"Company: {company_name}\n"
                f"Device Type: {device.dev_type}\n"
                f"Port Number: {device.port_num}\n"
                f"Associated Firmwares:\n\t{firmware_list}\n"
            )
            
            self.display_feedback(output_message)
        except Exception as e:
            self.display_feedback(f"Error retrieving device information:\n{e}")
