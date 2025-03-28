import logging
from typing import Any, Dict, Tuple

from sqlalchemy.orm import Session

from database.models import Templates

from .base_service import BaseService, JsonType
from .family import FamilyService

logger = logging.getLogger(__name__)
ALLOWED_TYPES: Tuple[str, ...] = (
    "hostname",
    "VLAN",
    "ssh",
    "type-commutation",
    "STP",
    "credentials",
    "addr-set",
    "interface",
    "GW",
    "telnet",
    "SNMP",
    "ZTP",
    "jumbo",
    "priority",
    "timezone",
    "DNS",
    "NTP",
    "cloud",
)


class TemplateService(BaseService[Templates]):
    """Service for managing template-related database operations."""

    def __init__(self, db: Session) -> None:
        """Initializes the TemplateService with a database session.

        Args:
            db: The SQLAlchemy database session.
        """
        logger.debug("Initializing TemplateService")
        super().__init__(db, Templates)

    def create(self, **kwargs: Any) -> "Templates":
        """Creates a new template with the given attributes.

        Args:
            **kwargs: Keyword arguments representing template attributes.

        Returns:
            The newly created Templates instance.

        Raises:
            ValueError: If the provided type is invalid.
        """
        template_type = kwargs.get("type")
        if template_type not in ALLOWED_TYPES:
            logger.error(
                "Invalid type provided when creating a template: %s", template_type
            )
            raise ValueError(
                f"Invalid type: '{template_type}'. Allowed types are: {ALLOWED_TYPES}"
            )

        logger.debug("Creating template with data: %s", kwargs)
        return super().create(**kwargs)

    def get_info(self, template: "Templates") -> JsonType:
        """Retrieves information about a specific template.

        Args:
            template: The Templates model instance.

        Returns:
            A dictionary containing template information.
        """
        logger.debug("Retrieving information for template: %s", template.name)
        family = FamilyService(self.db).get_one(id=template.family_id)
        template_info: Dict[str, JsonType] = {
            "name": template.name,
            "id": template.id,
            "family": family.name,
            "type": template.type,
            "role": template.role,
            "text": template.text,
        }
        return template_info
