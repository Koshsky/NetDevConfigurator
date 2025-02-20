import logging
import os
from functools import wraps
from config import config
from drivers import COMDriver, SSHDriver
from utils import set_env

logger = logging.getLogger("gui")


def prepare_config_file(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with SSHDriver(**self.app.driver) as conn:
            header = conn.get_header()
        config_path = f"/srv/tftp/tmp/{os.environ['CFG_FILENAME']}"

        with open(config_path, "w") as f:
            f.write(header + self.app.text_configuration)
            logger.info("Configuration saved: %s", config_path)

        return func(self, *args, **kwargs)

    return wrapper


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

    @prepare_config_file
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

    @prepare_config_file
    def load(self):
        self._execute_with_driver(SSHDriver, "update_startup_config")
