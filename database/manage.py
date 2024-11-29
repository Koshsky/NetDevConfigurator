import tkinter as tk
import psycopg2

def on_button_click():
    # Получаем данные из полей ввода и выводим их в консоль
    db_params = [entry.get() for entry in entries]
    print("Введенные данные:", db_params)

    # Распаковываем параметры подключения
    host, port, database_name, user, password = db_params

    try:
        # Устанавливаем соединение с базой данных
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database_name,
            user=user,
            password=password
        )
        print("Успешное подключение к базе данных")

        # Создаем курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Выполняем запрос к таблице devices
        cursor.execute("SELECT * FROM companies;")
        
        # Получаем все строки из результата запроса
        rows = cursor.fetchall()

        # Выводим данные
        print("Данные из таблицы devices:")
        for row in rows:
            print(row)

    except Exception as error:
        print("Ошибка при подключении к базе данных:", error)
        label = tk.Label(root, text='Ошибка при подключении к базе данных: ' + str(error), wraplength=200).pack()

    finally:
        # Закрываем соединение и курсор
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Соединение с базой данных закрыто")

# Создаем главное окно
root = tk.Tk()
root.title("Admin Panel for Database")
root.geometry("450x700")  # Устанавливаем размер окна

# Словарь для хранения меток и значений по умолчанию
fields = {
    "host": "localhost",
    "port": "5432",
    "database": "device_registry",
    "username": "postgres",
    "password": "postgres"
}

# Список для хранения полей ввода
entries = []

# Создаем метки и поля ввода
for label_text, default_value in fields.items():
    label = tk.Label(root, text=label_text)
    label.pack(pady=5)  # Отступ между меткой и полем ввода

    entry = tk.Entry(root)
    entry.insert(0, default_value)  # Устанавливаем значение по умолчанию
    entry.pack(pady=5)  # Добавляем отступ между полями
    entries.append(entry)

# Создаем кнопку
button = tk.Button(root, text="Отправить", command=on_button_click)
button.pack(pady=10)  # Отступ для кнопки

# Запускаем главный цикл приложения
root.mainloop()