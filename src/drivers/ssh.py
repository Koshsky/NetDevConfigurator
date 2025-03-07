import logging
import re
import socket
import time
from functools import wraps

import paramiko

from .base_driver import BaseDriver

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


class SSHBaseDriver(BaseDriver):
    def __init__(self, on_open_sequence, comms_prompt_pattern, **driver):
        self.on_open_sequence = on_open_sequence
        self.comms_prompt_pattern = comms_prompt_pattern
        self.address = driver["host"]
        self.username = driver["auth_username"]
        self.password = driver["auth_password"]
        self.port = 22
        self.ssh = None

    @property
    def __connection_string(self):
        return f"{self.username}:{self.password}@{self.address}:{self.port}"

    @check_port_open
    def send_command(self, command: str) -> str:
        self.ssh.send(f"{command}\n")
        logger.info("Send: %s", command)
        return self._get_response()

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
                timeout=4,
            )
            self.ssh = cl.invoke_shell()
            self.ssh.settimeout(1)
        except TimeoutError as e:
            logger.error(
                "Connection failed to %s via ssh: timed out", self.__connection_string
            )
            raise e
        except paramiko.SSHException as e:
            logger.error(
                "Connection failed to %s via ssh: %s", self.__connection_string, e
            )
            raise e
        except Exception as e:
            logger.critical("Unknown error during connection: %s (%s)", type(e), e)
            raise e
        logger.info("Successful connection to %s via ssh", self.__connection_string)
        self.execute(self.on_open_sequence)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ssh:
            self.ssh.close()
            logger.info("SSH connection closed.")
            self.ssh = None

        if exc_type is not None:
            logger.error("An exception occurred: %s", exc_val)

        return False  # Propagate the exception if one occurred
