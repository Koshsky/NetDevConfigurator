import logging

from config import config
from gui import BaseTab, apply_error_handler
from utils.environ import set_env

from .connection_handler import CONNECTION_TYPES

logger = logging.getLogger("gui")


@apply_error_handler
class HelloTab(BaseTab):
    def _create_widgets(self):
        self._create_device_block()
        self._create_common_block()
        self._create_connection_buttons()

    def prepare(self, connection_type):
        set_env("CONNECTION_TYPE", connection_type)
        set_env("CERT", self.fields["common"]["CERT"].get().strip())
        device = self.app.db_services["device"].get_one(
            name=self.fields["device"]["name"].get().strip()
        )
        self.app.register_device(device)

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
        for connection_type, label in CONNECTION_TYPES.items():
            self.create_button_in_line(
                (label, lambda ct=connection_type: self.prepare(ct))
            )
