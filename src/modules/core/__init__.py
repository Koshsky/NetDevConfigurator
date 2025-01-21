from .eltex import MES14xx24xx34xx37xx, MES23xx33xx35xx36xx53xx5400, MES11xx21xx20xx31xx
from scrapli.driver import GenericDriver
import logging


def get_core(family: str):
    cores = {
        "MES14xx/24xx/34xx/37xx": MES14xx24xx34xx37xx(),
        "MES11xx/21xx/22xx/31xx": MES11xx21xx20xx31xx(),
        "MES23xx/33xx/35xx/36xx/53xx/5400": MES23xx33xx35xx36xx53xx5400(),
    }
    core = cores.get(family, None)
    if core is None:
        raise ValueError(f"Unsupported device family: {family}")
    return core


def handle_device_open(cls: GenericDriver, commands):
    try:
        cls.channel.write(cls.auth_password)
        cls.channel.send_return()
        cls.send_commands(commands)
        logging.info("Successfully completed opening sequence")
    except Exception as e:
        logging.error(f"Error during opening sequence: {e}")


__all__ = [
    "handle_device_open",
    "get_core",
]
