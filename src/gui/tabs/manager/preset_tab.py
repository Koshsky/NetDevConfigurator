from gui import BaseTab, apply_error_handler


@apply_error_handler
class PresetTab(BaseTab):
    def __init__(self, app, parent, log_name="ConfigTab"):
        super().__init__(app, parent, log_name)
        self.preset_info = None

    def _create_widgets(self):
        self._create_preset_block()
        self._create_configuration_block()
        self.create_feedback_area()
        self.refresh_templates()

    def _create_preset_block(self):
        self.create_block(
            "preset",
            {
                "device": self.app.entity_collections["device"],
                "role": self.app.entity_collections["role"],
            },
        )
        self.create_button_in_line(("CREATE", self.create_preset))
        self.create_button_in_line(("DELETE", self.delete_preset))
        self.create_button_in_line(("REFRESH TEMPLATES", self.refresh_templates))

    def _create_configuration_block(self):
        self.create_block(
            "template",
            {
                "name": ("1", "2"),
                "ordered_number": tuple(map(str, range(1, 101))),
            },
        )
        self.create_button_in_line(("PUSH BACK", self.push_back))
        self.create_button_in_line(("INSERT", self.insert))
        self.create_button_in_line(("REMOVE", self.remove))
        self.create_button_in_line(("PREVIEW", self.preview))

    def create_preset(self):
        self.app.db_services["preset"].create(
            role=self.fields["preset"]["role"].get().strip(),
            device_id=self.selected_device.id,
        )

    def delete_preset(self):
        self.app.db_services["preset"].delete(self.selected_preset)

    @property
    def selected_device(self):
        return self.app.db_services["device"].get_one(
            name=self.fields["preset"]["device"].get().strip(),
        )

    @property
    def selected_preset(self):
        preset = self.app.db_services["preset"].get_one(
            device_id=self.selected_device.id,
            role=self.fields["preset"]["role"].get().strip(),
        )
        self.preset_info = self.app.db_services["preset"].get_info(preset)
        return preset

    @property
    def selected_template(self):
        return self.app.db_services["template"].get_one(
            name=self.fields["template"]["name"].get().strip(),
            family_id=self.selected_device.family_id,
            role=["common", self.selected_preset.role],
        )

    @property
    def relevant_templates(self):
        return [
            template.name
            for template in self.app.db_services["template"].get_all(
                family_id=self.selected_device.family_id,
                role=["common", self.selected_preset.role],
            )
        ]

    def remove(self) -> str:
        ordered_number = self.fields["template"]["ordered_number"].get().strip()
        self.app.db_services["preset"].remove(
            self.selected_preset.id, int(ordered_number)
        )
        self._display_configuration_status(
            f"Template in {ordered_number} successfully removed\n"
        )

    def push_back(self) -> str:
        self.app.db_services["preset"].push_back(
            self.selected_preset, self.selected_template
        )
        self._display_configuration_status(
            f"Template {self.selected_template.name} successfully pushed back\n"
        )

    def insert(self) -> str:
        ordered_number = self.fields["template"]["ordered_number"].get().strip()
        self.app.db_services["preset"].insert(
            self.selected_preset, self.selected_template, int(ordered_number)
        )
        self._display_configuration_status(
            f"Template {self.selected_template.name} successfully inserted at position {ordered_number}\n"
        )

    def refresh_templates(self):
        if not self.relevant_templates:
            raise ValueError("There are no suitable configuration templates")
        self.fields["template"]["name"]["values"] = self.relevant_templates
        self.fields["template"]["name"].set(self.relevant_templates[0])

    def preview(self):
        self.display_feedback(
            "\n".join(
                v["text"]
                for _, (_, v) in enumerate(
                    self.preset_info["configuration"].items(), start=1
                )
            )
        )

    def _display_configuration_status(self, message):
        status_message = (
            f"{message or ''}\n{self._config_meta()}\n\n{self._config_template()}"
        )
        self.display_feedback(status_message)

    def _config_meta(self):
        interfaces = len(
            [
                i
                for _, i in self.preset_info["configuration"].items()
                if i["type"] == "interface"
            ]
        )
        device_ports = len(
            self.app.db_services["device"].get_info_one(
                name=self.preset_info["device"]
            )["ports"]
        )
        return (
            f"Role: {self.preset_info['role']}\n"
            f"Device: {self.preset_info['device']}\n"
            f"Description: {self.preset_info['description']}\n"
            f"Described interfaces/Physical ports: {interfaces}/{device_ports}\n"
        )

    def _config_template(self):
        return "\n".join(
            f"{i}\t{v['name']}"
            for i, (k, v) in enumerate(
                self.preset_info["configuration"].items(), start=1
            )
        )
