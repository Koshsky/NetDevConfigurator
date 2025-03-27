from utils.environ import get_env

from .device_core import DeviceCore


class BaseZyxel(DeviceCore):
    comment_symbol = ";"
    comms_prompt_pattern = r"^(\n)?[a-zA-Z0-9_-]+[>#\$]\s*"
    open_sequence = []

    reload = "reload config 1\ny"
    show_run = "show running-config"

    @property
    def update_startup_config(self):
        return f"copy tftp config 1 {get_env('TFTP_ADDRESS')} {get_env('CFG_PATH')}"

    @property
    def base_configure_192(self):
        return [
            "configure",
            "vlan 1",
            f"ip address default-management {get_env('HOST_ADDRESS')} 255.255.255.0",
            "end",
        ]

    @property
    def load_firmware(self):
        return (
            f"copy tftp flash {get_env('TFTP_ADDRESS')} firmware/{get_env('FILENAME')}"
        )
