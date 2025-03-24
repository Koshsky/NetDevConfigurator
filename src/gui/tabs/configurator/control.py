import logging

from gui import BaseTab, apply_error_handler

from .connection_handler import get_connection_handler
from .device_handler import get_device_handler
from utils.environ import get_env

logger = logging.getLogger("gui")


@apply_error_handler
class ControlTab(BaseTab):
    """Control tab for managing network devices."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_handler = None
        self.device_handler = None
        self.base_loaded = None

    def update_envs(self):
        self.connection_handler.update_envs()
        self.device_handler.update_envs()

    def _create_widgets(self):
        """Creates and arranges widgets within the tab."""
        self.connection_handler = get_connection_handler(self)
        self.device_handler = get_device_handler(self)
        self.connection_handler.create_widgets()
        self.device_handler.create_widgets()
        self._create_action_buttons()

        if get_env("ADVANCED_MODE") == "true":
            self.create_feedback_area()

        logger.debug("Updating host info...")
        self.app.update_envs()

    def _create_action_buttons(self):
        """Creates action buttons for device management."""
        if get_env("ADVANCED_MODE") == "true":
            actions = self.get_advanced_actions()
        else:
            actions = self.get_actions()
        for action, callback in actions:
            self.create_button_in_line((action, callback))

    def get_actions(self):
        """Returns a list of actions."""
        return [
            ("LOAD CONFIGURATION", self.connection_handler.load_configuration),
            ("UPDATE FIRMWARE", self.connection_handler.update_firmwares),
            ("REBOOT", self.connection_handler.reboot),
        ]

    def get_advanced_actions(self):
        """Returns a list of advanced actions."""
        return [
            ("SHOW RUNNING", self.connection_handler.show_run),
            ("SHOW CANDIDATE", self.show_template),
        ] + self.get_actions()

    def show_template(self):
        """Displays the current configuration template."""
        logger.debug("Showing configuration template...")
        text = self.app.text_configuration
        if self.app and get_env("ADVANCED_MODE") == "true":
            self.display_feedback(text)
        else:
            logger.error("Application instance not available.")
