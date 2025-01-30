from config import config
from drivers import COMDriver, SSHDriver
from gui import BaseTab, apply_error_handler


from .decorators import prepare_config_file


@apply_error_handler
class HelloTab(BaseTab):
    def render_widgets(self):
        self.create_block(
            "preset",
            {
                "device": self.app.entity_collections["device"],
                "role": self.app.entity_collections["role"],
            },
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

        self.app.set_configuration_parameters(
            cert=self.fields["params"]["CERT"].get().strip(),
            OR=self.fields["params"]["OR"].get().strip(),
            device=device,
            preset=preset,
        )
