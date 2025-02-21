from sqlalchemy.orm import Session

from database.models import Ports
from .base_service import BaseService, JsonType


class PortService(BaseService):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Ports)

    def get_info(self, port: Ports) -> JsonType:
        return {
            "name": port.name,
            "material": port.material,
            "speed": port.speed,
        }
