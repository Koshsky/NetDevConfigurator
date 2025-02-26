import os
import logging
import subprocess

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


def _check_environment_variables():
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
    if os.environ["DEV_TYPE"] == "switch" and "DEV_ROLE" not in os.environ:
        raise EnvironmentError("Missing required environment variable: DEV_ROLE")


def _save_config(raw_config, device_company):
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


def save_configuration(raw_config) -> str:
    _check_environment_variables()

    if os.environ["DEV_TYPE"] == "router":
        return _save_ESR_configuration()

    elif os.environ["DEV_TYPE"] == "switch":
        if os.environ["DEV_COMPANY"] in ["Zyxel", "Eltex"]:
            return _save_config(raw_config, os.environ["DEV_COMPANY"])
        else:
            raise ValueError(f"Unsupported device company: {os.environ['DEV_COMPANY']}")
