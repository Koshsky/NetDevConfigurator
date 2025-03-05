import logging

from gui import BaseTab, apply_error_handler

from .connection_handler import get_connection_handler
from .device_handler import get_device_handler

logger = logging.getLogger("gui")


@apply_error_handler
class ControlTab(BaseTab):
    """Control tab for managing network devices."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_handler = None
        self.device_handler = None
        self.base_loaded = None

    def _create_widgets(self):
        """Creates and arranges widgets within the tab."""
        logger.debug("Creating connection handler...")
        self.connection_handler = get_connection_handler(self)
        logger.debug("Creating device handler...")
        self.device_handler = get_device_handler(self)

        logger.debug("Creating connection handler widgets...")
        self.connection_handler.create_widgets()
        logger.debug("Creating device handler widgets...")
        self.device_handler.create_widgets()
        logger.debug("Creating action buttons...")
        self._create_action_buttons()
        logger.debug("Creating feedback area...")
        self.create_feedback_area()

        logger.debug("Updating host info...")
        self.connection_handler.update_host_info()

    def _create_action_buttons(self):
        """Creates action buttons for device management."""
        actions = [
            ("RUNNING CONFIG", self.connection_handler.show_run),
            ("CANDIDATE CONFIG", self.show_template),
            ("LOAD TEMPLATE", self.connection_handler.update_startup_config),
            ("UPDATE FIRMWARES", self.connection_handler.update_firmwares),
            ("REBOOT DEVICE", self.connection_handler.reboot),
        ]
        for action, callback in actions:
            logger.debug(f"Creating button for action: {action}")
            self.create_button_in_line((action, callback))

    def show_template(self):
        """Displays the current configuration template."""
        logger.debug("Showing configuration template...")
        if self.app:
            self.display_feedback(self.app.text_configuration)
        else:
            logger.error("Application instance not available.")
