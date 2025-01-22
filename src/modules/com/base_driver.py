import serial
from config import config

from functools import wraps

from ..core import get_core

config = config["serial"]


def check_port_open(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.ser.is_open:
            raise Exception("Serial port is not open")
        return func(self, *args, **kwargs)

    return wrapper


class COMDriverBase:
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
        return self._get_result()

    def send_commands(self, commands):
        multi_response = []
        for command in commands:
            multi_response.append(self.send_command(command))
        return "\n".join(multi_response)

    @check_port_open
    def _get_response(self):
        response = [line.decode().strip() for line in self.ser.readlines()]
        return "\n".join(response)

    @check_port_open
    def _on_open(self):
        self.__log_in()
        for command in self.core.open_sequence:
            self.ser.write(f"{command}\n".encode())
        return self._get_response()

    def __enter__(self):
        if self.ser.is_open:
            self.__close_port()
        self.ser.open()
        if not self.ser.is_open:
            raise Exception("Failed to open serial port")
        self._on_open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ser.write("exit\n".encode())
        self.__close_port()

    def __close_port(self):
        if self.ser.is_open:
            self.ser.setDTR(False)  # Сброс линии DTR
            self.ser.setRTS(False)  # Сброс линии RTS
            self.ser.close()

    @check_port_open
    def __is_logged(self):
        self.ser.write(b"\n")
        self.ser.write(b"\n")
        self.ser.write(b"\n")
        response = [line.strip() for line in self.ser.readlines()]
        return len(set(line.strip() for line in response[-3::])) == 1

    @check_port_open
    def __log_in(self):
        if not self.__is_logged():
            self.ser.write(b"\n")
            self.ser.write(f"{self.username}\n".encode())
            self.ser.write(f"{self.password}\n".encode())
            response = self._get_response()
            if self.core.success_signs.intersection(response.lower().split()):
                print("Successfully logged in")
                return True
            raise Exception(
                f"failed to log in: wrong credentials: {self.username} {self.password}"
            )
        else:
            print("already logged in")
