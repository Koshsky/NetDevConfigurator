from ..base_handler import BaseHandler, handle_device_open

from scrapli.driver import GenericDriver
from scrapli.response import Response

from modules import apply_ssh_logger


@apply_ssh_logger
class MES14xx24xx34xx37xxHandler(BaseHandler):
    def on_open(self, cls: GenericDriver) -> Response:
        return handle_device_open(cls, ["set cli pagination off"])

    def update_startup_config(self, cls: GenericDriver, filename: str) -> Response:
        return cls.send_command(
            f"copy tftp://{cls.tftp_server}/{cls.tmp_folder}/{filename} startup-config"
        )

    def load_boot(self, cls: GenericDriver, filename: str) -> Response:
        return cls.send_command(
            f"copy tftp://{cls.tftp_server}/{cls.tmp_folder}/{filename} boot"
        )

    def load_firmware(self, cls: GenericDriver, filename: str) -> Response:
        return cls.send_command(
            f"copy tftp://{cls.tftp_server}/{cls.tmp_folder}/{filename} image"
        )
