import logging
import os

from gui import BaseTab, apply_error_handler

from .device_handler import (
    BaseDeviceHandler,
    SwitchHandler,
    RouterHandler,
)
from .connection_handler import (
    BaseConnectionHandler,
    COMSSHConnectionHandler,
    SSHConnectionHandler,
)

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
        self.connection_handler = self._get_connection_handler()
        self.device_handler = self._get_device_handler()

        self.connection_handler.create_widgets()
        self.device_handler.create_widgets()
        self._create_action_buttons()
        self.create_feedback_area()

        self.connection_handler.update_host_info()
        self.device_handler.update_params()

    def _get_connection_handler(self) -> BaseConnectionHandler:
        handlers = {
            "com+ssh": COMSSHConnectionHandler,
            "ssh": SSHConnectionHandler,
        }
        conn_type = os.environ["CONNECTION_TYPE"]
        if conn_type not in handlers:
            raise ValueError(f"Unknown connection type: {conn_type}")
        return handlers[conn_type](self)

    def _get_device_handler(self) -> BaseDeviceHandler:
        handlers = {
            "switch": SwitchHandler,
            "router": RouterHandler,
        }
        device_type = os.environ["DEV_TYPE"]
        if device_type not in handlers:
            raise ValueError(f"Unknown device type: {device_type}")
        return handlers[device_type](self)

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
        # TODO: move self.app.text_configuration to DeviceHandlers
        if (configuration := self.app.text_configuration) is None:
            self.display_feedback(
                "There is no configuration. Please select device role"
            )
        else:
            self.display_feedback(configuration)
