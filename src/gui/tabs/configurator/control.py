import logging
from typing import TYPE_CHECKING

from config import config
from gui import BaseTab, apply_error_handler
from utils.environ import env_converter, get_env
from locales import get_string
from .connection_handler import get_connection_handler
from .device_handler import get_device_handler
from .action_handler import ActionHandler

if TYPE_CHECKING:
    from .connection_handler import ConnectionHandler
    from .device_handler import DeviceHandler
    from .action_handler import ActionHandler

logger = logging.getLogger("gui")


class Refresher(BaseTab):
    """Manages widget updates and refreshes."""

    def __init__(self, parent, app, log_name, *args, **kwargs):
        """Initialize the refresher.

        Args:
            tab: The parent ControlTab instance.
        """
        self.app = app
        self.lang = self.app.lang
        self.connection_handler: "ConnectionHandler" = None
        self.device_handler: "DeviceHandler" = None
        self.action_handler: "ActionHandler" = None
        super().__init__(parent, app, log_name, *args, **kwargs)

    def initialize_handlers(self):
        """Initialize all handlers with the tab widget."""
        self.connection_handler = get_connection_handler(self)
        self.device_handler = get_device_handler(self)
        self.action_handler = ActionHandler(self.connection_handler, self)

    def _create_widgets(self):
        """Create all widgets using handlers."""
        self.initialize_handlers()
        self.connection_handler.create_widgets()
        self.device_handler.create_widgets()
        self.action_handler.create_buttons()
        self.create_feedback_area()
        self._actualize_values()

    def _actualize_values(self):
        """Actualize values from the connection handler."""
        self.connection_handler.actualize_values()
        self.device_handler.actualize_values()

@apply_error_handler
class ControlTab(Refresher):
    """Control tab for managing network devices."""

    def __init__(self, parent, app, log_name="ControlTab", *args, **kwargs):
        """Initialize the control tab.

        Args:
            tab: The tab widget.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(parent, app, log_name, *args, **kwargs)
        self.base_loaded = None

    def update_envs(self):
        """Update environment variables for all handlers."""
        self.connection_handler.update_envs()
        self.device_handler.update_envs()
