import yaml
import os


config = yaml.safe_load(open("./src/config/config.yml"))

# environment variables are used in drivers.core to form commands
os.environ["TFTP_ADDRESS"] = config["tftp-server"]["address"]
os.environ["TFTP_PORT"] = str(config["tftp-server"]["port"])
os.environ["TFTP_FOLDER"] = config["tftp-server"]["folder"]

os.environ["DEV_USERNAME"] = config["host"]["username"]
os.environ["DEV_PASSWORD"] = config["host"]["password"]
os.environ["DEV_ADDRESS"] = config["host"]["address"]
os.environ["DEV_PORT"] = str(config["host"]["port"])
