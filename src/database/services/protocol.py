import logging
from typing import Dict

from sqlalchemy.orm import Session

from database.models import Protocols

from .base_service import BaseService, JsonType

logger = logging.getLogger(__name__)


class ProtocolService(BaseService[Protocols]):
    """Service for managing protocol-related database operations."""

    def __init__(self, db: Session) -> None:
        """Initializes the ProtocolService with a database session.

        Args:
            db: The SQLAlchemy database session.
        """
        logger.debug("Initializing ProtocolService")
        super().__init__(db, Protocols)

    def get_info(self, protocol: Protocols) -> JsonType:
        """Retrieves information about a specific protocol.

        Args:
            protocol: The Protocols model instance.

        Returns:
            A dictionary containing protocol information.
        """
        logger.debug("Retrieving information for protocol: %s", protocol.name)
        protocol_info: Dict[str, JsonType] = {
            "id": protocol.id,
            "name": protocol.name,
        }
        return protocol_info
