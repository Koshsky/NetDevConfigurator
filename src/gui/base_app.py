from tkinter import ttk

from sqlalchemy.orm import sessionmaker

from .tabs import ConnectionTab
from database.services import setup_database_services, prepare_entity_collections

CONNECTION_TAB_TITLE = "CONNECTION"


class DatabaseApp:
    def __init__(self, root, title):
        self._init_root(root, title)
        self.session = None
        self.tabs = {}
        self.create_tabs()

    def create_tabs(self):
        self.create_tab(
            ConnectionTab,
            CONNECTION_TAB_TITLE,
            "normal",
            self.on_success_callback,
            self.on_failure_callback,
        )
        self.tabs[CONNECTION_TAB_TITLE].on_button_click()

    def create_tab(
        self, ClassTab: type, tab_name: str, state: str = "hidden", *args, **kwargs
    ):
        tab = ClassTab(self.notebook, self, *args, **kwargs)
        self.notebook.add(tab.frame, text=tab_name, state=state)
        self.tabs[tab_name] = tab

    def refresh_widgets(self):
        for _, tab in self.tabs.items():
            tab.refresh_widgets()

    def on_success_callback(self, engine):
        self.session = sessionmaker(bind=engine)()
        self.db_services = setup_database_services(self.session)
        self.entity_collections = prepare_entity_collections(self.db_services)

        for _, tab in self.tabs.items():
            self.notebook.add(tab.frame)
        self.notebook.hide(self.tabs[CONNECTION_TAB_TITLE].frame)
        self.refresh_widgets()
        print("Successful connection to the database")

    def on_failure_callback(self, error):
        self.session = None
        print(f"Connection failed: {error}")

    def _init_root(self, root, title):
        self.root = root
        self.root.title(title)
        self.notebook = ttk.Notebook(self.root)

        self.notebook.pack(fill="both", expand=True)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height - 40}")
