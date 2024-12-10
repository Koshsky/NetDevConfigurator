import tkinter as tk
from tkinter import ttk

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from internal.db_app.database_app import DatabaseApp
from .tabs import (
        ConnectionTab,
        TablesTab,
        UpdateTab,
        AddTab,
        DeleteTab,
        
        DeviceInfoTab,
        CompanyInfoTab,
        FirmwareInfoTab
)
from internal.database.services import (
        CompanyService, 
        DeviceService, 
        FirmwareService,
        ProtocolService,
        DeviceFirmwareService, 
        DeviceProtocolService
)

class DBManagerApp(DatabaseApp):        
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
