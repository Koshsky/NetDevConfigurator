import logging
from tkinter import ttk

from config import DatabaseConfig
from database.services import init_db_connection

from .tabs import ConnectionTab

CONNECTION_TAB_TITLE = "CONNECTION"
logger = logging.getLogger("gui")


class App:
    """Main application class.

    Initializes the main application window, creates tabs, and handles database
    connections.
    """

    def __init__(self, root, title):
        """Initialize the application.

        Args:
            root: The root Tkinter window.
            title: The title of the application window.
        """
        self._init_root(root, title)
        self.tabs = {}
        self.create_tabs()
        self.db_services = None
        self.session = None
        self._setup_keyboard_shortcuts()

    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for tab navigation."""
        self.root.bind("<Control-Tab>", self._next_tab)
        self.root.bind("<Control-Shift-Tab>", self._prev_tab)
        # Для Linux/Windows добавим альтернативные комбинации
        self.root.bind("<Control-Key-Page_Down>", self._next_tab)
        self.root.bind("<Control-Key-Page_Up>", self._prev_tab)

    def _next_tab(self, event):
        """Switch to the next tab."""
        current = self.notebook.index(self.notebook.select())
        tabs = self.notebook.tabs()
        if tabs:  # Если есть вкладки
            next_tab = (current + 1) % len(tabs)  # Циклический переход
            self.notebook.select(next_tab)
        return "break"  # Предотвращаем дальнейшую обработку события

    def _prev_tab(self, event):
        """Switch to the previous tab."""
        current = self.notebook.index(self.notebook.select())
        tabs = self.notebook.tabs()
        if tabs:  # Если есть вкладки
            prev_tab = (current - 1) % len(tabs)  # Циклический переход
            self.notebook.select(prev_tab)
        return "break"  # Предотвращаем дальнейшую обработку события

    def create_tabs(self):
        """Create the tabs for the application."""
        self.create_tab(
            ConnectionTab, CONNECTION_TAB_TITLE, "normal", self.on_connection_submit
        )

    def create_tab(
        self, ClassTab: type, tab_name: str, state: str = "hidden", *args, **kwargs
    ):
        """Create a tab.

        Args:
            ClassTab: The class of the tab to create.
            tab_name: The name of the tab.
            state: The initial state of the tab.
            *args: Additional arguments to pass to the tab's constructor.
            **kwargs: Additional keyword arguments to pass to the tab's constructor.
        """
        tab = ClassTab(self.notebook, self, log_name=tab_name, *args, **kwargs)
        self.notebook.add(tab.frame, text=tab_name, state=state)
        self.tabs[tab_name] = tab
        logger.debug("%s tab created (%s)", tab_name, state)

    def refresh_tabs(self):
        """Refresh the tabs."""
        for _, tab in self.tabs.items():
            tab.show()

        self.notebook.select(0)

    def init_database(self, db_params):
        """Initialize the database connection.

        Args:
            db_params: The database connection parameters.

        Returns:
            True if the connection was successful, False otherwise.
        """

        db_params = DatabaseConfig(**db_params)
        try:
            self.session, self.db_services = init_db_connection(db_params)
            return True
        except Exception as e:
            return self._handle_database_error(e)

    def _handle_database_error(self, e):
        """Handle database errors.

        Args:
            e: The exception raised by the database connection.

        Raises:
            The original exception `e`.
        """
        logger.error("an error occurred: %s", e)
        self.db_services = None
        self.session = None
        raise e

    def on_connection_submit(self, db_params):
        """Handle connection submit.

        Args:
            db_params: The database connection parameters.
        """
        if self.init_database(db_params):
            self.notebook.forget(self.tabs[CONNECTION_TAB_TITLE].frame)
            del self.tabs[CONNECTION_TAB_TITLE]
            logger.debug("%s is forgotten", CONNECTION_TAB_TITLE)

            self.refresh_tabs()

    def _init_root(self, root, title):
        """Initialize the root window.

        Args:
            root: The root Tkinter window.
            title: The title of the application window.
        """
        self.root = root
        self.root.title(title)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Устанавливаем минимальный размер окна и позволяем ему адаптироваться
        self.root.update_idletasks()  # Обновляем, чтобы получить реальные размеры виджетов
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        self.root.geometry(
            ""
        )  # Сбрасываем геометрию, чтобы окно подстроилось под содержимое
