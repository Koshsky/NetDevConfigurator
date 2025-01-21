from .base_driver import SSHDriverBase


class SSHDriver(SSHDriverBase):
    def show_run(self):
        return self.send_command(self.core.show_run).result

    def show_bootvar(self):
        return self.send_command(self.core.show_bootvar).result
