import logging
from typing import TYPE_CHECKING

from gui import BaseTab, apply_error_handler

from .connection_handler import get_connection_handler
from .device_handler import get_device_handler
from utils.environ import get_env
from .action_handler import ActionHandler

if TYPE_CHECKING:
    from .connection_handler import ConnectionHandler
    from .device_handler import DeviceHandler
    from .action_handler import ActionHandler

logger = logging.getLogger("gui")


class Refresher:
    """Manages widget updates and refreshes."""

    def __init__(self, parent: "ControlTab"):
        """Initialize the refresher.

        Args:
            parent: The parent ControlTab instance.
        """
        self.parent = parent
        self.connection_handler: "ConnectionHandler" = None
        self.device_handler: "DeviceHandler" = None
        self.action_handler: "ActionHandler" = None
        self.logger = logging.getLogger(__name__)

    def initialize_handlers(self):
        """Initialize all handlers with the parent widget."""
        self.connection_handler = get_connection_handler(self.parent)
        self.device_handler = get_device_handler(self.parent)
        self.action_handler = ActionHandler(self.connection_handler, self.parent)

    def create_widgets(self):
        """Create all widgets using handlers."""
        self.connection_handler.create_widgets()
        self.device_handler.create_widgets()
        self.action_handler.create_action_buttons()
        self.parent.create_feedback_area()

    def update_envs(self):
        """Update environment variables for all handlers."""
        self.connection_handler.update_envs()
        self.device_handler.update_envs()


@apply_error_handler
class ControlTab(BaseTab):
    """Control tab for managing network devices."""

    def __init__(self, parent, *args, **kwargs):
        """Initialize the control tab.

        Args:
            parent: The parent widget.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(parent, *args, **kwargs)
        self.refresher = Refresher(self)
        self.base_loaded = None

    def update_envs(self):
        """Update environment variables."""
        self.refresher.update_envs()

    def _create_widgets(self):
        """Creates and arranges widgets within the tab."""
        self.refresher.initialize_handlers()
        self.refresher.create_widgets()

    def show_template(self):
        """Displays the current configuration template."""
        logger.debug("Showing configuration template...")
        text = self.app.text_configuration
        self.display_feedback(text)
