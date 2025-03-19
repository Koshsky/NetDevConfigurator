import argparse
import logging
import os
import tkinter as tk
from typing import TYPE_CHECKING, Dict

from config import config
from gui.base_app import App
from gui.tabs.configurator import (
    ControlTab,
    HelloTab,
    InterfacesTab,
    RouterTab,
    TemplateTab,
)
from gui.tabs.configurator.connection_handler import CONNECTION_TYPES
from utils.config import save_configuration
from utils.environ import set_env, initialize_device_environment


if TYPE_CHECKING:
    from database.models import Device, Preset
    from gui.tabs import BaseTab

logger = logging.getLogger("ConfiguratorApp")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Network Device Configurator")
    parser.add_argument("--mock", action="store_true", help="Enable mock mode")
    parser.add_argument(
        "-A", "--advanced", action="store_true", help="Advanced mode for fine-tuning"
    )
    return parser.parse_args()


class TabRefresher:
    """Refreshes the visibility of tabs based on the application state."""

    def __init__(self, app: "App") -> None:
        self.app = app
        self.notebook = app.notebook
        self.tabs: Dict[str, BaseTab] = app.tabs
        self.advanced_mode = app.advanced_mode
        self.logger = logging.getLogger("TabRefresher")

    def refresh_tabs(self) -> None:
        """Refreshes the tabs based on the current environment."""
        connection_type = os.environ.get("CONNECTION_TYPE")
        self.logger.debug(
            f"Refreshing configurator tabs. CONNECTION_TYPE={connection_type}"
        )

        if connection_type is None:
            self._show_only_tab("HOME")
        elif connection_type in CONNECTION_TYPES:
            self._refresh_connected_tabs()
        else:
            self.logger.error(f"Unknown CONNECTION_TYPE: {connection_type}")
            self._show_only_tab("HOME")

    def _show_only_tab(self, tab_name: str) -> None:
        """Shows only the specified tab and hides all others."""
        for name, tab in self.tabs.items():
            if name == tab_name:
                tab.show()
            else:
                tab.hide()
        self.notebook.select(self.tabs[tab_name].frame)

    def _refresh_connected_tabs(self) -> None:
        """Refreshes tabs when a connection type is selected."""
        dev_type = os.environ.get("DEV_TYPE")
        dev_role_present = "DEV_ROLE" in os.environ
        self.logger.debug(
            f"Refreshing tabs for connection. DEV_TYPE={dev_type}, DEV_ROLE present={dev_role_present}"
        )

        for name, tab in self.tabs.items():
            if name in ("TEMPLATES", "INTERFACES"):
                tab.show_if(
                    dev_type == "switch" and self.advanced_mode and dev_role_present
                )
            elif name == "ROUTER":
                tab.show_if(dev_type == "router" and self.advanced_mode)
            elif name == "CONTROL":
                tab.show()
            elif name not in (
                "HOME",
                "CONNECTION",
            ):  # these tabs are always hidden at this point
                self.logger.warning(f"Unexpected tab: {name}")

        self.notebook.select(self.tabs["CONTROL"].frame)


