import tkinter as tk
from tkinter import ttk

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .connection_tab import ConnectionTab
from internal.database.services import (
        CompanyService, 
        DeviceService, 
        FirmwareService,
        ProtocolService,
        DeviceFirmwareService, 
        DeviceProtocolService
)

class DatabaseApp:
    def __init__(self, root):
        self.init_root(root)
        self.tabs = []
        
        self.company_service = None   # TODO: может быть это не ЛУЧШЕЕ РЕШЕНИЕ?? выглядит как говно-перечисление
        self.firmware_service = None
        self.device_service = None
        self.device_firmware_service = None
        self.protocol_service = None
        self.device_protocol_service = None
        
        self.session = None  # TODO: почему я сделал две переменные для сессии... действительно нужно ДВЕ или нет?
        self.Session = None
        
        self.create_tabs()
        self.hide_all_tabs()

    def init_root(self, root):
        self.root = root
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
    def create_tabs(self):
        self.connection_tab = ConnectionTab(self.notebook, self.on_success_callback, self.on_failure_callback, self)
        self.notebook.add(self.connection_tab.frame, text="Connection")
        
    def create_tab(self, ClassTab: type, tab_name: str):
        tab = ClassTab(self.notebook, self)
        self.notebook.add(tab.frame, text=tab_name)
        self.tabs.append(tab)

    def display_all_tabs(self):
        for tab in self.tabs:
            self.notebook.select(tab.frame)
        self.notebook.select(self.connection_tab.frame)  # чтобы не изменять активную вкладку

    def hide_all_tabs(self):
        for tab in self.tabs:
            self.notebook.hide(tab.frame)

    def on_success_callback(self, engine):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        # update services
        self.company_service = CompanyService(self.session)
        self.firmware_service = FirmwareService(self.session)
        self.device_service = DeviceService(self.session)
        self.device_firmware_service = DeviceFirmwareService(self.session)
        self.protocol_service = ProtocolService(self.session)
        self.device_protocol_service = DeviceProtocolService(self.session)
        
        print("session: ", self.session)
        self.display_all_tabs()

    def on_failure_callback(self, error):
        self.hide_all_tabs()
        self.session = None
        print("session: ", self.session)
        logging.error(f"Connection failed: {error}")  # Логирование ошибки