import logging
import logging.config
import os

import yaml


def set_env(key: str, value: str):
    os.environ[key] = str(value)
    logger.info(
        "Environmental variables set up: %s=%s",
        key,
        os.environ[key],
    )


router_params = {
    "TYPE_COMPLEX": {
        "Standard": "1",
        "All-in-one": "2",
    },
    "MODEL": {"ESR20": 1, "ESR21": 2, "ESR31": 3},
    "VERS": {"1.23 and newer": 1, "old": 2},
    "VPN": {"YES": 1, "NO": 2},
    "TELEPORT": {"YES": 1, "NO": 2},
    "RAISA": {"YES": 1, "NO": 2},
    "TRUECONF": {"YES": 1, "NO": 2},
    "TRUEROOM": {"YES": 1, "NO": 2},
}


LOGGING = yaml.safe_load(open("./src/config/logging_config.yml"))
logging.config.dictConfig(LOGGING)
logging.getLogger("paramiko").setLevel(logging.WARNING)
logger = logging.getLogger("config")

config = yaml.safe_load(open("./src/config/config.yml"))
config["router"] = yaml.safe_load(open("./src/config/common_router.yml"))

set_env("TFTP_ADDRESS", config["tftp-server"]["address"])
set_env("TFTP_PORT", config["tftp-server"]["port"])
set_env("TFTP_FOLDER", config["tftp-server"]["folder"])
