import logging
import os
import subprocess

logger = logging.getLogger("bash")


def save_ESR_configuration():
    SCRIPT_PATH = "./src/bash/config_esr/make_config.sh"
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
        logger.error("src.bash.get_esr_configuration: %s", e)

    with open(config_path, "r") as f:
        return f.read()
