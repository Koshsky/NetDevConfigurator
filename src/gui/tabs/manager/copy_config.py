from gui import apply_error_handler
from .common_config import CommonConfigTab, update_config

@apply_error_handler
class CopyConfigTab(CommonConfigTab):
    def create_widgets(self):
        self.create_block("preset", {
            "from": self.app.entity_collections['preset'],
            "to": self.app.entity_collections['preset']
        })
        self.create_button_in_line(("COPY", self.copy))
        self.create_feedback_area()

    def copy(self) -> str:
        source = self.check_preset_name(self.fields['preset']['from'].get())
        destination = self.check_preset_name(self.fields['preset']['to'].get())
        self.app.db_services['preset'].copy(source, destination)
        self.display_feedback("Success")