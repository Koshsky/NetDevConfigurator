import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import Session
from .services.company_service import CompanyService
from .services.device_service import DeviceService
from .services.firmware_service import FirmwareService

class DataTab:
    def __init__(self, parent, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        self.companies_button = tk.Button(self.frame, text="Companies", command=self.load_companies)
        self.companies_button.pack(pady=10)
        
        self.devices_button = tk.Button(self.frame, text="Devices", command=self.load_devices)
        self.devices_button.pack(pady=10)
        
        self.firmwares_button = tk.Button(self.frame, text="Firmwares", command=self.load_firmwares)
        self.firmwares_button.pack(pady=10)

        self.data_text = tk.Text(self.frame, wrap='word', width=80, height=20)
        self.data_text.pack(pady=10)

    def load_companies(self):
        if self.app.session is None:
            self.display_error("Error: No connection to the database.")
            return

        try:
            rows = self.app.company_service.get_all()
            self.display_data(rows)
        except Exception as e:
            self.display_error(f"Error loading data: {e}")

    def load_firmwares(self):
        if self.app.session is None:
            self.display_error("Error: No connection to the database.")
            return

        try:
            rows = self.app.firmware_service.get_all()
            self.display_data(rows)
        except Exception as e:
            self.display_error(f"Error loading data: {e}")

    def load_devices(self):
        if self.app.session is None:
            self.display_error("Error: No connection to the database.")
            return

        try:
            rows = self.app.device_service.get_all()
            self.display_data(rows)
        except Exception as e:
            self.display_error(f"Ошибка при загрузке данных: {e}")

    def display_data(self, rows):
        # Очищаем текстовое поле перед выводом новых данных
        self.data_text.delete(1.0, tk.END)

        if not rows:
            self.data_text.insert(tk.END, "No data found.")
            return

        # Получаем заголовки столбцов
        column_names = [column.name for column in rows[0].__table__.columns]
        self.data_text.insert(tk.END, "\t".join(column_names) + "\n")  # Заголовки

        # Форматируем и выводим данные в человеко-читаемом виде
        for row in rows:
            row_data = [str(getattr(row, column)) for column in column_names]
            self.data_text.insert(tk.END, "\t".join(row_data) + "\n")

    def display_error(self, message):
        self.data_text.delete(1.0, tk.END)
        self.data_text.insert(tk.END, message)