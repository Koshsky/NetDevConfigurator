import tkinter as tk

from internal.db_app.database_app import DatabaseApp
from .tabs import (
    TemplateTab
)

class ConfiguratorApp(DatabaseApp):        
    def init_root(self, root):
        super().init_root(root)
        self.root.title("Configurator")
        self.root.geometry("1200x900")
              
    def create_tabs(self):
        super().create_tabs()
        self.create_tab(TemplateTab, "TEMPLATE")
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfiguratorApp(root)
    root.mainloop()
