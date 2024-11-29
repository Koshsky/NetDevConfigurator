import tkinter as tk
from tkinter import ttk
import psycopg2
from psycopg2 import sql

class DatabaseApp:
    def __init__(self, root):
        self.init_root()
        self.create_tabs()
        self.connection = None

    def init_root(self):
        self.root = root
        self.root.title("Admin Panel for Database")
        self.root.geometry("800x700")

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # СОЗДАЕМ ВКЛАДКИ
        self.connection_tab = ConnectionTab(self.notebook, self.on_connection_success, self)
        self.notebook.add(self.connection_tab.frame, text="Подключение")

        self.data_tab = DataTab(self.notebook, self)
        self.notebook.add(self.data_tab.frame, text="Данные")
        # ....
        # СКРЫВАЕМ ВКЛАДКИ ДО УСПЕШНОГО ПОДКЛЮЧЕНИЯ
        self.notebook.hide(self.data_tab.frame)
        # ....

    def on_connection_success(self):
        # ОТОБРАЖАЕМ ВКЛАДКИ ПРИ УСПЕШНОМ ПОДЛКЮЧЕНИИ
        self.notebook.select(self.data_tab.frame)
        # ....


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

        button = tk.Button(self.frame, text="Подключиться", command=self.on_button_click)
        button.pack(pady=10)

        self.message_label = tk.Label(self.frame, text="", wraplength=200)
        self.message_label.pack(pady=5)

    def on_button_click(self):
        db_params = [entry.get() for entry in self.entries]
        print("Введенные данные:", db_params)

        host, port, database_name, user, password = db_params

        try:
            connection = psycopg2.connect(
                host=host,
                port=port,
                database=database_name,
                user=user,
                password=password
            )
            print("Успешное подключение к базе данных")

            self.app.connection = connection
            # Вызываем колбек при успешном подключении
            self.on_success_callback()
            self.message_label.config(text="Подключение успешно.", fg="green")

        except Exception as error:
            print("Ошибка при подключении к базе данных:", error)
            self.message_label.config(text='Ошибка: ' + str(error), fg="red")

class DataTab:
    def __init__(self, parent, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # Кнопка для загрузки данных
        self.load_button = tk.Button(self.frame, text="Загрузить данные из companies", command=self.load_data)
        self.load_button.pack(pady=10)

        # Текстовое поле для отображения данных
        self.data_text = tk.Text(self.frame, wrap='word', height=20, width=50)
        self.data_text.pack(pady=10)

    def load_data(self):
        if self.app.connection is None:
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, "Ошибка: Нет соединения с базой данных.")
            return

        try:
            cursor = self.app.connection.cursor()
            cursor.execute("SELECT * FROM companies;")
            rows = cursor.fetchall()

            # Очищаем текстовое поле перед выводом новых данных
            self.data_text.delete(1.0, tk.END)

            # Выводим данные в текстовое поле
            for row in rows:
                self.data_text.insert(tk.END, str(row) + "\n")

            cursor.close()

        except Exception as error:
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, 'Ошибка: ' + str(error))

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()