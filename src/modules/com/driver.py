from config import config


from .base_driver import COMDriverBase, check_port_open

config = config["serial"]


class COMDriver(COMDriverBase):
    @check_port_open
    def show_run(self):
        self.ser.write(f"{self.core.show_run}\n".encode())
        return self._get_response()

    @check_port_open
    def set_up(self):
        pass
        # TODO: первоначально: настроить vlan 1  (IMPORTANT NOT URGENT)
        # а конкретно дать ip address:
        # conf t; interface vlan 1; ip address 10.4.0.x (подходящий);
        # end; ip route 0.0.0.0 0.0.0.0 10.4.0.254   (??)
        # self.load_by_ssh()
