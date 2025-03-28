from utils.environ import get_env

from .device_core import DeviceCore


class BaseMES(DeviceCore):
    comment_symbol = "#"
    comms_prompt_pattern = r"^(\n)?[a-zA-Z0-9_-]+[>#\$]\s*$"
    open_sequence = []
    reload = "reload\nyy"
    show_run = "show running-config"

    @property
    def update_startup_config(self):
        return f"copy tftp://{get_env('TFTP_ADDRESS')}/{get_env('CFG_PATH')} startup-config"

    @property
    def base_configure_192(self):
        return [
            "configure terminal",
            "interface vlan 1",
            f"ip address {get_env('HOST_ADDRESS')} 255.255.255.0",
            "ssh enable",
            "!",
            # "interface gigabitethernet 0/1",
            # "no switchport general allowed vlan",
            # "switchport mode access",
            # "no switchport forbidden default-vlan",
            # "switchport access vlan 1",
            # "!",
            "end",
        ]


class MES14xx24xx34xx37xx(BaseMES):
    open_sequence = ["set cli pagination off"]

    @property
    def load_boot(self):
        return (
            f"copy tftp://{get_env('TFTP_ADDRESS')}/firmware/{get_env('FILENAME')} boot"
        )

    @property
    def load_firmware(self):
        return f"copy tftp://{get_env('TFTP_ADDRESS')}/firmware/{get_env('FILENAME')} image"


class MES23xx33xx35xx36xx53xx5400(BaseMES):
    open_sequence = ["terminal datadump", "terminal width 0", "terminal no prompt"]

    @property
    def load_firmware(self):
        return f"boot system tftp://{get_env('TFTP_ADDRESS')}/firmware/{get_env('FILENAME')}"


class MES11xx21xx20xx31xx(BaseMES):
    open_sequence = ["terminal datadump"]
    # load_boot = "boot system tftp://{0}/{1}/{2}"
    # load_firmware = "copy tftp://{0}/{1}/{2} image"
