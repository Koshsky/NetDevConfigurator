import logging

from gui import BaseTab, apply_error_handler

logger = logging.getLogger(__name__)


@apply_error_handler
class DeleteTab(BaseTab):
    """Tab for deleting entities from the database."""

    def _create_widgets(self) -> None:
        """Creates the widgets for the tab."""
        logger.debug("Creating widgets for DeleteTab")
        entities: list[str] = ["company", "family", "device", "protocol"]
        for entity in entities:
            self.create_block(
                entity,
                {"name": tuple(e.name for e in self.app.db_services[entity].get_all())},
                ("delete", lambda e=entity: self.delete_entity(e)),
            )

    def delete_entity(self, entity_type: str) -> None:
        """Deletes an entity from the database.

        Args:
            entity_type: The type of entity to delete (e.g., "company", "family").
        """
        logger.info("Deleting entity of type: %s", entity_type)
        entity_name: str = self.fields[entity_type]["name"].get()
        self.app.db_services[entity_type].delete_one(name=entity_name)
        logger.debug("Successfully deleted %s: %s", entity_type, entity_name)
        self.display_feedback(f"Successfully deleted from the {entity_type}s table.")
