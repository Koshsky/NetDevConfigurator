from config import config


class BaseMES:
    comms_prompt_pattern = r"^(\n)?[a-z0-9_]+[>#\$]\s*$"
    success_signs = {"succeeded", "successful", "success"}

    update_startup_config = "copy tftp://{0}/{1}/{2} startup-config"
    show_run = "show running-config"
    base_configure = [  # TODO: подумать еще!
        "configure terminal",
        "interface vlan 1",
        f"ip address {config['free-temp-ip']}",
        "ssh enable",
        "ip route 0.0.0.0 0.0.0.0 10.4.0.254",
        "end",
    ]


class MES14xx24xx34xx37xx(BaseMES):
    open_sequence = ["set cli pagination off"]
    # 0: tftp_server 1: tmp_folder 2: filename
    load_boot = "copy tftp://{0}/{1}/{2} boot"
    load_firmware = "copy tftp://{0}/{1}/{2} image"

    show_bootvar = "show bootvar"


class MES23xx33xx35xx36xx53xx5400(BaseMES):
    open_sequence = ["terminal datadump", "terminal width 0", "terminal no prompt"]
    # 0: tftp_server 1: tmp_folder 2: filename
    load_boot = "boot system tftp://{0}/{1}/{2}"
    # load_firmware = "copy tftp://{0}/{1}/{2} image"


class MES11xx21xx20xx31xx(BaseMES):
    open_sequence = ["terminal datadump"]
    # 0: tftp_server 1: tmp_folder 2: filename
    # load_boot = "boot system tftp://{0}/{1}/{2}"
    # load_firmware = "copy tftp://{0}/{1}/{2} image"
