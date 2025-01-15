from ..base_handler import BaseHandler, handle_device_open

from scrapli.driver import GenericDriver
from scrapli.response import Response

from modules import ssh_logger


class MES11xx21xx31xxHandler(BaseHandler):
    @ssh_logger
    def on_open(self, cls: GenericDriver) -> Response:
        return handle_device_open(cls, ["terminal datadump"])

    def on_close(self, cls: GenericDriver) -> None:
        cls.channel.write(channel_input="exit")
        cls.channel.send_return()
