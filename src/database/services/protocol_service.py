from sqlalchemy.orm import Session

from database.models import Protocols
from .base_service import BaseService, JsonType


class ProtocolService(BaseService):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Protocols)

    def get_info(self, protocol: Protocols) -> JsonType:
        return {
            "id": protocol.id,
            "name": protocol.name,
        }
