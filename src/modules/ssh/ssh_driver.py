from .handlers import (
    MES14xx24xx34xx37xxHandler,
    MES11xx21xx20xx31xxHandler,
    MES23xx33xx35xx36xx53xx5400Handler,
)

from config import config
from scrapli.driver import GenericDriver


class SSHDriver(GenericDriver):
    def __init__(self, family: str, **kwargs) -> None:
        kwargs["transport"] = "ssh2"
        handler_map = {
            "MES14xx/24xx/34xx/37xx": MES14xx24xx34xx37xxHandler(),
            "MES11xx/21xx/22xx/31xx": MES11xx21xx20xx31xxHandler(),
            "MES23xx/33xx/35xx/36xx/53xx/5400": MES23xx33xx35xx36xx53xx5400Handler(),
        }
        self.handler = handler_map.get(family, None)
        if self.handler is None:
            raise ValueError(f"Unsupported device family: {family}")

        kwargs["on_open"] = self.handler.on_open
        kwargs["on_close"] = self.handler.on_close
        super().__init__(**kwargs)

        self.family = family
        self.tftp_server = config["tftp-server"]["address"]
        self.tmp_folder = config["tftp-server"]["folder"]["tmp"]
        self.firmware_folder = config["tftp-server"]["folder"]["firmware"]

        self.comms_prompt_pattern = self.handler.comms_prompt_pattern
        self.ssh_config_file = self.handler.ssh_config_file

    def __getattr__(self, name):
        if self.handler and hasattr(self.handler, name):
            return getattr(self.handler, name)
        raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'")
