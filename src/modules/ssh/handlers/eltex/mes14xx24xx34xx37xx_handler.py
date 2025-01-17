from ..base_handler import BaseHandler, handle_device_open

from scrapli.driver import GenericDriver
from scrapli.response import Response

from modules import ssh_logger


class MES14xx24xx34xx37xxHandler(BaseHandler):
    @ssh_logger
    def on_open(self, cls: GenericDriver) -> Response:
        return handle_device_open(cls, ["set cli pagination off"])

    def on_close(self, cls: GenericDriver) -> None:
        cls.channel.write(channel_input="exit")
        cls.channel.send_return()

    def load_boot(self, cls: GenericDriver) -> Response:
        raise NotImplementedError("Subclasses should implement  load_boot method")

    def load_uboot(self, cls: GenericDriver) -> Response:
        raise NotImplementedError("Subclasses should implement  load_uboot method")

    def load_firmware(self, cls: GenericDriver) -> Response:
        raise NotImplementedError("Subclasses should implement  load_firmware method")
