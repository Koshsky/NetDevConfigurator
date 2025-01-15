from functools import wraps


def prepare_config_file(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        template = self._get_text_configuration()
        config_path = f"/srv/tftp/{self.app.config_filename}"
        with open(config_path, "w") as f:
            f.write(template)
        self.display_feedback(f"Template saved:\n{config_path}")

        return func(self, *args, **kwargs)

    return wrapper


class update_driver:
    def __init__(self, transport):
        self.transport = transport

    def __call__(cls, func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.driver = {
                "auth_strict_key": False,  # important for unknown hosts
                "family": self.app.params["FAMILY"],
                "host": self.fields["host"]["IP"].get(),
                "auth_username": self.fields["credentials"]["username"].get(),
                "auth_password": self.fields["credentials"]["password"].get(),
                "transport": cls.transport,
            }

        return wrapper
