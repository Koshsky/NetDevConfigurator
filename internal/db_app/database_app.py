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
        DevicePortService,
        FamilyService,
        PortService,
        TemplatePieceService
)

class DatabaseApp:
    def __init__(self, root, title):
        self.init_root(root)
        self.tabs = []
        
        self.session = None  # TODO: почему я сделал две переменные для сессии... действительно нужно ДВЕ или нет?
        self.Session = None
        self.create_connection_tab()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height-40}")
        self.root.title(title)


    def init_root(self, root):
        self.root = root
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
    def create_connection_tab(self):
        self.connection_tab = ConnectionTab(self.notebook, self.on_success_callback, self.on_failure_callback, self)
        self.notebook.add(self.connection_tab.frame, text="CONNECTION")
        
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
        self.init_db_services()
        self.get_tuples_of_entities()
        print("session: ", self.session)

    def init_db_services(self):
        self.entity_services = {
            'company': CompanyService(self.session),
            'family': FamilyService(self.session),
            'device': DeviceService(self.session),
            'firmware': FirmwareService(self.session),
            'protocol': ProtocolService(self.session),
            'port': PortService(self.session),
            'device_firmware': DeviceFirmwareService(self.session),
            'device_protocol': DeviceProtocolService(self.session),
            'device_port': DevicePortService(self.session),
            'template_piece': TemplatePieceService(self.session),
        }
        
    def get_tuples_of_entities(self):
        self.companies = tuple(company.name for company in self.entity_services["company"].get_all())
        self.families = tuple(family.name for family in self.entity_services["family"].get_all())
        self.devices = tuple(device.name for device in self.entity_services["device"].get_all())
        self.protocols = tuple(protocol.name for protocol in self.entity_services["protocol"].get_all())
        self.ports = (None, ) + tuple(port.name for port in self.entity_services["port"].get_all())

    def on_failure_callback(self, error):
        self.hide_all_tabs()
        self.session = None
        print(f"Connection failed: {error}")