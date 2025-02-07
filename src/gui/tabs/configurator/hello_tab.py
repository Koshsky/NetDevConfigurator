import logging

from config import config
from gui import BaseTab, apply_error_handler


logger = logging.getLogger("gui")


@apply_error_handler
class HelloTab(BaseTab):
    def render_widgets(self):
        self.create_block(
            "device",
            {
                "name": self.app.entity_collections["device"],
            },
        )
        self.create_block(
            "common",
            {
                "CERT": (config["default-cert"],),
            },
        )

        self.create_button_in_line(("COM+SSH", lambda: self.prepare("com+ssh")))
        self.create_button_in_line(("SSH", lambda: self.prepare("ssh")))

    def prepare(self, mode):
        self.register_device()
        self.app.mode = mode
        self.app.refresh_tabs()

    def register_device(self):
        device = self.check_device_name(self.fields["device"]["name"].get())
        self.app.device = device
        logger.info("Device selected. device=%s", device.name)

        self.app.config_params["CERT"] = self.fields["common"]["CERT"].get().strip()
