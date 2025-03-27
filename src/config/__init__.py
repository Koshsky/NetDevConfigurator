import logging
import logging.config
from contextlib import contextmanager

import yaml

from .config import (
    AppConfig,
    Config,
    DatabaseConfig,
    HostConfig,
    RouterConfig,
    TFTPConfig,
)

LOGGING = yaml.safe_load(open("./src/config/logging_config.yaml"))
logging.config.dictConfig(LOGGING)
logging.getLogger("paramiko").setLevel(logging.WARNING)

config = Config()


@contextmanager
def disable_logging():
    try:
        logging.disable(logging.CRITICAL)
        yield
    finally:
        logging.disable(logging.NOTSET)


__all__ = [
    "config",
    "disable_logging",
    "DatabaseConfig",
    "TFTPConfig",
    "HostConfig",
    "RouterConfig",
    "AppConfig",
]
