import tkinter as tk

from gui.base_app import DatabaseApp
from gui.tabs.manager import (
    TablesTab,
    InfoTab,
    AddTab,
    UpdateTab,
    DeleteTab,
    DeviceTab,
    CommonConfigTab,
    CopyConfigTab,
)


class DBManagerApp(DatabaseApp):
    def create_tabs(self):
        self.create_tab(TablesTab, "TABLES")
        self.create_tab(InfoTab, "INFO")
        self.create_tab(AddTab, "ADD")
        self.create_tab(DeleteTab, "DELETE")
        self.create_tab(UpdateTab, "FIRMWARE")
        self.create_tab(DeviceTab, "PORTS")
        self.create_tab(CommonConfigTab, "CONFIG")
        self.create_tab(CopyConfigTab, "COPY CONFIG")


if __name__ == "__main__":
    root = tk.Tk()
    app = DBManagerApp(root, "Database Manager")
    root.mainloop()
