from gui import BaseTab, apply_error_handler

from config import config


@apply_error_handler
class HelloTab(BaseTab):
    def create_widgets(self):
        self.create_block(
            "device",
            {  # for filtering presets
                "name": self.app.entity_collections["device"],
                "role": self.app.entity_collections["role"],
            },
            ("REFRESH", self.refresh_presets),
        )
        self.create_block(
            "params",
            {
                "preset": ("1", "2"),
                "CERT": None,
                "OR": None,
            },
        )
        self.create_button_in_line(("UPDATE TABS", self.update_tabs))
        self.create_block(
            "host",
            {
                "address": (config["host"]["address"],),
                "port": ("22",),
            },
        )
        self.create_block(
            "credentials",
            {
                "username": (config["host"]["username"],),
                "password": (config["host"]["password"],),
            },
        )
        self.create_button_in_line(("UPDATE CREDENTIALS", self.update_host_info))
        self.create_feedback_area()
        self.refresh_presets()

    def update_host_info(self):
        address = self.fields["host"]["address"].get()
        port = self.fields["host"]["port"].get()
        username = self.fields["credentials"]["username"].get()
        password = self.fields["credentials"]["password"].get()
        if not all([address, port, username, password]):
            raise ValueError("Please fill all fields")
        self.app.update_host_info(address, port, username, password)

    def update_tabs(self):
        preset = self.check_preset_name(self.fields["params"]["preset"].get())
        device = self.check_device_name(self.fields["device"]["name"].get())
        if preset.device_id != device.id:
            raise ValueError("Preset and device do not match")

        self.app.register_parameters(
            cert=self.fields["params"]["CERT"].get().strip(),
            OR=self.fields["params"]["OR"].get().strip(),
            device=device,
            preset=preset,
        )
        self.app.update_config_tabs()

    def refresh_presets(self):
        device = self.check_device_name(self.fields["device"]["name"].get())
        role = self.fields["device"]["role"].get().strip()
        if not role or role not in self.app.entity_collections["role"]:
            raise ValueError(
                f"Invalid role: '{role}'. Role must be one of {list(self.app.entity_collections['role'])}."
            )

        presets = self.app.db_services["preset"].get_all_by_device_id(device.id)
        self.filtered_presets = [
            preset.name for preset in presets if preset.role == role
        ]
        self.fields["params"]["preset"]["values"] = self.filtered_presets
        self.fields["params"]["preset"].set(
            self.filtered_presets[0] if self.filtered_presets else ""
        )
        self.display_feedback("Presets refreshed.")
