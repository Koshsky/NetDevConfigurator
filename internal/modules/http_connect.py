from scrapli.driver import Driver
from scrapli.response import Response

def http_connect():
    conn = Driver(
        host="192.168.1.1",
        auth_username="admin",
        auth_password="1234",
        auth_strict_key=False,
    #    platform="generic"
    )

    conn.open()

    # Аутентификация
    login_response: Response = conn.send_request(
        "/login.php",
        method="post",
        data={
            "username": "admin",
            "password": "1234"
        }
    )

    # Проверка успешности аутентификации
    if "logout.php" in login_response.result:
        print("Успешная аутентификация!")
    else:
        print("Ошибка аутентификации")

    # Дальнейшая навигация по веб-интерфейсу
    network_response: Response = conn.send_request("/network.php")
    print(network_response.result)

    # Применение новых настроек
    update_response: Response = conn.send_request(
        "/network.php",
        method="post",
        data={
            "vlan1_ip": "192.168.2.1",
            "vlan1_mask": "255.255.255.0"
        }
    )
    print(update_response.result)

    conn.close()