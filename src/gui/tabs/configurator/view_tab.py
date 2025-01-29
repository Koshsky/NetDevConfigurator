from gui import BaseTab, apply_error_handler

from .decorators import prepare_config_file
from drivers import SSHDriver, COMDriver


@apply_error_handler
class ViewTab(BaseTab):
    def refresh_widgets(self):
        super().refresh_widgets()
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
            print(conn.update_boot())
            print(conn.update_uboot())
            print(conn.update_firmware())

    def show_template(self):
        self.display_feedback(self.app.text_configuration)
