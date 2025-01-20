import ipaddress
import os
import subprocess

mgmt_network = "10.4.0.0/24"  # TODO: вынести в config.yaml


def find_first_available_ip(network):  # TODO: IMPORTANT URGENT: TEST THIS
    net = ipaddress.IPv4Network(network, strict=False)

    for ip in net.hosts():
        # if ip.packed[-1] < 10 or ip.packed[-1] > 254:
        #     continue  # Пропускаем адреса, которые не входят в диапазон 10-254

        response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")

        if response != 0:
            return str(ip)


def set_ip_address(interface, ip_address):
    try:
        subprocess.run(
            ["sudo", "ip", "addr", "add", f"{ip_address}/16", "dev", interface],
            check=True,
        )
        print(f"IP-адрес {ip_address} успешно установлен на интерфейсе {interface}.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке IP-адреса: {e}")


interface = "enc32421341"  # Имя сетевого интерфейса
ip_address = "10.4.0.10"

set_ip_address(interface, ip_address)
available_ip = find_first_available_ip(mgmt_network)
print(f"Первый свободный IP-адрес в сети {mgmt_network}: {available_ip}")
