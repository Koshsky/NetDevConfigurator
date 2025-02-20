import os

from utils import env_converter, set_env


class BaseDeviceHandler:
    def __init__(self, control_tab):
        self.tab = control_tab
        self.app = control_tab.app

    def create_widgets(self):
        raise NotImplementedError

    def actualize_params(self):
        raise NotImplementedError

    def update_params(self):
        raise NotImplementedError


class SwitchHandler(BaseDeviceHandler):
    def create_widgets(self):
        self.tab.create_block(
            "params",
            {
                "role": self.app.device["roles"],
                "or": tuple(str(i) for i in range(1, 26)),
            },
            ("UPDATE", self.update_params),
        )

    def actualize_params(self):
        self.tab.fields["params"]["role"].set(os.environ["DEV_ROLE"])
        self.tab.fields["params"]["or"].set(os.environ["OR"])

    # TODO: это может вызвать исключение, которое не перехватить декоратором.
    def update_params(self):
        # стоит повесить декоратор на ConfiguratorApp?
        self.app.register_preset(
            self.tab.check_role_name(self.tab.fields["params"]["role"].get()),
            self.tab.fields["params"]["or"].get().strip(),
        )


class RouterHandler(BaseDeviceHandler):
    def create_widgets(self):
        self.tab.create_block(
            "params",
            {
                "TYPE_COMPLEX": tuple(env_converter["TYPE_COMPLEX"]),
            },
            ("UPDATE", self.update_params),
        )

    def actualize_params(self):
        self.tab.fields["params"]["TYPE_COMPLEX"].set(
            env_converter.get_human("TYPE_COMPLEX")
        )

    def update_params(self):
        set_env(
            "TYPE_COMPLEX",
            env_converter.to_machine(
                "TYPE_COMPLEX",
                self.tab.fields["params"]["TYPE_COMPLEX"].get().strip(),
            ),
        )
