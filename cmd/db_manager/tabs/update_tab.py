from internal.db_app.base_tab import BaseTab

class UpdateTab(BaseTab):                          # TODO: ДОБАВИТЬ СВЯЗКУ УСТРОЙСТВ С ПРОТОКОЛАМИ. КАК ЭТО СДЕЛАТЬ?
    def create_widgets(self):
        self.create_block("device", {"name":None}, None)
        self.create_block("firmware", {"name":None}, None)
        self.create_button_in_line(("LINK", self.link))
        self.create_block("devicе", {"name":None}, None)     # not ASCII symbol to avoid conflicts
        self.create_block("firmwarе", {"name":None}, None)
        self.create_button_in_line(("UNLINK", self.unlink))
        self.create_feedback_area()

    def link(self):
        try:
            device = self.check_device_name(self.fields["device"]["name"].get().strip())
            firmware = self.check_firmware_name(self.fields["firmware"]["name"].get().strip())

            self.app.device_firmware_service.link(device.id, firmware.id)
            self.display_feedback("Linked device with firmware successfully.")
        except ValueError as e:
            self.display_feedback(f"Error: {e}")
        except Exception as e:
            self.display_feedback(f"Error adding to database:\n{e}")
            self.app.session.rollback()


    def unlink(self):
        try:
            device = self.check_device_name(self.fields["devicе"]["name"].get().strip())
            firmware = self.check_firmware_name(self.fields["firmwarе"]["name"].get().strip())

            self.app.device_firmware_service.unlink(device.id, firmware.id)
            self.display_feedback("Unlinked device with firmware successfully.")
        except ValueError as e:
            self.display_feedback(f"Error: {e}")
        except Exception as e:
            self.display_feedback(f"Error adding to database:\n{e}")
            self.app.session.rollback()