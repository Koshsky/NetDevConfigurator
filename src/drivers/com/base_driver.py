import logging
from functools import wraps

import serial

from config import config

from ..core import get_core

logger = logging.getLogger("COM")


def check_port_open(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.ser.is_open:
            logger.error(
                "Attempted to call %s but the serial port is not open.", func.__name__
            )
            raise Exception("Serial port is not open")
        return func(self, *args, **kwargs)

    return wrapper


class COMBaseDriver:
    def __init__(self, device, **driver):
        self.core = get_core(device["family"]["name"])
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
        self.password = driver["auth_password"]
        self.username = driver["auth_username"]

    @check_port_open
    def send_command(self, command):
        self.ser.write(f"{command}\n".encode())
        logger.info("Send: %s", command)
        return self._get_response()

    @check_port_open
    def send_commands(self, commands):
        for command in commands:
            self.ser.write(f"{command}\n".encode())
            logger.info("Send: %s", command)
        return self._get_response()

    @check_port_open
    def _get_response(self):
        output = "\n".join(line.decode().strip() for line in self.ser.readlines())
        logger.debug(
            f"Read {len(output)} symbols. No more data to read.",
        )
        return output

    @check_port_open
    def _on_open(self):
        self.__log_in()
        self.send_commands(self.core.open_sequence)
        logger.debug(
            "On open sequence for %s was sent successfully", type(self.core).__name__
        )

    def __enter__(self):
        if self.ser.is_open:
            self.__close_port()
        try:
            self.ser.open()
        except serial.SerialException as e:
            logger.error("Serial port cannot be open: %s", e)
            raise Exception("Failed to open serial port")
        self._on_open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ser.write("exit\n".encode())
        self.__close_port()

    def __close_port(self):
        if self.ser.is_open:
            self.ser.setDTR(False)
            self.ser.setRTS(False)
            self.ser.close()

    @check_port_open
    def __is_logged(self):
        self.ser.write(b"\n\n\n\n\n\n")
        response = [line.strip() for line in self.ser.readlines()]
        return len({line.strip() for line in response[-5::]}) == 1

    @check_port_open
    def __log_in(self):
        if not self.__is_logged():
            logger.info("Logging in...")
            self.ser.write(b"\n")
            self.ser.write(f"{self.username}\n".encode())
            self.ser.write(f"{self.password}\n".encode())
            response = self._get_response()
            if self.core.success_signs.intersection(response.lower().split()):
                logger.info("Logged in successfully")
                return True
            # TODO: НЕВАЖНО ЭТО ВЫЗВАНО НЕ ТОЛЬКО WRONG CREDENTIALS
            logger.error(
                "Login error: wrong credentials. username:%s password:%s",
                self.username,
                self.password,
            )
            raise Exception(
                "Login error: wrong credentials. username:%s password:%s",
                self.username,
                self.password,
            )
        else:
            logger.info("No need to log in. Already logged in")
