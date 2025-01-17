from modules.com import SerialConnection

# Пример использования
if __name__ == "__main__":
    with SerialConnection() as ser:
        # Теперь вы можете использовать ser для отправки и получения данных
        ser.write(b"show bootvar\r\n")
        response = ser.read(10)  # Чтение 10 байт
        print(response)
