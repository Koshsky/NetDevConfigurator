import logging
from tkinter import ttk

from sqlalchemy.orm import sessionmaker

from config import config
from database.services import prepare_entity_collections, setup_database_services

from .tabs import ConnectionTab

CONNECTION_TAB_TITLE = "CONNECTION"
logger = logging.getLogger("gui")


class App:
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

    def create_tab(
        self, ClassTab: type, tab_name: str, state: str = "hidden", *args, **kwargs
    ):
        tab = ClassTab(self.notebook, self, log_name=tab_name, *args, **kwargs)
        self.notebook.add(tab.frame, text=tab_name, state=state)
        self.tabs[tab_name] = tab
        logger.debug("%s tab created (%s)", tab_name, state)

    def refresh_tabs(self):
        for _, tab in self.tabs.items():
            tab.show()

        self.notebook.select(0)

    def on_success_callback(self, engine):
        self.session = sessionmaker(bind=engine)()
        self.db_services = setup_database_services(self.session)
        self.entity_collections = prepare_entity_collections(self.db_services)

        self.notebook.forget(self.tabs[CONNECTION_TAB_TITLE].frame)
        del self.tabs[CONNECTION_TAB_TITLE]
        logger.debug("%s is forgotten", CONNECTION_TAB_TITLE)

        self.refresh_tabs()

    def on_failure_callback(self, error):
        logger.error("an error occurred: %s", error)
        self.session = None

    def _init_root(self, root, title):
        self.root = root
        self.root.title(title)
        self.notebook = ttk.Notebook(self.root)

        self.notebook.pack(fill="both", expand=True)
        self.root.geometry(config["app"]["geometry"])
