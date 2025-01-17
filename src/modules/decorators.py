from functools import wraps


def ssh_logger(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"Calling {func.__name__}...")
        resp = func(self, *args, **kwargs)
        print(resp.result())
        print("========================================================")

    return wrapper


def apply_ssh_logger(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            setattr(cls, attr_name, ssh_logger(attr_value))
    return cls
