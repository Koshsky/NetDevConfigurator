import logging.config
import os

import yaml

config = yaml.safe_load(open("./src/config/config.yml"))
LOGGING = yaml.safe_load(open("./src/config/logging_config.yaml"))
logging.config.dictConfig(LOGGING)

os.environ["TFTP_ADDRESS"] = config["tftp-server"]["address"]
os.environ["TFTP_PORT"] = str(config["tftp-server"]["port"])
os.environ["TFTP_FOLDER"] = config["tftp-server"]["folder"]

os.environ["DEV_USERNAME"] = config["host"]["username"]
os.environ["DEV_PASSWORD"] = config["host"]["password"]
os.environ["DEV_ADDRESS"] = config["host"]["address"]
os.environ["DEV_PORT"] = str(config["host"]["port"])
