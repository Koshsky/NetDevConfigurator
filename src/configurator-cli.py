import argparse
import logging
import re
import sys
from typing import Optional, Tuple

from config import config
from database.services import init_db_connection
from utils.config import save_configuration
from utils.environ import initialize_device_environment, set_env

logger = logging.getLogger(__name__)


def parse_role(role_string: str) -> Tuple[str, Optional[str]]:
    """Parses the role string into role and OS version.

    Args:
        role_string: The role string in the format 'role[OR]'.

    Returns:
        A tuple containing the role and the OS version (if present).

    Raises:
        ValueError: If the role string format is invalid.
    """
    if not (match := re.match(r"([a-zA-Z]+)(\d+)?", role_string)):
        raise ValueError(f"Invalid role format: {role_string}")
    set_env("DEV_ROLE", match[1])
    if match[2]:
        set_env("OR", match[2])
    return match[1], match[2]


def main(cert: str, device_name: str, role_string: Optional[str] = None) -> None:
    """
    CLI utility for finding the most recent file.

    Args:
        cert: The certificate type.
        device_name: The device name.
        role_string: The optional role string (e.g., "tsh12").

    Raises:
        ValueError: If the device is a switch and the role is not provided,
            or if the device is not found.
    """
    set_env("CERT", cert)
    set_env("TFTP_FOLDER", config["tftp-server"]["folder"])

    _, db_services = init_db_connection(config["database"])
    device = db_services["device"].get_one(name=device_name)
    initialize_device_environment(db_services, device)

    if device.dev_type == "switch":
        if not role_string:
            logger.error("The --role argument is required for switches.")
            sys.exit(1)
        role, OR = parse_role(role_string) if role_string else (None, None)
        preset = db_services["preset"].get_info_one(device_id=device.id, role=role)
        res = save_configuration("", preset)
        print(res)  # TODO: or print path to file?
    elif device.dev_type == "router":
        res = save_configuration()
        print(res)
    else:
        logger.error()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI utility for finding files.")
    parser.add_argument("--cert", required=True, help="The certificate type.")
    parser.add_argument("--device", required=True, help="The device name.")
    parser.add_argument(
        "--role", help="The role (e.g., 'tsh12'). Required for switches."
    )

    args = parser.parse_args()

    try:
        main(args.cert, args.device, args.role)
    except Exception as e:
        logger.exception("An error occurred: %s", e)
        sys.exit(1)
