import argparse
import logging
import os
import tkinter as tk
import uuid

from config import config
from gui.base_app import App
from gui.tabs.configurator import ControlTab, HelloTab, RouterTab, TemplateTab
from utils.config import save_configuration
from utils.environ import del_env, env_converter, set_env

logger = logging.getLogger("gui")


class ConfiguratorApp(App):
    def __init__(self, root, title, advanced, *args, **kwargs):
        super().__init__(root, title)
        self.advanced_mode = advanced
        self.device = None
        self.preset = None

    @property
    def driver(self):
        return {
            "auth_strict_key": False,  # important for unknown hosts
            "device": self.device,
            "host": os.environ.get("HOST_ADDRESS"),
            "port": os.environ.get("HOST_PORT"),
            "auth_username": os.environ["HOST_USERNAME"],  # required parameter
            "auth_password": os.environ["HOST_PASSWORD"],  # required parameter
        }

    @property
    def text_configuration(self):
        self._prepare_configuration()
        with open(
            f"{os.environ['TFTP_FOLDER']}/tmp/{os.environ['CFG_FILENAME']}", "r"
        ) as f:
            return f.read()

    def _prepare_configuration(self):
        self.tabs["CONTROL"].connection_handler.update_host_info()
        self.tabs["CONTROL"].device_handler.update_device_info()
        if self.advanced_mode:
            if os.environ["DEV_TYPE"] == "router":
                self.tabs["ROUTER"].update_config()
            else:
                self.tabs["TEMPLATES"].update_config()
                self.tabs["INTERFACES"].update_config()
        header = self.tabs["CONTROL"].connection_handler.get_header()
        save_configuration(header, self.preset["configuration"])

    def create_tabs(self):
        super().create_tabs()
        self.create_tab(HelloTab, "HOME")
        self.create_tab(
            TemplateTab,
            "TEMPLATES",
            width=config["app"]["templates"]["width"],
            allow_none=config["app"]["templates"]["allow-none"],
            template_filter=lambda x: x["type"] != "interface",
        )
        self.create_tab(
            TemplateTab,
            "INTERFACES",
            width=config["app"]["interfaces"]["width"],
            allow_none=config["app"]["interfaces"]["allow-none"],
            template_filter=lambda x: x["type"] == "interface",
        )
        self.create_tab(RouterTab, "ROUTER")
        self.create_tab(ControlTab, "CONTROL")

    def register_device(self, device):
        self.device = self.db_services["device"].get_info(device)
        set_env("CFG_FILENAME", f"config_{uuid.uuid4()}.conf")
        del_env("DEV_ROLE")
        set_env("DEV_NAME", device.name)
        set_env("DEV_TYPE", device.dev_type)
        set_env(
            "DEV_COMPANY",
            self.db_services["company"].get_one(id=device.company_id).name,
        )
        if os.environ["DEV_TYPE"] == "router":
            for env_param, env_value in config["router"].items():
                set_env(env_param, env_value)
            set_env("MODEL", env_converter.to_machine("MODEL", device.name))
        else:
            self.register_preset(self.device["roles"][0], 1)
        logger.debug("Device selected. device=%s", os.environ["DEV_NAME"])

        if os.environ["DEV_TYPE"] == "router":
            self.refresh_tabs()

    def register_preset(self, role: str, OR: str):
        set_env("OR", OR)
        if "DEV_ROLE" in os.environ and os.environ["DEV_ROLE"] == role:
            return
        device = self.db_services["device"].get_one(name=os.environ["DEV_NAME"])
        preset = self.db_services["preset"].get_one(
            device_id=device.id,
            role=role,
        )
        self.preset = self.db_services["preset"].get_info(preset, check=True)
        set_env("DEV_ROLE", preset.role)
        set_env("OR", OR)
        logger.debug(
            "Preset selected. preset=(%s:%s)",
            os.environ["DEV_NAME"],
            os.environ["DEV_ROLE"],
        )

        self.refresh_tabs()

    def refresh_tabs(self):
        if "CONNECTION_TYPE" not in os.environ:
            self.__refresh_tabs_none()
        elif os.environ["CONNECTION_TYPE"] in (
            "ssh",
            "com+ssh",
            "mock",
        ):  # TODO ВАЖНО убрать этот кортеж в переменную
            self.__refresh_tabs()
        else:
            logger.critical(
                "Refreshing configurator tabs: unknown CONNECTION_TYPE: %s",
                os.environ["CONNECTION_TYPE"],
            )
        logger.debug("Configurator tabs refreshed successfully")

    def __refresh_tabs_none(self):
        logger.debug("Refreshing configurator tabs (CONNECTION_TYPE None): ")
        for _, tab in self.tabs.items():
            if isinstance(tab, HelloTab):
                tab.show()
            else:
                tab.hide()
        self.notebook.select(self.tabs["HOME"].frame)

    def __refresh_tabs(self):
        logger.debug(
            "Refreshing configurator tabs (CONNECTION_TYPE %s): ",
            os.environ["CONNECTION_TYPE"],
        )
        for _, tab in self.tabs.items():
            if isinstance(tab, HelloTab):
                pass
            elif isinstance(tab, TemplateTab):
                if (
                    os.environ["DEV_TYPE"] == "switch"
                    and self.advanced_mode
                    and "DEV_ROLE" in os.environ
                ):
                    tab.show()
                else:
                    tab.hide()
            elif isinstance(tab, RouterTab):
                if os.environ["DEV_TYPE"] == "router" and self.advanced_mode:
                    tab.show()
                else:
                    tab.hide()
            elif isinstance(tab, ControlTab):
                tab.show()
            else:
                logger.critical(
                    "Unknown type of tab during refreshing ConfiguratorApp: %s",
                    type(tab).__name__,
                )
        self.notebook.select(self.tabs["CONTROL"].frame)


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
