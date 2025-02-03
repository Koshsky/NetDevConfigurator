from drivers import SSHDriver
from config import config


device = {
    "id": 27,
    "name": "mes2428",
    "dev_type": "switch",
    "family": {"name": "MES14xx/24xx/34xx/37xx", "id": 9},
    "company": {"name": "Eltex", "id": 41},
    "pattern": {
        "boot": "mes2400-????-???.boot",
        "uboot": "",
        "firmware": "mes2400-????-???.iss",
    },
    "protocols": [
        {"id": 2, "name": "COM"},
        {"id": 4, "name": "SNMP"},
        {"id": 5, "name": "ssh"},
    ],
    "ports": [
        {
            "interface": "gigabitethernet 0/1",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/2",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/3",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/4",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/5",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/6",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/7",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/8",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/9",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/10",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/11",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/12",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/13",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/14",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/15",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/16",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/17",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/18",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/19",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/20",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/21",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/22",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/23",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/24",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/25",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/26",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/27",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
        {
            "interface": "gigabitethernet 0/28",
            "name": "1000Mbps copper",
            "material": "copper",
            "speed": 1000,
        },
    ],
}
with SSHDriver(
    device,
    host=config["host"]["address"],
    auth_username=config["host"]["username"],
    auth_password=config["host"]["password"],
) as conn:
    conn.update_uboot()
    conn.update_boot()
    conn.update_firmware()
