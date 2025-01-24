import paramiko
import socket
from functools import wraps
from modules.core import get_core


def check_port_open(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.ssh is None:
            raise Exception("SSH port is not open")
        return func(self, *args, **kwargs)

    return wrapper


class SSHBaseDriver:
    def __init__(self, device, host, auth_username, auth_password, port=22, **kwargs):
        self.core = get_core(device["family"]["name"])
        self.device = device
        self.address = host
        self.username = auth_username
        self.password = auth_password
        self.port = port
        self.ssh = None

    @check_port_open
    def send_command(self, command: str) -> str:
        print("SSH send:", command)
        self.ssh.send(f"{command}\n")
        return self._get_response()

    @check_port_open
    def _get_response(self):
        output = ""
        while True:
            try:
                part = self.ssh.recv(1024).decode("utf-8")
                output += part
            except socket.timeout:
                break

        return output

    def __enter__(self):
        cl = paramiko.SSHClient()
        cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cl.connect(
            hostname=self.address,
            username=self.username,
            password=self.password,
            look_for_keys=False,
            allow_agent=False,
        )
        self.ssh = cl.invoke_shell()
        self.ssh.settimeout(1)
        self._on_open()
        return self

    def _on_open(self):
        for command in self.core.open_sequence:
            self.send_command(command)
        return self._get_response()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ssh:
            self.ssh.close()
            self.ssh = None
