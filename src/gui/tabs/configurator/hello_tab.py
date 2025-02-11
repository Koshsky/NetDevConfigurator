import logging

from config import config
from gui import BaseTab, apply_error_handler
from utils import set_env

logger = logging.getLogger("gui")


@apply_error_handler
class HelloTab(BaseTab):
    def _create_widgets(self):
        self._create_device_block()
        self._create_common_block()
        self._create_connection_buttons()

    def prepare(self, connection_type):
        device = self.check_device_name(self.fields["device"]["name"].get())
        self.app.register_device(device)

        set_env("CERT", self.fields["common"]["CERT"].get().strip())
        set_env("CONNECTION_TYPE", connection_type)
        self.app.refresh_tabs()

    def _create_device_block(self):
        self.create_block(
            "device",
            {
                "name": self.app.entity_collections["device"],
            },
        )

    def _create_common_block(self):
        self.create_block(
            "common",
            {
                "CERT": (config["default-cert"],),
            },
        )

    def _create_connection_buttons(self):
        connection_types = [("COM+SSH", "com+ssh"), ("SSH", "ssh")]
        for label, connection_type in connection_types:
            self.create_button_in_line(
                (label, lambda ct=connection_type: self.prepare(ct))
            )
