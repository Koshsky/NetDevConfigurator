import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from database.models.base import Base
from database.services.company_service import CompanyService

class ConnectionTab:
    def __init__(self, parent, on_success_callback, on_failure_callback, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.on_success_callback = on_success_callback
        self.on_failure_callback = on_failure_callback

        self.fields = {  # Default values
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
            self.entries[label_text] = entry  # Store entry by label text

        button = tk.Button(self.frame, text="Connect", command=self.on_button_click)
        button.pack(pady=10)

        self.message_label = tk.Label(self.frame, text="", wraplength=400)
        self.message_label.pack(pady=5)

    def on_button_click(self):
        db_params = {key: entry.get() for key, entry in self.entries.items()}
        print("Entered data:", db_params)

        try:
            connection = psycopg2.connect(
                host=db_params["host"],
                port=db_params["port"],
                database=db_params["database"],
                user=db_params["username"],
                password=db_params["password"]
            )
            print("Successful connection to the database")

            # Create SQLAlchemy engine and session
            DATABASE_URL = f'postgresql://{db_params["username"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}'
            engine = create_engine(DATABASE_URL)
            Base.metadata.create_all(engine)
            Session = scoped_session(sessionmaker(bind=engine))
            session = Session()

            # Initialize services
            self.app.company_service = CompanyService(session)

            self.app.connection = connection
            self.on_success_callback()
            self.message_label.config(text="Connection successful.", fg="green")

        except Exception as error:
            print("Error connecting to database:", error)
            self.on_failure_callback()
            self.message_label.config(text='Error: ' + str(error), fg="red")