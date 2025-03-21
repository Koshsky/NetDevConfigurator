from config import config, disable_logging
from utils.environ import set_env

from .base_driver import AuthenticationError, ConnectionError, DriverError
from .conn_manager import ConnectionManager

with disable_logging():
    set_env("TFTP_ADDRESS", config.tftp.address)
    set_env("TFTP_PORT", config.tftp.port)
    set_env("TFTP_FOLDER", config.tftp.folder)

__all__ = [
    "ConnectionManager",
    "DriverError",
    "ConnectionError",
    "AuthenticationError",
]
