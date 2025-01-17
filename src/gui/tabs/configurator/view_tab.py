from gui import BaseTab, apply_error_handler

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
            resp = ssh.update_startup_config(ssh, self.app.config_filename)
            print(resp.result)

    def load_by_COM(self):
        # TODO: первоначально: настроить vlan 1
        # а конкретно дать ip address:
        # conf t; interface vlan 1; ip address 10.4.0.x (подходящий);   // TODO: реализовать это как метод SSHDriver?
        # end; ip route 0.0.0.0 0.0.0.0 10.4.0.254   (??)
        # self.load_by_ssh()
        pass

    @prepare_config_file
    @update_driver
    def load_by_http(self):
        pass

    @prepare_config_file
    @update_driver
    def load_by_snmp(self):
        pass

    def update_firmwares(self):
        # TODO: СДЕЛАТЬ ПОИСК ФАЙЛОВ ПО МАСКЕ ИЗ ТАБЛИЦЫ DEVICES
        # firmwares = self.app.db_services["device"].get_info(self.app._device)[
        #     "firmwares"
        # ]
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
