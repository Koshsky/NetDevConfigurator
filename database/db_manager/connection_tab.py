import tkinter as tk
from tkinter import ttk
import psycopg2


class ConnectionTab:
    def __init__(self, parent, on_success_callback, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.on_success_callback = on_success_callback

        self.fields = {
            "host": "localhost",
            "port": "5432",
            "database": "device_registry",
            "username": "postgres",
            "password": "postgres"
        }

        self.entries = []
        self.create_widgets()

    def create_widgets(self):
        for label_text, default_value in self.fields.items():
            label = tk.Label(self.frame, text=label_text)
            label.pack(pady=5)

            entry = tk.Entry(self.frame)
            entry.insert(0, default_value)
            entry.pack(pady=5)
            self.entries.append(entry)

        button = tk.Button(self.frame, text="Connect", command=self.on_button_click)
        button.pack(pady=10)

        self.message_label = tk.Label(self.frame, text="", wraplength=200)
        self.message_label.pack(pady=5)

    def on_button_click(self):
        db_params = [entry.get() for entry in self.entries]
        print("Entered data:", db_params)

        host, port, database_name, user, password = db_params

        try:
            connection = psycopg2.connect(
                host=host,
                port=port,
                database=database_name,
                user=user,
                password=password
            )
            print("Successful connection to the database")

            self.app.connection = connection
            self.on_success_callback()
            self.message_label.config(text="Connection successful.", fg="green")

        except Exception as error:
            print("Error connecting to database:", error)
            self.message_label.config(text='Error: ' + str(error), fg="red")
