import logging
import re
import socket
import time
from functools import wraps
from typing import Any, List

import paramiko

from .base_driver import BaseDriver, ConnectionError

logger = logging.getLogger("ssh")


class SSHPortOpenError(ConnectionError):
    """Raised when attempting to interact with an unopened SSH connection."""

    pass


def check_port_open(func: callable) -> callable:
    """Decorator to check if the SSH port is open before executing a function.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.

    Raises:
        Exception: If the SSH port is not open.
    """

    @wraps(func)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        if self.ssh is None:
            logger.critical(
                "SSH port is not open. Please use context manager to manipulate with network device via SSH"
            )
            raise SSHPortOpenError("SSH port is not open")
        return func(self, *args, **kwargs)

    return wrapper


class SSHBaseDriver(BaseDriver):
    """Base driver for SSH connections.

    This class provides the basic functionality for interacting with
    network devices via SSH, including sending commands and receiving responses.
    """

    def __init__(
        self, on_open_sequence: List[str], comms_prompt_pattern: str, **driver: Any
    ) -> None:
        """Initializes the SSHBaseDriver.

        Args:
            on_open_sequence (str): The sequence of commands to execute upon opening the connection.
            comms_prompt_pattern (str): The regex pattern to match the command prompt.
            **driver (dict): Additional driver parameters.
        """
        self.on_open_sequence = on_open_sequence
        self.comms_prompt_pattern = comms_prompt_pattern
        self.address = driver["host"]
        self.username = driver["auth_username"]
        self.password = driver["auth_password"]
        self.port = 22
        self.ssh = None

    @property
    def __connection_string(self) -> str:
        """Returns the connection string."""
        return f"{self.username}:{self.password}@{self.address}:{self.port}"

    @check_port_open
    def send_command(self, command: str) -> str:
        """Sends a command to the SSH server.

        Args:
            command: The command to send.

        Returns:
            The response from the server.
        """
        self.ssh.send(f"{command}\n")
        logger.info("Send: %s", command)
        return self._get_response()

    @check_port_open
    def _get_response(self) -> str:
        """Gets the response from the SSH server.

        Returns:
            The response from the server.
        """
        output = ""

        while True:
            try:
                time.sleep(0.2)
                part = self.ssh.recv(1024).decode("utf-8")
                output += part

                last_line = output.strip().splitlines()[-1] if output.strip() else ""

                if re.match(self.core.comms_prompt_pattern, last_line):
                    logger.debug("The last line matches the pattern: '%s'", last_line)
                    break
                else:
                    logger.debug(
                        "The last line does not match the pattern: '%s'", last_line
                    )

            except socket.timeout:
                logger.debug("Socket timeout occurred.")
                continue
        return "\n".join(output.split("\n")[1:-1])

    def __enter__(self) -> "SSHBaseDriver":
        """Enters the context manager and establishes the SSH connection.

        Returns:
            The SSHBaseDriver instance.

        Raises:
            TimeoutError: If the connection times out.
            paramiko.SSHException: If there is an SSH error.
            Exception: For any other connection error.
        """
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=self.address,
                port=self.port,
                username=self.username,
                password=self.password,
                look_for_keys=False,
                allow_agent=False,
                timeout=4,
            )
            self.ssh = client.invoke_shell()
            self.ssh.settimeout(1)
            logger.info("Successful connection to %s via ssh", self.__connection_string)
            self.execute(self.on_open_sequence)
            return self
        except TimeoutError as e:
            logger.error(
                f"Connection to {self.__connection_string} via ssh timed out: {e}"
            )
            raise
        except paramiko.SSHException as e:
            logger.error(f"SSH connection to {self.__connection_string} failed: {e}")
            raise
        except Exception as e:
            logger.critical(
                f"Unknown error during connection to {self.__connection_string}: {type(e)}: {e}"
            )
            raise

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exits the context manager and closes the SSH connection.

        Closes the SSH connection and logs any exceptions that occurred.
        """
        if self.ssh:
            self.ssh.close()
            logger.info("SSH connection closed.")
            self.ssh = None

        if exc_type is not None:
            logger.error("An exception occurred: %s", exc_val)
