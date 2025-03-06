import logging
import tkinter as tk

from config import config
from gui.decorators import apply_error_handler

from .base_tab import BaseTab

logger = logging.getLogger("gui")


@apply_error_handler
class ConnectionTab(BaseTab):
    def __init__(
        self,
        parent,
        app,
        on_click_callback,
        log_name="ConnectionTab",
    ):
        super().__init__(parent, app, log_name)
        self.on_click_callback = on_click_callback

        self.entries = {}
        self.refresh_widgets()

    def _create_widgets(self):
        for label_text, default_value in config["database"].items():
            label = tk.Label(self.frame, text=label_text)
            label.pack(pady=5)

            entry = tk.Entry(self.frame, show="*" if label_text == "password" else "")
            entry.insert(0, default_value)
            entry.pack(pady=5)
            self.entries[label_text] = entry

        button = tk.Button(self.frame, text="Connect", command=self.on_button_click)
        button.pack(pady=10)

        self.message_label = tk.Label(self.frame, text="", wraplength=400)
        self.message_label.pack(pady=5)

    def on_button_click(self):
        try:
            db_params = {key: entry.get() for key, entry in self.entries.items()}
            self.on_click_callback(db_params)

        except Exception as error:
            self.message_label.config(text=f"Error: {str(error)}", fg="red")
