import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

class ConnectionTab:
    def __init__(self, parent, on_success_callback, on_failure_callback, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.on_success_callback = on_success_callback
        self.on_failure_callback = on_failure_callback

        self.fields = {  # значения по умолчанию
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

        connection_string = f"postgresql://{db_params['username']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"

        try:
            # Создание движка и попытка подключения
            engine = create_engine(connection_string)
            connection = engine.connect()  # Проверка подключения
            connection.close()  # Закрытие подключения, если оно успешно

            print("Successful connection to the database")
            self.app.session = connection  # Устанавливаем сессию в приложении
            self.on_success_callback(connection_string)  # Вызываем коллбек успеха
            self.message_label.config(text="Connection successful.", fg="green")

        except BaseException as error:
            print("Error connecting to database:", error)
            self.on_failure_callback(error)  # Передаем ошибку в коллбек неудачи
            self.message_label.config(text='Error: ' + str(error), fg="red")