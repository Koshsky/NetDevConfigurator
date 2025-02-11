from pprint import pformat

from gui import BaseTab, apply_error_handler


@apply_error_handler
class InfoTab(BaseTab):
    def _render_widgets(self):
        entity_types = ["company", "family", "device", "template"]
        for entity_type in entity_types:
            self.create_block(
                entity_type,
                {"name": self.app.entity_collections[entity_type]},
                ("SHOW", getattr(self, f"show_{entity_type}_info")),
            )
        self.create_block(
            "preset",
            {
                "device": self.app.entity_collections["device"],
                "role": self.app.entity_collections["role"],
            },
            ("SHOW", self.show_preset_info),
        )
        self.create_feedback_area()

    def __getattr__(self, name):
        if name.startswith("show_") and name.endswith("_info"):
            entity_type = name[5:-5]  # Extract entity type from method name

            def dynamic_show_info():
                return self.__show_info(entity_type)

            return dynamic_show_info
        return super().__getattr__(name)

    def show_preset_info(self):
        device = self.check_device_name(self.fields["preset"]["device"].get())
        role = self.fields["preset"]["role"].get()
        preset = self.app.db_services["preset"].get_by_device_and_role(device, role)
        self.display_feedback(
            pformat(self.app.db_services["preset"].get_info(preset), sort_dicts=False)
        )

    def __show_info(self, entity_type: str):
        entity_name = self.fields[entity_type]["name"].get().strip()
        self.display_feedback(
            pformat(
                self.app.db_services[entity_type].get_info_by_name(entity_name),
                sort_dicts=False,
            )
        )
