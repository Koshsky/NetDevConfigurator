from gui import BaseTab, apply_error_handler

from .decorators import prepare_config_file
from modules.ssh import SSHDriver


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
        if "http" in protocols:
            self.create_button_in_line(("LOAD BY HTTP", self.load_by_http))
        if "SNMP" in protocols:
            self.create_button_in_line(("LOAD BY SNMP", self.load_by_snmp))
        self.create_button_in_line(("UPDATE FIRMWARES", self.update_firmwares))
        self.create_feedback_area()

    @prepare_config_file
    def load_by_ssh(self):
        with SSHDriver(**self.app.driver) as conn:
            resp = conn.update_startup_config(conn, self.app.config_filename)
            self.display_feedback(resp)

    def load_by_COM(self):
        # TODO: первоначально: настроить vlan 1  (IMPORTANT NOT URGENT)
        # а конкретно дать ip address:
        # conf t; interface vlan 1; ip address 10.4.0.x (подходящий);
        # end; ip route 0.0.0.0 0.0.0.0 10.4.0.254   (??)
        # self.load_by_ssh()
        raise NotImplementedError("load_by_COM not implemented")

    @prepare_config_file
    def load_by_http(self):
        raise NotImplementedError("load_by_http not implemented")

    @prepare_config_file
    def load_by_snmp(self):
        raise NotImplementedError("load_by_snmp not implemented")

    def update_firmwares(self):
        # TODO: СДЕЛАТЬ ПОИСК ФАЙЛОВ ПО МАСКЕ ИЗ ТАБЛИЦЫ DEVICES (IMPORTANT NOT URGENT)
        # firmwares = self.app.db_services["device"].get_info(self.app.device)[
        #     "firmwares"``
        # ]
        raise NotImplementedError("update_firmwares not implemented")

    def show_template(self):
        self.display_feedback(self.app.text_configuration)
