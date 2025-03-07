import logging
import os

from utils.environ import set_env
from utils.filesystem import find_most_recent_file
from utils.network import find_available_ip

from .com import COMBaseDriver
from .core import get_core
from .mock import MockDriver
from .ssh import SSHBaseDriver

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self, device, connection_type: str, **driver_kwargs):
        self.core = get_core(device["family"]["name"])
        self.device = device

        if driver_class := {
            "ssh": SSHBaseDriver,
            "com": COMBaseDriver,
            "mock": MockDriver,
        }.get(connection_type.lower()):
            self.driver = driver_class(
                on_open_sequence=self.core.open_sequence,
                comms_prompt_pattern=self.core.comms_prompt_pattern,
                **driver_kwargs,
            )
        else:
            raise ValueError(f"Invalid connection type: {connection_type}")

    def __enter__(self):
        self.driver.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.__exit__(exc_type, exc_val, exc_tb)

    def base_configure_192(self):
        available_ip = find_available_ip(
            "192.168.3.0/24",  # hardcode bc 192 in function name
            lambda ip: ip.packed[-1] >= 100 and ip.packed[-1] < 201,
        )
        set_env("HOST_ADDRESS", available_ip)
        return self.driver.execute(self.core.base_configure_192)

    def show_run(self):
        return self.driver.execute(self.core.show_run)

    def get_header(self):
        config = self.show_run()
        header = "".join(
            line + "\n"
            for line in config.split("\n")
            if line.startswith(self.core.comment_symbol)
        )
        return header + "!\n"

    def update_startup_config(self):
        command = self.core.update_startup_config
        return self.driver.execute(command)

    def reboot(self):
        self.driver.execute(self.core.reload)

    def update_boot(self):
        filename = find_most_recent_file(
            f"{os.environ['TFTP_FOLDER']}/firmware", self.device["pattern"]["boot"]
        )
        if filename is None:
            logger.warning(
                "There is no boot file for %s in %s matching %s",
                self.device["name"],
                os.environ["TFTP_FOLDER"],
                self.device["pattern"]["boot"],
            )
            return ""
        else:
            set_env("FILENAME", filename)
            return self.driver.execute(self.core.load_boot)

    def update_uboot(self):
        filename = find_most_recent_file(
            f"{os.environ['TFTP_FOLDER']}/firmware", self.device["pattern"]["uboot"]
        )
        if filename is None:
            logger.warning(
                "There is no uboot file for %s in %s matching %s",
                self.device["name"],
                os.environ["TFTP_FOLDER"],
                self.device["pattern"]["uboot"],
            )
            return ""
        else:
            set_env("FILENAME", filename)
            return self.driver.execute(self.core.load_uboot)

    def update_firmware(self):
        filename = find_most_recent_file(
            f"{os.environ['TFTP_FOLDER']}/firmware", self.device["pattern"]["firmware"]
        )
        if filename is None:
            logger.warning(
                "There is no firmware file for %s in %s matching %s",
                self.device["name"],
                os.environ["TFTP_FOLDER"],
                self.device["pattern"]["firmware"],
            )
            return ""
        else:
            set_env("FILENAME", filename)
            return self.driver.execute(self.core.load_firmware)

    def update_firmwares(self):
        res = self.update_boot()
        res += self.update_uboot()
        return res + self.update_firmware()
