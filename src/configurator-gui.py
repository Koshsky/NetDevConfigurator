import argparse
import logging
import os
import tkinter as tk
from typing import TYPE_CHECKING

from config import config
from gui.base_app import App
from gui.tabs.configurator import (
    ControlTab,
    HelloTab,
    InterfacesTab,
    RouterTab,
    TemplateTab,
)
from gui.tabs import ConnectionTab
from gui.tabs.configurator.connection_handler import CONNECTION_TYPES
from utils.config import save_configuration
from utils.environ import get_env, initialize_device_environment, set_env
from locales import get_string
if TYPE_CHECKING:
    from database.models import Device

logger = logging.getLogger("ConfiguratorApp")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Network Device Configurator")
    parser.add_argument("--mock", action="store_true", help="Enable mock mode")
    parser.add_argument(
        "-A", "--advanced", action="store_true", help="Advanced mode for fine-tuning"
    )
    parser.add_argument(
        "-L", "--lang", type=str, default="ru", help="Language for the application"
    )
    return parser.parse_args()


class AppRefresher(App):
    """Refreshes the visibility of tabs based on the application state."""

    def __init__(self, lang: str, mock_enabled: bool, advanced: bool, *args, **kwargs) -> None:
        """Initialize the tab refresher.

        Args:
            app: The parent application instance.
        """
        self.lang = lang
        self.mock_enabled = mock_enabled
        self.advanced = advanced
        set_env("ADVANCED_MODE", "true" if advanced else "false")

        self.hello_name = get_string(self.lang, "TABS", "HOME")
        self.templates_name = get_string(self.lang, "TABS", "TEMPLATES")
        self.interfaces_name = get_string(self.lang, "TABS", "INTERFACES")
        self.router_name = get_string(self.lang, "TABS", "ROUTER")
        self.control_name = get_string(self.lang, "TABS", "CONTROL")
        self.connection_name = get_string(self.lang, "TABS", "CONNECTION")
        super().__init__(*args, **kwargs)
        self.tabs[self.connection_name].on_button_click()


    def create_tabs(self) -> None:
        """Create and add tabs to the application."""
        # Создаем вкладку подключения
        self.create_tab(
            ConnectionTab,
            self.connection_name,
            "normal",
            self.on_connection_submit
        )

        # Создаем остальные вкладки
        self.create_tab(HelloTab, self.hello_name, mock_enabled=self.mock_enabled)
        self.create_tab(
            TemplateTab,
            self.templates_name,
            width=config.app.templates_width,
            allow_none=config.app.templates_allow_none,
        )
        self.create_tab(
            InterfacesTab,
            self.interfaces_name,
            width=config.app.interfaces_width,
            allow_none=config.app.interfaces_allow_none,
        )
        self.create_tab(RouterTab, self.router_name)
        self.create_tab(ControlTab, self.control_name)

    def refresh_tabs(self) -> None:
        """Refreshes the tabs based on the current environment."""
        connection_type = get_env("CONNECTION_TYPE")
        self.logger.debug(
            f"Refreshing configurator tabs. CONNECTION_TYPE={connection_type}"
        )
        if connection_type is None:
            self._show_only_tab(self.hello_name)
        elif connection_type in CONNECTION_TYPES:
            self._refresh_connected_tabs()
        else:
            self.logger.error(f"Unknown CONNECTION_TYPE: {connection_type}")
            self._show_only_tab(self.hello_name)

    def _show_only_tab(self, tab_name: str) -> None:
        """Shows only the specified tab and hides all others."""
        self.logger.debug(f"Showing only tab: {tab_name}")
        for name, tab in self.tabs.items():
            if name == tab_name:
                tab.show()
            else:
                tab.hide()
        self.notebook.select(self.tabs[tab_name].frame)

    def _refresh_connected_tabs(self) -> None:
        """Refreshes tabs when a connection type is selected."""
        dev_type = get_env("DEV_TYPE")
        dev_role_present = get_env("DEV_ROLE")
        self.logger.debug(
            f"Refreshing tabs for connection. DEV_TYPE={dev_type}, DEV_ROLE present={dev_role_present}"
        )

        for name, tab in self.tabs.items():
            if name in (self.templates_name, self.interfaces_name):
                tab.show_if(
                    dev_type == "switch"
                    and get_env("ADVANCED_MODE") == "true"
                    and dev_role_present
                )
            elif name == self.router_name:
                tab.show_if(dev_type == "router" and get_env("ADVANCED_MODE") == "true")
            elif name == self.control_name:
                tab.show()
            elif name not in (
                self.hello_name,
                self.connection_name,
            ):  # these tabs are always hidden at this point
                self.logger.warning(f"Unexpected tab: {name}")

        self.notebook.select(self.tabs[self.control_name].frame)

