import tkinter as tk
from tkinter import ttk
import psycopg2

class DataTab:
    def __init__(self, parent, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        self.companies_button = tk.Button(self.frame, text="companies", command=lambda : self.load_data("companies"))
        self.companies_button.pack(pady=10)
        self.devices_button = tk.Button(self.frame, text="devices", command=lambda : self.load_data("devices"))
        self.devices_button.pack(pady=10)
        self.firmwares_button = tk.Button(self.frame, text="firmwares", command=lambda : self.load_data("firmwares"))
        self.firmwares_button.pack(pady=10)

        self.data_text = tk.Text(self.frame, wrap='word', width=80, height=20)
        self.data_text.pack(pady=10)

    def load_data(self, table_name):
        if self.app.connection is None:
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, "Ошибка: Нет соединения с базой данных.")
            return

        try:
            cursor = self.app.connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()

            # Получаем заголовки столбцов
            column_names = [desc[0] for desc in cursor.description]

            # Очищаем текстовое поле перед выводом новых данных
            self.data_text.delete(1.0, tk.END)

            # Выводим заголовки столбцов
            self.data_text.insert(tk.END, "\t".join(column_names) + "\n")  # Используем табуляцию для разделения заголовков

            # Выводим данные в текстовое поле
            for row in rows:
                self.data_text.insert(tk.END, str(row) + "\n")

            cursor.close()

        except Exception as e:
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, f"Ошибка при загрузке данных: {e}")
