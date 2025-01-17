from ..base_handler import BaseHandler, handle_device_open

from scrapli.driver import GenericDriver
from scrapli.response import Response

from modules import apply_ssh_logger


@apply_ssh_logger
class MES23xx33xx35xx36xx53xx5400Handler(BaseHandler):  # + mes3300
    def on_open(self, cls: GenericDriver) -> Response:
        return handle_device_open(
            cls, ["terminal datadump", "terminal width 0", "terminal no prompt"]
        )

    def update_startup_config(
        self, cls: GenericDriver, filename: str
    ) -> Response:  # TODO: выяснить так ли это
        return cls.send_command(  # если так, вынести это в base_handler
            f"copy tftp://{cls.tftp_server}/{cls.tmp_folder}/{filename} startup-config"
        )

    def load_boot(self, cls: GenericDriver, filename: str) -> Response:
        return cls.send_command(
            f"boot system tftp://{cls.tftp_server}/{cls.firmware_folder}/{filename}"
        )
