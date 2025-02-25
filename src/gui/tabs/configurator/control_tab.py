import logging

from gui import BaseTab, apply_error_handler

from .connection_handler import get_connection_handler
from .device_handler import get_device_handler

logger = logging.getLogger("gui")


@apply_error_handler
class ControlTab(BaseTab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("init control tab")
        self.connection_handler = None
        self.device_handler = None
        print("init control tab")

    def _create_widgets(self):
        self.connection_handler = get_connection_handler(self)
        self.device_handler = get_device_handler(self)

        self.connection_handler.create_widgets()
        self.device_handler.create_widgets()
        self._create_action_buttons()
        self.create_feedback_area()

        self.connection_handler.update_host_info()
        self.device_handler.update_params()
        self.app.prepare_configuration()

    def _create_action_buttons(self):
        actions = [
            ("SHOW TEMPLATE", self.show_template),
            ("LOAD TEMPLATE", self.connection_handler.load),
            ("UPDATE FIRMWARES", self.connection_handler.update_firmwares),
            ("REBOOT DEVICE", self.connection_handler.reboot),
            ("SHOW RUN", self.connection_handler.show_run),
        ]
        for action in actions:
            self.create_button_in_line(action)

    def show_template(self):
        if self.app.text_configuration is None:
            self.display_feedback(
                "There is no configuration. Please select device role"
            )
        else:
            self.display_feedback(self.app.text_configuration)
