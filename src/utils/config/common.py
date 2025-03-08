import logging
import os
from typing import Dict, Any

from utils.environ import replace_env_vars, check_environment_variables
from .esr import save_ESR_configuration
from .zyxel import prepare_zyxel_environs

logger = logging.getLogger(__name__)


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

    if os.environ["DEV_TYPE"] == "router":
        logger.debug("Saving configuration for router.")
        configuration = save_ESR_configuration(header)
    elif os.environ["DEV_TYPE"] == "switch":
        logger.debug("Saving configuration for switch.")
        configuration = header + _process_json_config(
            preset["configuration"], os.environ["DEV_COMPANY"]
        )
    else:
        logger.error("Unknown device type: %s", os.environ["DEV_TYPE"])
        raise ValueError(f"Unknown device type: {os.environ['DEV_TYPE']}")

    config_path = os.path.join(
        os.environ["TFTP_FOLDER"], "tmp", os.environ["CFG_FILENAME"]
    )
    logger.debug("Saving configuration to: %s", config_path)
    try:
        with open(config_path, "w") as f:
            f.write(configuration)
            logger.info("Configuration saved to %s", config_path)
    except IOError as e:
        logger.exception("Failed to write configuration to %s: %s", config_path, e)
        raise IOError(f"Failed to write configuration to {config_path}: {e}") from e
    return configuration
