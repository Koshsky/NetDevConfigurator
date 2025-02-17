import logging
import os

logger = logging.getLogger("env")


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
        return self.from_human(env_name, os.environ[env_name])

    def from_human(self, env_name, human_value):
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
