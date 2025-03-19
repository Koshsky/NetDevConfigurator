import logging
from pprint import pformat
from typing import Any

from database.services import allowed_roles
from gui import BaseTab, apply_error_handler

logger = logging.getLogger(__name__)


@apply_error_handler
class InfoTab(BaseTab):
    """Tab for displaying information about various entities."""

    def _create_widgets(self) -> None:
        """Creates and arranges widgets within the tab."""
        entity_types = ["company", "family", "device", "template"]
        for entity_type in entity_types:
            self.create_block(
                entity_type,
                {
                    "name": tuple(
                        e.name for e in self.app.db_services[entity_type].get_all()
                    )
                },
                ("SHOW", getattr(self, f"show_{entity_type}_info")),
            )
        self.create_block(
            "preset",
            {
                "device": tuple(
                    d.name for d in self.app.db_services["device"].get_all()
                ),
                "role": allowed_roles,
            },
            ("SHOW", self.show_preset_info),
        )
        self.create_feedback_area()

    def __getattr__(self, name: str) -> Any:
        """Dynamically creates show_info methods for different entity types."""
        if name.startswith("show_") and name.endswith("_info"):
            entity_type = name[5:-5]  # Extract entity type from method name

            def dynamic_show_info() -> None:
                return self.__show_info(entity_type)

            return dynamic_show_info
        return super().__getattr__(name)

    def show_preset_info(self) -> None:
        """Displays information about the selected preset."""
        device_name = self.fields["preset"]["device"].get()
        device = self.app.db_services["device"].get_one(name=device_name)
        role = self.fields["preset"]["role"].get()
        logger.info(f"Showing preset info for device '{device_name}' and role '{role}'")

        preset_info = self.app.db_services["preset"].get_info_one(
            device_id=device.id, role=role
        )
        formatted_info = pformat(preset_info, sort_dicts=False)
        self.display_feedback(formatted_info)

    def __show_info(self, entity_type: str) -> None:
        """Displays information about the specified entity type."""
        entity_name = self.fields[entity_type]["name"].get().strip()
        logger.info(f"Showing info for {entity_type} '{entity_name}'")

        entity_info = self.app.db_services[entity_type].get_info_all(name=entity_name)
        formatted_info = pformat(entity_info, sort_dicts=False)
        self.display_feedback(formatted_info)
