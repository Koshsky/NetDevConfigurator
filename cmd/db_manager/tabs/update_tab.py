from internal.db_app.base_tab import BaseTab
from sqlalchemy.exc import IntegrityError
class UpdateTab(BaseTab):                          # TODO: ДОБАВИТЬ СВЯЗКУ УСТРОЙСТВ С ПРОТОКОЛАМИ. КАК ЭТО СДЕЛАТЬ?
    def create_widgets(self):
        self.create_block("device", {"name":None}, None)
        self.create_block("firmware", {"name":None}, None)
        self.create_button_in_line(("LINK", self.link))
        self.create_button_in_line(("UNLINK", self.unlink))
        self.create_feedback_area()

    def link(self):
        try:
            device = self.check_device_name(self.fields["device"]["name"].get().strip())
            firmware = self.check_firmware_name(self.fields["firmware"]["name"].get().strip())

            self.app.entity_services["device_firmware"].create({"device_id": device.id, "firmware_id": firmware.id})
            self.display_feedback("Linked device with firmware successfully.")
        except ValueError as e:
            self.show_error("Retrieval Error", e)
        except IntegrityError as e:
            self.show_error("Integrity Error", e)
            self.app.session.rollback()
        except Exception as e:
            print(e, type(e))


    def unlink(self):
        try:
            device = self.check_device_name(self.fields["device"]["name"].get().strip())
            firmware = self.check_firmware_name(self.fields["firmware"]["name"].get().strip())
            self.app.entity_services["device_firmware"].delete_by_device_firmware_id(device.id, firmware.id)
            self.display_feedback("Unlinked device with firmware successfully.")
        except ValueError as e:
            self.show_error("Retrieval Error", e)
        except Exception as e:
            print(e, type(e))