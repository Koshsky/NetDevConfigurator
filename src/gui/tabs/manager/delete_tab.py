from gui import BaseTab, apply_error_handler


@apply_error_handler
class DeleteTab(BaseTab):
    def create_widgets(self):
        entities = ["company", "family", "device", "firmware", "protocol", "preset"]
        for entity in entities:
            self.create_block(
                entity,
                {"name": self.app.entity_collections[entity]},
                ("delete", lambda e=entity: self.delete_entity(e)),
            )

        self.create_block(
            "template",
            {
                "name": self.app.entity_collections["template"],
                "role": self.app.entity_collections["role"] + ("common",),
            },
            ("delete", self.delete_template),
        )
        self.create_feedback_area()

    def delete_template(self):
        name = self.fields["template"]["name"].get().strip()
        role = self.fields["template"]["role"].get().strip()
        template = self.app.db_services["template"].get_by_name_and_role(name, role)
        self.app.db_services["template"].delete(template)
        self.display_feedback("Successfully deleted from the templates table.")

    def delete_entity(self, entity_type):
        self.app.db_services[entity_type].delete_by_name(
            self.fields[entity_type]["name"].get()
        )
        self.display_feedback(f"Successfully deleted from the {entity_type}s table.")
