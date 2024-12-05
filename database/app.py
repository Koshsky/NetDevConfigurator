import tkinter as tk
from tkinter import ttk

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import logging

from .tabs import (
        ConnectionTab,
        TablesTab,
        DeviceInfoTab,
        UpdateTab,
        AddTab,
        DeleteTab
)
from .services import (
        CompanyService, 
        DeviceFirmwareService, 
        DeviceService, 
        FirmwareService
)

# TODO: if SSH=1 and COM=1, SSH + COM = 1  # на будущее (другая программа)

# TODO: добавить выпадающие  списки к add_tab

# TODO: ДОБАВИТЬ ВКЛАДКУ ДЛЯ ОТОБРАЖЕНИЯ ИНФОРМАЦИИ О КОМПАНИИ
# TODO: ДОБАВИТЬ ВКЛАДКУ ДЛЯ ОТОБРАЖЕНИЯ ИНФОРМАЦИИ О ПРОШИВКЕ

# TODO: ДОБАВИТЬ СВЯЗКУ УСТРОЙСТВ С ПРОТОКОЛАМИ. КАК ЭТО СДЕЛАТЬ?

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
        self.root.geometry("850x650")

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.connection_tab = ConnectionTab(self.notebook, self.on_success_callback, self.on_failure_callback, self)
        self.notebook.add(self.connection_tab.frame, text="Connection")

        self.data_tab = TablesTab(self.notebook, self)
        self.notebook.add(self.data_tab.frame, text="Tables")

        self.info_tab = DeviceInfoTab(self.notebook, self)
        self.notebook.add(self.info_tab.frame, text="Device info")

        self.add_tab = AddTab(self.notebook, self)
        self.notebook.add(self.add_tab.frame, text="Add")

        self.update_tab = UpdateTab(self.notebook, self)
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