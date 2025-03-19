import logging
from typing import Dict, Type

from utils.environ import env_converter, get_env, set_env

from ..base_tab import BaseTab

logger = logging.getLogger("gui")


class BaseDeviceHandler:
    """Base class for device handlers."""

    def __init__(self, tab: BaseTab):
        self.tab = tab
        self.app = tab.app

    def create_widgets(self):
        """Creates the necessary widgets for the device type.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError

    def update_device_info(self):
        """Updates the device information based on user input.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError


class DeviceHandlerFactory:
    """Factory class for creating device handlers based on device type."""

    def __init__(self, tab: BaseTab):
        self.tab = tab
        self.handlers: Dict[str, Type[BaseDeviceHandler]] = {
            "switch": SwitchHandler,
            "router": RouterHandler,
        }

    def create_handler(self) -> BaseDeviceHandler:
        """Creates and returns a device handler based on the environment variable DEV_TYPE.

        Returns:
            BaseDeviceHandler: An instance of a device handler.

        Raises:
            ValueError: If DEV_TYPE is not set or if the device type is unknown.
        """
        device_type = get_env("DEV_TYPE")
        if not device_type:
            raise ValueError("DEV_TYPE environment variable not set.")
        if handler_class := self.handlers.get(device_type):
            return handler_class(self.tab)
        else:
            raise ValueError(f"Unknown device type: {device_type}")


class SwitchHandler(BaseDeviceHandler):
    """Device handler for switches."""

    def create_widgets(self):
        """Creates widgets for switch parameters."""
        self.tab.create_block(
            "params",
            {
                "role": self.app.device["roles"],
                "or": tuple(str(i) for i in range(1, 26)),
            },
        )
        self._actualize_values()

    def _actualize_values(self):
        """Sets initial values for switch parameters from environment variables."""
        logger.debug("Actualizing values for switch...")
        self.tab.fields["params"]["role"].set(get_env("DEV_ROLE") or "")
        self.tab.fields["params"]["or"].set(get_env("OR") or "")

    def update_device_info(self):
        """Updates switch information based on user input."""
        logger.debug("Updating device info for switch...")
        self.app.register_preset(
            self.tab.fields["params"]["role"].get().strip(),
            self.tab.fields["params"]["or"].get().strip(),
        )


class RouterHandler(BaseDeviceHandler):
    """Device handler for routers."""

    def create_widgets(self):
        """Creates widgets for router parameters."""
        logger.debug("Creating widgets for router...")
        self.tab.create_block(
            "params",
            {
                "TYPE_COMPLEX": tuple(env_converter["TYPE_COMPLEX"]),
            },
            ("UPDATE", self.update_device_info),
        )

    def update_device_info(self):
        """Updates router information based on user input."""
        logger.debug("Updating device info for router...")
        set_env(
            "TYPE_COMPLEX",
            env_converter.to_machine(
                "TYPE_COMPLEX",
                self.tab.fields["params"]["TYPE_COMPLEX"].get().strip(),
            ),
        )


def get_device_handler(tab: BaseTab) -> BaseDeviceHandler:
    """Creates and returns a device handler using the DeviceHandlerFactory.

    Args:
        tab: The current tab instance.

    Returns:
        A device handler instance.
    """
    factory = DeviceHandlerFactory(tab)
    return factory.create_handler()
