from internal.db_app.base_tab import BaseTab

class FirmwareInfoTab(BaseTab):
    def create_widgets(self):
        self.create_block("firmware", {"name":None}, ("SHOW", self.show_information))  # TODO: тут должен быть нормальный список прошивок...
        self.create_feedback_area()

    def show_information(self):
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
