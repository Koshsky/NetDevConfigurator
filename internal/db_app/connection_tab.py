import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine

class ConnectionTab:
    def __init__(self, parent, on_success_callback, on_failure_callback, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.on_success_callback = on_success_callback
        self.on_failure_callback = on_failure_callback

        self.fields = {
            "host": "localhost",
            "port": "5432",
            "database": "device_registry",
            "username": "postgres",
            "password": "postgres"
        }

        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
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
            connect = engine.connect()  # Checking the connection
            connect.close()

            self.on_success_callback(engine)
            self.message_label.config(text="Connection successful.", fg="green")
        except Exception as error:
            self.on_failure_callback(error)
            self.message_label.config(text=f'Error: {str(error)}', fg="red")
