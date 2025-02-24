from gui import BaseTab, apply_error_handler


@apply_error_handler
class DeleteTab(BaseTab):
    def _create_widgets(self):
        entities = ["company", "family", "device", "protocol"]
        for entity in entities:
            self.create_block(
                entity,
                {"name": self.app.entity_collections[entity]},
                ("delete", lambda e=entity: self.delete_entity(e)),
            )

        self.create_block(
            "preset",
            {
                "device": self.app.entity_collections["device"],
                "role": self.app.entity_collections["role"],
            },
            ("delete", self.delete_preset),
        )
        self.create_feedback_area()

    def delete_preset(self):
        device = self.check_device_name(self.fields["preset"]["device"].get())
        role = self.fields["template"]["role"].get().strip()
        self.app.db_services["preset"].delete_one(device_id=device.id, role=role)
        self.display_feedback("Successfully deleted from the presets table.")

    def delete_entity(self, entity_type):
        self.app.db_services[entity_type].delete_one(
            name=self.fields[entity_type]["name"].get()
        )
        self.display_feedback(f"Successfully deleted from the {entity_type}s table.")
