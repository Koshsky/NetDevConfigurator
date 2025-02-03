import logging
import os

from utils.network import find_available_ip

from .base_driver import COMBaseDriver

logger = logging.getLogger("COM")


class COMDriver(COMBaseDriver):
    def base_configure_192(self):
        available_ip = find_available_ip(
            "192.168.3.0/24",  # hardcode bc 192 in function name
            lambda ip: ip.packed[-1] >= 100 and ip.packed[-1] < 201,
        )
        os.environ["HOST_ADDRESS"] = available_ip
        logger.info(
            f"Environmental variable set up: HOST_ADDRESS={os.environ['HOST_ADDRESS']}"
        )
        return self.send_commands(self.core.base_configure_192)

    def show_run(self):
        return self.send_command(self.core.show_run)
