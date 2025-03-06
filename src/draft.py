import argparse
import logging
import re
import sys
from typing import Optional, Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config
from database.services import setup_database_services
from utils import find_most_recent_file

logger = logging.getLogger(__name__)


def parse_role(role_string: str) -> Tuple[str, Optional[str]]:
    """Parses the role string into role and OS version.

    Args:
        role_string: The role string in the format 'role[OS_version]'.

    Returns:
        A tuple containing the role and the OS version (if present).

    Raises:
        ValueError: If the role string format is invalid.
    """
    if match := re.match(r"([a-zA-Z]+)(\d+)?", role_string):
        return match[1], match[2]
    else:
        raise ValueError(f"Invalid role format: {role_string}")


def init_db_connection(config):
    """Initializes the database connection and services.

    Args:
        config: The configuration dictionary.

    Returns:
        A tuple containing the database session and services.

    Raises:
        SystemExit: If the database connection fails.
    """
    try:
        connection_string = (
            f"postgresql://"
            f"{config['database']['username']}:"
            f"{config['database']['password']}@"
            f"{config['database']['host']}:"
            f"{config['database']['port']}/"
            f"{config['database']['database']}"
        )
        engine = create_engine(connection_string)
        session = sessionmaker(bind=engine)()
        db_services = setup_database_services(session)

        # Проверка подключения
        session.execute("SELECT 1").scalar()
        logger.info("Успешное подключение к базе данных")
        return session, db_services

    except Exception as e:
        logger.error("Ошибка подключения к базе данных: %s", e)
        sys.exit(1)


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

    session, db_services = init_db_connection(config)
    device = db_services["device"].get_one(name=device_name)

    if not device:
        raise ValueError(f"Device '{device_name}' not found.")

    if device.dev_type == "switch" and not role_string:
        raise ValueError("The --role argument is required for switches.")

    role, os_version = parse_role(role_string) if role_string else (None, None)

    logger.info(
        f"Running with cert={cert}, device={device_name}, role={role}, os_version={os_version}"
    )

    # Example usage (replace with your actual logic)
    path = find_most_recent_file("/srv/tftp/firmware", "*")
    print(f"Most recent file: {path}")


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
