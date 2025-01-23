from .base_driver import COMBaseDriver


class COMDriver(COMBaseDriver):
    def base_configure_192(self):
        return self.send_commands(self.core.base_configure_192)

    def show_run(self):
        return self.send_command(self.core.show_run)
