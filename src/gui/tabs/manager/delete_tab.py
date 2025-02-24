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

    def delete_entity(self, entity_type):
        self.app.db_services[entity_type].delete_one(
            name=self.fields[entity_type]["name"].get()
        )
        self.display_feedback(f"Successfully deleted from the {entity_type}s table.")
