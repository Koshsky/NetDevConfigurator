import tkinter as tk

from gui.base_app import DatabaseApp
from gui.tabs.configurator import HelloTab, TemplateTab, ViewTab
import uuid

from modules.ssh import SSHDriver
from config import config


class ConfiguratorApp(DatabaseApp):
    def __init__(self, *args, **kwargs):
        self.config_params = {
            "CERT": None,
            "OR": None,
        }  # ROLE from preset, MODEL from device
        self.device = None
        self.preset = None
        self.config_template = None
        self.config_filename = None
        self.host_info = {
            "address": config["host"]["address"],
            "port": config["host"]["port"],
            "username": config["host"]["username"],
            "password": config["host"]["password"],
        }
        super().__init__(*args, **kwargs)

    def create_config_tabs(self):
        templates, interfaces = {}, {}
        for k, v in app.config_template.items():
            if v["type"] == "interface":
                interfaces[k] = v
            else:
                templates[k] = v
        self.create_tab(
            TemplateTab,
            "Templates",
            templates,
            width=config["app"]["templates"]["width"],
            allow_none=config["app"]["templates"]["allow-none"],
        )
        self.create_tab(
            TemplateTab,
            "Interfaces",
            interfaces,
            width=config["app"]["interfaces"]["width"],
            allow_none=config["app"]["interfaces"]["allow-none"],
        )
        self.create_tab(ViewTab, "VIEW")

    def on_success_callback(self, engine):
        super().on_success_callback(engine)
        self.create_tab(HelloTab, "Device")
        self.notebook.select(self.tabs[0].frame)

    def update_host_info(self, address, port, username, password):
        self.host_info = {
            "address": address,
            "port": port,
            "username": username,
            "password": password,
        }

    @property
    def driver(self):
        return {
            "auth_strict_key": False,  # important for unknown hosts
            "device": self.db_services["device"].get_info(self.device),
            "host": self.host_info["address"],
            "auth_username": self.host_info["username"],
            "auth_password": self.host_info["password"],
            "ssh_config_file": config["ssh-config-file"],
        }

    @property
    def text_configuration(self):
        with SSHDriver(**self.driver) as conn:
            template = conn.get_header()
        for k, v in self.config_template.items():
            if v["type"] == "header":
                continue  # TODO: убрать временный костыль.
            if v["text"]:
                template += v["text"].replace("{INTERFACE_ID}", k) + "\n"
        template = template.replace("{CERT}", self.config_params["CERT"])
        template = template.replace("{OR}", self.config_params["OR"])
        template = template.replace("{MODEL}", self.device.name)  # MODEL
        template = template.replace("{ROLE}", self.preset.role)  # ROLE
        return template + "end\n"

    def register_parameters(
        self, cert, OR, device, preset
    ):  # TODO: think and rename (NOT IMPORTANT NOT URGENT)
        if not (cert and OR and device and preset):
            raise ValueError("All parameters must be set")
        if preset.device_id != device.id:
            raise ValueError("preset.device_id != device.id")
        self.config_params["CERT"] = cert
        self.config_params["OR"] = OR
        self.device = device
        self.preset = preset
        self.config_template = self.db_services["preset"].get_info(preset, check=True)[
            "configuration"
        ]
        self.config_filename = f"config_{uuid.uuid4()}.conf"

    def update_config_tabs(self):
        self.remove_config_tabs()
        self.create_config_tabs()

    def remove_config_tabs(self):
        while len(self.tabs) > 1:
            self.notebook.forget(2)
            self.tabs.pop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ConfiguratorApp(root, "Configurator")
    root.mainloop()
