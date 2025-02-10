import argparse
import logging
import os
import tkinter as tk
import uuid

from config import config
from utils import set_env
from gui.base_app import App
from gui.tabs.configurator import ControlTab, TemplateTab, HelloTab, RouterTab

logger = logging.getLogger("gui")


class ConfiguratorApp(App):
    def __init__(self, root, title, advanced, *args, **kwargs):
        self.config_params = {
            "CERT": config["default-cert"],
            "OR": None,  # only for tsh, or, raisa_or
        }
        self.device = None
        self.preset = None
        self.config_template = None
        self.config_filename = None
        self.advanced_mode = advanced
        super().__init__(root, title)

    def register_device(self, device):
        self.device = device
        self.preset = None

        if device.dev_type == "router":
            set_env("DEV_TYPE", "router")
            logger.info("setting router environmental variables to default:")
            for env_param, env_value in config["router"].items():
                set_env(env_param, env_value)
        elif device.dev_type == "switch":
            set_env("DEV_TYPE", "switch")

        logger.info("Device selected. device=%s", device.name)

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

    def register_preset(self, preset):
        self.preset = preset
        logger.info(
            "ConfiguratorApp.preset := (%s; %s)", self.device.name, self.preset.role
        )
        self.config_template = self.db_services["preset"].get_info(preset, check=True)[
            "configuration"
        ]
        self.config_filename = f"config_{uuid.uuid4()}.conf"  # TODO: TO ENV var
        logger.info("Create file for switch configuration: %s", self.config_filename)

    def refresh_tabs(self):
        logger.debug(
            "Refreshing configurator tabs (mode %s): ",
            os.environ["MODE"] if "MODE" in os.environ else "None",
        )
        if "MODE" not in os.environ:
            self.__refresh_tabs_none()
        elif os.environ["MODE"] in ("ssh", "com+ssh"):
            self.__refresh_tabs()
        else:
            logger.critical(
                "Refreshing configurator tabs: unknown mode: %s", os.environ["MODE"]
            )
        logger.debug("Configurator tabs refreshed successfully")

    def __refresh_tabs_none(self):
        for _, tab in self.tabs.items():
            if isinstance(tab, HelloTab):
                tab.show()
            else:
                tab.hide()
        self.notebook.select(self.tabs["HOME"].frame)

    def __refresh_tabs(self):
        for _, tab in self.tabs.items():
            if isinstance(tab, HelloTab):
                pass
            elif isinstance(tab, TemplateTab):
                if (
                    os.environ["DEV_TYPE"] == "switch"
                    and self.advanced_mode
                    and self.preset is not None
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

    @property
    def driver(self):
        return {
            "auth_strict_key": False,  # important for unknown hosts
            "device": self.db_services["device"].get_info(self.device),
            "host": os.environ["HOST_ADDRESS"],
            "port": os.environ["HOST_PORT"],
            "auth_username": os.environ["HOST_USERNAME"],
            "auth_password": os.environ["HOST_PASSWORD"],
        }

    @property
    def text_configuration(self):
        if os.environ["DEV_TYPE"] == "switch":
            return self.__switch_config()
        elif os.environ["DEV_TYPE"] == "router":
            return self.__router_config()

    def __router_config(self):  # TODO: РЕАЛИЗОВАТЬ ЭТО С ПОМОЩЬЮ БАШ-СКРИПТОВ
        raise NotImplementedError("__router_config not implemented")

    def __switch_config(self):
        template = ""
        for k, v in self.config_template.items():
            if v["text"]:
                template += v["text"].replace("{INTERFACE_ID}", k) + "\n"
        template = template.replace("{CERT}", self.config_params["CERT"])
        template = template.replace("{OR}", self.config_params["OR"])
        template = template.replace("{MODEL}", self.device.name)
        template = template.replace("{ROLE}", self.preset.role)
        return template + "end\n"


if __name__ == "__main__":
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
