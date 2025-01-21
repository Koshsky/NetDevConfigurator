import ipaddress
import os
from config import config


def find_first_available_ip(network):
    net = ipaddress.IPv4Network(network, strict=False)

    for ip in net.hosts():
        if ip.packed[-1] < 100 or ip.packed[-1] > 200:
            continue

        response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")

        if response != 0:
            return str(ip)


if __name__ == "__main__":
    available_ip = find_first_available_ip(config["host"]["network"])
    print(
        f"Первый свободный IP-адрес в сети {config['host']['network']}: {available_ip}"
    )
    available_ip = find_first_available_ip(config["host"]["network"])
    print(
        f"Первый свободный IP-адрес в сети {config['host']['network']}: {available_ip}"
    )
