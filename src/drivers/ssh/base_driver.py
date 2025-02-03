import logging
import socket
import re
from functools import wraps
import paramiko
import time
from drivers.core import get_core

logger = logging.getLogger("ssh")


def check_port_open(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.ssh is None:
            logger.critical(
                "SSH port is not open. Please use context manager to manipulate with network device via SSH"
            )
            raise Exception("SSH port is not open")
        return func(self, *args, **kwargs)

    return wrapper


class SSHBaseDriver:
    def __init__(self, device, **driver):
        self.core = get_core(device["family"]["name"])
        self.device = device
        self.address = driver["host"]
        self.username = driver["auth_username"]
        self.password = driver["auth_password"]
        self.port = 22  # TODO: may be as parameter?
        self.ssh = None

    @property
    def __connection_string(self):
        return f"{self.username}:{self.password}@{self.address}:{self.port}"

    @check_port_open
    def send_command(self, command: str, get_response=True) -> str:
        self.ssh.send(f"{command}\n")
        logger.info(f"Send: {command}")
        return self._get_response() if get_response else None

    @check_port_open
    def send_commands(self, commands, get_response=True):
        for command in commands:
            self.ssh.send(f"{command}\n")
            logger.info(f"Send: {command}")
        return self._get_response() if get_response else None

    @check_port_open
    def _get_response(self):
        output = ""

        while True:
            try:
                time.sleep(0.2)
                part = self.ssh.recv(1024).decode("utf-8")
                output += part

                last_line = output.strip().splitlines()[-1] if output.strip() else ""

                if re.match(self.core.comms_prompt_pattern, last_line):
                    logger.debug(f"The last line matches the pattern: '{last_line}'")
                    break
                else:
                    logger.debug(
                        f"The last line does not match the pattern: '{last_line}'"
                    )

            except socket.timeout:
                logger.warning("Socket timeout occurred.")
                continue
        return output

    def __enter__(self):
        try:
            cl = paramiko.SSHClient()
            cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            cl.connect(
                hostname=self.address,
                port=self.port,
                username=self.username,
                password=self.password,
                look_for_keys=False,
                allow_agent=False,
                timeout=2,
            )
            self.ssh = cl.invoke_shell()
            self.ssh.settimeout(1)
        except TimeoutError as e:
            logger.error(
                f"Connection failed to {self.__connection_string} via ssh: timed out"
            )
            raise e
        except paramiko.SSHException as e:
            logger.error(
                f"Connection failed to {self.__connection_string} via ssh: {e}"
            )
            raise e
        except Exception as e:
            logger.critical(f"Unknown error during connection: {type(e)} ({e})")
            raise e
        logger.info(f"Successful connection to {self.__connection_string} via ssh")
        self._on_open()
        return self

    def _on_open(self):
        return self.send_commands(self.core.open_sequence)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ssh:
            self.ssh.close()
            logger.info("SSH connection closed.")
            self.ssh = None

        if exc_type is not None:
            logger.error("An exception occurred: %s", exc_val)

        return False  # Propagate the exception if one occurred
