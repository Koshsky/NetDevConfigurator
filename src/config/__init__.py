import yaml
from utils.network import find_available_ip


config = yaml.safe_load(open("./src/config/config.yml"))
available_ip = find_available_ip(
    config["mvs-network"],
    lambda ip: ip.packed[-1] >= 100 and ip.packed[-1] < 201,
)
config["available-ip"] = available_ip
