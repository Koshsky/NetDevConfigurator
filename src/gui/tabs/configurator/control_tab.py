import logging
import os
from functools import wraps

from config import config
from drivers import COMDriver, SSHDriver
from gui import BaseTab, apply_error_handler
from utils import set_env, env_converter

logger = logging.getLogger("gui")


def prepare_config_file(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with SSHDriver(**self.app.driver) as conn:
            header = conn.get_header()
        configuration = header + self.app.text_configuration

        config_path = f"/srv/tftp/tmp/{os.environ['CFG_FILENAME']}"
        with open(config_path, "w") as f:
            f.write(configuration)
            logger.info("Configuration saved: %s", config_path)

        return func(self, *args, **kwargs)

    return wrapper


@apply_error_handler
class ControlTab(BaseTab):
    def _create_widgets(self):
        self._create_connection_widgets()
        self._create_device_widgets()
        self._create_action_buttons()
        self.create_feedback_area()
        self.update_host_info()

    def load(self):
        if os.environ["CONNECTION_TYPE"] == "com+ssh":
            with COMDriver(**self.app.driver) as conn:
                conn.base_configure_192()
        self.load_by_ssh()

    @prepare_config_file
    def load_by_ssh(self):
        with SSHDriver(**self.app.driver) as conn:
            resp = conn.update_startup_config()
            self.display_feedback(resp)

    def actualize(self):
        self.fields["params"]["role"].set(os.environ["DEV_ROLE"])

    def update_params(self):
        if os.environ["DEV_TYPE"] == "switch":
            self.app.register_preset(
                self.check_role_name(self.fields["params"]["role"].get())
            )
        elif os.environ["DEV_TYPE"] == "router":
            set_env(
                "TYPE_COMPLEX",
                env_converter.from_human[
                    self.fields["params"]["TYPE_COMPLEX"].get().strip()
                ],
            )
        self.app.refresh_tabs()
        self.actualize()

    def update_host_info(self):
        set_env("HOST_ADDRESS", "NO")
        set_env("HOST_PORT", "NO")

        if os.environ["CONNECTION_TYPE"] == "ssh":
            # TODO: add validation of IP address
            set_env("HOST_ADDRESS", self.fields["host"]["address"].get().strip())
            set_env("HOST_PORT", self.fields["host"]["port"].get().strip())

        set_env("HOST_PASSWORD", self.fields["host"]["password"].get().strip())
        set_env("HOST_USERNAME", self.fields["host"]["username"].get().strip())

    def reboot(self):
        with SSHDriver(**self.app.driver) as conn:
            conn.reboot()

    def update_firmwares(self):
        with SSHDriver(**self.app.driver) as conn:
            conn.update_boot()
            conn.update_uboot()
            conn.update_firmware()

    def show_template(self):
        if (
            configuration := self.app.text_configuration is None
        ):  # TODO: использовать перемемнную в дисплей.
            self.display_feedback(
                "There is no configuration. Please select device role"
            )
        else:
            self.display_feedback(self.app.text_configuration)

    def _create_connection_widgets(self):
        connection_type = os.environ["CONNECTION_TYPE"]
        if connection_type == "com+ssh":
            self._create_widgets_com()
        elif connection_type == "ssh":
            self._create_widgets_ssh()

    def _create_device_widgets(self):
        device_type = os.environ["DEV_TYPE"]
        if device_type == "switch":
            self._create_widgets_switch()
        elif device_type == "router":
            self._create_widgets_router()

    def _create_action_buttons(self):
        actions = [
            ("SHOW TEMPLATE", self.show_template),
            ("LOAD TEMPLATE", self.load),
            ("UPDATE FIRMWARES", self.update_firmwares),
            ("REBOOT DEVICE", self.reboot),
        ]
        for action in actions:
            self.create_button_in_line(action)

    def _create_widgets_com(self):
        self.create_block(
            "host",
            {
                "username": (config["host"]["username"],),
                "password": (config["host"]["password"],),
            },
            ("SELECT", self.update_host_info),
        )

    def _create_widgets_ssh(self):
        self.create_block(
            "host",
            {
                "address": (config["host"]["address"],),
                "port": (config["host"]["port"],),
                "username": (config["host"]["username"],),
                "password": (config["host"]["password"],),
            },
            ("SELECT", self.update_host_info),
        )

    def _create_widgets_switch(self):
        self.create_block(
            "params",
            {
                "role": self.app.db_services["device"].get_roles_by_name(
                    os.environ["DEV_NAME"]
                ),
                "or": tuple(str(i) for i in range(1, 26)),
            },
            ("UPDATE", self.update_params),
        )

    def _create_widgets_router(self):
        self.create_block(
            "params",
            {
                "TYPE_COMPLEX": tuple(env_converter["TYPE_COMPLEX"]),
            },
        )