class ConfiguratorApp(AppRefresher):
    """Main application class for the network device configurator."""

    def __init__(
        self,
        master: tk.Tk,
        title: str,
        mock_enabled: bool = False,
        advanced: bool = False,
        lang: str = "ru",
        *args,
        **kwargs,
    ) -> None:
        """Initialize the application.

        Args:
            master: The root Tkinter window.
            title: The title of the application window.
            mock_enabled: Whether MOCK connection is enabled.
            advanced: Whether advanced mode is enabled.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.preset = None
        self.logger = logging.getLogger("ConfiguratorApp")
        self.device: "Device" | None = None
        super().__init__(lang, mock_enabled, advanced, master, title, *args, **kwargs)

    def update_envs(self):
        if get_env("DEV_TYPE") == "router":
            set_env("CFG_PATH", f"{config.tftp.backup_folder}/{get_env('CERT')}/{get_env('DEV_NAME')}.conf")
        else:
            set_env("CFG_PATH", f"{config.tftp.backup_folder}/{get_env('CERT')}/{get_env('DEV_ROLE')}.conf")

        for tab in self.tabs.values():
            if hasattr(tab, "update_envs"):
                tab.update_envs()

    @property
    def driver(self) -> dict:
        """Returns the driver configuration."""
        return {
            "auth_strict_key": False,
            "address": get_env("HOST_ADDRESS"),
            "port": get_env("HOST_PORT"),
            "username": get_env("HOST_USERNAME"),
            "password": get_env("HOST_PASSWORD"),
        }

    @property
    def text_configuration(self) -> str:
        """Returns the generated text configuration."""
        self.prepare_configuration()
        return self._read_configuration_file()

    def update_config(self):
        dev_type = get_env("DEV_TYPE")
        if dev_type == "router":
            self.tabs[self.router_name].update_config()
        elif dev_type == "switch":
            self.tabs[self.templates_name].update_config()
            self.tabs[self.interfaces_name].update_config()
        else:
            raise ValueError(
                f"Invalid or unset DEV_TYPE environment variable: {dev_type}"
            )

    def prepare_configuration(self) -> None:
        """Prepares the configuration by updating tabs and saving."""
        self.update_envs()

        if get_env("ADVANCED_MODE") == "true":
            self.update_config()

        save_configuration(self.preset)

    def _read_configuration_file(self) -> str:
        """Reads and returns the generated text configuration."""
        config_filepath = os.path.join(
            get_env("TFTP_FOLDER"), get_env("CFG_PATH")
        )
        try:
            with open(config_filepath, "r") as f:
                return f.read()
        except FileNotFoundError as e:
            self.logger.error("Configuration file not found: %s", config_filepath)
            raise FileNotFoundError(
                f"Configuration file not found: {config_filepath}"
            ) from e

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
        if get_env("DEV_ROLE") and get_env("DEV_ROLE") == role:
            return

        device = self.db_services["device"].get_one(name=get_env("DEV_NAME"))
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
    ConfiguratorApp(
        root,
        "Network Device Configurator",
        mock_enabled=args.mock,
        advanced=args.advanced,
        lang=args.lang,
    )
    root.mainloop()


if __name__ == "__main__":
    main()
