import logging
import os
import re

logger = logging.getLogger("env")


def replace_env_vars(configuration: str) -> str:
    env_vars = re.findall(r"{([A-Z0-9_]+)}", configuration)

    missing_vars = [var for var in env_vars if var not in os.environ]
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

    for var in env_vars:
        configuration = configuration.replace(f"{{{var}}}", os.environ[var])

    return configuration


def check_environment_variables():
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
    if os.environ["DEV_COMPANY"] not in ["Zyxel", "Eltex"]:
        raise ValueError(f"Unsupported device company: {os.environ['DEV_COMPANY']}")


def set_env(key: str, value: str) -> bool:
    if key in os.environ:
        if str(value) != os.environ[key]:
            os.environ[key] = str(value)
            logger.info("Environmental variable updated: %s=%s", key, os.environ[key])
            return True
    else:
        os.environ[key] = str(value)
        logger.info(
            "Environmental variable set up: %s=%s",
            key,
            os.environ[key],
        )
        return True
    return False


def del_env(key: str):
    if key in os.environ:
        del os.environ[key]
        logger.info("Environmental variables deleted: %s", key)


class EnvConverter(dict):
    def get_human(self, env_name):
        return self.to_human(env_name, os.environ[env_name])

    def to_machine(self, env_name, human_value):
        if env_name in self:
            return self[env_name][human_value]
        return human_value

    def to_human(self, env_name, machine):
        try:
            for key, value in self[env_name].items():
                if value == machine:
                    return key
        except Exception:
            return machine


env_converter = EnvConverter(
    {
        "TYPE_COMPLEX": {
            "Standard": "1",
            "All-in-one": "2",
        },
        "MODEL": {
            "ESR20": "1",
            "ESR21": "2",
            "ESR31": "3",
            "esr20": "1",
            "esr21": "2",
            "esr31": "3",
        },
        "VERS": {"1.23 and newer": "1", "old": "2"},
        "VPN": {"YES": "1", "NO": "2"},
        "TELEPORT": {"YES": "1", "NO": "2"},
        "RAISA": {"YES": "1", "NO": "2"},
        "TRUECONF": {"YES": "1", "NO": "2"},
        "TRUEROOM": {"YES": "1", "NO": "2"},
    }
)
