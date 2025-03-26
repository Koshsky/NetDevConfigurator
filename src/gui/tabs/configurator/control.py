import logging
from typing import TYPE_CHECKING

from config import config
from gui import BaseTab, apply_error_handler
from utils.environ import env_converter, get_env
from .connection_handler import get_connection_handler
from .device_handler import get_device_handler
from .action_handler import ActionHandler

if TYPE_CHECKING:
    from .connection_handler import ConnectionHandler
    from .device_handler import DeviceHandler
    from .action_handler import ActionHandler

logger = logging.getLogger("gui")


class Refresher:
    """Manages widget updates and refreshes."""

    def __init__(self, tab: "ControlTab"):
        """Initialize the refresher.

        Args:
            tab: The parent ControlTab instance.
        """
        self.tab = tab
        self.lang = tab.app.lang
        self.connection_handler: "ConnectionHandler" = None
        self.device_handler: "DeviceHandler" = None
        self.action_handler: "ActionHandler" = None
        self.logger = logging.getLogger(__name__)

    def initialize_handlers(self):
        """Initialize all handlers with the tab widget."""
        self.connection_handler = get_connection_handler(self.tab)
        self.device_handler = get_device_handler(self.tab)
        self.action_handler = ActionHandler(self.connection_handler, self.tab)

    def create_widgets(self):
        """Create all widgets using handlers."""
        self._create_connection_widgets()
        self._create_device_widgets()
        self._create_action_buttons()
        self.tab.create_feedback_area()
        self._actualize_values()

    def _actualize_values(self):
        """Actualize values from the connection handler."""
        logger.debug("Actualizing connection values...")
        for var_name, field in self.connection_handler.env_vars.items():
            field = field[self.lang]
            if field in self.tab.fields["host"] and (value := get_env(var_name)):
                self.tab.fields["host"][field].set(value)
        logger.debug("Actualizing device values...")
        for env_var, field in self.device_handler.env_vars.items():
            field = field[self.lang]
            if field in self.tab.fields[""] and (value := get_env(env_var)):
                self.tab.fields[""][field].set(value)

    def _create_connection_widgets(self):
        """Creates widgets for connection parameters."""
        self.tab.create_block(
            "host",
            {
                field[self.lang]: tuple(getattr(config.host, field['en']))
                for field in self.connection_handler.env_vars.values()
            },
        )

    def _create_device_widgets(self):
        """Create device-related widgets."""
        if get_env("DEV_TYPE") == "switch":
            self.tab.create_block(
                "",
                {
                    field[self.lang]: self.app.device["roles"]
                    for field in self.device_handler.env_vars.values()
                },
            )
        elif get_env("DEV_TYPE") == "router":
            self.tab.create_block(
                "",
                {
                    field[self.lang]: tuple(env_converter["TYPE_COMPLEX"],)
                    for field in self.device_handler.env_vars.values()
                },
            )

    def _create_action_buttons(self):
        """Create action buttons."""
        for text, action in self.action_handler.get_available_actions():
            self.tab.create_button_in_line((text[self.lang], action))

@apply_error_handler
class ControlTab(BaseTab):
    """Control tab for managing network devices."""

    def __init__(self, tab, *args, **kwargs):
        """Initialize the control tab.

        Args:
            tab: The tab widget.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(tab, *args, **kwargs)
        self.refresher = Refresher(self)
        self.base_loaded = None

    def update_envs(self):
        """Update environment variables for all handlers."""
        self.connection_handler.update_envs()
        self.device_handler.update_envs()


    def _create_widgets(self):
        """Creates and arranges widgets within the tab."""
        self.refresher.initialize_handlers()
        self.refresher.create_widgets()

    def show_template(self):
        """Displays the current configuration template."""
        logger.debug("Showing configuration template...")
        text = self.app.text_configuration
        self.display_feedback(text)
