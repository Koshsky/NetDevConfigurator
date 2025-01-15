from .base_handler import BaseHandler, handle_device_open

from scrapli.driver import GenericDriver
from scrapli.response import Response
from modules import ssh_logger


class ubuntuHandler(BaseHandler):  # r"^(\n)?.+@.+[#>$]\s*$"
    @ssh_logger
    def on_open(self, cls: GenericDriver) -> Response:
        handle_device_open(cls, [])

    def on_close(self, cls: GenericDriver) -> None:
        pass
