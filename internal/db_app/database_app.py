from tkinter import ttk

from sqlalchemy.orm import sessionmaker

from .connection_tab import ConnectionTab
from internal.database.services import (
        CompanyService, 
        DeviceService, 
        FirmwareService,
        ProtocolService,
        DeviceFirmwareService, 
        DeviceProtocolService,
        FamilyService
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
        self.family_service = None
        
        self.session = None  # TODO: почему я сделал две переменные для сессии... действительно нужно ДВЕ или нет?
        self.Session = None
        
        self.create_tabs()

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

        self.init_db_services()
        self.get_tuples_of_entities()
        
        print("session: ", self.session)

    def init_db_services(self):
        self.company_service = CompanyService(self.session)
        self.firmware_service = FirmwareService(self.session)
        self.device_service = DeviceService(self.session)
        self.device_firmware_service = DeviceFirmwareService(self.session)
        self.protocol_service = ProtocolService(self.session)
        self.device_protocol_service = DeviceProtocolService(self.session)
        self.family_service = FamilyService(self.session)
        
    def get_tuples_of_entities(self):
        self.companies = tuple(company.name for company in self.company_service.get_all())
        self.protocols = tuple(protocol.name for protocol in self.protocol_service.get_all())
        self.families = tuple(family.name for family in self.family_service.get_all())

    def on_failure_callback(self, error):
        self.hide_all_tabs()
        self.session = None
        print(f"Connection failed: {error}")