from tkinter import ttk

from sqlalchemy.orm import sessionmaker

from .tabs import ConnectionTab
from database.services import setup_database_services, prepare_entity_collections


class DatabaseApp:
    def __init__(self, root, title):
        self._init_root(root)

        self.session = None
        self._create_connection_tab()  # self.connection_tab = ...
        self.tabs = []
        self.create_tabs()  # self.tabs = [...]

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height - 40}")
        self.root.title(title)

    def create_tabs(self):
        self._hide_all_tabs()

    def _init_root(self, root):
        self.root = root
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

    def _create_connection_tab(self):
        self.connection_tab = ConnectionTab(
            self.notebook, self.on_success_callback, self.on_failure_callback, self
        )
        self.notebook.add(self.connection_tab.frame, text="CONNECTION")

    def create_tab(self, ClassTab: type, tab_name: str, *args, **kwargs):
        tab = ClassTab(self.notebook, self, *args, **kwargs)
        self.notebook.add(tab.frame, text=tab_name)
        self.tabs.append(tab)

    def _display_all_tabs(self):
        self.refresh_widgets()
        self.notebook.select(self.tabs[0].frame)  # to not change the active tab
        self.notebook.hide(self.connection_tab.frame)

    def refresh_widgets(self):
        for tab in self.tabs:
            tab.refresh_widgets()

    def _hide_all_tabs(self):
        for tab in self.tabs:
            self.notebook.hide(tab.frame)
        self.notebook.select(self.connection_tab.frame)

    def on_success_callback(self, engine):
        self.session = sessionmaker(bind=engine)()
        self.db_services = setup_database_services(self.session)
        self.entity_collections = prepare_entity_collections(self.db_services)
        self._display_all_tabs()
        print("Successful connection to the database")

    def on_failure_callback(self, error):
        self.session = None
        print(f"Connection failed: {error}")
