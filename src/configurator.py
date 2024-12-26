import tkinter as tk

from gui.base_app import DatabaseApp
from gui.tabs.configurator import *
import uuid
import os


class ConfiguratorApp(DatabaseApp):
    def __init__(self, *args, **kwargs):
        self.directory = '/srv/tftp/tmp'
        os.makedirs(self.directory, exist_ok=True)
        self.params = {
            "CERT": None,
            "OR": None,
            "MODEL": None,
            "ROLE": None
        }
        self._device = None
        self._preset = None
        self._config = None
        self._path = None
        super().__init__(*args, **kwargs)

    def on_success_callback(self, engine):
        super().on_success_callback(engine)
        self.create_tab(HelloTab, "Device")
        self.notebook.select(self.tabs[0].frame)

    def register_settings(self, cert, OR, device, preset):
        if not (cert and OR and device and preset):
            raise ValueError("All parameters must be set")
        if preset.device_id != device.id:
            raise ValueError("preset.device_id != device.id")
        self.params["CERT"] = cert
        self.params["OR"] = OR
        self.params["MODEL"] = device.name
        self.params["ROLE"] = preset.role
        self._device = device
        self._preset = preset
        self._config = self.db_services['preset'].get_info(preset)['configuration']
        self._path = self.generate_filename()

    def generate_filename(self):
        filename = f"config_{uuid.uuid4()}.conf"
        return os.path.join(self.directory, filename)

    def update_config_tabs(self):
        self.remove_config_tabs()
        self.create_config_tabs()

    def remove_config_tabs(self):
        while len(self.tabs) > 1:
            self.notebook.forget(2)
            self.tabs.pop()

    def create_config_tabs(self):
        self.templates = {k: v for k, v in app._config.items() if v['type'] != 'interface'}
        self.interfaces = {k: v for k, v in app._config.items() if v['type'] == 'interface'}
        self.create_tab(TemplateTab, "Templates", self.templates, width=6)
        self.create_tab(TemplateTab, "Interfaces", self.interfaces, width=12)
        self.create_tab(ViewTab, "VIEW")


if __name__ == "__main__":
    root = tk.Tk()
    app = ConfiguratorApp(root, "Configurator")
    root.mainloop()
