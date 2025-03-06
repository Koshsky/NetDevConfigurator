import tkinter as tk

from gui.base_app import App
from gui.tabs.manager import (
    AddTab,
    PresetTab,
    DeleteTab,
    InfoTab,
    UpdateTab,
    TemplateTab,
)


class DBManagerApp(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabs["CONNECTION"].on_button_click()

    def create_tabs(self):
        super().create_tabs()
        self.create_tab(AddTab, "ADD")
        self.create_tab(DeleteTab, "DELETE")
        self.create_tab(InfoTab, "INFO")
        self.create_tab(UpdateTab, "DEVICE")
        self.create_tab(TemplateTab, "TEMPLATE")
        self.create_tab(PresetTab, "PRESET")


if __name__ == "__main__":
    root = tk.Tk()
    app = DBManagerApp(root, "Database Manager")
    root.mainloop()