class ConfiguratorApp(App):
    """Main application class for the network device configurator."""

    def __init__(
        self,
        master: tk.Tk,
        title: str,
        mock_enabled: bool = False,
        advanced: bool = False,
        *args,
        **kwargs,
    ) -> None:
        """Initialize the application.

        Args:
            master: The root Tkinter window.
            title: The title of the application window.
            mock_enabled: Whether mock mode is enabled.
            advanced: Whether advanced mode is enabled.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.mock_enabled = mock_enabled
        self.advanced_mode = advanced
        self.preset = None
        super().__init__(master, title, *args, **kwargs)
        self.logger = logging.getLogger("ConfiguratorApp")
        self.device: "Device" | None = None  # type hint added
        self.refresher = TabRefresher(self)
        self.tabs["CONNECTION"].on_button_click()

    def refresh_tabs(self) -> None:
        """Refreshes the tab visibility."""
        self.refresher.refresh_tabs()

    @property
    def driver(self) -> dict:
        """Returns the driver configuration."""

        return {
            "auth_strict_key": False,
            "address": os.environ.get("HOST_ADDRESS"),
            "port": os.environ.get("HOST_PORT"),
            "username": os.environ.get("HOST_USERNAME"),
            "password": os.environ.get("HOST_PASSWORD"),
        }

    @property
    def text_configuration(self) -> str:
        """Returns the generated text configuration."""
        self._prepare_configuration()
        return self._read_configuration_file()

    def _prepare_configuration(self) -> None:
        """Prepares the configuration by updating tabs and saving."""
        control_tab = self.tabs["CONTROL"]
        control_tab.connection_handler.update_host_info()
        control_tab.device_handler.update_device_info()

        if self.advanced_mode:
            dev_type = os.environ.get("DEV_TYPE")
            if dev_type == "router":
                self.tabs["ROUTER"].update_config()
            elif dev_type == "switch":
                self.tabs["TEMPLATES"].update_config()
                self.tabs["INTERFACES"].update_config()
            else:
                raise ValueError(
                    f"Invalid or unset DEV_TYPE environment variable: {dev_type}"
                )

        header = control_tab.connection_handler.get_header()
        save_configuration(header, self.preset)

    def _read_configuration_file(self) -> str:
        """Reads and returns the generated text configuration."""
        config_filepath = os.path.join(
            os.environ["TFTP_FOLDER"], "tmp", os.environ["CFG_FILENAME"]
        )
        try:
            with open(config_filepath, "r") as f:
                return f.read()
        except FileNotFoundError as e:
            self.logger.error("Configuration file not found: %s", config_filepath)
            raise FileNotFoundError(
                f"Configuration file not found: {config_filepath}"
            ) from e

    def create_tabs(self) -> None:
        """Create and add tabs to the application."""
        super().create_tabs()
        self.create_tab(HelloTab, "HOME", mock_enabled=self.mock_enabled)
        self.create_tab(
            TemplateTab,
            "TEMPLATES",
            width=config.app.templates_width,
            allow_none=config.app.templates_allow_none,
        )
        self.create_tab(
            InterfacesTab,
            "INTERFACES",
            width=config.app.interfaces_width,
            allow_none=config.app.interfaces_allow_none,
        )
        self.create_tab(RouterTab, "ROUTER")
        self.create_tab(ControlTab, "CONTROL")

    def register_device(self, device: "Device") -> None:
        """Register a device with the application.

        Args:
            device: The device to register.
        """
        self.device = self.db_services["device"].get_info(device)
        initialize_device_environment(self.db_services, device)

        if self.device["dev_type"] == "switch" and self.device["roles"]:
            self.register_preset(self.device["roles"][0])
        else:
            self.logger.warning("No roles found for device: %s", device.name)

        self.logger.debug("Device registered: %s", device.name)
        self.refresh_tabs()

    def register_preset(self, role: str, or_value: str = "1") -> None:
        """Registers the selected preset and updates the environment."""
        set_env("OR", or_value)
        if "DEV_ROLE" in os.environ and os.environ["DEV_ROLE"] == role:
            return

        device = self.db_services["device"].get_one(name=os.environ["DEV_NAME"])
        if preset := self.db_services["preset"].get_one(device_id=device.id, role=role):
            self.preset = self.db_services["preset"].get_info(preset, check=True)
            set_env("DEV_ROLE", preset.role)
            set_env("OR", or_value)
            self.logger.debug("Preset registered: %s:%s", device.name, preset.role)

            self.refresh_tabs()
        else:
            self.logger.error(
                "Preset not found for device %s and role %s", device.name, role
            )


def main():
    """Main entry point of the application."""
    args = parse_args()

    root = tk.Tk()
    app = ConfiguratorApp(
        root,
        "Network Device Configurator",
        mock_enabled=args.mock,
        advanced=args.advanced,
    )
    root.mainloop()


if __name__ == "__main__":
    set_env("CERT", config.default_cert)
    set_env("OR", "1")
    main()
