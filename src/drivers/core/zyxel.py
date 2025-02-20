import os


class BaseZyxel:
    comms_prompt_pattern = r"^(\n)?[a-zA-Z0-9_-]+[>#\$]\s*$"
    success_signs = {
        "Copyright",
    }
    open_sequence = ["set cli pagination off"]  # TODO: not actual

    reload = "reload config 1\ny"
    show_run = "show running-config"

    @property
    def update_startup_config(self):
        return f"copy tftp config 1 {os.environ['TFTP_ADDRESS']} tmp/{os.environ['CFG_FILENAME']}"

    @property
    def base_configure_192(self):  # TODO: not actual
        return [
            "configure terminal",
            "interface vlan 1",
            f"ip address {os.environ['HOST_ADDRESS']} 255.255.255.0",
            "ssh enable",
            "!",
            "interface gigabitethernet 0/1",
            "no switchport general allowed vlan",
            "switchport mode access",
            "no switchport forbidden default-vlan",
            "switchport access vlan 1",
            "!",
            "end",
        ]

    @property
    def load_firmware(self):
        return f"copy tftp flash {os.environ['TFTP_ADDRESS']} firmware/{os.environ['FILENAME']}"
