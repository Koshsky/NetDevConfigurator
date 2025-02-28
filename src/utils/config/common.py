import logging
import os

from utils.environ import replace_env_vars

from ..environ import check_environment_variables
from .esr import save_ESR_configuration
from .zyxel import prepare_zyxel_environs

logger = logging.getLogger("bash")


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


def save_configuration(header, json_config) -> str:
    check_environment_variables()

    if os.environ["DEV_TYPE"] == "router":
        return save_ESR_configuration()

    elif os.environ["DEV_TYPE"] == "switch":
        configuration = header + _process_json_config(
            json_config, os.environ["DEV_COMPANY"]
        )

    config_path = os.path.join(
        os.environ["TFTP_FOLDER"], "tmp", os.environ["CFG_FILENAME"]
    )
    try:
        with open(config_path, "w") as f:
            f.write(configuration)
            logger.info(f"Configuration saved in {config_path}")
    except IOError as e:
        raise IOError(f"Failed to write configuration to {config_path}: {e}")
