import logging
import os
import re
from typing import Any, Dict

from utils.environ import get_env

from .esr import save_ESR_configuration
from .zyxel import prepare_zyxel_environs

logger = logging.getLogger(__name__)


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
    logger.debug("Replacing environment variables in configuration:")
    for match in re.finditer(r"{([A-Z0-9_]+)}", configuration):
        env_var = match.group(1)
        logger.debug("Found placeholder for environment variable: %s", env_var)
        if not get_env(env_var):
            logger.error("Missing environment variable: %s", env_var)
            raise ValueError(f"Missing environment variable: {env_var}")
        value = get_env(env_var)
        logger.debug("Replacing placeholder with value: %s", value)
        configuration = configuration.replace(f"{{{env_var}}}", value)
    return configuration


def check_environment_variables():
    """Checks if all required environment variables are set.

    Raises:
        EnvironmentError: If a required environment variable is missing.
        ValueError: If the device company is not supported.
    """
    logger.debug("Checking environment variables...")
    required_vars = {
        "CERT": None,
        "DEV_NAME": None,
        "DEV_TYPE": ["router", "switch"],
        "TFTP_FOLDER": None,
        "CFG_PATH": None,
        "DEV_COMPANY": ["Zyxel", "Eltex"],
    }

    if missing_vars := [var for var in required_vars if not get_env(var)]:
        logger.error(
            "Missing required environment variables: %s", ", ".join(missing_vars)
        )
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    if get_env("DEV_TYPE") not in required_vars["DEV_TYPE"]:
        logger.error("Unsupported device type: %s", get_env("DEV_TYPE"))
        raise ValueError(f"Unsupported device type: {get_env('DEV_TYPE')}")

    if get_env("DEV_TYPE") == "switch":
        if not get_env("DEV_ROLE"):
            logger.error("Missing required environment variable: DEV_ROLE")
            raise EnvironmentError("Missing required environment variable: DEV_ROLE")
        if get_env("DEV_ROLE") in [
            "tsh",
            "or",
        ]:
            if not get_env("OR"):
                logger.error("Missing required environment variable: OR")
                raise EnvironmentError("Missing required environment variable: OR")
            if not get_env("OR").isdigit():
                logger.error("Environmental variable OR must be integer.")
                raise EnvironmentError("Environmental variable OR must be integer.")

    if get_env("DEV_COMPANY") not in required_vars["DEV_COMPANY"]:
        logger.error("Unsupported device company: %s", get_env("DEV_COMPANY"))
        raise ValueError(f"Unsupported device company: {get_env('DEV_COMPANY')}")

    logger.debug("All required environment variables are set.")


def _process_json_config(json_config: Dict[str, Any], device_company: str) -> str:
    """Processes the JSON configuration based on the device company.

    Args:
        json_config: The JSON configuration dictionary.
        device_company: The name of the device company.

    Returns:
        The processed configuration string.
    """
    logger.debug("Processing JSON configuration for %s", device_company)
    if device_company == "Zyxel":
        logger.debug("Applying Zyxel specific processing.")
        json_config = prepare_zyxel_environs(json_config)
    else:  # Eltex and other companies
        logger.debug("No company-specific processing required.")

    configuration = "".join(
        f"{v['text'].replace('{INTERFACE_ID}', k)}\n"
        for k, v in json_config.items()
        if v["text"]
    )
    return replace_env_vars(configuration) + "end\n"


def save_configuration(header: str = "", preset: Dict[str, Any] = None) -> str:
    """Saves the generated configuration to a file.

    Args:
        header: The header string for the configuration.
        preset: The preset dictionary containing the configuration data.

    Returns:
        The complete configuration string.

    Raises:
        IOError: If the configuration file cannot be written.
    """
    logger.debug("Saving configuration...")
    check_environment_variables()

    if get_env("DEV_TYPE") == "router":
        logger.debug("Saving configuration for router.")
        configuration = save_ESR_configuration(header)
    elif get_env("DEV_TYPE") == "switch":
        logger.debug("Saving configuration for switch.")
        configuration = header + _process_json_config(
            preset["configuration"], get_env("DEV_COMPANY")
        )
    else:
        logger.error("Unknown device type: %s", get_env("DEV_TYPE"))
        raise ValueError(f"Unknown device type: {get_env('DEV_TYPE')}")

    config_path = os.path.join(get_env("TFTP_FOLDER"), get_env("CFG_PATH"))
    logger.info("Saving configuration to: %s", config_path)
    try:
        if not os.path.exists(os.path.dirname(config_path)):
            logger.debug("Creating directory: %s", os.path.dirname(config_path))
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            logger.debug("Created directory: %s", os.path.dirname(config_path))
        with open(config_path, "w") as f:
            f.write(configuration)
            logger.info("Configuration saved to %s", config_path)
    except IOError as e:
        logger.exception("Failed to write configuration to %s: %s", config_path, e)
        raise IOError(f"Failed to write configuration to {config_path}: {e}") from e
    return configuration
