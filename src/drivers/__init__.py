from config import config
from utils.environ import set_env

from .conn_manager import ConnectionManager
from .base_driver import DriverError, ConnectionError, AuthenticationError

set_env("TFTP_ADDRESS", config["tftp-server"]["address"])
set_env("TFTP_PORT", config["tftp-server"]["port"])
set_env("TFTP_FOLDER", config["tftp-server"]["folder"])

__all__ = [
    "ConnectionManager",
    "DriverError",
    "ConnectionError",
    "AuthenticationError",
]
