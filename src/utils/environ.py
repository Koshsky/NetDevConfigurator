import logging
import os
import re

logger = logging.getLogger("env")


def replace_env_vars(configuration: str) -> str:
    """Replaces environment variables placeholders in a string with their values.

    Placeholders are enclosed in curly braces, e.g., "{VAR_NAME}".

    Args:
        configuration: The string containing environment variable placeholders.

    Returns:
        The string with placeholders replaced by their environment variable values.

    Raises:
        ValueError: If any referenced environment variable is not set.
    """
    for match in re.finditer(r"{([A-Z0-9_]+)}", configuration):
        env_var = match.group(1)
        if env_var not in os.environ:
            raise ValueError(f"Missing environment variable: {env_var}")
        configuration = configuration.replace(f"{{{env_var}}}", os.environ[env_var])

    return configuration


def check_environment_variables():
    """Checks if all required environment variables are set.

    Raises:
        EnvironmentError: If a required environment variable is missing.
        ValueError: If the device company is not supported.
    """
    required_vars = {
        "CERT": None,
        "OR": None,
        "DEV_NAME": None,
        "TFTP_FOLDER": None,
        "CFG_FILENAME": None,
        "DEV_TYPE": None,
        "DEV_COMPANY": ["Zyxel", "Eltex"],
    }

    if missing_vars := [var for var in required_vars if var not in os.environ]:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    if os.environ["DEV_TYPE"] == "switch" and "DEV_ROLE" not in os.environ:
        raise EnvironmentError("Missing required environment variable: DEV_ROLE")

    if os.environ["DEV_COMPANY"] not in required_vars["DEV_COMPANY"]:
        raise ValueError(f"Unsupported device company: {os.environ['DEV_COMPANY']}")


def set_env(key: str, value: str | int) -> bool:
    """Sets an environment variable.

    Args:
        key: The name of the environment variable.
        value: The value of the environment variable.

    Returns:
        True if the environment variable was set or updated, False otherwise.
    """
    value = str(value)
    if key not in os.environ or os.environ[key] != value:
        os.environ[key] = value
        logger.info(
            f"Environmental variable {'updated' if key in os.environ else 'set up'}: {key}={value}"
        )
        return True
    return False


def del_env(key: str):
    """Deletes an environment variable.

    Args:
        key: The name of the environment variable to delete.
    """
    if key in os.environ:
        del os.environ[key]
        logger.info("Environmental variable deleted: %s", key)


class EnvConverter(dict):
    """Converts between human-readable and machine-readable environment variable values."""

    def get_human(self, env_name: str) -> str:
        """Gets the human-readable value of an environment variable.

        Args:
            env_name: The name of the environment variable.

        Returns:
            The human-readable value of the environment variable.
        """
        return self.to_human(env_name, os.environ[env_name])

    def to_machine(self, env_name: str, human_value: str) -> str:
        """Converts a human-readable value to a machine-readable value.

        Args:
            env_name: The name of the environment variable.
            human_value: The human-readable value.

        Returns:
            The machine-readable value.
        """
        return self[env_name][human_value] if env_name in self else human_value

    def to_human(self, env_name: str, machine_value: str) -> str:
        """Converts a machine-readable value to a human-readable value.

        Args:
            env_name: The name of the environment variable.
            machine_value: The machine-readable value.

        Returns:
            The human-readable value.
        """
        try:
            return next(
                (
                    key
                    for key, value in self[env_name].items()
                    if value == machine_value
                ),
                machine_value,
            )
        except KeyError:
            return machine_value


env_converter = EnvConverter(
    {
        "TYPE_COMPLEX": {
            "Standard": "1",
            "All-in-one": "2",
        },
        "MODEL": {
            "ESR20": "1",
            "ESR21": "2",
            "ESR31": "3",
            "esr20": "1",
            "esr21": "2",
            "esr31": "3",
        },
        "VERS": {"1.23 and newer": "1", "old": "2"},
        "VPN": {"YES": "1", "NO": "2"},
        "TELEPORT": {"YES": "1", "NO": "2"},
        "RAISA": {"YES": "1", "NO": "2"},
        "TRUECONF": {"YES": "1", "NO": "2"},
        "TRUEROOM": {"YES": "1", "NO": "2"},
    }
)
