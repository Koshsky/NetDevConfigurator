import logging
import os
from functools import wraps

from config import config
from drivers import COMDriver, SSHDriver
from gui import BaseTab, apply_error_handler


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
            logger.info(f"Configuration saved: {config_path}")

        return func(self, *args, **kwargs)

    return wrapper


@apply_error_handler
class ControlTab(BaseTab):
    def render_widgets(self):
        if self.app.mode == "com+ssh":
            self.__render_widgets_com()
        elif self.app.mode == "ssh":
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
        if self.app.mode == "com+ssh":
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
        )

    def __render_widgets_router(self):
        self.create_block(
            "params",
            {
                "TYPE_COMPLEX": ("1", "2"),
            },
        )

    def update_host_info(self):
        if self.app.mode == "ssh":
            os.environ["HOST_ADDRESS"] = self.fields["host"]["address"].get().strip()
            logger.info(
                "Environmental variable set up: HOST_ADDRESS=%s",
                os.environ["HOST_ADDRESS"],
            )
            os.environ["HOST_PORT"] = self.fields["host"]["port"].get().strip()
            logger.info(
                "Environmental variable set up: HOST_PORT=%s",
                os.environ["HOST_PORT"],
            )
        os.environ["HOST_PASSWORD"] = self.fields["host"]["password"].get().strip()
        logger.info(
            "Environmental variables set up: HOST_PASSWORD=%s",
            os.environ["HOST_PASSWORD"],
        )
        os.environ["HOST_USERNAME"] = self.fields["host"]["username"].get().strip()
        logger.info(
            "Environmental variables set up: HOST_USERNAME=%s",
            os.environ["HOST_USERNAME"],
        )

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
