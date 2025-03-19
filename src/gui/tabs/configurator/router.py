import logging
import os
from typing import Any, Dict, Tuple

from gui import BaseTab, apply_error_handler
from utils.environ import env_converter, set_env

logger = logging.getLogger("tab")


@apply_error_handler
class RouterTab(BaseTab):
    """Manages router-related environment variables."""

    def __init__(self, parent: Any, app: Any, log_name: str = "RouterTab") -> None:
        """Initializes the RouterTab."""
        super().__init__(parent, app, log_name)
        self.width: int = 10

    def _create_widgets(self) -> None:
        """Creates the widgets for the RouterTab."""
        self.create_block("env", {"vars": self._get_env_vars()}, width=self.width)
        self._actualize()

    def _actualize(self) -> None:
        """Actualizes the values of the environment variable fields."""
        for env_name, field in self.fields["env"]["vars"].items():
            if env_name not in os.environ:
                set_env(env_name, field.get().strip())
            field.set(env_converter.to_human(env_name, os.environ[env_name]))

    def update_config(self) -> None:
        """Updates the environment variables with the values from the fields."""
        for env_name, field in self.fields["env"]["vars"].items():
            try:
                env_value = env_converter.to_machine(env_name, field.get())
                set_env(env_name, env_value)
            except KeyError:
                logger.error(f"Incorrect value for {env_name}: {field.get()}")
        self.refresh_widgets()

    def _get_env_vars(self) -> Dict[str, Tuple[Any, ...]]:
        """Retrieves the environment variables and their possible values."""
        env_vars: Dict[str, Tuple[Any, ...]] = {
            "PUBLIC_IP": (env_converter.get_human("PUBLIC_IP"),),
            "PUBLIC_MASK": (env_converter.get_human("PUBLIC_MASK"),),
            "GW": (env_converter.get_human("GW"),),
            "VERS": tuple(env_converter["VERS"]),
        }
        if os.environ["TYPE_COMPLEX"] == "1":
            env_vars |= {
                "PH_COUNT": tuple(range(1, 26)),
                "STREAM_COUNT": tuple(range(1, 26)),
            }

        env_vars |= {
            "VPN": tuple(env_converter["VPN"]),
            "TELEPORT": tuple(env_converter["VPN"]),
            "RAISA": tuple(env_converter["VPN"]),
        }
        if os.environ["RAISA"] == "1":
            env_vars["RAISA_IP"] = (env_converter.get_human("RAISA_IP"),)
        env_vars["TRUECONF"] = tuple(env_converter["TRUECONF"])

        if os.environ["TRUECONF"] == "1":
            env_vars["TRUEROOM"] = tuple(env_converter["TRUEROOM"])

        if os.environ["TRUEROOM"] == os.environ["TRUECONF"] == "1":
            env_vars["TRUEROOM_COUNT"] = tuple(range(1, 26))
            env_vars["TRUEROOM_IP1"] = (env_converter.get_human("TRUEROOM_IP1"),)
        return env_vars
