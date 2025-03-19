import logging
from dataclasses import dataclass, field
from typing import Dict

from .environ import get_env

logger = logging.getLogger("config")


@dataclass
class RouterConversion:
    """Конвертация значений роутера."""

    model_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "ESR20": "1",
            "ESR21": "2",
            "ESR31": "3",
            "esr20": "1",
            "esr21": "2",
            "esr31": "3",
        }
    )
    type_complex_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "Standard": "1",
            "All-in-one": "2",
        }
    )
    vers_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "1.23 and newer": "1",
            "old": "2",
        }
    )
    vpn_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "YES": "1",
            "NO": "2",
        }
    )
    teleport_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "YES": "1",
            "NO": "2",
        }
    )
    raisa_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "YES": "1",
            "NO": "2",
        }
    )
    trueconf_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "YES": "1",
            "NO": "2",
        }
    )
    trueroom_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "YES": "1",
            "NO": "2",
        }
    )

    def __getitem__(self, key: str) -> Dict[str, str]:
        """Get the conversion dictionary for a given environment variable.

        Args:
            key: The name of the environment variable.

        Returns:
            The conversion dictionary for the environment variable.

        Raises:
            KeyError: If no conversion dictionary is found for the environment variable.
        """
        conversion_map = {
            "MODEL": self.model_conversion,
            "TYPE_COMPLEX": self.type_complex_conversion,
            "VERS": self.vers_conversion,
            "VPN": self.vpn_conversion,
            "TELEPORT": self.teleport_conversion,
            "RAISA": self.raisa_conversion,
            "TRUECONF": self.trueconf_conversion,
            "TRUEROOM": self.trueroom_conversion,
        }
        if key not in conversion_map:
            raise KeyError(f"No conversion found for {key}")
        return conversion_map[key]

    def get(self, key: str, default: Dict[str, str] = None) -> Dict[str, str]:
        """Get the conversion dictionary for a given environment variable.

        Args:
            key: The name of the environment variable.
            default: The default value to return if no conversion is found.

        Returns:
            The conversion dictionary for the environment variable or the default value.
        """
        try:
            return self[key]
        except KeyError:
            return default if default is not None else {}

    def get_human(self, env_name: str) -> str:
        """Gets the human-readable value of an environment variable.

        Args:
            env_name: The name of the environment variable.

        Returns:
            The human-readable value of the environment variable.
        """
        logger.debug("Getting human-readable value for %s", env_name)
        try:
            machine_value = get_env(env_name)
            human_value = self.to_human(env_name, machine_value)
            logger.debug(f"Human-readable value for {env_name}: {human_value}")
            return human_value
        except KeyError:
            logger.warning(f"Environment variable not found: {env_name}")
            return ""

    def to_machine(self, env_name: str, human_value: str) -> str:
        """Converts a human-readable value to a machine-readable value.

        Args:
            env_name: The name of the environment variable.
            human_value: The human-readable value.

        Returns:
            The machine-readable value.
        """
        logger.debug(
            "Converting human-readable value '%s' to machine-readable for %s",
            human_value,
            env_name,
        )
        machine_value = self.get(env_name, {}).get(human_value, human_value)
        logger.debug(f"Machine-readable value for {env_name}: {machine_value}")
        return machine_value

    def to_human(self, env_name: str, machine_value: str) -> str:
        """Converts a machine-readable value to a human-readable value.

        Args:
            env_name: The name of the environment variable.
            machine_value: The machine-readable value.

        Returns:
            The human-readable value, or the original value if no conversion is found.
        """
        logger.debug(
            "Converting machine-readable value '%s' to human-readable for %s",
            machine_value,
            env_name,
        )

        try:
            human_value = next(
                (
                    key
                    for key, value in self[env_name].items()
                    if value == machine_value
                ),
                machine_value,
            )
            logger.debug(f"Human-readable value for {env_name}: {human_value}")
            return human_value
        except KeyError:
            logger.warning(
                f"No conversion found for {env_name} with value {machine_value}"
            )
            return machine_value


env_converter = RouterConversion()
