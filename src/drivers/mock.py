import logging
from typing import Any, List

from .base_driver import BaseDriver

logger = logging.getLogger("mock")


class MockDriver(BaseDriver):
    """Mock driver for testing purposes."""

    def __init__(
        self, on_open_sequence: List[str], comms_prompt_pattern: str, **driver: Any
    ) -> None:
        """Initialize MockDriver.

        Args:
            on_open_sequence: List of commands to execute on open.
            comms_prompt_pattern: Pattern for the command prompt.
            **driver: Additional driver arguments.
        """
        self.on_open_sequence = on_open_sequence
        self.comms_prompt_pattern = comms_prompt_pattern

    def send_command(self, command: str) -> str:
        """Simulate sending a command.

        Args:
            command: The command to send.

        Returns:
            A mocked response string.
        """
        logger.info("Send: %s", command)
        return f"<resp>{command}<@resp>\n"

    def send_commands(self, commands: List[str]) -> str:
        """Simulate sending multiple commands.

        Args:
            commands: The list of commands to send.

        Returns:
            A mocked response string.
        """

        return "".join(self.send_command(command) for command in commands)

    def __enter__(self) -> "MockDriver":
        """Enters the context manager and simulates connection opening.

        Returns:
            The MockDriver instance.
        """
        self.send_commands(self.on_open_sequence)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exits the context manager and simulates connection closing."""
