import tkinter as tk
from tkinter import ttk

from connection_tab import ConnectionTab
from data_tab import DataTab
from add_tab import AddTab

class DatabaseApp:
    def __init__(self, root):
        self.init_root(root)
        self.create_tabs()
        self.connection = None

    def init_root(self, root):
        self.root = root
        self.root.title("Database Manager")
        self.root.geometry("800x700")

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # СОЗДАЕМ ВКЛАДКИ
        self.connection_tab = ConnectionTab(self.notebook, self.on_connection_success, self)
        self.notebook.add(self.connection_tab.frame, text="Connection")

        self.data_tab = DataTab(self.notebook, self)
        self.notebook.add(self.data_tab.frame, text="Tables")

        self.info_tab = DataTab(self.notebook, self)
        self.notebook.add(self.info_tab.frame, text="Device info")

        self.add_tub = AddTab(self.notebook, self)
        self.notebook.add(self.add_tub.frame, text="Add")

        self.update_tub = DataTab(self.notebook, self)
        self.notebook.add(self.update_tub.frame, text="Update")

        self.delete_tub = DataTab(self.notebook, self)
        self.notebook.add(self.delete_tub.frame, text="Delete")

        # СКРЫВАЕМ ВКЛАДКИ ДО УСПЕШНОГО ПОДКЛЮЧЕНИЯ
        self.notebook.hide(self.data_tab.frame)
        self.notebook.hide(self.info_tab.frame)
        self.notebook.hide(self.add_tub.frame)
        self.notebook.hide(self.update_tub.frame)
        self.notebook.hide(self.delete_tub.frame)

    def on_connection_success(self):
        # ОТОБРАЖАЕМ ВКЛАДКИ ПРИ УСПЕШНОМ ПОДЛКЮЧЕНИИ
        self.notebook.select(self.data_tab.frame)
        self.notebook.select(self.info_tab.frame)
        self.notebook.select(self.add_tub.frame)
        self.notebook.select(self.update_tub.frame)
        self.notebook.select(self.delete_tub.frame)
        self.notebook.select(self.connection_tab.frame)  # чтобы не изменять активную вкладку

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()