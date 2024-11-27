from scrapli.driver.core import IOSXEDriver

def ssh_connect():

    device_driver = {
        "host": "192.168.3.201",
        "auth_username": "mvsadmin",
        "auth_password": "MVS_admin20",
        "auth_strict_key": False,
    }

    ssh = IOSXEDriver(**device_driver)
    ssh.open()
    ssh.get_prompt()
    r = ssh.send_command("sh running-config")
    r.result
    ssh.close()

    #with IOSXEDriver(**device_driver) as ssh:
    #    print(ssh.get_prompt())
    #    r = ssh.send_command("sh running-config")
    #    r.result

    # Открываем соединение
    #device.open()

    # Выполняем команду и получаем вывод
    #output = device.send_command("show running-config")
    #print(output.result)

    # Закрываем соединение
    #device.close()


