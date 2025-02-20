from functools import wraps
import logging


logger = logging.getLogger("app")


def error_handler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            logger.error("%s: %s", type(e).__name__, e)
            self.show_error(type(e).__name__, e)
        finally:
            if self.app.session is not None:
                self.app.session.rollback()

    return wrapper


def apply_error_handler(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            setattr(cls, attr_name, error_handler(attr_value))
    return cls
