import logging
import os

from drivers.core import get_core
from utils.environ import set_env
from utils.filesystem import find_most_recent_file

logger = logging.getLogger("mock")


class MockDriver:
    def __init__(self, device, **driver):
        self.core = get_core(device["family"]["name"])
        self.device = device

    def send_command(self, command):
        logger.info("Send: %s", command)

    def send_commands(self, commands):
        for command in commands:
            self.send_command(command)

    def __enter__(self):
        self.send_commands(self.core.open_sequence)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def show_run(self):
        self.send_command(self.core.show_run)
        return f"""
{self.core.comment_symbol} header line 1
{self.core.comment_symbol} header line 2

hostname pup-123

interface 1
    be
!
interface 2
    be
!
"""

    def get_header(self):
        config = self.show_run()
        header = ""
        for line in config.split("\n"):
            if line.startswith(self.core.comment_symbol):
                header += line + "\n"
        return header + "!\n"

    def update_startup_config(self):
        command = self.core.update_startup_config
        if isinstance(command, str):
            self.send_command(command)
        else:
            self.send_commands(command)

    def reboot(self):
        self.send_command(self.core.reload)

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
        else:
            set_env("FILENAME", filename)
            return self.send_command(self.core.load_boot)

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
        else:
            set_env("FILENAME", filename)
            return self.send_command(self.core.load_uboot)

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
        else:
            set_env("FILENAME", filename)
            return self.send_command(self.core.load_firmware)

    def update_firmwares(self):
        res = self.update_boot()
        res += self.update_uboot()
        return res + self.update_firmware()
