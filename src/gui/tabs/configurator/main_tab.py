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
class HelloTab(BaseTab):
    def render_widgets(self):
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
        self.create_block(
            "preset",
            {
                "device": self.app.entity_collections["device"],
                "role": self.app.entity_collections["role"],
            },
            ("SELECT", self.register_preset),
        )
        self.create_block(
            "params",
            {
                "CERT": (config["default-cert"],),
                "OR": tuple(str(i) for i in range(1, 26)),
            },
        )
        self.register_preset()

        self.create_button_in_line(("SHOW TEMPLATE", self.show_template))
        self.create_button_in_line(("LOAD BY COM+SSH", self.load_by_COM))
        self.create_button_in_line(("LOAD BY SSH", self.load_by_ssh))
        self.create_button_in_line(("UPDATE FIRMWARES", self.update_firmwares))
        self.create_button_in_line(("REBOOT", self.reboot))
        self.create_feedback_area()
        self.update_host_info()

    def update_host_info(self):
        os.environ["HOST_ADDRESS"] = self.fields["host"]["address"].get().strip()
        os.environ["HOST_PORT"] = self.fields["host"]["port"].get().strip()
        os.environ["HOST_PASSWORD"] = self.fields["host"]["password"].get().strip()
        os.environ["HOST_USERNAME"] = self.fields["host"]["username"].get().strip()
        logger.info(
            "Environmental variables set up: HOST_ADDRESS=%s, HOST_PORT=%s, HOST_USERNAME=%s, HOST_PASSWORD=%s",
            os.environ["HOST_ADDRESS"],
            os.environ["HOST_PORT"],
            os.environ["HOST_USERNAME"],
            os.environ["HOST_PASSWORD"],
        )

    @prepare_config_file
    def load_by_ssh(self):
        with SSHDriver(**self.app.driver) as conn:
            resp = conn.update_startup_config(self.app.config_filename)
            self.display_feedback(resp)

    def load_by_COM(self):
        with COMDriver(**self.app.driver) as conn:
            conn.base_configure_192()
        self.load_by_ssh()

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

    def register_preset(self):
        device = self.check_device_name(self.fields["preset"]["device"].get())
        role = self.check_role_name(self.fields["preset"]["role"].get())
        preset = self.app.db_services["preset"].get_by_device_and_role(device, role)
        preset_info = self.app.db_services["preset"].get_info(preset)
        logger.info(
            "Preset selected. device=%s, role=%s, family=%s",
            preset_info["target"],
            preset_info["role"],
            preset_info["family"],
        )

        self.app.set_configuration_parameters(
            cert=self.fields["params"]["CERT"].get().strip(),
            OR=self.fields["params"]["OR"].get().strip(),
            device=device,
            preset=preset,
        )
