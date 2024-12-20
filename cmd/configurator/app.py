import tkinter as tk

from internal.db_app.database_app import DatabaseApp
from .tabs import (
    TemplateTab,
    DeviceTab
)

class ConfiguratorApp(DatabaseApp):
    def init_root(self, root):
        self.device = None
        self.ports = None
        self.interface_templates = None
        self.header_templates = None
        self.footer_templates = None
        super().init_root(root)

    def on_success_callback(self, engine):
        super().on_success_callback(engine)
        self.create_tab(DeviceTab, "Device")
        self.notebook.select(self.tabs[0].frame)
        self.create_tab(TemplateTab, "TEMPLATE")


    def _get_port_map(self):
        ports = self.entity_services['device_port'].get_device_ports(self.device.id)
        return {
            f'{idx+1}. {port.Ports.speed}Mbps {port.Ports.material}': self.interface_templates
            for idx, port in enumerate(ports)
        }



if __name__ == "__main__":
    root = tk.Tk()
    app = ConfiguratorApp(root, "Configurator")
    root.mainloop()
