import logging
import os
from functools import wraps

from config import config
from drivers import COMDriver, SSHDriver
from gui import BaseTab, apply_error_handler
from utils import env_converter, set_env

logger = logging.getLogger("gui")


def prepare_config_file(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with SSHDriver(**self.app.driver) as conn:
            header = conn.get_header()
        configuration = header + self.app.text_configuration

        config_path = f"/srv/tftp/tmp/{self.app.config_filename}"
        with open(config_path, "w") as f:
            f.write(configuration)
            logger.info("Configuration saved: %s", config_path)

        return func(self, *args, **kwargs)

    return wrapper


@apply_error_handler
class ControlTab(BaseTab):
    def render_widgets(self):
        if os.environ["MODE"] == "com+ssh":
            self.__render_widgets_com()
        elif os.environ["MODE"] == "ssh":
            self.__render_widgets_ssh()

        if self.app.device.dev_type == "switch":
            self.__render_widgets_switch()
        elif self.app.device.dev_type == "router":
            self.__render_widgets_router()

        self.create_button_in_line(("SHOW TEMPLATE", self.show_template))
        self.create_button_in_line(("LOAD TEMPLATE", self.load))
        self.create_button_in_line(("UPDATE FIRMWARES", self.update_firmwares))
        self.create_button_in_line(("REBOOT DEVICE", self.reboot))
        self.create_feedback_area()
        self.update_host_info()

    def load(self):
        if os.environ["MODE"] == "com+ssh":
            with COMDriver(**self.app.driver) as conn:
                conn.base_configure_192()
        self._load_by_ssh()

    @prepare_config_file
    def _load_by_ssh(self):
        with SSHDriver(**self.app.driver) as conn:
            resp = conn.update_startup_config(self.app.config_filename)
            self.display_feedback(resp)

    def __render_widgets_com(self):
        self.create_block(
            "host",
            {
                "username": (config["host"]["username"],),
                "password": (config["host"]["password"],),
            },
            ("SELECT", self.update_host_info),
        )

    def __render_widgets_ssh(self):
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

    def __render_widgets_switch(self):
        self.create_block(
            "params",
            {
                "role": self.app.entity_collections["role"],
                "or": tuple(str(i) for i in range(1, 26)),
            },
            ("UPDATE", self.update_params),
        )

    def __render_widgets_router(self):
        pass
        # self.create_block(
        #     "params",
        #     {
        #         "TYPE_COMPLEX": tuple(env_converter["TYPE_COMPLEX"]),
        #     }
        #     if not self.app.advanced_mode
        #     else {
        #         "TYPE_COMPLEX": tuple(env_converter["TYPE_COMPLEX"]),
        #         "TRUEROOM_COUNT": tuple(map(str, range(25))),
        #     },
        #     ("UPDATE", self.update_params),
        # )

    def update_params(self):
        if self.app.device.dev_type == "switch":
            role = self.check_role_name(self.fields["params"]["role"].get())
            preset = self.app.db_services["preset"].get_by_device_and_role(
                self.app.device, role
            )
            self.app.register_preset(preset)
        elif self.app.device.dev_type == "router":
            type_complex = self.fields["params"]["TYPE_COMPLEX"].get().strip()
            set_env("TYPE_COMPLEX", env_converter["TYPE_COMPLEX"][type_complex])
            trueroom_count = (
                self.fields["params"]["TRUEROOM_COUNT"].get().strip()
                if self.app.advanced_mode
                else 1
            )
            set_env("TRUEROOM_COUNT", trueroom_count)
        self.app.refresh_tabs()

    def update_host_info(self):
        set_env("HOST_ADDRESS", "NO")
        set_env("HOST_PORT", "NO")

        if os.environ["MODE"] == "ssh":
            # TODO: add validation of ip address
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
        self.display_feedback(self.app.text_configuration)
