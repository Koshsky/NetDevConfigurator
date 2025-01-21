from .base_driver import COMDriverBase


class COMDriver(COMDriverBase):
    def base_configure(self):
        return self.send_commands(self.core.base_configure)
