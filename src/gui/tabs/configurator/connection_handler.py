import logging
import os

from config import config
from drivers import COMDriver, SSHDriver
from utils import set_env

from ..base_tab import BaseTab

logger = logging.getLogger("gui")


class BaseConnectionHandler:
    def __init__(self, control_tab):
        self.tab = control_tab
        self.app = control_tab.app
        self.fields_config = []
        self.env_vars = []

    def create_widgets(self):
        self.tab.create_block(
            "host",
            {field: tuple(config["host"][field]) for field in self.fields_config},
            ("SELECT", self.update_host_info),
        )

    def update_host_info(self):
        for var_name, field in self.env_vars:
            if field in self.tab.fields["host"]:
                set_env(var_name, self.tab.fields["host"][field].get().strip())

    def _execute_with_driver(self, Driver, operation, *args):
        with Driver(**self.app.driver) as conn:
            method = getattr(conn, operation)
            result = method(*args)
            if operation == "show_run":
                self.tab.display_feedback(result)
            return result

    def load(self):
        raise NotImplementedError

    def reboot(self):
        self._execute_with_driver(self.driver, "reboot")

    def show_run(self):
        self._execute_with_driver(self.driver, "show_run")

    def update_firmwares(self):
        for operation in ["update_boot", "update_uboot", "update_firmware"]:
            self._execute_with_driver(self.driver, operation)


class COMSSHConnectionHandler(BaseConnectionHandler):
    def __init__(self, control_tab):
        super().__init__(control_tab)
        self.driver = COMDriver
        self.fields_config = ["username", "password"]
        self.env_vars = [("HOST_USERNAME", "username"), ("HOST_PASSWORD", "password")]

    def load(self):
        self._execute_with_driver(COMDriver, "base_configure_192")
        self._load_via_ssh()

    def _load_via_ssh(self):
        self._execute_with_driver(SSHDriver, "update_startup_config")


class SSHConnectionHandler(BaseConnectionHandler):
    def __init__(self, control_tab):
        super().__init__(control_tab)
        self.driver = SSHDriver
        self.fields_config = ["address", "port", "username", "password"]
        self.env_vars = [
            ("HOST_ADDRESS", "address"),
            ("HOST_PORT", "port"),
            ("HOST_USERNAME", "username"),
            ("HOST_PASSWORD", "password"),
        ]

    def load(self):
        self._execute_with_driver(SSHDriver, "update_startup_config")


def get_connection_handler(tab: BaseTab) -> BaseConnectionHandler:
    handlers = {
        "com+ssh": COMSSHConnectionHandler,
        "ssh": SSHConnectionHandler,
    }
    conn_type = os.environ["CONNECTION_TYPE"]
    if conn_type not in handlers:
        raise ValueError(f"Unknown connection type: {conn_type}")
    return handlers[conn_type](tab)
