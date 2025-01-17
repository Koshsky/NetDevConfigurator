from functools import wraps
from scrapli.response import Response


def ssh_logger(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"Calling {func.__name__}...")
        resp = func(self, *args, **kwargs)
        if isinstance(resp, Response):
            print(resp.result())
        else:
            print(resp)
        print("========================================================")

    return wrapper


def apply_ssh_logger(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            setattr(cls, attr_name, ssh_logger(attr_value))
    return cls
