import logging.config

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(module)s - %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "/home/koshsky/github/NetDevConfigurator/netdevconfigurator.log",
            "formatter": "simple",
            "mode": "a",
        },
    },
    "loggers": {
        "": {
            "handlers": ["stdout", "file"],
            "level": "DEBUG",
        }
    },
}

logging.config.dictConfig(LOGGING)
