from utils.environ import get_env
from .device_core import DeviceCore


class BaseESR(DeviceCore):
    comment_symbol = "#"
    comms_prompt_pattern = r"^(\n)?.+[>#\$]\s*"
    open_sequence = ["terminal datadump"]

    show_run = "show running-config extended"
    reload = ["reload system", "y"]

    @property
    def update_startup_config(self):
        return [
            f"copy tftp://{get_env('TFTP_ADDRESS')}:/tmp/{get_env('CFG_FILENAME')} system:candidate-config",
        ]

    show_diff = "show configuration changes"
    rollback = "rollback"
    commit = "commit"

    @property
    def base_configure_192(self):
        return [
            "configure",
            "interface vlan 1",
            f"ip address {get_env('HOST_ADDRESS')} 255.255.255.0",
            "!",
            "interface gigabitethernet 1/0/1",
            "switchport mode access",
            "no switchport forbidden default-vlan",
            "switchport access vlan 1",
            "!",
            "end",
        ]

    def show_bootvar(self):
        return "show bootvar"


class ESR2x(BaseESR):
    @property
    def load_boot(self):
        return (
            f"copy tftp://{get_env('TFTP_ADDRESS')}/firmware/{get_env('FILENAME')} system:boot-1"
        )

    @property
    def load_uboot(self):
        return f"copy tftp://{get_env('TFTP_ADDRESS')}/firmware/{get_env('FILENAME')} system:boot-2"

    @property
    def load_firmware(self):
        return f"copy tftp://{get_env('TFTP_ADDRESS')}/firmware/{get_env('FILENAME')} system:firmware"


class ESR3x(BaseESR):
    @property
    def load_uboot(self):
        return f"copy tftp://{get_env('TFTP_ADDRESS')}/firmware/{get_env('FILENAME')} system:boot"

    @property
    def load_firmware(self):
        return f"copy tftp://{get_env('TFTP_ADDRESS')}/firmware/{get_env('FILENAME')} system:firmware"
