import os
import sys
from typing import TYPE_CHECKING, Dict, Any

from config import config, disable_logging
from database.services import EntityNotFoundError, init_db_connection
from utils.config import save_configuration
from utils.environ import initialize_device_environment, set_env

if TYPE_CHECKING:
    from database.models import Devices

CONNECTION_TYPE = "ssh"


def get_cert() -> str:
    """Get the certificate from user input.

    Prompts the user to enter a certificate, using the default certificate
    from the configuration if no input is provided.
    """
    cert = (
        input(f"Enter certificate [{config['default-cert']}]: ")
        or config["default-cert"]
    )
    set_env("CERT", cert)


def get_device(db_services: Dict[str, Any]) -> "Devices":
    """Get the device from user input.

    Prompts the user to enter a device name and retrieves the device
    from the database. If the device is not found, prompts the user again.
    """
    while True:
        device_name = input("Enter device name: ")
        try:
            device = db_services["device"].get_one(name=device_name)
            initialize_device_environment(db_services, device)
            return device
        except EntityNotFoundError:
            print(f"Device '{device_name}' not found. Please try again.")


def get_switch_role(device_info: Dict[str, Any]) -> str | None:
    """Get the switch role from user input.

    Prompts the user to enter a switch role, validating the input against the
    available roles for the device. If the role is invalid, prompts the user again.
    """
    if device_info["dev_type"] != "switch":
        return None

    while True:
        role = input(f"Enter switch role ({device_info['roles']}): ")
        if role in device_info["roles"]:
            set_env("DEV_ROLE", role)
            return role
        print(f"There is no {role} role for {device_info['name']}. Please try again.")


def get_operating_room(role: str) -> str | None:
    """Get the operating room from user input.

    Prompts the user to enter an operating room, validating the input.
    If the role is not "tsh" or "or", returns None.
    """
    if role not in ["tsh", "or"]:
        return None

    while True:
        OR = input("Enter operating room [1]: ") or "1"
        if OR.isdigit() and int(OR) > 0:
            set_env("OR", OR)
            return OR
        print(f"Invalid {role} operating room number. Please try again.")


def prepare_configuration_file() -> Dict[str, Any]:
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
            conf = save_configuration(
                "header\n", preset
            )  # TODO: ВАЖНО need to retrieve original header.
        else:
            conf = save_configuration(
                "header\n"
            )  # TODO: ВАЖНО need to retrieve original header.
        return conf, device_info
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)


def prepare_credentials(device_info: dict[str, Any]):
    """Prepare and save host credentials.

    Retrieves user input for host credentials, then saves them as environment variables.
    """
    while True:
        driver = {}
        for var_name, default_values in config["host"].items():
            var_value = (
                input(f"Enter {var_name} [{default_values[0]}]: ") or default_values[0]
            )
            driver[var_name] = var_value
        try:
            with ConnectionManager(
                device_info, connection_type=CONNECTION_TYPE, **driver
            ):
                print("Successful connection via ssh!")
                break  # successful connection
        except (TimeoutError, DriverError):
            connection_string = f"{os.environ.get('USER')}:{os.environ.get('PASSWORD')}@{os.environ.get('HOST')}:{os.environ.get('PORT')}"
            print(f"Cannot connection to {connection_string}. Please try again.")
    return driver


def prepare_tftp():
    """Prepare and save the TFTP server address.

    Prompts the user to confirm or change the current TFTP server address,
    and updates the environment variable accordingly.
    """
    current_address = os.environ.get("TFTP_ADDRESS")
    while (
        input(
            f"Current tftp-address is {current_address}. Do you want to change this? y/n "
        ).lower()
        == "y"
    ):
        new_address = input("Enter new tftp-address: ")
        set_env("TFTP_ADDRESS", new_address)
        current_address = new_address  # update current address for next prompt


if __name__ == "__main__":
    with disable_logging():
        from drivers import ConnectionManager, DriverError

        conf, device_info = prepare_configuration_file()
        driver = prepare_credentials(device_info)
        prepare_tftp()

        with ConnectionManager(
            device_info, connection_type=CONNECTION_TYPE, **driver
        ) as conn:
            print(conn.show_run())
            # if input("Load configuration? y/n ").lower() == "y":
            #     conn.update_startup_config()
            # if input("Update firmwares? y/n ").lower() == "y":
            #     conn.update_firmwares()
            # if input("Reload device? y/n ").lower() == "y":
            #     conn.reboot()
