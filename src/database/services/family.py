import logging
from typing import Dict

from sqlalchemy.orm import Session

from database.models import Families

from .base_service import BaseService, JsonType
from .device import DeviceService

logger = logging.getLogger(__name__)


class FamilyService(BaseService[Families]):
    """Service for managing family-related database operations."""

    def __init__(self, db: Session) -> None:
        """Initializes the FamilyService with a database session.

        Args:
            db: The SQLAlchemy database session.
        """
        logger.debug("Initializing FamilyService")
        super().__init__(db, Families)

    def get_info(self, family: Families) -> JsonType:
        """Retrieves information about a specific family.

        Args:
            family: The Families model instance.

        Returns:
            A dictionary containing family information, including associated devices.
        """
        logger.debug("Retrieving information for family: %s", family.name)
        associated_devices = DeviceService(self.db).get_all(family_id=family.id)
        family_info: Dict[str, JsonType] = {
            "id": family.id,
            "name": family.name,
            "associated_devices": [device.name for device in associated_devices],
        }
        return family_info
