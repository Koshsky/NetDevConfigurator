from .base_driver import SSHDriverBase
from utils import find_most_recent_file

from config import config


class SSHDriver(SSHDriverBase):
    TFTP_FOLDER = config["tftp-server"]["folder"]

    def show_run(self):
        return self.send_command(self.core.show_run).result

    def get_header(self):
        config = self.show_run()
        header = ""
        for line in config.split("\n"):
            if not line.startswith("#"):
                break
            header += line + "\n"
        return header + "!\n"

    def base_configure(self):
        return "\n".join(
            resp.result for resp in self.send_commands(self.core.base_configure)
        )

    def update_startup_config(self, filename):
        command = self.core.update_startup_config.format(filename)
        return self.send_command(command).result

    def show_bootvar(self):
        return self.send_command(self.core.show_bootvar).result

    def reboot(self):
        if isinstance(self.core.reload, str):
            self.send_command(self.core.reload)
        else:
            self.send_commands(self.core.reload)

    def update_boot(self):
        filename = find_most_recent_file(
            f"{self.TFTP_FOLDER}/firmware", self.device["pattern"]["boot"]
        )
        return self.send_command(self.core.load_boot.format(filename)).result

    def update_uboot(self):
        filename = find_most_recent_file(
            f"{self.TFTP_FOLDER}/firmware",
            self.device["pattern"]["uboot"],
        )
        return self.send_command(self.core.load_uboot.format(filename)).result

    def update_firmware(self):
        filename = find_most_recent_file(
            f"{self.TFTP_FOLDER}/firmware",
            self.device["pattern"]["firmware"],
        )
        return self.send_command(self.core.load_firmware.format(filename)).result
