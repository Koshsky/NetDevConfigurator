import logging

from utils.environ import get_env, set_env
from utils.filesystem import find_most_recent_file
from utils.network import find_available_ip

from .com import COMBaseDriver
from .core import CoreFactory
from .mock import MockDriver
from .ssh import SSHBaseDriver

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages the connection to a network device.

    This class handles the initialization and management of the connection
    to a network device using different driver types (SSH, COM, Mock).
    It provides methods for configuring the device, retrieving information,
    and updating firmware.
    """

    def __init__(self, device: dict, connection_type: str, **driver_kwargs):
        """Initializes the ConnectionManager.

        Args:
            device: A dictionary containing device information.
            connection_type: The type of connection ("ssh", "com", or "mock").
            **driver_kwargs: Additional keyword arguments for the driver.

        Raises:
            ValueError: If the connection type is invalid.
        """
        self.core = CoreFactory.get_core(device["family"]["name"])
        self.device = device

        if driver_class := {
            "ssh": SSHBaseDriver,
            "com": COMBaseDriver,
            "mock": MockDriver,
        }.get(connection_type.lower()):
            self.driver = driver_class(
                on_open_sequence=self.core.open_sequence,
                comms_prompt_pattern=self.core.comms_prompt_pattern,
                **driver_kwargs,
            )
        else:
            raise ValueError(f"Invalid connection type: {connection_type}")

    def __enter__(self) -> "ConnectionManager":
        """Enters the context manager and establishes the connection to the device.

        Returns:
            The ConnectionManager instance.
        """
        self.driver.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits the context manager and closes the connection to the device."""
        self.driver.__exit__(exc_type, exc_val, exc_tb)

    def base_configure_192(self) -> str:
        """Configures the device with a base 192.168.3.x IP address.

        Returns:
            The output of the configuration commands.
        """
        available_ip = find_available_ip(
            "192.168.3.0/24",  # hardcode bc 192 in function name
            lambda ip: ip.packed[-1] >= 100 and ip.packed[-1] < 201,
        )
        set_env("HOST_ADDRESS", available_ip)
        return self.driver.execute(self.core.base_configure_192)

    def show_run(self) -> str:
        """Executes the 'show running-config' command.

        Returns:
            The running configuration of the device.
        """
        return self.driver.execute(self.core.show_run)

    def get_header(self) -> str:
        """Retrieves the header from the running configuration.

        Returns:
            The header of the running configuration.
        """
        config = self.show_run()
        for line in config.splitlines()[:10]:
            print(line)

        return "".join(
            line + "\n"
            for line in config.splitlines()
            if line.startswith(self.core.comment_symbol)
        )

    def update_startup_config(self) -> str:
        """Updates the startup configuration.

        Returns:
            The output of the update command.
        """
        if get_env("DEV_TYPE") == "switch":
            return self._update_startup_config_switch()
        elif get_env("DEV_TYPE") == "router":
            return self._update_startup_config_router()
        else:
            raise TypeError(f"Invalid DEV_TYPE: {get_env('DEV_TYPE')}")

    def _update_startup_config_switch(self):
        return self.driver.execute(self.core.update_startup_config)

    def _update_startup_config_router(self):
        result = self.driver.execute(self.core.update_startup_config)
        if "not parsed" in result:
            logger.error("ROLLBACK. Cannot apply candidate configuration: %s", result)
            self.driver.execute(self.core.rollback)
            return f"Cannot apply candidate configuration:\n\n{result}"
        if diff := self.driver.execute(self.core.show_diff):
            self.driver.execute(self.core.commit)
            return f"Startup config has updated successfully. Changes:\n\n{diff}"
        else:
            raise RuntimeError("No changes to apply")

    def reboot(self) -> None:
        """Reboots the device."""
        self.driver.execute(self.core.reload)

    def _load_firmware_component(self, component_type: str) -> str:
        """Updates a specific firmware component (boot, uboot, or firmware).

        Args:
            component_type: The type of the firmware component ("boot", "uboot", "firmware").

        Returns:
            The output of the update command, or an empty string if no file is found.
        """

        filename = find_most_recent_file(
            f"{get_env('TFTP_FOLDER')}/firmware",
            self.device["pattern"][component_type] or "",
        )
        if not filename:
            return ""

        set_env("FILENAME", filename)
        return self.driver.execute(getattr(self.core, f"load_{component_type}"))

    def update_firmwares(self) -> str:
        """Updates all firmware components (boot, U-Boot, firmware).

        Returns:
            The combined output of all update commands.
        """
        return (
            self._load_firmware_component("boot")
            + self._load_firmware_component("uboot")
            + self._load_firmware_component("firmware")
        )
