import tkinter as tk

from internal.db_app.database_app import DatabaseApp
from .tabs import (
    TemplateTab,
    DeviceTab
)

class ConfiguratorApp(DatabaseApp):        
    def init_root(self, root):
        self.device = None
        super().init_root(root)
              
    def on_success_callback(self, engine):
        super().on_success_callback(engine)
        self.create_tab(DeviceTab, "Device")
        self.notebook.select(self.tabs[0].frame)
        self.create_tab(TemplateTab, "TEMPLATE")
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfiguratorApp(root, "Configurator")
    root.mainloop()
