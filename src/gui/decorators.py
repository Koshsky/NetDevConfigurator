import logging
from functools import wraps

logger = logging.getLogger("app")


def error_handler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            logger.error("%s: %s", type(e).__name__, e)
            self.show_error(type(e).__name__, e)
            self.app.session.rollback()
            raise e

    return wrapper


def apply_error_handler(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            setattr(cls, attr_name, error_handler(attr_value))
    return cls
