import tkinter as tk

from gui.base_app import DatabaseApp
from gui.tabs.configurator import HelloTab, TemplateTab, ViewTab
import uuid

from modules.ssh import SSHDriver
from scrapli.exceptions import ScrapliConnectionNotOpened


class ConfiguratorApp(DatabaseApp):
    def __init__(self, *args, **kwargs):
        self.params = {"CERT": None, "OR": None, "MODEL": None, "ROLE": None}
        self.ssh = None
        self.device = None
        self.preset = None
        self.device_configuration = None
        self.config_filename = None
        super().__init__(*args, **kwargs)

    def create_config_tabs(self):
        templates, interfaces = {}, {}
        for k, v in app.device_configuration.items():
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

    def update_driver(self, ip, port, username, password):
        # TODO: close?
        driver = {
            "auth_strict_key": False,  # important for unknown hosts
            "family": self.params["FAMILY"],
            "host": ip,  # TODO: port?????
            "auth_username": username,
            "auth_password": password,
        }
        self.ssh2 = SSHDriver(**driver)
        try:
            self.ssh2.open()
        except ScrapliConnectionNotOpened as e:
            self.ssh2 = None
            print(f"{e.__name_}_: {e}")

    def register_settings(
        self, cert, OR, device, preset
    ):  # TODO: подумать и переименовать
        if not (cert and OR and device and preset):
            raise ValueError("All parameters must be set")
        if preset.device_id != device.id:
            raise ValueError("preset.device_id != device.id")
        self.params["CERT"] = cert
        self.params["OR"] = OR
        self.params["MODEL"] = device.name
        self.params["ROLE"] = preset.role
        self.params["FAMILY"] = (
            self.db_services["family"].get_by_id(device.family_id).name
        )
        self.device = device
        self.preset = preset
        self.device_configuration = self.db_services["preset"].get_info(
            preset, check=True
        )["configuration"]
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
