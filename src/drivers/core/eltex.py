import os


class ESRxx:
    comment_symbol = "#"
    comms_prompt_pattern = r"^(\n)?[a-zA-Z0-9().\-_]+[>#\$]\s*"
    open_sequence = ["terminal datadump"]

    show_run = "show running-config extended"
    reload = "reload system"

    @property
    def update_startup_config(self):
        return [
            f"copy tftp://{os.environ['TFTP_ADDRESS']}:/tmp/{os.environ['CFG_FILENAME']} system:candidate-config",
        ]

    # @property
    # def load_boot(
    #     self,
    # ):
    #     return f"copy tftp://{os.environ['TFTP_ADDRESS']}/firmware/{os.environ['FILENAME']} boot"

    @property
    def base_configure_192(self):
        return [
            "configure",
            "interface vlan 1",
            f"ip address {os.environ['HOST_ADDRESS']} 255.255.255.0",
            "!",
            "interface gigabitethernet 1/0/1",
            "switchport mode access",
            "no switchport forbidden default-vlan",
            "switchport access vlan 1",
            "!",
            "end",
        ]

    @property
    def load_uboot(self):
        return f"copy tftp://{os.environ['TFTP_ADDRESS']}/firmware/{os.environ['FILENAME']} system:boot-2"

    @property
    def load_firmware(self):
        return f"copy tftp://{os.environ['TFTP_ADDRESS']}/firmware/{os.environ['FILENAME']} system:firmware"
        # TODO: БУДУЩЕЕ распарсить show bootvar и определить более новый образ
        # boot system image-[12]

    def show_bootvar(self):
        return "show bootvar"


class BaseMES:
    comment_symbol = "#"
    comms_prompt_pattern = r"^(\n)?[a-zA-Z0-9_-]+[>#\$]\s*$"

    reload = "reload\nyy"  # cause 'y' 'y' DOESN'T require '\n'
    show_run = "show running-config"

    @property
    def update_startup_config(self):
        return f"copy tftp://{os.environ['TFTP_ADDRESS']}/tmp/{os.environ['CFG_FILENAME']} startup-config"

    @property
    def base_configure_192(self):
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


class MES14xx24xx34xx37xx(BaseMES):
    open_sequence = ["set cli pagination off"]

    @property
    def load_boot(self):
        return f"copy tftp://{os.environ['TFTP_ADDRESS']}/firmware/{os.environ['FILENAME']} boot"

    @property
    def load_firmware(self):
        return f"copy tftp://{os.environ['TFTP_ADDRESS']}/firmware/{os.environ['FILENAME']} image"


class MES23xx33xx35xx36xx53xx5400(BaseMES):
    open_sequence = ["terminal datadump", "terminal width 0", "terminal no prompt"]

    @property
    def load_boot(self):
        return f"boot system tftp://{os.environ['TFTP_ADDRESS']}/firmware/{os.environ['FILENAME']}"


class MES11xx21xx20xx31xx(BaseMES):
    open_sequence = ["terminal datadump"]
    # load_boot = "boot system tftp://{0}/{1}/{2}"
    # load_firmware = "copy tftp://{0}/{1}/{2} image"
