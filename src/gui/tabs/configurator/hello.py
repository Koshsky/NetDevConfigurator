import logging

from config import config
from gui import BaseTab, apply_error_handler
from utils.environ import set_env

from .connection_handler import CONNECTION_TYPES

logger = logging.getLogger("gui")


@apply_error_handler
class HelloTab(BaseTab):
    """Initial setup tab for device and connection configuration."""

    def __init__(self, parent, app, log_name="HelloTab", mock_enabled=False):
        """Initialize the HelloTab.

        Args:
            parent: The parent widget.
            app: The application instance.
            log_name: The name of the tab for logging.
            mock_enabled: Whether mock mode is enabled.
        """
        super().__init__(parent, app, log_name)
        self.mock_enabled = mock_enabled

    def _create_widgets(self) -> None:
        """Creates the widgets for the HelloTab."""
        self._create_device_block()
        self._create_common_block()
        self._create_connection_buttons()

    def update_envs(self):
        set_env("CERT", self.fields["common"]["CERT"].get().strip())
        set_env("TFTP_ADDRESS", self.fields["common"]["TFTP"].get().strip())

    def prepare(self, connection_type: str) -> None:
        """Prepares the connection by setting environment variables and registering the device.

        Args:
            connection_type: The type of connection.
        """
        set_env("CONNECTION_TYPE", connection_type)
        self.update_envs()
        device = self.app.db_services["device"].get_one(
            name=self.fields["device"]["name"].get().strip()
        )
        self.app.register_device(device)

    def _create_device_block(self) -> None:
        """Creates the device selection block."""
        devices = self.app.db_services["device"].get_all()
        self.create_block("device", {"name": tuple(d.name for d in devices)})

    def _create_common_block(self) -> None:
        """Creates the common settings block, currently for certificates."""
        self.create_block(
            "common", {"CERT": (config.default_cert,), "TFTP": (config.tftp.address,)}
        )

    def _create_connection_buttons(self) -> None:
        """Creates the connection type selection buttons."""
        # Фильтруем типы подключений в зависимости от флага mock_enabled
        available_types = {
            k: v
            for k, v in CONNECTION_TYPES.items()
            if k != "mock" or self.mock_enabled
        }

        for connection_type, label in available_types.items():
            self.create_button_in_line(
                (label, lambda ct=connection_type: self.prepare(ct))
            )
