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
from config import config


class DBManagerApp(DatabaseApp):
    def on_success_callback(self, engine):
        super().on_success_callback(engine)
        if self.tabs:
            self.display_all_tabs()
            return
        self.create_tab(TablesTab, "TABLES")
        self.create_tab(InfoTab, "INFO")
        self.create_tab(AddTab, "ADD")
        self.create_tab(UpdateTab, "UPDATE")
        self.create_tab(DeleteTab, "DELETE")
        self.create_tab(DeviceTab, "DEVICE")
        self.create_tab(CommonConfigTab, "CONFIG")
        self.create_tab(CopyConfigTab, "COPY CONFIG")


if __name__ == "__main__":
    root = tk.Tk()
    app = DBManagerApp(root, config["manager"]["title"])
    root.mainloop()
