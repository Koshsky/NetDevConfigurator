import logging
import os

from config import config, env_converter, set_env
from gui import BaseTab, apply_error_handler

logger = logging.getLogger("tab")


# TODO: наполнить этот класс ЛОГИКОЙ. КОРРЕКТНОЙ
@apply_error_handler
class RouterTab(BaseTab):
    def __init__(
        self,
        parent,
        app,
        log_name="RouterTab",
    ):
        super().__init__(parent, app, log_name)
        self.width = 10

    def render_widgets(self):
        self.create_block(
            "env",
            {
                "vars": self.__get_configuration(),
            },
            width=self.width,
        )
        self.create_button_in_line(("UPDATE", self.update))
        self.create_feedback_area()
        self.actualize()

    def actualize(self):
        for env_name, field in self.fields["env"]["vars"].items():
            if env_name.startswith("TRUEROOM_IP") and env_name not in os.environ:
                field.set("MUST BE SET")
            else:
                field.set(os.environ[env_name])

    def update(self):
        for env_name, field in self.fields["env"]["vars"].items():
            env_value = field.get()
            set_env(env_name, env_value)
        self.refresh_widgets()

    def __get_configuration(self):
        env_vars = {
            "PUBLIC_IP": tuple(["1", "2"]),
            "PUBLIC_MASK": tuple(["1", "2"]),
            "GW": tuple(["1", "2"]),
            "VERS": tuple(["1", "2"]),
            "TYPE_COMPLEX": tuple(["1", "2"]),
        }

        if os.environ.get("TYPE_COMPLEX") == "1":
            env_vars.update(
                {
                    "PH_COUNT": tuple(["1", "2"]),
                    "STREAM_COUNT": tuple(["1", "2"]),
                }
            )

        env_vars.update(
            {
                "VPN": tuple(["1", "2"]),
                "TELEPORT": tuple(["1", "2"]),
                "RAISA": tuple(["1", "2"]),
            }
        )
        if os.environ.get("RAISA") == "1":
            env_vars["RAISA_IP"] = tuple(["1", "2"])
        env_vars["TRUECONF"] = tuple(["1", "2"])

        if os.environ.get("TRUECONF") == "1":
            env_vars.update(
                {
                    "TRUEROOM": tuple(["1", "2"]),
                }
            )

        if os.environ.get("TRUEROOM") == "1":
            env_vars.update(
                {
                    "TRUEROOM_COUNT": tuple(range(1, 26)),
                }
            )

            tr_room_count = int(os.environ["TRUEROOM_COUNT"])
            for i in range(1, tr_room_count + 1):
                env_vars[f"TRUEROOM_IP{i}"] = tuple(["1", "2"])

        return env_vars
