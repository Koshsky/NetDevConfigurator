from ..base_handler import BaseHandler, handle_device_open

from scrapli.driver import GenericDriver
from scrapli.response import Response

from modules import ssh_logger


class MES23xx33xx35xx36xx53xx5400Handler(BaseHandler):  # + mes3300
    @ssh_logger
    def on_open(self, cls: GenericDriver) -> Response:
        return handle_device_open(
            cls, ["terminal datadump", "terminal width 0", "terminal no prompt"]
        )

    def on_close(self, cls: GenericDriver) -> None:
        cls.channel.write(channel_input="exit")
        cls.channel.send_return()

    def load_boot(self, cls: GenericDriver) -> Response:
        raise NotImplementedError("Subclasses should implement  load_boot method")

    def load_uboot(self, cls: GenericDriver) -> Response:
        raise NotImplementedError("Subclasses should implement  load_uboot method")

    def load_firmware(self, cls: GenericDriver) -> Response:
        raise NotImplementedError("Subclasses should implement  load_firmware method")
