import logging
from functools import wraps
from typing import Callable
import re
import serial

from config import config

from .base_driver import BaseDriver, ConnectionError, AuthenticationError

logger = logging.getLogger("COM")


class SerialPortOpenError(ConnectionError):
    """Raised when there is an error opening the serial port."""

    pass


class LoginError(AuthenticationError):
    """Raised when there is an error logging in to the device."""

    pass


def check_port_open(func: Callable) -> Callable:
    """Decorator to check if the serial port is open before executing a function.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.

    Raises:
        SerialPortOpenError: If the serial port is not open.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.ser.is_open:
            logger.error(
                "Attempted to call %s but the serial port is not open.", func.__name__
            )
            raise SerialPortOpenError("Serial port is not open")
        return func(self, *args, **kwargs)

    return wrapper


class COMBaseDriver(BaseDriver):
    """Base driver for COM connections.

    This class provides the basic functionality for interacting with
    network devices via a serial COM port, including sending commands
    and receiving responses.
    """

    def __init__(self, on_open_sequence, comms_prompt_pattern, **driver):
        """Initializes the COMBaseDriver.

        Args:
            on_open_sequence: The sequence of commands to execute upon opening the connection.
            comms_prompt_pattern: The regex pattern to match the command prompt.
            **driver: Additional driver parameters.
        """
        self.on_open_sequence = on_open_sequence
        self.comms_prompt_pattern = comms_prompt_pattern
        self.ser = serial.Serial(
            port=config["serial-port"],
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
        )
        self.password = driver["password"]
        self.username = driver["username"]

    @check_port_open
    def send_command(self, command: str) -> str:
        """Sends a command to the serial port.

        Args:
            command: The command to send.

        Returns:
            The response from the device.
        """
        self.ser.write(f"{command}\n".encode())
        logger.info("Send: %s", command)
        return self._get_response()

    @check_port_open
    def _get_response(self) -> str:
        """Reads the response from the serial port.

        Returns:
            The response from the device.
        """
        output = "\n".join(line.decode().strip() for line in self.ser.readlines())
        logger.debug(
            f"Read {len(output)} symbols. No more data to read.",
        )
        return output

    @check_port_open
    def __is_logged(self) -> bool:
        """Checks if the user is logged in to the device.

        Returns:
            True if logged in, False otherwise.
        """
        self.ser.write(b"\n\n")
        response = [line.strip() for line in self.ser.readlines()]
        last_line = response[-1].decode("utf-8")
        return re.match(self.comms_prompt_pattern, last_line)

    def __enter__(self) -> "COMBaseDriver":
        """Enters the context manager and establishes the serial connection.

        Opens the serial port, logs in to the device, and executes
        the initial open sequence commands.

        Returns:
            The COMBaseDriver instance.

        Raises:
            SerialPortOpenError: If the serial port cannot be opened.
            Exception: If the login process fails.
        """
        if self.ser.is_open:
            self.__close_port()
        try:
            self.ser.open()
        except serial.SerialException as e:
            logger.error("Serial port cannot be open: %s", e)
            raise SerialPortOpenError("Failed to open serial port") from e
        self.__log_in()
        self.execute(self.on_open_sequence)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits the context manager and closes the serial connection.

        Sends the "exit" command and closes the serial port.
        """
        self.ser.write("exit\n".encode())
        self.__close_port()

    def __close_port(self):
        """Closes the serial port if it is open.

        Sets DTR and RTS to False before closing to ensure a clean disconnect.
        """
        if self.ser.is_open:
            self.ser.setDTR(False)
            self.ser.setRTS(False)
            self.ser.close()

    @check_port_open
    def __log_in(self):
        """Logs in to the device via the serial port.

        Sends the username and password to the device.
        Raises an exception if the login fails.
        """
        if not self.__is_logged():
            logger.info("Logging in...")

            self.ser.write(b"\n")
            self.ser.write(f"{self.username}\n".encode())
            self.ser.write(f"{self.password}\n".encode())
            if self.__is_logged():
                logger.info("Logged in successfully")
                return True
            # TODO: НЕВАЖНО ЭТО ВЫЗВАНО НЕ ТОЛЬКО WRONG CREDENTIALS (пока паттерн не учитывает conf режим.)
            logger.error(
                "Login error: wrong credentials. username:%s password:%s",
                self.username,
                self.password,
            )
            raise LoginError(
                "Login error: wrong credentials. username:%s password:%s",
                self.username,
                self.password,
            )
        else:
            logger.info("No need to log in. Already logged in")
