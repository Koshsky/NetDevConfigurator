from time import sleep  # TODO: проверить необходимость задержок
import logging
from typing import List

from scrapli.driver import GenericDriver
from scrapli.response import Response

def handle_device_open(cls: GenericDriver, commands: List[str]) -> None:
    """Handle the opening sequence for devices."""
    try:
        cls.channel.write(cls.auth_password)
        cls.channel.send_return()
        for command in commands:
            cls.send_command(command)
        logging.info(f"Successfully completed opening sequence for {cls.family}.")
    except Exception as e:
        logging.error(f"Error during opening sequence for {cls.family}: {e}")

class DeviceHandler:
    """Base class for device handlers."""
    def __init__(
        self,
        comms_prompt_pattern: str = r"^(\\n)?[a-z0-9\.\-_@/:]{1,63}[#>]\s*$",
        ssh_config_file: str = "~/NetDevConfigurator/src/modules/ssh/default_ssh_config"
    ) -> None:
        self.comms_prompt_pattern = comms_prompt_pattern
        self.ssh_config_file = ssh_config_file

    def on_open(self, cls: GenericDriver) -> None:
        raise NotImplementedError("Subclasses should implement this method.")

    def tftp_send(self, cls: GenericDriver, path_to_file: str) -> Response:
        if path_to_file.startswith(self.tftp_folder):
            path_to_file = path_to_file[len(self.tftp_folder):]
        return cls.send_command(f'copy tftp://{cls.tftp_server}/{path_to_file} running-config')  # TODO: running-config -> startup-config

    def show_run(self, cls: GenericDriver) -> Response:
        return cls.send_command("show running-config")

class ubuntuHandler(DeviceHandler):
    def __init__(self):
        super().__init__()

    def on_open(self, cls: GenericDriver) -> None:
        handle_device_open(cls, [])

    def test_func(self, cls: GenericDriver) -> str:
        return f"{cls.tftp_server}/{cls.tftp_folder}"

class MES14xx24xx37xxHandler(DeviceHandler):
    def on_open(self, cls: GenericDriver) -> None:
        handle_device_open(cls, ["set cli pagination off"])


class MES11xx21xx31xxHandler(DeviceHandler):
    def on_open(self, cls: GenericDriver) -> None:
        handle_device_open(cls, ["terminal datadump"])


class MES23xx35xxHandler(DeviceHandler):
    def on_open(self, cls: GenericDriver) -> None:
        handle_device_open(cls, ["terminal datadump", "terminal width 0", "terminal no prompt"])


class MES54487048Handler(DeviceHandler):
    def on_open(self, cls: GenericDriver) -> None:
        handle_device_open(cls, ["enable", "terminal length 0"])
