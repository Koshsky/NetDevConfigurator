from scrapli.driver.core import IOSXEDriver

def main():
    try:
        with IOSXEDriver(
            host='127.0.0.1',
            auth_username='koshsky',
            auth_password='fdsjkl',
            port=22,
        ) as conn:
            with open('RESPONSE.txt', 'w') as file:
                file.write("абаюнда")
            response = conn.send_command('uname -a')
            # Запись результата в файл RESPONSE.txt
            with open('RESPONSE.txt', 'w') as file:
                file.write(response.result)
    except Exception as e:
        # Обработка исключений, если необходимо
        with open('RESPONSE.txt', 'w') as file:
            file.write(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
