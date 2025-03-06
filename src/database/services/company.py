import logging
from typing import Dict

from sqlalchemy.orm import Session

from database.models import Companies

from .base_service import BaseService, JsonType
from .device import DeviceService

logger = logging.getLogger(__name__)


class CompanyService(BaseService[Companies]):
    """Service for managing company-related database operations."""

    def __init__(self, db: Session) -> None:
        """Initializes the CompanyService with a database session.

        Args:
            db: The SQLAlchemy database session.
        """
        logger.debug("Initializing CompanyService")
        super().__init__(db, Companies)

    def get_info(self, company: Companies) -> JsonType:
        """Retrieves information about a specific company.

        Args:
            company: The Companies model instance.

        Returns:
            A dictionary containing company information, including associated devices.
        """
        logger.debug("Retrieving information for company: %s", company.name)
        associated_devices = DeviceService(self.db).get_all(company_id=company.id)
        company_info: Dict[str, JsonType] = {
            "id": company.id,
            "name": company.name,
            "associated_devices": [device.name for device in associated_devices],
        }
        return company_info
