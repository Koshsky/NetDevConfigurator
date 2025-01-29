import os

from utils import find_most_recent_file

from .base_driver import SSHBaseDriver


class SSHDriver(SSHBaseDriver):
    def show_run(self):
        return self.send_command(self.core.show_run)

    def get_header(self):
        config = self.show_run()
        header = ""
        for line in config.split("\n"):
            if not line.startswith("#"):
                break
            header += line + "\n"
        return header + "!\n"

    def update_startup_config(self, filename):
        command = self.core.update_startup_config.format(filename)
        return self.send_command(command)

    def show_bootvar(self):
        return self.send_command(self.core.show_bootvar)

    def reboot(self):
        if isinstance(self.core.reload, str):
            self.send_command(self.core.reload)
        else:
            self.send_commands(self.core.reload)

    def update_boot(self):
        filename = find_most_recent_file(
            f"{os.environ['TFTP_FOLDER']}/firmware", self.device["pattern"]["boot"]
        )
        return self.send_command(self.core.load_boot.format(filename))

    def update_uboot(self):
        filename = find_most_recent_file(
            f"{os.environ['TFTP_FOLDER']}/firmware",
            self.device["pattern"]["uboot"],
        )
        return self.send_command(self.core.load_uboot.format(filename))

    def update_firmware(self):
        filename = find_most_recent_file(
            f"{os.environ['TFTP_FOLDER']}/firmware",
            self.device["pattern"]["firmware"],
        )
        return self.send_command(self.core.load_firmware.format(filename))
