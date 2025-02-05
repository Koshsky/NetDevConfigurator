import os


class BaseMES:
    comms_prompt_pattern = r"^(\n)?[a-zA-Z0-9_-]+[>#\$]\s*$"
    success_signs = {"succeeded", "successful", "success"}

    reload = "reload\nyy"  # cause 'y' 'y' DOESN'T require '\n'
    show_bootvar = "show bootvar"
    show_run = "show running-config"

    @property
    def update_startup_config(self):
        return f"copy tftp://{os.environ['TFTP_ADDRESS']}/tmp/{os.environ['FILENAME']} startup-config"

    @property
    def base_configure_192(self):
        return [
            "configure terminal",
            "interface vlan 1",
            f"ip address {os.environ['HOST_ADDRESS']} 255.255.255.0",
            "ssh enable",
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
