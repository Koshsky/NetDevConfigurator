import logging

from config import config
from gui import BaseTab, apply_error_handler
from locales import get_string
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
            mock_enabled: Whether MOCK connection is enabled.
        """
        super().__init__(parent, app, log_name)
        self.mock_enabled = mock_enabled
        self.lang = app.lang

    def _create_widgets(self) -> None:
        """Creates the widgets for the HelloTab."""
        self._create_device_block()
        self._create_common_block()
        self._create_connection_buttons()

    def update_envs(self):
        set_env(
            "CERT",
            self.fields[get_string(self.lang, "HELLO", "COMMON_BLOCK")][
                get_string(self.lang, "HELLO", "CERT")
            ]
            .get()
            .strip(),
        )
        set_env(
            "TFTP_ADDRESS",
            self.fields[get_string(self.lang, "HELLO", "COMMON_BLOCK")][
                get_string(self.lang, "HELLO", "TFTP")
            ]
            .get()
            .strip(),
        )

    def prepare(self, connection_type: str) -> None:
        """Prepares the connection by setting environment variables and registering the device.

        Args:
            connection_type: The type of connection.
        """
        set_env("CONNECTION_TYPE", connection_type)
        device = self.app.db_services["device"].get_one(
            name=self.fields[get_string(self.lang, "HELLO", "DEVICE_BLOCK")][
                get_string(self.lang, "HELLO", "DEVICE_NAME")
            ]
            .get()
            .strip()
        )
        self.app.register_device(device)

    def _create_device_block(self) -> None:
        """Creates the device selection block."""
        devices = self.app.db_services["device"].get_all()
        self.create_block(
            get_string(self.lang, "HELLO", "DEVICE_BLOCK"),
            {
                get_string(self.lang, "HELLO", "DEVICE_NAME"): tuple(
                    d.name for d in devices
                )
            },
        )

    def _create_common_block(self) -> None:
        """Creates the common settings block, currently for certificates."""
        self.create_block(
            get_string(self.lang, "HELLO", "COMMON_BLOCK"),
            {
                get_string(self.lang, "HELLO", "CERT"): config.default_cert,
                get_string(self.lang, "HELLO", "TFTP"): config.tftp.address,
            },
        )

    def _create_connection_buttons(self) -> None:
        """Creates the connection type selection buttons."""
        # Фильтруем типы подключений в зависимости от флага mock_enabled
        available_types = CONNECTION_TYPES

        for connection_type in available_types:
            if connection_type == "MOCK" and not self.mock_enabled:
                continue
            self.create_button_in_line(
                (
                    get_string(self.lang, "HELLO", f"CONNECTION_{connection_type}"),
                    lambda ct=connection_type: self.prepare(ct),
                )
            )
