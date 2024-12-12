from internal.db_app.base_tab import BaseTab

class DeviceTab(BaseTab):
    def create_widgets(self):
        self.create_block("device", {
                "name":None,
                "protocols": self.app.protocols,
                "ports": self.get_port_list()
        }, width=15)


    def get_port_list(self):
        return {        
            f"0/{i}": self.app.ports
            for i in range(60)
        }

    def link(self):
        try:
            device = self.check_device_name(self.fields["device"]["name"].get().strip())
            firmware = self.check_firmware_name(self.fields["firmware"]["name"].get().strip())

            self.app.entity_services["device_firmware"].link(device.id, firmware.id)
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

            self.app.entity_services["device_firmware"].unlink(device.id, firmware.id)
            self.display_feedback("Unlinked device with firmware successfully.")
        except ValueError as e:
            self.display_feedback(f"Error: {e}")
        except Exception as e:
            self.display_feedback(f"Error adding to database:\n{e}")
            self.app.session.rollback()