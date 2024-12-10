import tkinter as tk

from internal.db_app.database_app import DatabaseApp
from .tabs import (
        TablesTab,
        UpdateTab,
        AddTab,
        DeleteTab,
        
        DeviceInfoTab,
        CompanyInfoTab,
        FirmwareInfoTab
)

class DBManagerApp(DatabaseApp):
    def init_root(self, root):
        super().init_root(root)
        self.root.title("Database Manager")
        self.root.geometry("850x650")
        
    def create_tabs(self):
        super().create_tabs()
        self.create_tab(TablesTab, "Tables")
        self.create_tab(CompanyInfoTab, "Company_info")
        self.create_tab(DeviceInfoTab, "Device info")   
        self.create_tab(FirmwareInfoTab, "Firmware info")
        self.create_tab(AddTab, "Add")
        self.create_tab(UpdateTab, "Update")
        self.create_tab(DeleteTab, "Delete")

if __name__ == "__main__":
    root = tk.Tk()
    app = DBManagerApp(root)
    root.mainloop()
