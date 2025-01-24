from config import config


class BaseMES:
    comms_prompt_pattern = r"^(\n)?[a-z0-9_]+[>#\$]\s*$"
    success_signs = {"succeeded", "successful", "success"}
    update_startup_config = (
        f"copy tftp://{config['tftp-server']['address']}/" + "tmp/{0} startup-config"
    )
    show_run = "show running-config"
    base_configure_192 = [
        "configure terminal",
        "interface vlan 1",
        "ip address {0} 255.255.255.0".format(next(config["available-ip"])),
        "ssh enable",
        "end",
    ]
    reload = "reload\nyy"  # cause 'y' 'y' DOESN'T require '\n'
    show_bootvar = "show bootvar"


class MES14xx24xx34xx37xx(BaseMES):
    open_sequence = ["set cli pagination off"]
    load_boot = f"copy tftp://{config['tftp-server']['address']}/" + "firmware/{0} boot"
    load_firmware = (
        f"copy tftp://{config['tftp-server']['address']}/" + "firmware/{0} image"
    )


class MES23xx33xx35xx36xx53xx5400(BaseMES):
    open_sequence = ["terminal datadump", "terminal width 0", "terminal no prompt"]
    load_boot = (
        f"boot system tftp://{config['tftp-server']['address']}/" + "firmware/{0}"
    )


class MES11xx21xx20xx31xx(BaseMES):
    open_sequence = ["terminal datadump"]
    # load_boot = "boot system tftp://{0}/{1}/{2}"
    # load_firmware = "copy tftp://{0}/{1}/{2} image"
