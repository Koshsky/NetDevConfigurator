from internal.db_app import error_handler
from .common_config import CommonConfigTab, update_config

class CopyConfigTab(CommonConfigTab):
    def create_widgets(self):
        self.create_block("preset", {
            "from": list(self.app.entity_collections['preset']),
            "to": None
        })
        self.create_button_in_line(("COPY", self.copy))
        self.create_feedback_area()

    @error_handler
    @update_config
    def copy(self) -> str:
        source = self.check_preset_name(self.fields['preset']['from'].get())
        destination = self.check_preset_name(self.fields['preset']['to'].get())
        if source == destination:
            raise ValueError("source == destination")