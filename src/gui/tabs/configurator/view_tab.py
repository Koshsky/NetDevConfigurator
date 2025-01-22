from gui import BaseTab, apply_error_handler

from .decorators import prepare_config_file
from modules.ssh import SSHDriver
from ssh2.exceptions import SocketRecvError


@apply_error_handler
class ViewTab(BaseTab):
    def create_widgets(self):
        self.create_button_in_line(("SHOW TEMPLATE", self.show_template))

        protocols = [
            protocol["name"]
            for protocol in self.app.db_services["device"].get_info(self.app.device)[
                "protocols"
            ]
        ]
        if "COM" in protocols:
            self.create_button_in_line(("LOAD BY COM", self.load_by_COM))
        if "ssh" in protocols:
            self.create_button_in_line(("LOAD BY SSH", self.load_by_ssh))
        self.create_button_in_line(("UPDATE FIRMWARES", self.update_firmwares))
        self.create_button_in_line(("REBOOT", self.reboot))
        self.create_feedback_area()

    @prepare_config_file
    def load_by_ssh(self):
        with SSHDriver(**self.app.driver) as conn:
            resp = conn.update_startup_config(self.app.config_filename)
            self.display_feedback(resp)

    def reboot(self):
        try:
            with SSHDriver(**self.app.driver) as conn:
                conn.reboot()
        except SocketRecvError:
            self.display_feedback("Reboot successful")

    def load_by_COM(self):
        raise NotImplementedError("load_by_COM not implemented")

    def update_firmwares(self):
        raise NotImplementedError("update_firmwares not implemented")

    def show_template(self):
        self.display_feedback(self.app.text_configuration)
