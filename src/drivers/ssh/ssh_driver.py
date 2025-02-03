import logging
import os

from utils import find_most_recent_file

from .base_driver import SSHBaseDriver

logger = logging.getLogger("ssh")


class SSHDriver(SSHBaseDriver):
    def show_run(self):
        return self.send_command(self.core.show_run)

    def get_header(self):
        config = self.show_run()
        header = ""
        for line in config.split("\n"):
            if line.startswith("#"):
                header += line + "\n"
        return header + "!\n"

    def update_startup_config(self, filename):
        os.environ["FILENAME"] = filename
        command = self.core.update_startup_config
        return self.send_command(command)

    def show_bootvar(self):
        return self.send_command(self.core.show_bootvar)

    def reboot(self):
        self.ssh.send(f"{self.core.reload}\n")
        logger.info(f"Send: {self.core.reload}")

    def update_boot(self):
        os.environ["FILENAME"] = find_most_recent_file(
            f"{os.environ['TFTP_FOLDER']}/firmware", self.device["pattern"]["boot"]
        )
        return self.send_command(self.core.load_boot)

    def update_uboot(self):
        os.environ["FILENAME"] = find_most_recent_file(
            f"{os.environ['TFTP_FOLDER']}/firmware",
            self.device["pattern"]["uboot"],
        )
        return self.send_command(self.core.load_uboot)

    def update_firmware(self):
        os.environ["FILENAME"] = find_most_recent_file(
            f"{os.environ['TFTP_FOLDER']}/firmware",
            self.device["pattern"]["firmware"],
        )
        return self.send_command(self.core.load_firmware)
