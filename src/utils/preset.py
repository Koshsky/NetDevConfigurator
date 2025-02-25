import os
from bash import save_ESR_configuration
import logging

logger = logging.getLogger("bash")  # пусть так


def check_environment_variables():
    required_vars = [
        "CERT",
        "OR",
        "DEV_NAME",
        "TFTP_FOLDER",
        "CFG_FILENAME",
        "DEV_TYPE",
        "DEV_COMPANY",
    ]
    for var in required_vars:
        if var not in os.environ:
            raise EnvironmentError(f"Missing required environment variable: {var}")
    if os.environ["DEV_TYPE"] == "switch" and "ROLE" not in os.environ:
        raise EnvironmentError("Missing required environment variable: ROLE")


def save_configuration(raw_config, device_company):
    configuration = ""
    for k, v in raw_config.items():
        if v["text"]:
            configuration += f"{v['text'].replace('{INTERFACE_ID}', k)}\n"

    configuration = configuration.replace("{CERT}", os.environ["CERT"])
    configuration = configuration.replace("{OR}", os.environ["OR"])
    configuration = configuration.replace("{MODEL}", os.environ["DEV_NAME"])
    configuration = configuration.replace("{ROLE}", os.environ["DEV_ROLE"])

    if device_company == "Zyxel":
        # TODO: усложнить логику с pvid и че-то там такое
        pass

    config_path = os.path.join(
        os.environ["TFTP_FOLDER"], "tmp", os.environ["CFG_FILENAME"]
    )
    try:
        with open(config_path, "w") as f:
            f.write(configuration)
            logger.info(f"Configuration saved in {config_path}")
    except IOError as e:
        raise IOError(f"Failed to write configuration to {config_path}: {e}")

    return configuration + "end\n"


def render_configuration(raw_config) -> str:
    check_environment_variables()

    if os.environ["DEV_TYPE"] == "router":
        return save_ESR_configuration()

    elif os.environ["DEV_TYPE"] == "switch":
        if os.environ["DEV_COMPANY"] in ["Zyxel", "Eltex"]:
            return save_configuration(raw_config, os.environ["DEV_COMPANY"])
        else:
            raise ValueError(f"Unsupported device company: {os.environ['DEV_COMPANY']}")
