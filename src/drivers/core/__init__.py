from .device_core import DeviceCore
import logging

logger = logging.getLogger("core")

from .mes import (
    MES11xx21xx20xx31xx,
    MES14xx24xx34xx37xx,
    MES23xx33xx35xx36xx53xx5400,
)
from .esr import (
    ESR2x,
    ESR3x,
)

from .zyxel import BaseZyxel
class CoreFactory:
    _devices = {
        "MES14xx/24xx/34xx/37xx": MES14xx24xx34xx37xx,
        "MES11xx/21xx/22xx/31xx": MES11xx21xx20xx31xx,
        "MES23xx/33xx/35xx/36xx/53xx/5400": MES23xx33xx35xx36xx53xx5400,
        "ESR2x": ESR2x,
        "ESR3x": ESR3x,
        "BaseZyxel": BaseZyxel,
    }

    @classmethod
    def get_core(cls, family: str) -> DeviceCore:
        device_class = cls._devices.get(family)
        if device_class is None:
            raise ValueError(f"Unsupported device family: {family}")

        device = device_class()
        logger.debug(f"Successfully created device instance for family: {family}")
        return device


__all__ = [
    "handle_device_open",
    "CoreFactory",
    "DeviceCore",
]
