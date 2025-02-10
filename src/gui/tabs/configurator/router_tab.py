import logging
import os

from gui import BaseTab, apply_error_handler
from utils import env_converter, set_env

logger = logging.getLogger("tab")


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
                field.set(env_converter.to_human(env_name, os.environ[env_name]))

    def update(self):
        for env_name, field in self.fields["env"]["vars"].items():
            try:
                env_value = env_converter.from_human(env_name, field.get())
            except KeyError:
                logger.error("Incorrect value for %s: %s", env_name, field.get())
            set_env(env_name, env_value)
        self.refresh_widgets()

    def __get_configuration(self):
        env_vars = {
            "PUBLIC_IP": tuple(
                [
                    env_converter.get_human("PUBLIC_IP"),
                ]
            ),
            "PUBLIC_MASK": tuple(
                [
                    env_converter.get_human("PUBLIC_MASK"),
                ]
            ),
            "GW": tuple(
                [
                    env_converter.get_human("GW"),
                ]
            ),
            "VERS": tuple(env_converter["VERS"]),
            "TYPE_COMPLEX": tuple(env_converter["TYPE_COMPLEX"]),
        }
        if os.environ["TYPE_COMPLEX"] == "1":
            env_vars.update(
                {
                    "PH_COUNT": tuple(range(1, 26)),
                    "STREAM_COUNT": tuple(range(1, 26)),
                }
            )

        env_vars.update(
            {
                "VPN": tuple(env_converter["VPN"]),
                "TELEPORT": tuple(env_converter["VPN"]),
                "RAISA": tuple(env_converter["VPN"]),
            }
        )
        if os.environ["RAISA"] == "1":
            env_vars["RAISA_IP"] = tuple(
                [
                    env_converter.get_human("RAISA_IP"),
                ]
            )
        env_vars["TRUECONF"] = tuple(env_converter["TRUECONF"])

        if os.environ["TRUECONF"] == "1":
            env_vars["TRUEROOM"] = tuple(env_converter["TRUEROOM"])

        if os.environ["TRUEROOM"] == os.environ["TRUECONF"] == "1":
            env_vars["TRUEROOM_COUNT"] = tuple(range(1, 26))

            tr_room_count = int(os.environ["TRUEROOM_COUNT"])
            for i in range(1, tr_room_count + 1):
                env_vars[f"TRUEROOM_IP{i}"] = tuple(
                    [
                        "127.0.0.1",
                    ]
                )

        return env_vars
