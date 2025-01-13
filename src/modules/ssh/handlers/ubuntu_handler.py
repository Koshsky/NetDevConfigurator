from .base_handler import BaseHandler, handle_device_open

from scrapli.driver import GenericDriver


class ubuntuHandler(BaseHandler):  # r"^(\n)?.+@.+[#>$]\s*$"
    def on_open(self, cls: GenericDriver) -> None:
        handle_device_open(cls, [])

    def on_close(self, cls: GenericDriver) -> None:
        pass
