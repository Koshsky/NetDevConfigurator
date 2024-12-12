import tkinter as tk

from internal.db_app.database_app import DatabaseApp
from .tabs import (
        TablesTab,
        UpdateTab,
        AddTab,
        DeleteTab,
        InfoTab,
        DeviceTab
)

class DBManagerApp(DatabaseApp):
    def init_root(self, root):
        super().init_root(root)
        self.root.title("Database Manager")
        self.root.geometry("850x650")
        
    def on_success_callback(self, engine):
        super().on_success_callback(engine)
        if self.tabs:
            return
        self.create_tab(TablesTab, "TABLES")
        self.create_tab(InfoTab, "INFO")
        self.create_tab(AddTab, "ADD")
        self.create_tab(UpdateTab, "UPDATE")
        self.create_tab(DeleteTab, "DELETE")
        self.create_tab(DeviceTab, "DEVICE")

if __name__ == "__main__":
    root = tk.Tk()
    app = DBManagerApp(root)
    root.mainloop()
