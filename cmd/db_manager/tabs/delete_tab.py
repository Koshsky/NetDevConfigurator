from internal.db_app import BaseTab, error_handler

class DeleteTab(BaseTab):
    def create_widgets(self):
        entities = ["company", "family", "device", "firmware", "protocol", "template", 'preset']
        for entity in entities:
            self.create_block(entity, {"name": None}, ("delete", lambda e=entity: self.delete_entity(e)))

        self.create_feedback_area()

    @error_handler
    def delete_entity(self, entity_type):
        self.app.entity_services[entity_type].delete_by_name(self.fields[entity_type]["name"].get())
        self.display_feedback(f"Successfully deleted from the {entity_type}s table.")

