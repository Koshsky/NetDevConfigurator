import logging
import tkinter as tk

from gui.base_app import App
from gui.tabs.manager import (
    AddTab,
    DeleteTab,
    InfoTab,
    PresetTab,
    TemplateTab,
    UpdateTab,
)
from locales import get_string
logger = logging.getLogger(__name__)


class DBManagerApp(App):
    """Main application class for the database manager."""

    def __init__(self, master: tk.Tk, title: str, *args, **kwargs) -> None:
        """Initialize the database manager application.

        Args:
            master: The root Tkinter window.
            title: The title of the application window.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        logger.debug("Initializing DBManagerApp")
        super().__init__(master, title, *args, **kwargs)
        self.connection_name = get_string(self.lang, "TABS", "CONNECTION")
        self.tabs[self.connection_name].on_button_click()

    def create_tabs(self) -> None:
        """Create and add tabs to the application."""
        logger.debug("Creating tabs")
        super().create_tabs()
        self.create_tab(AddTab, "ADD")
        self.create_tab(DeleteTab, "DELETE")
        self.create_tab(InfoTab, "INFO")
        self.create_tab(UpdateTab, "DEVICE")
        self.create_tab(TemplateTab, "TEMPLATE")
        self.create_tab(PresetTab, "PRESET")


if __name__ == "__main__":
    root = tk.Tk()
    app = DBManagerApp(root, "Database Manager")
    root.mainloop()
