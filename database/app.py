import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import logging

from .connection_tab import ConnectionTab
from .data_tab import DataTab
from .add_tab import AddTab
from .delete_tab import DeleteTab

from .services.company_service import CompanyService
from .services.device_firmwares_service import DeviceFirmwareService
from .services.device_service import DeviceService
from .services.firmware_service import FirmwareService

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.ERROR)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class DatabaseApp:
    def __init__(self, root):
        self.init_root(root)
        self.company_service = None
        self.firmware_service = None
        self.device_service = None
        self.device_firmware_service = None
        self.session = None
        self.Session = None
        self.create_tabs()

    def init_root(self, root):
        self.root = root
        self.root.title("Database Manager")
        self.root.geometry("500x600")

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.connection_tab = ConnectionTab(self.notebook, self.on_success_callback, self.on_failure_callback, self)
        self.notebook.add(self.connection_tab.frame, text="Connection")

        self.data_tab = DataTab(self.notebook, self)
        self.notebook.add(self.data_tab.frame, text="Tables")

        self.info_tab = DataTab(self.notebook, self)
        self.notebook.add(self.info_tab.frame, text="Device info")

        self.add_tab = AddTab(self.notebook, self)
        self.notebook.add(self.add_tab.frame, text="Add")

        self.update_tab = DataTab(self.notebook, self)
        self.notebook.add(self.update_tab.frame, text="Update")

        self.delete_tab = DeleteTab(self.notebook, self)
        self.notebook.add(self.delete_tab.frame, text="Delete")

        self.hide_all_tabs()

    def display_all_tabs(self):
        self.notebook.select(self.data_tab.frame)
        self.notebook.select(self.info_tab.frame)
        self.notebook.select(self.add_tab.frame)
        self.notebook.select(self.update_tab.frame)
        self.notebook.select(self.delete_tab.frame)
        self.notebook.select(self.connection_tab.frame)  # чтобы не изменять активную вкладку

    def hide_all_tabs(self):
        self.notebook.hide(self.data_tab.frame)
        self.notebook.hide(self.info_tab.frame)
        self.notebook.hide(self.add_tab.frame)
        self.notebook.hide(self.update_tab.frame)
        self.notebook.hide(self.delete_tab.frame)

    def on_success_callback(self, engine):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        # update services
        self.company_service = CompanyService(self.session)
        self.firmware_service = FirmwareService(self.session)
        self.device_service = DeviceService(self.session)
        self.device_firmware_service = DeviceFirmwareService(self.session)
        print("session: ", self.session)
        self.display_all_tabs()

    def on_failure_callback(self, error):
        self.hide_all_tabs()
        self.session = None
        print("session: ", self.session)
        logging.error(f"Connection failed: {error}")  # Логирование ошибки


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()