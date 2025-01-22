from functools import wraps


def prepare_config_file(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        configuration = self.app.text_configuration
        config_path = f"/srv/tftp/tmp/{self.app.config_filename}"
        with open(config_path, "w") as f:
            f.write(configuration)
        self.display_feedback(f"Configuration saved:\n{config_path}")

        return func(self, *args, **kwargs)

    return wrapper


class check_driver:
    def __init__(self, transport):
        self.transport = transport

    def __call__(cls, func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if cls.transport == "ssh2" and self.app.ssh2 is None:
                raise Exception("SSH2 driver is not configured")

        return wrapper
