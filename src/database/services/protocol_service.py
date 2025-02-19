from sqlalchemy.orm import Session

from database.models import Protocols
from .base_service import BaseService


class ProtocolService(BaseService):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Protocols)
