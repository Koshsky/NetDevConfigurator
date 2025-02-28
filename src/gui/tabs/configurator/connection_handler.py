import logging
import os

from config import config
from drivers import COMDriver, SSHDriver
from utils.environ import set_env

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
        )
        self._actualize_values()

    def _actualize_values(self):
        for var_name, field in self.env_vars:
            if field in self.tab.fields["host"] and var_name in os.environ:
                self.tab.fields["host"][field].set(os.environ[var_name])

    def update_host_info(self):
        for var_name, field in self.env_vars:
            if field in self.tab.fields["host"]:
                if set_env(var_name, self.tab.fields["host"][field].get().strip()):
                    set_env("BASE_LOADED", "false")

    def __getattr__(self, name):
        if hasattr(SSHDriver, name):

            def dynamic_method(*args):
                return self._execute_with_driver(operation=name, *args)

            return dynamic_method
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def _execute_with_driver(self, operation, Driver=SSHDriver, *args):
        self.update_host_info()

        with Driver(**self.app.driver) as conn:
            method = getattr(conn, operation)
            result = method(*args)
            if operation == "show_run":
                self.tab.display_feedback(result)
            self.tab.display_feedback(result)
            return result


class COMSSHConnectionHandler(BaseConnectionHandler):
    def __init__(self, control_tab):
        super().__init__(control_tab)
        self.fields_config = ["username", "password"]
        self.env_vars = [
            ("HOST_USERNAME", "username"),
            ("HOST_PASSWORD", "password"),
        ]

    def _execute_with_driver(self, operation, *args):
        if os.environ["BASE_LOADED"] == "false":
            super()._execute_with_driver("base_configure_192", Driver=COMDriver)
            set_env("BASE_LOADED", "true")
        return super()._execute_with_driver(operation, *args)


class SSHConnectionHandler(BaseConnectionHandler):
    def __init__(self, control_tab):
        super().__init__(control_tab)
        self.fields_config = ["address", "port", "username", "password"]
        self.env_vars = [
            ("HOST_ADDRESS", "address"),
            ("HOST_PORT", "port"),
            ("HOST_USERNAME", "username"),
            ("HOST_PASSWORD", "password"),
        ]


def get_connection_handler(tab: BaseTab) -> BaseConnectionHandler:
    handlers = {
        "com+ssh": COMSSHConnectionHandler,
        "ssh": SSHConnectionHandler,
    }
    conn_type = os.environ["CONNECTION_TYPE"]
    if conn_type not in handlers:
        raise ValueError(f"Unknown connection type: {conn_type}")
    return handlers[conn_type](tab)
