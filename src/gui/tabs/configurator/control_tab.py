import logging
from gui import BaseTab, apply_error_handler

from .connection_handler import get_connection_handler
from .device_handler import get_device_handler

logger = logging.getLogger("gui")


# TODO: ВАЖНО подумать над механизмом онбовления параметров device and host handlers
# перед любым действием. желательно так, чтобы лишний раз не обновлять приложение.
# если необходимо обновить преложение, не обновлять CONTROL TAB - лучшее решение????
@apply_error_handler
class ControlTab(BaseTab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_handler = None
        self.device_handler = None
        self.base_loaded = None

    def _create_widgets(self):
        self.connection_handler = get_connection_handler(self)
        self.device_handler = get_device_handler(self)

        self.connection_handler.create_widgets()
        self.device_handler.create_widgets()
        self._create_action_buttons()
        self.create_feedback_area()

        self.connection_handler.update_host_info()

    def _create_action_buttons(self):
        actions = [
            ("RUNNING CONFIG", self.connection_handler.show_run),
            ("CANDIDATE CONFIG", self.show_template),
            ("LOAD TEMPLATE", self.connection_handler.update_startup_config),
            ("UPDATE FIRMWARES", self.connection_handler.update_firmwares),
            ("REBOOT DEVICE", self.connection_handler.reboot),
        ]
        for action in actions:
            self.create_button_in_line(action)

    def show_template(self):
        self.display_feedback(self.app.text_configuration)
