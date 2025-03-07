import os
import sys

from config import config, disable_logging
from database.services import init_db_connection, EntityNotFoundError
from utils.config import save_configuration
from utils.environ import initialize_device_environment, set_env


def get_cert():
    cert = (
        input(f"Enter certificate [{config['default-cert']}]: ")
        or config["default-cert"]
    )
    set_env("CERT", cert)


def get_device(db_services):
    while True:
        device_name = input("Enter device name: ")
        try:
            device = db_services["device"].get_one(name=device_name)
            initialize_device_environment(db_services, device)
            return device
        except EntityNotFoundError:
            print(f"Device '{device_name}' not found. Please try again.")


def get_switch_role(device_info):
    if device_info["dev_type"] != "switch":
        return None

    while True:
        role = input(f"Enter switch role ({device_info['roles']}): ")
        if role in device_info["roles"]:
            set_env("DEV_ROLE", role)
            return role
        print(f"There is no {role} role for {device_info['name']}. Please try again.")


def get_operating_room(role):
    if role not in ["tsh", "or"]:
        return None

    while True:
        OR = input("Enter operating room [1]: ") or "1"
        if OR.isdigit() and int(OR) > 0:
            set_env("OR", OR)
            return OR
        print(f"Invalid {role} operating room number. Please try again.")


def prepare_configuration_file():
    """Prepare and save the configuration file.

    Retrieves user input for device, role, and operating room, then saves the
    configuration to a file.
    """
    _, db_services = init_db_connection(config["database"])

    get_cert()
    device = get_device(db_services)
    device_info = db_services["device"].get_info(device)
    role = get_switch_role(device_info)
    get_operating_room(role)

    try:
        if "DEV_ROLE" in os.environ:
            preset = db_services["preset"].get_info_one(device_id=device.id, role=role)
            save_configuration(
                "header\n", preset
            )  # TODO: ВАЖНО need to retrieve original header.
        else:
            save_configuration("header\n")
        print(f"Path to file: {os.environ['CFG_FILENAME']}")
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)


def prepare_credentials():
    """Prepare and save host credentials.

    Retrieves user input for host credentials, then saves them as environment variables.
    """
    while True:
        for var_name, default_values in config["host"].items():
            var_value = (
                input(f"Enter {var_name} [{default_values[0]}]: ") or default_values[0]
            )
            set_env(var_name, var_value)
        if False:  # TODO: test connection.
            connection_string = "aa:bb@cc:dd"
            print(f"Cannot connection to {connection_string}. Please try again.")
        else:
            break


if __name__ == "__main__":
    with disable_logging():
        from drivers import ConnectionManager

        prepare_credentials()
        prepare_configuration_file()
