from gui import BaseTab, apply_error_handler
from config import config


@apply_error_handler
class HelloTab(BaseTab):
    def refresh_widgets(self):
        super().refresh_widgets()
        self.create_block(
            "preset",
            {
                "device": self.app.entity_collections["device"],
                "role": self.app.entity_collections["role"],
            },
            ("REFRESH", self.refresh_presets),
        )
        self.create_block(
            "params",
            {
                "preset": ("1", "2"),
                "CERT": (config["default-cert"],),
                "OR": tuple(str(i) for i in range(1, 26)),
            },
        )
        self.create_button_in_line(("UPDATE TABS", self.update_tabs))

    def update_tabs(self):
        device = self.check_device_name(self.fields["preset"]["device"].get())
        preset = self.app.db_services["preset"].get_by_device_and_role(
            device, self.fields["preset"]["role"].get()
        )

        self.app.set_configuration_parameters(
            cert=self.fields["params"]["CERT"].get().strip(),
            OR=self.fields["params"]["OR"].get().strip(),
            device=device,
            preset=preset,
        )
        self.app.refresh_tabs()
        self.app.notebook.select(self.app.tabs["COMMANDS"].frame)
