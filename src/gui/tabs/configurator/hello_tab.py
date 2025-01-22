from gui import BaseTab, apply_error_handler


@apply_error_handler
class HelloTab(BaseTab):
    def refresh_widgets(self):
        super().refresh_widgets()
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
        self.refresh_presets()

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
        self.app.notebook.select(self.app.tabs[-1].frame)

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
