import logging
from typing import List

from scrapli.driver import GenericDriver
from scrapli.response import Response

class BaseHandler:
    """Base class for device handlers."""
    def __init__(
        self,
        comms_prompt_pattern: str = r"^(\n)?.+[#>$]\s*$",
        ssh_config_file: str = "~/NetDevConfigurator/src/modules/ssh/default_ssh_config"
    ) -> None:
        self.comms_prompt_pattern = comms_prompt_pattern
        self.ssh_config_file = ssh_config_file

    def on_open(self, cls: GenericDriver) -> None:
        raise NotImplementedError("Subclasses should implement on_open method.")

    def on_close(self, cls: GenericDriver) -> None:
        raise NotImplementedError("Subclasses should implement on_close method.")
    

    def tftp_send(self, cls: GenericDriver, path_to_file: str) -> Response:
        if path_to_file.startswith(cls.tftp_folder):
            path_to_file = path_to_file[len(cls.tftp_folder):]
        print('tftp_send:', f'copy tftp://{cls.tftp_server}/{path_to_file} startup-config')
        return cls.send_command(f'copy tftp://{cls.tftp_server}{path_to_file} startup-config')  # TODO: running-config -> startup-config

    def show_run(self, cls: GenericDriver) -> Response:
        return cls.send_command("show running-config")


def handle_device_open(cls: GenericDriver, commands: List[str]) -> None:
    """Handle the opening sequence for devices."""
    try:
        cls.channel.write(cls.auth_password)
        cls.channel.send_return()
        for command in commands:
            print(f'on_open: execute {command}')
            if resp := cls.send_command(command):
                print(resp.result)
        logging.info(f"Successfully completed opening sequence for {cls.family}.")
    except Exception as e:
        logging.error(f"Error during opening sequence for {cls.family}: {e}")
