import logging
from typing import Dict

from sqlalchemy.orm import Session

from database.models import Ports

from .base_service import BaseService, JsonType

logger = logging.getLogger(__name__)


class PortService(BaseService[Ports]):
    """Service for managing port-related database operations."""

    def __init__(self, db: Session) -> None:
        """Initializes the PortService with a database session.

        Args:
            db: The SQLAlchemy database session.
        """
        logger.debug("Initializing PortService")
        super().__init__(db, Ports)

    def get_info(self, port: Ports) -> JsonType:
        """Retrieves information about a specific port.

        Args:
            port: The Ports model instance.

        Returns:
            A dictionary containing port information.
        """
        logger.debug("Retrieving information for port: %s", port.name)
        port_info: Dict[str, JsonType] = {
            "name": port.name,
            "material": port.material,
            "speed": port.speed,
        }
        return port_info
