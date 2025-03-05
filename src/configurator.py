import argparse
import logging
import os
import tkinter as tk
import uuid
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
from utils.environ import del_env, env_converter, set_env


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
            if name == "TEMPLATES":
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


if TYPE_CHECKING:
    from database.models import Device, Preset
    from gui.tabs import BaseTab

logger = logging.getLogger("ConfiguratorApp")


class ConfiguratorApp(App):
    """Main application class for the network device configurator."""

    def __init__(
        self, root: tk.Tk, title: str, advanced: bool, *args, **kwargs
    ) -> None:
        super().__init__(root, title)
        self.logger = logging.getLogger("ConfiguratorApp")
        self.advanced_mode: bool = advanced
        self.device: "Device" | None = None  # type hint added
        self.preset: "Preset" | None = None  # type hint added
        self.refresher = TabRefresher(self)
        self.tabs["CONNECTION"].on_button_click()

    def refresh_tabs(self) -> None:
        """Refreshes the tab visibility."""
        self.refresher.refresh_tabs()

    @property
    def driver(self) -> dict:
        """Returns the driver configuration."""
        host_address = os.environ.get("HOST_ADDRESS")
        host_port = os.environ.get("HOST_PORT")
        try:
            host_username = os.environ["HOST_USERNAME"]
            host_password = os.environ["HOST_PASSWORD"]
        except KeyError as e:
            self.logger.error("Missing required environment variable: %s", e)
            raise  # Re-raise the exception after logging

        return {
            "auth_strict_key": False,
            "device": self.device,  # Use self.device directly
            "host": host_address,
            "port": host_port,
            "auth_username": host_username,
            "auth_password": host_password,
        }

    @property
    def text_configuration(self) -> str:
        """Returns the generated text configuration."""
        self._prepare_configuration()
        config_filepath = os.path.join(
            os.environ["TFTP_FOLDER"], "tmp", os.environ["CFG_FILENAME"]
        )
        try:
            with open(config_filepath, "r") as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error("Configuration file not found: %s", config_filepath)
            return ""  # Return empty string if file not found

    def _prepare_configuration(self) -> None:
        """Prepares the configuration by updating tabs and saving."""
        control_tab = self.tabs["CONTROL"]
        control_tab.connection_handler.update_host_info()
        control_tab.device_handler.update_device_info()

        if self.advanced_mode:
            dev_type = os.environ.get("DEV_TYPE")
            if dev_type == "router":
                self.tabs["ROUTER"].update_config()
            else:
                self.tabs["TEMPLATES"].update_config()
                self.tabs["INTERFACES"].update_config()

        header = control_tab.connection_handler.get_header()
        save_configuration(header, self.preset)

    def create_tabs(self) -> None:
        """Creates and adds tabs to the notebook."""
        super().create_tabs()
        self.create_tab(HelloTab, "HOME")
        self.create_tab(TemplateTab, "TEMPLATES", **config["app"]["templates"])
        self.create_tab(InterfacesTab, "INTERFACES", **config["app"]["interfaces"])
        self.create_tab(RouterTab, "ROUTER")
        self.create_tab(ControlTab, "CONTROL")

    def register_device(self, device: "Device") -> None:
        """Registers the selected device and updates the environment."""
        self.device = self.db_services["device"].get_info(device)
        set_env("CFG_FILENAME", f"config_{uuid.uuid4()}.conf")
        del_env("DEV_ROLE")
        set_env("DEV_NAME", device.name)
        set_env("DEV_TYPE", device.dev_type)
        company_name = self.db_services["company"].get_one(id=device.company_id).name
        set_env("DEV_COMPANY", company_name)

        if os.environ["DEV_TYPE"] == "router":
            for env_param, env_value in config["router"].items():
                set_env(env_param, env_value)
            set_env("MODEL", env_converter.to_machine("MODEL", device.name))
        elif (
            self.device and "roles" in self.device and self.device["roles"]
        ):  # Check if roles exist
            self.register_preset(self.device["roles"][0], "1")  # Default OR to "1"
        else:
            self.logger.warning("No roles found for device: %s", device.name)

        self.logger.debug("Device registered: %s", device.name)
        self.refresh_tabs()

    def register_preset(self, role: str, or_value: str) -> None:
        """Registers the selected preset and updates the environment."""
        set_env("OR", or_value)
        if "DEV_ROLE" in os.environ and os.environ["DEV_ROLE"] == role:
            return

        device = self.db_services["device"].get_one(name=os.environ["DEV_NAME"])
        preset = self.db_services["preset"].get_one(device_id=device.id, role=role)
        self.preset = self.db_services["preset"].get_info(preset, check=True)
        set_env("DEV_ROLE", preset.role)
        set_env("OR", or_value)
        self.logger.debug("Preset registered: %s:%s", device.name, preset.role)

        self.refresh_tabs()


if __name__ == "__main__":
    set_env("CERT", config["default-cert"])
    set_env("OR", "1")

    parser = argparse.ArgumentParser(
        description="Upload configurations and manage network devices"
    )
    parser.add_argument(
        "-A", "--advanced", action="store_true", help="Advanced mode for fine-tuning"
    )
    args = parser.parse_args()
    root = tk.Tk()
    app = ConfiguratorApp(root, "Configurator", args.advanced)
    root.mainloop()
