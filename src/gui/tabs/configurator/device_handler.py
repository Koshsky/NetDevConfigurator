import logging
from typing import Dict, Type

from utils.environ import env_converter, get_env, set_env

from ..base_tab import BaseTab

from locales import get_string

logger = logging.getLogger("gui")


class BaseDeviceHandler:
    """Base class for device handlers."""

    def __init__(self, tab: BaseTab):
        self.tab = tab
        self.app = tab.app
        self.lang = tab.lang
        self.env_vars: Dict[str, str] = {}
        self.fields: Dict[str, str] = {}

    def create_widgets(self):
        """Create widgets for the device handler."""
        raise NotImplementedError


    def actualize_values(self):
        """Actualize values from the device handler."""
        logger.debug("Actualizing device values...")
        for env_var, field in self.env_vars.items():
            field = field
            if field in self.fields and (value := get_env(env_var)):
                self.fields[field].set(env_converter.to_human(env_var, value))

    def update_envs(self):
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

    def __init__(self, tab: BaseTab):
        super().__init__(tab)
        self.env_vars = {
            "DEV_ROLE": get_string(self.app.lang, "SWITCH", "DEV_ROLE"),
            "OR": get_string(self.app.lang, "SWITCH", "OR"),
        }

    def create_widgets(self):
        """Create widgets for the device handler."""
        logger.debug("Creating device widgets for switch...")
        self.tab.create_block(
            get_string(self.lang, "SWITCH", "TITLE"),
            {
                field: self.app.device["roles"]
                for field in self.env_vars.values()
            },
        )
        self.fields = self.tab.fields[get_string(self.app.lang, "SWITCH", "TITLE")]

    def update_envs(self):
        """Updates switch information based on user input."""
        logger.debug("Updating device info for switch...")
        self.app.register_preset(
            self.fields[get_string(self.app.lang, "SWITCH", "DEV_ROLE")].get().strip(),
            self.fields[get_string(self.app.lang, "SWITCH", "OR")].get().strip(),
        )


class RouterHandler(BaseDeviceHandler):
    """Device handler for routers."""

    def __init__(self, tab: BaseTab):
        super().__init__(tab)
        self.env_vars = {
            "TYPE_COMPLEX": get_string(self.app.lang, "ROUTER", "TYPE_COMPLEX"),
        }

    def create_widgets(self):
        """Create widgets for the device handler."""
        logger.debug("Creating device widgets for router...")
        self.tab.create_block(
            get_string(self.lang, "ROUTER", "TITLE"),
            {
                field: tuple(env_converter["TYPE_COMPLEX"],)
                for field in self.env_vars.values()
            },
        )
        self.fields = self.tab.fields[get_string(self.app.lang, "ROUTER", "TITLE")]

    def update_envs(self):
        """Updates router information based on user input."""
        logger.debug("Updating device info for router...")
        set_env(
            "TYPE_COMPLEX",
            env_converter.to_machine(
                "TYPE_COMPLEX",
                self.fields[get_string(self.app.lang, "ROUTER", "TYPE_COMPLEX")].get().strip(),
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
