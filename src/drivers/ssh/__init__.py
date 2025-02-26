from .ssh_driver import SSHDriver
from config import config
from utils.environ import set_env

set_env("TFTP_ADDRESS", config["tftp-server"]["address"])
set_env("TFTP_PORT", config["tftp-server"]["port"])
set_env("TFTP_FOLDER", config["tftp-server"]["folder"])

__all__ = ["SSHDriver"]
