import logging
import logging.config
import os

import yaml

config = yaml.safe_load(open("./src/config/config.yml"))
LOGGING = yaml.safe_load(open("./src/config/logging_config.yaml"))
logging.config.dictConfig(LOGGING)


os.environ["TFTP_ADDRESS"] = config["tftp-server"]["address"]
os.environ["TFTP_PORT"] = str(config["tftp-server"]["port"])
os.environ["TFTP_FOLDER"] = config["tftp-server"]["folder"]

logger = logging.getLogger("config")
logger.info(
    "Environmental variables set up: TFTP_ADDRESS=%s, TFTP_PORT=%s, TFTP_FOLDER=%s",
    os.environ["TFTP_ADDRESS"],
    os.environ["TFTP_PORT"],
    os.environ["TFTP_FOLDER"],
)
