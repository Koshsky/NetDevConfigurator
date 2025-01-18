import tkinter as tk

from gui.base_app import DatabaseApp
from gui.tabs.configurator import HelloTab, TemplateTab, ViewTab
import uuid


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
        self.credentials = None
        super().__init__(*args, **kwargs)

    def create_config_tabs(self):
        templates, interfaces = {}, {}
        for k, v in app.config_template.items():
            if v["type"] == "interface":
                interfaces[k] = v
            else:
                templates[k] = v
        self.create_tab(TemplateTab, "Templates", templates, width=6)
        self.create_tab(
            TemplateTab, "Interfaces", interfaces, width=12, allow_none=False
        )
        self.create_tab(ViewTab, "VIEW")

    def on_success_callback(self, engine):
        super().on_success_callback(engine)
        self.create_tab(HelloTab, "Device")
        self.notebook.select(self.tabs[0].frame)

    def update_credentials(self, ip, port, username, password):
        self.credentials = {
            "ip": ip,
            "port": port,
            "username": username,
            "password": password,
        }

    @property
    def text_configuration(self):
        template = "=============HEADER=============\n"  # TODO: get from connection (com/ssh/...)
        for k, v in self.config_template.items():
            if v["text"]:
                template += v["text"].replace("{INTERFACE_ID}", k) + "\n"
        template = template.replace("{CERT}", self.config_params["CERT"])
        template = template.replace("{OR}", self.config_params["OR"])
        template = template.replace("{MODEL}", self.device.name)  # MODEL
        template = template.replace("{ROLE}", self.preset.role)  # ROLE
        return template + "end\n"

    def register_settings(
        self, cert, OR, device, preset
    ):  # TODO: подумать и переименовать
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
