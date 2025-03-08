import logging
from abc import ABC, abstractmethod
from typing import List, Any

logger = logging.getLogger("COM")


class DriverError(Exception):
    """Base class for all driver-related exceptions."""

    pass


class ConnectionError(DriverError):
    """Base class for exceptions related to connection problems."""

    pass


class AuthenticationError(DriverError):
    """Base class for exceptions related to authentication problems."""

    pass


class BaseDriver(ABC):
    """Abstract base class for device drivers."""

    @abstractmethod
    def __init__(
        self, on_open_sequence: List[str], comms_prompt_pattern: str, **driver: Any
    ):
        """Initialize the base driver.

        Args:
            on_open_sequence: List of commands to execute on connection open.
            comms_prompt_pattern: Regex pattern to match the command prompt.
            **driver: Additional driver-specific keyword arguments.
        """
        pass

    @abstractmethod
    def send_command(self, command: str) -> str:
        """Send a single command to the device.

        Args:
            command: The command to send.

        Returns:
            The device's response to the command.
        """
        pass

    def execute(self, commands: str | list) -> str:
        """Execute a single command or a list of commands.

        Args:
            commands: A single command string or a list of command strings.

        Returns:
            The combined output of all executed commands.

        Raises:
            TypeError: If the input is not a string or a list.
        """
        if isinstance(commands, str):
            return self.send_command(commands)
        elif isinstance(commands, list):
            return "".join(self.send_command(command) for command in commands)
        else:
            raise TypeError(
                f"BaseDriver.execute: argument must be str or List[str]. Given: {type(commands).__name__}"
            )

    @abstractmethod
    def __enter__(self) -> "BaseDriver":
        """Enter the driver's context manager."""
        pass

    @abstractmethod
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the driver's context manager."""
        pass
