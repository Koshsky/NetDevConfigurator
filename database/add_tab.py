import tkinter as tk
from tkinter import ttk
import os

from database.services.firmware_service import FirmwareService

firmware_folder = "../../firmwares/"

class AddTab:
    def __init__(self, parent, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.create_widgets()
        self.frame.pack(padx=10, pady=10)

    def create_widgets(self):
        # COMPANY BLOCK
        cur_row = 0
        self.entity_1 = ttk.Label(self.frame, text="company:")
        self.entity_1.grid(row=cur_row, column=0, padx=5, pady=5)

        self.param_1_1 = ttk.Label(self.frame, text="name:")
        self.param_1_1.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_1_1 = ttk.Entry(self.frame)
        self.field_1_1.grid(row=cur_row, column=2, padx=5, pady=5)

        self.button_1 = tk.Button(self.frame, text="SUBMIT", command=self.submit_company)
        self.button_1.grid(row=cur_row, column=3, padx=5, pady=5)
        
        cur_row += 1

        # FIRMWARE BLOCK
        self.entity_2 = ttk.Label(self.frame, text="firmware:")
        self.entity_2.grid(row=cur_row, column=0, padx=5, pady=5)

        self.param_2_1 = ttk.Label(self.frame, text="name:")
        self.param_2_1.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_2_1 = ttk.Entry(self.frame)
        self.field_2_1.grid(row=cur_row, column=2, padx=5, pady=5)

        self.button_2_1 = tk.Button(self.frame, text="SUBMIT", command=self.submit_firmware)
        self.button_2_1.grid(row=cur_row, column=3, padx=5, pady=5)

        cur_row += 1

        self.param_2_2 = ttk.Label(self.frame, text="folder:")
        self.param_2_2.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_2_2 = ttk.Entry(self.frame)
        self.field_2_2.grid(row=cur_row, column=2, padx=5, pady=5)

        self.button_2_2 = tk.Button(self.frame, text="SEARCH", command=self.submit_firmwares_from_folder)
        self.button_2_2.grid(row=cur_row, column=3, padx=5, pady=5)

        cur_row += 1

        # DEVICE BLOCK
        self.entity_3 = ttk.Label(self.frame, text="device:")
        self.entity_3.grid(row=cur_row, column=0, padx=5, pady=5)

        self.param_3_1 = ttk.Label(self.frame, text="name:")
        self.param_3_1.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_3_1 = ttk.Entry(self.frame)
        self.field_3_1.grid(row=cur_row, column=2, padx=5, pady=5)

        cur_row += 1

        self.param_3_2 = ttk.Label(self.frame, text="company:")  # TODO: изменить на выпадающий список
        self.param_3_2.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_3_2 = ttk.Entry(self.frame)
        self.field_3_2.grid(row=cur_row, column=2, padx=5, pady=5)

        cur_row += 1

        self.param_3_3 = ttk.Label(self.frame, text="dev_type:")  # TODO: изменить на выпадающий список
        self.param_3_3.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_3_3 = ttk.Entry(self.frame)
        self.field_3_3.grid(row=cur_row, column=2, padx=5, pady=5)

        cur_row += 1

        self.param_3_4 = ttk.Label(self.frame, text="prim_conf:")  # TODO: изменить на выпадающий список
        self.param_3_4.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_3_4 = ttk.Entry(self.frame)
        self.field_3_4.grid(row=cur_row, column=2, padx=5, pady=5)
        
        cur_row += 1

        self.param_3_5 = ttk.Label(self.frame, text="port_num:")
        self.param_3_5.grid(row=cur_row, column=1, padx=5, pady=5)
        self.field_3_5 = ttk.Entry(self.frame)
        self.field_3_5.grid(row=cur_row, column=2, padx=5, pady=5)

        self.button_3 = tk.Button(self.frame, text="SUBMIT", command=lambda: self.on_button_click("SUBMIT 3"))
        self.button_3.grid(row=cur_row, column=3, padx=5, pady=5)

        cur_row += 1
        
        # Текстовое поле для обратной связи
        self.feedback_text = tk.Text(self.frame, wrap='word', width=50, height=10)
        self.feedback_text.grid(row=cur_row, column=0, columnspan=4 , padx=5, pady=5)
        self.feedback_text.insert(tk.END, "Feedback will be here...\n")
        self.feedback_text.config(state=tk.DISABLED)

    def display_feedback(self, message):
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, message)
        self.feedback_text.config(state=tk.DISABLED)
        print(message)

    def on_button_click(self, button_name):
        print(f"{button_name} clicked")

    def submit_firmwares_from_folder(self):
        folder_name = self.field_2_2.get().strip()  # Получаем имя папки и убираем лишние пробелы

        if not folder_name:
            self.display_feedback("Error: Folder name cannot be empty.")
            return

        # Проверка на существование папки
        if not os.path.isdir(folder_name):
            self.display_feedback(f"Error: Folder '{folder_name}' does not exist.")
            return

        try:
            cursor = self.app.connection.cursor()

            # Перебор всех файлов в папке
            for filename in os.listdir(folder_name):
                firmware_name = filename.strip()  # Убираем лишние пробелы

                if not firmware_name:
                    continue  # Пропускаем пустые имена файлов

                # Проверка на наличие firmware_name в таблице
                cursor.execute("SELECT COUNT(*) FROM firmwares WHERE name = %s", (firmware_name,))
                count = cursor.fetchone()[0]

                if count > 0:
                    self.display_feedback(f"Firmware '{firmware_name}' already exists in the table. Skipping.")
                    continue  # Пропускаем, если прошивка уже существует

                # Вставка нового firmware_name в таблицу
                cursor.execute("INSERT INTO firmwares (name) VALUES (%s)", (firmware_name,))
                self.app.connection.commit()

            self.display_feedback("Successfully added new firmwares from the folder.")
        except Exception as e:
            self.display_feedback(f"Error adding firmwares from folder: {e}")
        finally:
            cursor.close()

    def submit_company(self):
        company_name = self.field_1_1.get().strip()  # Получаем имя и убираем лишние пробелы

        if not company_name:
            self.display_feedback("Error: Company name cannot be empty.")
            return

        try:
            cursor = self.app.connection.cursor()

            # Проверка на наличие company_name в таблице
            cursor.execute("SELECT COUNT(*) FROM companies WHERE name = %s", (company_name,))
            count = cursor.fetchone()[0]

            if count > 0:
                self.display_feedback(f"Error: company '{company_name}' already exists in the table.")
                return

            # Вставка нового company_name в таблицу
            cursor.execute("INSERT INTO companies (name) VALUES (%s)", (company_name,))
            self.app.connection.commit()
            self.display_feedback("Successfully added to the companies table.")
        except Exception as e:
            self.display_feedback(f"Error adding to companies table: {e}")
        finally:
            cursor.close()

    def submit_firmware(self):
        firmware_name = self.field_2_1.get().strip()  # Получаем имя и убираем лишние пробелы

        if not firmware_name:
            self.display_feedback("Error: Firmware name cannot be empty.")
            return

        firmware_path = os.path.join(firmware_folder, firmware_name)
        if not os.path.isfile(firmware_path):
            self.display_feedback(f"Error: file '{firmware_name}' not found in firmwares folder.")
            return

        try:
            # Проверка на наличие firmware_name в таблице
            existing_firmware = self.firmware_service.get_all_firmwares()
            if any(f.version == firmware_name for f in existing_firmware):
                self.display_feedback(f"Error: firmware '{firmware_name}' already exists in the table.")
                return

            # Вставка нового firmware_name в таблицу
            new_firmware = self.firmware_service.create_firmware(version=firmware_name)
            self.display_feedback("Successfully added to the firmwares table.")
        except Exception as e:
            self.display_feedback(f"Error when adding firmware to the table: {e}")



# Пример использования
if __name__ == "__main__":
    root = tk.Tk()
    app = None  # Замените на ваш объект приложения, если необходимо
    data_tab = AddTab(root, app)
    root.mainloop()