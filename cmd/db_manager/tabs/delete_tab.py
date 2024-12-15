from internal.db_app import BaseTab, error_handler

class DeleteTab(BaseTab):
    def create_widgets(self):
        entities = ["company", "family", "device", "firmware", "protocol", "template_piece"]
        for entity in entities:
            self.create_block(entity, {"name": None}, ("delete", lambda e=entity: self.delete_entity(e)))

        self.create_feedback_area()

    @error_handler
    def delete_entity(self, entity_type):
        check_method = getattr(self, f"check_{entity_type}_name")
        delete_method = self.app.entity_services[entity_type].delete

        entity = check_method(self.fields[entity_type]["name"].get())
        delete_method(entity)
        self.display_feedback(f"Successfully deleted from the {entity_type}s table.")

