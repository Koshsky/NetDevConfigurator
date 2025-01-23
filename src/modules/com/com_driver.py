from .base_driver import COMBaseDriver


class COMDriver(COMBaseDriver):
    def base_configure(self):
        return self.send_commands(self.core.base_configure)

    def show_run(self):
        return self.send_command(self.core.show_run)
