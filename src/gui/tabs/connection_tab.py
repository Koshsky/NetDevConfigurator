import logging
import tkinter as tk

from sqlalchemy import create_engine

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
        on_success_callback,
        on_failure_callback,
        log_name="ConnectionTab",
    ):
        super().__init__(parent, app, log_name)
        self.on_success_callback = on_success_callback
        self.on_failure_callback = on_failure_callback

        self.fields = config["database"]

        self.entries = {}
        self.refresh_widgets()

    def render_widgets(self):
        for label_text, default_value in self.fields.items():
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
        db_params = {key: entry.get() for key, entry in self.entries.items()}

        connection_string = (
            f"postgresql://"
            f"{db_params['username']}:"
            f"{db_params['password']}@"
            f"{db_params['host']}:"
            f"{db_params['port']}/"
            f"{db_params['database']}"
        )

        try:
            engine = create_engine(connection_string)
            connect = engine.connect()
            connect.close()
            logger.info("Successful connection to the database %s", connection_string)

            self.on_success_callback(engine)
        except Exception as error:
            logger.error("Connection failed to %s", connection_string)
            self.on_failure_callback(error)
            self.message_label.config(text=f"Error: {str(error)}", fg="red")
