import tkinter as tk
import psycopg2

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel for Database")
        self.root.geometry("450x700")

        # Словарь для хранения меток и значений по умолчанию
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
        # Создаем метки и поля ввода
        for label_text, default_value in self.fields.items():
            label = tk.Label(self.root, text=label_text)
            label.pack(pady=5)

            entry = tk.Entry(self.root)
            entry.insert(0, default_value)
            entry.pack(pady=5)
            self.entries.append(entry)

        # Создаем кнопку
        button = tk.Button(self.root, text="Отправить", command=self.on_button_click)
        button.pack(pady=10)

        # Создаем метку для отображения сообщений
        self.message_label = tk.Label(self.root, text="", wraplength=200)
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

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM companies;")
            rows = cursor.fetchall()

            print("Данные из таблицы companies:")
            for row in rows:
                print(row)

            self.message_label.config(text="Данные успешно получены.", fg="green")

        except Exception as error:
            print("Ошибка при подключении к базе данных:", error)
            self.message_label.config(text='Ошибка: ' + str(error), fg="red")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                print("Соединение с базой данных закрыто")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()