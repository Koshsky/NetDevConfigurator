import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base
from services.company_service import CompanyService
from services.device_service import DeviceService
from services.firmware_service import FirmwareService
from services.device_firmware_service import DeviceFirmwareService
from models.db import create_engine_and_session

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление базой данных")

        # Поля для ввода данных
        tk.Label(root, text="Имя пользователя:").grid(row=0, column=0)
        self.user_entry = tk.Entry(root)
        self.user_entry.grid(row=0, column=1)

        tk.Label(root, text="Пароль:").grid(row=1, column=0)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Label(root, text="Хост:").grid(row=2, column=0)
        self.host_entry = tk.Entry(root)
        self.host_entry.grid(row=2, column=1)

        tk.Label(root, text="Порт:").grid(row=3, column=0)
        self.port_entry = tk.Entry(root)
        self.port_entry.grid(row=3, column=1)

        tk.Label(root, text="Имя базы данных:").grid(row=4, column=0)
        self.database_entry = tk.Entry(root)
        self.database_entry.grid(row=4, column=1)

        # Кнопка для подключения
        self.connect_button = tk.Button(root, text="Подключиться", command=self.connect_to_database)
        self.connect_button.grid(row=5, columnspan=2)

        # Поля для управления компаниями
        tk.Label(root, text="Имя компании:").grid(row=6, column=0)
        self.company_name_entry = tk.Entry(root)
        self.company_name_entry.grid(row=6, column=1)

        self.company_service = None

    def connect_to_database(self):
        user = self.user_entry.get()
        password = self.password_entry.get()
        host = self.host_entry.get() or "localhost"
        port = self.port_entry.get() or "5432"
        database = self.database_entry.get()

        try:
            DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{database}'
            engine = create_engine(DATABASE_URL)
            Base.metadata.create_all(engine)
            Session = scoped_session(sessionmaker(bind=engine))
            session = Session()

            # Инициализация сервисов
            self.company_service = CompanyService(session)

            messagebox.showinfo("Успех", "Подключение к базе данных успешно!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось подключиться к базе данных:\n{e}")

    def add_company(self):
        company_name = self.company_name_entry.get()
        if company_name:
            try:
                self.company_service.create_company(company_name)
                messagebox.showinfo("Успех", "Компания добавлена!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить компанию:\n{e}")
        else:
            messagebox.showwarning("Предупреждение", "Введите имя компании.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()