import logging

from config import config
from gui import BaseTab, apply_error_handler
from utils import set_env

logger = logging.getLogger("gui")


@apply_error_handler
class HelloTab(BaseTab):
    def _render_widgets(self):
        self.create_block(
            "device",
            {
                "name": self.app.entity_collections["device"],
            },
        )
        self.create_block(
            "common",
            {
                "CERT": (config["default-cert"],),
            },
        )

        self.create_button_in_line(("COM+SSH", lambda: self.prepare("com+ssh")))
        self.create_button_in_line(("SSH", lambda: self.prepare("ssh")))

    def prepare(self, connection_type):
        self.register_device()
        set_env("CONNECTION_TYPE", connection_type)
        self.app.refresh_tabs()

    def register_device(self):
        device = self.check_device_name(self.fields["device"]["name"].get())
        self.app.register_device(device)

        set_env("CERT", self.fields["common"]["CERT"].get().strip())
