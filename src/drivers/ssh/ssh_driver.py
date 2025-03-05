import logging
import os

from utils.environ import set_env
from utils.filesystem import find_most_recent_file

from .base_driver import SSHBaseDriver

logger = logging.getLogger("ssh")


class SSHDriver(SSHBaseDriver):
    def show_run(self):
        return self.send_command(self.core.show_run)

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
        if isinstance(command, str):
            return self.send_command(command)
        else:
            return self.send_commands(
                command
            )  # for zyxel, they require command sequence

    def reboot(self):
        self.ssh.send(f"{self.core.reload}\n")
        logger.info("Send: %s", self.core.reload)

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
