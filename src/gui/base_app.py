from tkinter import ttk

from sqlalchemy.orm import sessionmaker

from .tabs import ConnectionTab
from database.services import setup_database_services, prepare_entity_collections


class DatabaseApp:
    def __init__(self, root, title):
        self._init_root(root, title)
        self.session = None
        self._create_connection_tab()  # self.connection_tab = ...

    def create_tabs(self):
        raise NotImplementedError("databaseApp.create_tabs not implemented")

    def _init_root(self, root, title):
        self.root = root
        self.root.title(title)
        self.notebook = ttk.Notebook(self.root)

        self.notebook.pack(fill="both", expand=True)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height - 40}")

    def _create_connection_tab(self):
        self.connection_tab = ConnectionTab(
            self.notebook, self.on_success_callback, self.on_failure_callback, self
        )
        self.notebook.add(self.connection_tab.frame, text="CONNECTION")
        self.connection_tab.on_button_click()

    def create_tab(self, ClassTab: type, tab_name: str, *args, **kwargs):
        tab = ClassTab(self.notebook, self, *args, **kwargs)
        self.notebook.add(tab.frame, text=tab_name)
        self.tabs.append(tab)

    def refresh_widgets(self):
        for tab in self.tabs:
            tab.refresh_widgets()

    def _hide_connection_tab(self):
        self.notebook.hide(self.connection_tab.frame)

    def on_success_callback(self, engine):
        self.session = sessionmaker(bind=engine)()
        self.db_services = setup_database_services(self.session)
        self.entity_collections = prepare_entity_collections(self.db_services)

        self.tabs = []
        self.create_tabs()  # self.tabs = [...]
        self.refresh_widgets()
        self._hide_connection_tab()
        print("Successful connection to the database")

    def on_failure_callback(self, error):
        self.session = None
        print(f"Connection failed: {error}")
