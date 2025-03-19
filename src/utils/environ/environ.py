import logging
import os

logger = logging.getLogger(__name__)


# TODO: need tftp_enviroment setup function


def get_env(key: str) -> str | int | None:
    """Gets an environment variable.

    Args:
        key: The name of the environment variable.
    """
    key = key.upper()
    return os.environ.get(key)


def set_env(key: str, value: str | int | None) -> bool:
    """Sets an environment variable.

    Args:
        key: The name of the environment variable.
        value: The value of the environment variable.

    Returns:
        True if the environment variable was set or updated, False otherwise.
    """
    if value is None:
        return

    value = str(value)
    key = key.upper()
    if key not in os.environ or os.environ[key] != value:
        os.environ[key] = value
        logger.info(
            f"Environmental variable {'updated' if key in os.environ else 'set up'}: {key}={value}"
        )
        return True
    return False


def del_env(key: str):
    """Deletes an environment variable.

    Args:
        key: The name of the environment variable to delete.
    """
    logger.debug("Deleting environment variable: %s", key)
    key = key.upper()
    if key in os.environ:
        del os.environ[key]
        logger.info("Environmental variable deleted: %s", key)
    else:
        logger.debug("Environment variable %s not found.", key)
