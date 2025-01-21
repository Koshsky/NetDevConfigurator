from .base_driver import SSHDriverBase
from utils import find_most_recent_file


class SSHDriver(SSHDriverBase):
    def show_run(self):
        return self.send_command(self.core.show_run).result

    def base_configure(self):
        return "\n".join(
            resp.result for resp in self.send_commands(self.core.base_configure)
        )

    def show_bootvar(self):
        return self.send_command(self.core.show_bootvar).result

    def reboot(self):
        return "\n".join(resp.result for resp in self.send_commands(self.core.reload))

    def update_boot(self):
        filename = find_most_recent_file(
            f"{self.TFTP_FOLDER}/{self.FIRMWARE_FOLDER}", self.device["pattern"]["boot"]
        )
        return self.send_command(
            self.core.load_boot.format(self.tftp_server, self.TMP_FOLDER, filename)
        ).result

    def update_uboot(self):
        filename = find_most_recent_file(
            f"{self.TFTP_FOLDER}/{self.FIRMWARE_FOLDER}",
            self.device["pattern"]["uboot"],
        )
        return self.send_command(
            self.core.load_uboot.format(self.tftp_server, self.TMP_FOLDER, filename)
        ).result

    def update_firmware(self):
        filename = find_most_recent_file(
            f"{self.TFTP_FOLDER}/{self.FIRMWARE_FOLDER}",
            self.device["pattern"]["firmware"],
        )
        return self.send_command(
            self.core.load_firmware.format(
                self.tftp_server, self.FIRMWARE_FOLDER, filename
            )
        ).result
