from .base_driver import COMDriverBase, check_port_open


class COMDriver(COMDriverBase):
    @check_port_open
    def base_configure(self):
        for command in self.core.base_configure:
            self.ser.write(f"{command}\n".encode())
