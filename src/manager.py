import tkinter as tk

from gui.base_app import DatabaseApp
from gui.tabs.manager import (
    TablesTab,
    InfoTab,
    AddTab,
    UpdateTab,
    DeleteTab,
    CommonConfigTab,
)


class DBManagerApp(DatabaseApp):
    def create_tabs(self):
        self.create_tab(TablesTab, "TABLES")
        self.create_tab(InfoTab, "INFO")
        self.create_tab(AddTab, "ADD")
        self.create_tab(DeleteTab, "DELETE")
        self.create_tab(UpdateTab, "DEVICE")
        self.create_tab(CommonConfigTab, "CONFIG")
        super().create_tabs()


if __name__ == "__main__":
    root = tk.Tk()
    app = DBManagerApp(root, "Database Manager")
    root.mainloop()
