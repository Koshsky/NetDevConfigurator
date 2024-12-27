from .handlers import (
    MES14xx24xx37xxHandler,
    MES11xx21xx31xxHandler,
    MES23xx35xxHandler,
    MES54487048Handler,
    ubuntuHandler
)

from scrapli.driver import GenericDriver


class SSHDriver(GenericDriver):
    def __init__(
        self,
        family: str,
        tftp_server: str,
        tftp_folder: str = '/srv/tftp/',
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.family = family
        self.tftp_server = tftp_server
        self.tftp_folder = tftp_folder

        handler_map = {
            "MES14xx/24xx/34xx/37xx": MES14xx24xx37xxHandler(),
            "MES11xx/21xx/22xx/31xx": MES11xx21xx31xxHandler(),
            "MES23xx/33xx/35xx/36xx/53xx/5400": MES23xx35xxHandler(),
            "MES5448/7048": MES54487048Handler(),
            "ubuntu": ubuntuHandler()
        }
        self.handler = handler_map.get(family, None)
        if self.handler is None:
            raise ValueError(f"Unsupported device family: {family}")

        self.comms_prompt_pattern = self.handler.comms_prompt_pattern
        self.ssh_config_file = self.handler.ssh_config_file

    def __getattr__(self, name):
        if self.handler and hasattr(self.handler, name):
            return getattr(self.handler, name)
        raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'")