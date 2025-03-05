import logging

from config import config
from gui import BaseTab, apply_error_handler
from utils.environ import set_env

from .connection_handler import CONNECTION_TYPES

logger = logging.getLogger("gui")


@apply_error_handler
class HelloTab(BaseTab):
    """Initial setup tab for device and connection configuration."""

    def _create_widgets(self) -> None:
        """Creates the widgets for the HelloTab."""
        self._create_device_block()
        self._create_common_block()
        self._create_connection_buttons()

    def prepare(self, connection_type: str) -> None:
        """Prepares the connection by setting environment variables and registering the device.

        Args:
            connection_type: The type of connection.
        """
        set_env("CONNECTION_TYPE", connection_type)
        set_env("CERT", self.fields["common"]["CERT"].get().strip())
        device = self.app.db_services["device"].get_one(
            name=self.fields["device"]["name"].get().strip()
        )
        self.app.register_device(device)

    def _create_device_block(self) -> None:
        """Creates the device selection block."""
        self.create_block("device", {"name": self.app.entity_collections["device"]})

    def _create_common_block(self) -> None:
        """Creates the common settings block, currently for certificates."""
        self.create_block("common", {"CERT": (config["default-cert"],)})

    def _create_connection_buttons(self) -> None:
        """Creates the connection type selection buttons."""
        for connection_type, label in CONNECTION_TYPES.items():
            self.create_button_in_line(
                (label, lambda ct=connection_type: self.prepare(ct))
            )
