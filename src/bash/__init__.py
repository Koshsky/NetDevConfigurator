import logging
import subprocess

logger = logging.getLogger("bash")


def get_esr_configuration():
    SCRIPT_PATH = "./src/bash/config_esr/make_config.sh"
    logger.info("running make_config.sh")
    try:
        result = subprocess.run(
            ["bash", SCRIPT_PATH], check=True, text=True, capture_output=True
        )
        logger.debug("src.basg.get_ser_configuration: %s", result)
    except subprocess.CalledProcessError as e:
        logger.error("src.bash.get_esr_configuration: %s", e)

    return "./src/bash/config_esr/config.cfg"
