import logging
import logging.config

import yaml


LOGGING = yaml.safe_load(open("./src/config/logging_config.yaml"))
logging.config.dictConfig(LOGGING)
logging.getLogger("paramiko").setLevel(logging.WARNING)
logger = logging.getLogger("config")

config = yaml.safe_load(open("./src/config/config.yaml"))
config["router"] = yaml.safe_load(open("./src/config/router.yaml"))
