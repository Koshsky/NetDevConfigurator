from gui import BaseTab, apply_error_handler
import os

from modules.ssh import SSHDriver
from .decorators import prepare_config_file, update_driver


@apply_error_handler
class ViewTab(BaseTab):
    def create_widgets(self):
        self.create_block(
            "host",
            {
                "IP": ("10.3.1.13",),
                "port": ("22",),
            },
        )
        self.create_block(
            "credentials",
            {
                "username": ("mvsadmin",),
                "password": ("MVS_admin", None),
            },
        )
        self.create_button_in_line(("SHOW TEMPLATE", self.show_template))

        protocols = [
            protocol["name"]
            for protocol in self.app.db_services["device"].get_info(self.app._device)[
                "protocols"
            ]
        ]
        if "COM" in protocols:
            self.create_button_in_line(("LOAD BY COM", self.load_by_COM))
        if "ssh" in protocols:
            self.create_button_in_line(("LOAD BY SSH", self.load_by_ssh))
        if "http" in protocols:
            self.create_button_in_line(("LOAD BY HTTP", self.load_by_http))
        if "SNMP" in protocols:
            self.create_button_in_line(("LOAD BY SNMP", self.load_by_snmp))
        self.create_button_in_line(("UPDATE FIRMWARES", self.update_firmwares))
        self.create_feedback_area()

    @update_driver("ssh2")
    @prepare_config_file
    def load_by_ssh(self):
        with SSHDriver(**self.driver) as ssh:
            resp = ssh.tftp_send(ssh, self.app.config_path)
            print(resp.result)

    @prepare_config_file
    @update_driver
    def load_by_http(self):
        pass

    @prepare_config_file
    @update_driver
    def load_by_COM(self):
        pass

    @prepare_config_file
    @update_driver
    def load_by_snmp(self):
        pass

    def update_firmwares(self):
        firmwares = self.app.db_services["device"].get_info(self.app._device)[
            "firmwares"
        ]
        for firmware in firmwares:
            path = firmware["full_path"]
            if not os.path.exists(path):
                raise Exception(f"File {path} not found")
        pass
        pass
        pass

    def show_template(self):
        template = self._get_text_configuration()
        self.display_feedback(template)

    def _get_text_configuration(self):
        template = ""
        for k, v in self.app.device_configuration.items():
            if v["text"]:
                template += v["text"].replace("{INTERFACE_ID}", k) + "\n"
        template = template.replace("{CERT}", self.app.params["CERT"])
        template = template.replace("{OR}", self.app.params["OR"])
        template = template.replace("{MODEL}", self.app.params["MODEL"])
        template = template.replace("{ROLE}", self.app.params["ROLE"])
        return template + "end\n"
