from config import config
from utils.environ import set_env

from .base_driver import AuthenticationError, ConnectionError, DriverError
from .conn_manager import ConnectionManager

set_env("TFTP_ADDRESS", config.tftp.address)
set_env("TFTP_PORT", config.tftp.port)
set_env("TFTP_FOLDER", config.tftp.folder)

__all__ = [
    "ConnectionManager",
    "DriverError",
    "ConnectionError",
    "AuthenticationError",
]
