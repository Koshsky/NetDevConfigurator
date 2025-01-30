import tkinter as tk

from gui.base_app import App
from gui.tabs.manager import (
    AddTab,
    CommonConfigTab,
    DeleteTab,
    InfoTab,
    UpdateTab,
)


class DBManagerApp(App):
    def create_tabs(self):
        self.create_tab(AddTab, "ADD")
        self.create_tab(DeleteTab, "DELETE")
        self.create_tab(InfoTab, "INFO")
        self.create_tab(UpdateTab, "DEVICE")
        self.create_tab(CommonConfigTab, "PRESET")
        super().create_tabs()


if __name__ == "__main__":
    root = tk.Tk()
    app = DBManagerApp(root, "Database Manager")
    root.mainloop()
