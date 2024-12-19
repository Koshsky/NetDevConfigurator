from tkinter import ttk

from sqlalchemy.orm import sessionmaker

from .connection_tab import ConnectionTab
from internal.database.services import *

class DatabaseApp:
    def __init__(self, root, title):
        self.init_root(root)
        self.tabs = []

        self.session = None  # TODO: почему я сделал две переменные для сессии... действительно нужно ДВЕ или нет?
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
        self.session = sessionmaker(bind=engine)()
        self.entity_services = setup_database_services(self.session)
        self.entity_collections = prepare_entity_collections(self.entity_services)
        print("Successful connection to the database")

    def on_failure_callback(self, error):
        self.hide_all_tabs()
        self.session = None
        print(f"Connection failed: {error}")