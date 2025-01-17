import logging
from typing import List

from scrapli.driver import GenericDriver
from scrapli.response import Response
from config import config
from modules import ssh_logger


class BaseHandler:
    """Base class for device handlers."""

    def __init__(
        self,
        comms_prompt_pattern: str = r"^(\n)?.+[#>$]\s*$",
        ssh_config_file: str = config["ssh-config-file"],
    ) -> None:
        self.comms_prompt_pattern = comms_prompt_pattern
        self.ssh_config_file = ssh_config_file

    def on_open(self, cls: GenericDriver) -> None:
        raise NotImplementedError("Subclasses should implement on_open method.")

    def on_close(self, cls: GenericDriver) -> None:
        raise NotImplementedError("Subclasses should implement on_close method.")

    def get_header(self, cls: GenericDriver) -> str:
        resp = cls.send_command("show running-config").result()
        res = ""
        for line in resp.split("\n"):
            if not line.startswith("#"):
                break
            res += line + "\n"
        return res.strip()

    def load_boot(self, cls: GenericDriver) -> Response:
        raise NotImplementedError("Subclasses should implement  load_boot method")

    def load_uboot(self, cls: GenericDriver) -> Response:
        raise NotImplementedError("Subclasses should implement  load_uboot method")

    def load_firmware(self, cls: GenericDriver) -> Response:
        raise NotImplementedError("Subclasses should implement  load_firmware method")

    @ssh_logger
    def update_startup_config(self, cls: GenericDriver, path_to_file: str) -> Response:
        return cls.send_command(
            f"copy tftp://{cls.tftp_server}{cls.tmp_folder}/{path_to_file} startup-config"
        )

    @ssh_logger
    def show_run(self, cls: GenericDriver) -> Response:
        return cls.send_command("show running-config")


def handle_device_open(cls: GenericDriver, commands: List[str]) -> Response:
    """Handle the opening sequence for devices."""
    try:
        cls.channel.write(cls.auth_password)
        cls.channel.send_return()
        for command in commands:
            print(f"on_open: execute {command}")
            if resp := cls.send_command(command):
                return resp
        logging.info(f"Successfully completed opening sequence for {cls.family}.")
    except Exception as e:
        logging.error(f"Error during opening sequence for {cls.family}: {e}")
