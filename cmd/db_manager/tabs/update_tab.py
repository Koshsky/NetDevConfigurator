from internal.db_app import BaseTab, error_handler
from sqlalchemy.exc import IntegrityError
class UpdateTab(BaseTab):                          # TODO: ДОБАВИТЬ СВЯЗКУ УСТРОЙСТВ С ПРОТОКОЛАМИ. КАК ЭТО СДЕЛАТЬ?
    def create_widgets(self):
        self.create_block("device", {"name":None}, None)
        self.create_block("firmware", {"name":None}, None)
        self.create_button_in_line(("LINK", self.link))
        self.create_button_in_line(("UNLINK", self.unlink))
        self.create_feedback_area()

    @error_handler
    def link(self):
        device = self.check_device_name(self.fields["device"]["name"].get().strip())
        firmware = self.check_firmware_name(self.fields["firmware"]["name"].get().strip())

        self.app.entity_services["device_firmware"].create({"device_id": device.id, "firmware_id": firmware.id})
        self.display_feedback("Linked device with firmware successfully.")

    @error_handler
    def unlink(self):
            device = self.check_device_name(self.fields["device"]["name"].get().strip())
            firmware = self.check_firmware_name(self.fields["firmware"]["name"].get().strip())
            self.app.entity_services["device_firmware"].delete_by_device_firmware_id(device.id, firmware.id)
            self.display_feedback("Unlinked device with firmware successfully.")
            