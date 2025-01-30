import logging

from .eltex import MES11xx21xx20xx31xx, MES14xx24xx34xx37xx, MES23xx33xx35xx36xx53xx5400

logger = logging.getLogger("core")


def get_core(family: str):
    cores = {
        "MES14xx/24xx/34xx/37xx": MES14xx24xx34xx37xx(),
        "MES11xx/21xx/22xx/31xx": MES11xx21xx20xx31xx(),
        "MES23xx/33xx/35xx/36xx/53xx/5400": MES23xx33xx35xx36xx53xx5400(),
    }
    core = cores.get(family, None)
    if core is None:
        logger.error(f"Unsupported device family: {family}")
        raise ValueError(f"Unsupported device family: {family}")
    logger.info(f"Successfully retrieved core for device family: {family}")
    return core


__all__ = [
    "handle_device_open",
    "get_core",
]
