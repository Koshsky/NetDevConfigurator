from config import config
from scrapli.driver import GenericDriver

from ..core import handle_device_open, get_core


class SSHDriverBase(GenericDriver):
    def __init__(self, family: str, **kwargs) -> None:
        self.core = get_core(family)

        kwargs["transport"] = "ssh2"
        kwargs["on_open"] = self.on_open
        kwargs["on_close"] = self.on_close
        kwargs["comms_prompt_pattern"] = self.core.comms_prompt_pattern
        super().__init__(**kwargs)

        self.tftp_server = config["tftp-server"]["address"]
        self.tmp_folder = config["tftp-server"]["folder"]["tmp"]
        self.firmware_folder = config["tftp-server"]["folder"]["firmware"]

    def on_open(self, cls: GenericDriver):
        return handle_device_open(cls, self.core.open_sequence)

    def on_close(self, cls: GenericDriver):
        cls.channel.write("exit")
        cls.channel.send_return()
