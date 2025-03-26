import logging
import os
import subprocess

from utils.environ import get_env

logger = logging.getLogger(__name__)


def save_ESR_configuration(header: str) -> str:
    """Saves the ESR configuration to a file and prepends a header.

    Runs the `make_config.sh` script to generate the configuration,
    then adds the provided header to the beginning of the file.

    Args:
        header: The header string to prepend to the configuration file.

    Returns:
        The complete configuration string with the header.

    Raises:
        subprocess.CalledProcessError: If the `make_config.sh` script fails.
        FileNotFoundError: If the generated configuration file is not found.
    """
    script_path = "./src/utils/config/config_esr/make_config.sh"
    config_path = os.path.join(get_env("TFTP_FOLDER"), get_env("CFG_PATH"))

    logger.debug("Running %s", script_path)
    try:
        result = subprocess.run(
            ["bash", script_path], check=True, text=True, capture_output=True
        )
        logger.debug("Script output: %s", result.stdout)
    except subprocess.CalledProcessError as e:
        logger.exception("Error generating ESR configuration: %s", e)
        raise

    try:
        with open(config_path, "r") as f:
            config = f.read()
    except FileNotFoundError:
        logger.exception("Configuration file not found at %s", config_path)
        raise

    complete_config = header + config

    with open(config_path, "w") as f:
        f.write(complete_config)
    logger.debug("Configuration saved to %s", config_path)

    return complete_config
