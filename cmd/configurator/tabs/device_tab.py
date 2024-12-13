from internal.db_app.base_tab import BaseTab
from typing import Dict, List


class DeviceTab(BaseTab):        
    def create_widgets(self):
        self.create_block("device", {"name": list(self.app.devices)})
        self.create_button_in_line(("UPDATE TABS", self.update_tabs))
        self.create_feedback_area()

    def update_tabs(self):
        try:
            self.app.device = self.check_device_name(self.fields["device"]["name"].get())
            self.app.ports = self.app.entity_services['device_port'].get_device_ports(self.app.device.id)
            self.app.interface_templates = ["role1", "role2", "role3"]
            self.app.header_templates = ["header1", "header2", "header3"]
            self.app.footer_templates = ["footer1", "footer2", "footer3"]
            for tab in self.app.tabs[1:]:
                tab.clear_frame()
                tab.create_widgets()
            self.display_feedback(f'device {self.app.device.name} registered.\n')
        except Exception as e:
            self.display_feedback(f"An error: {e}")
