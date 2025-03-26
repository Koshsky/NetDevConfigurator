import logging

from gui import BaseTab, apply_error_handler

from .connection_handler import get_connection_handler
from .device_handler import get_device_handler
from utils.environ import get_env
from .action_handler import ActionHandler

logger = logging.getLogger("gui")


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
        self.connection_handler = None
        self.device_handler = None
        self.base_loaded = None
        self.action_handler = None

    def update_envs(self):
        self.connection_handler.update_envs()
        self.device_handler.update_envs()

    def _create_widgets(self):
        """Creates and arranges widgets within the tab."""
        self.connection_handler = get_connection_handler(self)
        self.device_handler = get_device_handler(self)
        self.action_handler = ActionHandler(self.connection_handler, self)

        self.connection_handler.create_widgets()
        self.device_handler.create_widgets()
        self.action_handler.create_action_buttons()

        self.create_feedback_area()

        logger.debug("Updating host info...")
        self.app.update_envs()

    def show_template(self):
        """Displays the current configuration template."""
        logger.debug("Showing configuration template...")
        text = self.app.text_configuration
        self.display_feedback(text)
