"""Handler for device actions."""

import logging
from typing import Callable, List, Tuple

from utils.environ import get_env

logger = logging.getLogger(__name__)


class ActionHandler:
    """Handler for device actions."""

    def __init__(self, connection_handler, parent):
        """Initialize the action handler.

        Args:
            connection_handler: The connection handler instance.
            parent: The parent widget for creating buttons.
        """
        self.connection_handler = connection_handler
        self.parent = parent
        self.logger = logging.getLogger(__name__)

    def get_actions(self) -> List[Tuple[str, Callable]]:
        """Returns a list of basic actions.

        Returns:
            List of tuples containing action name and callback function.
        """
        return [
            (
                {"ru": "ЗАГРУЗИТЬ КОНФИГУРАЦИЮ", "en": "LOAD CONFIGURATION"},
                self.connection_handler.load_configuration,
            ),
            (
                {"ru": "ОБНАРУЖИТЬ УСТРОЙСТВО", "en": "UPDATE FIRMWARE"},
                self.connection_handler.update_firmware,
            ),
            (
                {"ru": "ПЕРЕЗАГРУЗИТЬ", "en": "REBOOT"},
                self.connection_handler.reboot,
            ),
        ]

    def get_advanced_actions(self) -> List[Tuple[str, Callable]]:
        """Returns a list of advanced actions.

        Returns:
            List of tuples containing action name and callback function.
        """
        return [
            (
                {"ru": "ПОКАЗАТЬ РАБОЧУЮ", "en": "SHOW RUNNING"},
                self.connection_handler.show_run,
            ),
            (
                {"ru": "ПОКАЗАТЬ КАНДИДАТ", "en": "SHOW CANDIDATE"},
                self.parent.show_template,
            ),
        ] + self.get_actions()

    def get_available_actions(self) -> List[Tuple[str, Callable]]:
        """Returns a list of available actions based on the current mode.

        Returns:
            List of tuples containing action name and callback function.
        """
        if get_env("ADVANCED_MODE") == "true":
            self.logger.debug("Advanced mode enabled, returning advanced actions")
            return self.get_advanced_actions()
        else:
            self.logger.debug("Basic mode enabled, returning basic actions")
            return self.get_actions()
