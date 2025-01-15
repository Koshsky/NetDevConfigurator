from ..base_handler import BaseHandler, handle_device_open

from scrapli.driver import GenericDriver


class MES23xx35xxHandler(BaseHandler):  # + mes3300
    def on_open(self, cls: GenericDriver) -> None:
        handle_device_open(
            cls, ["terminal datadump", "terminal width 0", "terminal no prompt"]
        )

    def on_close(self, cls: GenericDriver) -> None:
        cls.channel.write(channel_input="exit")
        cls.channel.send_return()
