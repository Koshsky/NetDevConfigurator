import argparse
import logging
import os
import tkinter as tk
import uuid

from config import config
from drivers.ssh import SSHDriver
from gui.base_app import App
from gui.tabs.configurator import HelloTab, TemplateTab

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

    def refresh_tabs(self):
        logger.debug("Refreshing configurator tabs:")
        for tab_name, tab in self.tabs.items():
            if isinstance(tab, TemplateTab) and (
                self.device is None or not self.advanced_mode
            ):
                self.notebook.hide(tab.frame)
                logger.debug(f"{tab_name} tab is hidden")
            else:
                tab.refresh_widgets()
        logger.debug("Configurator tabs refreshed")

    def create_tabs(self):
        super().create_tabs()
        self.create_tab(HelloTab, "MAIN")
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

    @property
    def driver(self):
        return {
            "auth_strict_key": False,  # important for unknown hosts
            "device": self.db_services["device"].get_info(self.device),
            "host": os.environ["HOST_ADDRESS"],
            "auth_username": os.environ["HOST_USERNAME"],
            "auth_password": os.environ["HOST_PASSWORD"],
        }

    @property
    def text_configuration(self):
        with SSHDriver(**self.driver) as conn:
            template = conn.get_header()
        for k, v in self.config_template.items():
            if v["text"]:
                template += v["text"].replace("{INTERFACE_ID}", k) + "\n"
        template = template.replace("{CERT}", self.config_params["CERT"])
        template = template.replace("{OR}", self.config_params["OR"])
        template = template.replace("{MODEL}", self.device.name)
        template = template.replace("{ROLE}", self.preset.role)
        return template + "end\n"

    def set_configuration_parameters(self, cert, OR, device, preset):
        if not (cert and OR and device and preset):
            logger.error(
                "All parameters (CERT, OR, device name, preset name) must be set in MAIN tab"
            )
            raise ValueError("All parameters must be set")
        if preset.device_id != device.id:  # unreachable code
            logger.critical(f"Preset is not suitable for device {device.name}")
            raise ValueError("preset.device_id != device.id")
        self.config_params["CERT"] = cert
        self.config_params["OR"] = OR
        self.device = device
        self.preset = preset
        self.config_template = self.db_services["preset"].get_info(preset, check=True)[
            "configuration"
        ]
        self.config_filename = f"config_{uuid.uuid4()}.conf"


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
