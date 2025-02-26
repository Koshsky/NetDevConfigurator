import logging
import os
import subprocess

from utils.environ import replace_env_vars

from ..environ import check_environment_variables
from .zyxel import prepare_zyxel_environs

logger = logging.getLogger("bash")


def _save_ESR_configuration():
    SCRIPT_PATH = "./src/utils/config_esr/make_config.sh"
    logger.debug("running make_config.sh")
    config_path = os.path.join(
        os.environ["TFTP_FOLDER"], "tmp", os.environ["CFG_FILENAME"]
    )
    try:
        subprocess.run(
            ["bash", SCRIPT_PATH], check=True, text=True, capture_output=True
        )
        logger.info("Configuration saved in %s", config_path)
    except subprocess.CalledProcessError as e:
        logger.error("src.utils.get_esr_configuration: %s", e)

    with open(config_path, "r") as f:
        return f.read()


def _process_json_config(json_config, device_company) -> str:
    # Eltex switches don't need any extra processing
    #
    if device_company == "Zyxel":  # Zyxel need extra processing:
        configuration = prepare_zyxel_environs(json_config)
    # TODO: what about ARUBA switches?

    configuration = ""
    for k, v in json_config.items():
        if v["text"]:
            configuration += f"{v['text'].replace('{INTERFACE_ID}', k)}\n"

    return replace_env_vars(configuration) + "end\n"


def save_configuration(json_config) -> str:
    check_environment_variables()

    if os.environ["DEV_TYPE"] == "router":
        return _save_ESR_configuration()

    elif os.environ["DEV_TYPE"] == "switch":
        configuration = _process_json_config(json_config, os.environ["DEV_COMPANY"])

    config_path = os.path.join(
        os.environ["TFTP_FOLDER"], "tmp", os.environ["CFG_FILENAME"]
    )
    try:
        with open(config_path, "w") as f:
            f.write(configuration)
            logger.info(f"Configuration saved in {config_path}")
    except IOError as e:
        raise IOError(f"Failed to write configuration to {config_path}: {e}")
