from bash import get_esr_configuration
import os


def get_eltex_config(raw_config):
    configuration = ""
    for k, v in raw_config.items():
        if v["text"]:
            configuration += v["text"].replace("{INTERFACE_ID}", k) + "\n"
    configuration = configuration.replace("{CERT}", os.environ["CERT"])
    configuration = configuration.replace("{OR}", os.environ["OR"])
    configuration = configuration.replace("{MODEL}", os.environ["DEV_NAME"])
    configuration = configuration.replace("{ROLE}", os.environ["DEV_ROLE"])
    return configuration + "end\n"


def get_zyxel_config(raw_config):
    # TODO: усложнить логику с pvid и че-то там такое
    configuration = ""
    for k, v in raw_config.items():
        if v["text"]:
            configuration += v["text"].replace("{INTERFACE_ID}", k) + "\n"
    configuration = configuration.replace("{CERT}", os.environ["CERT"])
    configuration = configuration.replace("{OR}", os.environ["OR"])
    configuration = configuration.replace("{MODEL}", os.environ["DEV_NAME"])
    configuration = configuration.replace("{ROLE}", os.environ["DEV_ROLE"])
    return configuration + "end\n"


def render_configuration(raw_config) -> str:
    if os.environ["DEV_TYPE"] == "router":
        return get_esr_configuration()

    elif os.environ["DEV_TYPE"] == "switch":
        # if "DEV_ROLE" not in os.environ:
        #     raise Exception("Please set up switch role")
        if os.environ["DEV_COMPANY"] == "Zyxel":
            return get_zyxel_config(raw_config)
        elif os.environ["DEV_COMPANY"] == "Eltex":
            return get_eltex_config(raw_config)
