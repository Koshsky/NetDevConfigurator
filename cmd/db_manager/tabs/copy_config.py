from internal.db_app import error_handler
from .common_config import CommonConfigTab, update_config

class CopyConfigTab(CommonConfigTab):
    def create_widgets(self):
        self.create_block("from", {
            "device": list(self.app.entity_collections['devices']),
            "preset": list(self.app.entity_collections['presets'])
        })
        self.create_block("to", {
            "device": list(self.app.entity_collections['devices']),
            "preset": None
        })
        self.create_button_in_line(("COPY", self.copy))
        self.create_feedback_area()

    @error_handler
    @update_config
    def copy(self) -> str:
        device = self.check_device_name(self.fields['from']['device'].get())
        dist_device = self.check_device_name(self.fields['to']['device'].get())
        if device == dist_device:
            raise ValueError("device_from == device_to")

        preset = self.fields['from']['preset'].get().strip()
        if preset not in self.app.entity_collections['presets']:
            raise ValueError("Unknown preset_from")

        new_preset = self.fields['to']['preset'].get().strip()
        if new_preset in self.app.entity_collections['presets']:
            raise ValueError("preset_to already exists")



        self.preset = preset
        self.device = device
