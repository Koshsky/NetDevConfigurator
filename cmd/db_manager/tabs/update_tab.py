from internal.db_app import BaseTab, error_handler
from sqlalchemy.exc import IntegrityError


class UpdateTab(BaseTab):
    def create_widgets(self):
        self.create_block("device", {"name":None}, None)
        self.create_block("firmware", {"name":None}, None)
        self.create_button_in_line(("LINK", lambda: self._manage_link(link=True)))
        self.create_button_in_line(("UNLINK", lambda: self._manage_link(link=False)))
        self.create_feedback_area()

    @error_handler
    def _manage_link(self, link: bool):
        device = self.check_device_name(self.fields["device"]["name"].get().strip())
        firmware = self.check_firmware_name(self.fields["firmware"]["name"].get().strip())

        service = self.app.entity_services["device_firmware"]

        if link:
            service.create({"device_id": device.id, "firmware_id": firmware.id})
            message = "Linked device with firmware successfully."
        else:
            service.delete_by_device_firmware_id(device.id, firmware.id)
            message = "Unlinked device with firmware successfully."

        self.display_feedback(message)

