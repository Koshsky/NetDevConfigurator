import os


class BaseZyxel:
    comment_symbol = ";"
    comms_prompt_pattern = r"^(\n)?[a-zA-Z0-9_-]+[>#\$]\s*"
    open_sequence = []

    reload = "reload config 1\ny"
    show_run = "show running-config"

    @property
    def update_startup_config(self):
        return f"copy tftp config 1 {os.environ['TFTP_ADDRESS']} tmp/{os.environ['CFG_FILENAME']}"

    @property
    def base_configure_192(self):
        return [
            "configure",
            "vlan 1",
            f"ip address default-management {os.environ['HOST_ADDRESS']} 255.255.255.0",
            "end",
        ]

    @property
    def load_firmware(self):
        return f"copy tftp flash {os.environ['TFTP_ADDRESS']} firmware/{os.environ['FILENAME']}"
