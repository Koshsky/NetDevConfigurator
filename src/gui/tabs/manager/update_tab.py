from gui import BaseTab, apply_error_handler


@apply_error_handler
class UpdateTab(BaseTab):
    def refresh_widgets(self):
        super().refresh_widgets()
        self.create_block("device", {"name": self.app.entity_collections["device"]})
        self.create_block("maska", {"boot": None, "uboot": None, "firmware": None})
        self.create_button_in_line(("UPDATE", lambda: self.write_maska(link=True)))
        self.create_feedback_area()

    def write_maska(self, link: bool):
        device = self.check_device_name(self.fields["device"]["name"].get().strip())
        self.app.db_services["device"].update_files(
            device,
            boot=self.fields["maska"]["boot"].get().strip(),
            uboot=self.fields["maska"]["uboot"].get().strip(),
            firmware=self.fields["maska"]["firmware"].get().strip(),
        )
        self.display_feedback("Linked device with firmware successfully.")
