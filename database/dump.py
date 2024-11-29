import subprocess
import os

db_params = ['localhost', 'device_registry', 5432, 'postgres', 'postgres']

def backup_postgres_db(db_params, dest_file):
    """Создание дампа базы данных с помощью pg_dump."""
    host, database_name, port, user, password = db_params
    
    command = [
        'pg_dump',
        '-h', host,
        '-p', str(port),
        '-U', user,
        '-F', 'c',  # Формат дампа: custom
        '-f', dest_file,
        database_name
    ]

    # Установка переменной окружения для пароля
    env = {'PGPASSWORD': password}

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        output, error = process.communicate()

        if process.returncode != 0:
            print(f'Ошибка при создании дампа: {error.decode()}')
        else:
            print(f'Успешно создан дамп базы данных {database_name} в {dest_file}')

    except Exception as e:
        print(f'Произошла ошибка: {e}')


def restore_postgres_db(db_params, dump_file):
    """Восстановление базы данных с помощью pg_restore."""
    host, database_name, port, user, password = db_params

    # Проверка существования файла дампа
    if not os.path.isfile(dump_file):
        print(f'Ошибка: Файл дампа {dump_file} не существует.')
        return

    # Удаление существующей базы данных
    drop_command = [
        'psql',
        '-h', host,
        '-p', str(port),
        '-U', user,
        '-c', f'DROP DATABASE IF EXISTS {database_name};'
    ]

    create_command = [
        'psql',
        '-h', host,
        '-p', str(port),
        '-U', user,
        '-c', f'CREATE DATABASE {database_name};'
    ]

    # Установка переменной окружения для пароля
    env = {'PGPASSWORD': password}

    try:
        # Удаление базы данных
        drop_process = subprocess.Popen(drop_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        drop_output, drop_error = drop_process.communicate()

        if drop_process.returncode != 0:
            print(f'Ошибка при удалении базы данных: {drop_error.decode()}')
            return
        
        print(f'База данных {database_name} успешно удалена.')

        # Создание новой базы данных
        create_process = subprocess.Popen(create_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        create_output, create_error = create_process.communicate()

        if create_process.returncode != 0:
            print(f'Ошибка при создании базы данных: {create_error.decode()}')
            return
        
        print(f'База данных {database_name} успешно создана.')

        # Восстановление базы данных из дампа
        restore_command = [
            'pg_restore',
            '-h', host,
            '-p', str(port),
            '-U', user,
            '-d', database_name,
            dump_file
        ]

        restore_process = subprocess.Popen(restore_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        restore_output, restore_error = restore_process.communicate()

        if restore_process.returncode != 0:
            print(f'Ошибка при восстановлении базы данных: {restore_error.decode()}')
        else:
            print(f'Успешно восстановлена база данных {database_name} из {dump_file}')

    except Exception as e:
        print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    print("restore/backup? r/b ")
    ans = input()
    if ans == 'r':
        restore_postgres_db(db_params, f'{db_params[1]}.sql')
    elif ans == 'b':
        backup_postgres_db(db_params, f'{db_params[1]}.sql')
    else:
        print("Invalid input")  # Если пользователь ввел что-то не то, вывести
