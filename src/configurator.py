import tkinter as tk

from gui.base_app import App
from gui.tabs.configurator import HelloTab, TemplateTab, ViewTab
import uuid

from modules.ssh import SSHDriver
from config import config


class ConfiguratorApp(App):
    def __init__(self, *args, **kwargs):
        self.config_params = {
            "CERT": config["default-cert"],
            "OR": None,
        }
        self.device = None
        self.preset = None
        self.config_template = None
        self.config_filename = None
        self.host_info = config["host"]
        super().__init__(*args, **kwargs)

    def refresh_tabs(self):
        for _, tab in self.tabs.items():
            if isinstance(tab, TemplateTab):
                if self.device is None:
                    self.notebook.hide(tab.frame)
                else:
                    self.notebook.add(tab.frame)
                    tab.refresh_widgets()
            else:
                tab.refresh_widgets()

    def create_tabs(self):
        self.create_tab(HelloTab, "Hello")
        self.create_tab(
            TemplateTab,
            "Templates",
            width=config["app"]["templates"]["width"],
            allow_none=config["app"]["templates"]["allow-none"],
            template_filter=lambda x: x["type"] != "interface",
        )
        self.create_tab(
            TemplateTab,
            "Interfaces",
            width=config["app"]["interfaces"]["width"],
            allow_none=config["app"]["interfaces"]["allow-none"],
            template_filter=lambda x: x["type"] == "interface",
        )
        self.create_tab(ViewTab, "COMMANDS")
        super().create_tabs()

    @property
    def driver(self):
        return {
            "auth_strict_key": False,  # important for unknown hosts
            "device": self.db_services["device"].get_info(self.device),
            "host": self.host_info["address"],
            "auth_username": self.host_info["username"],
            "auth_password": self.host_info["password"],
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
            raise ValueError("All parameters must be set")
        if preset.device_id != device.id:
            raise ValueError("preset.device_id != device.id")
        if cert:
            self.config_params["CERT"] = cert
        self.config_params["OR"] = OR
        self.device = device
        self.preset = preset
        self.config_template = self.db_services["preset"].get_info(preset, check=True)[
            "configuration"
        ]
        self.config_filename = f"config_{uuid.uuid4()}.conf"


if __name__ == "__main__":
    root = tk.Tk()
    app = ConfiguratorApp(root, "Configurator")
    root.mainloop()
