import logging

from sqlalchemy.orm import Session

from database.models import Templates

from .base_service import BaseService, JsonType
from .family_service import FamilyService

logger = logging.getLogger("db")
allowed_types = (
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


class TemplateService(BaseService):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Templates)

    def create(self, **kwargs):
        type = kwargs.get("type")
        if type not in allowed_types:
            logger.error(
                "Attempted to create an entity with an invalid type: %s. Allowed types are: %s",
                type,
                allowed_types,
            )
            raise ValueError(
                f"Invalid type: '{type}'. Allowed types are: {allowed_types}"
            )

        super().create(**kwargs)

    def get_info(self, template) -> JsonType:
        family = FamilyService(self.db).get_one(id=template.family_id)
        return {
            "name": template.name,
            "id": template.id,
            "family": family.name,
            "type": template.type,
            "role": template.role,
            "text": template.text,
        }
