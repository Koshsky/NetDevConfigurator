from sqlalchemy.orm import Session

from internal.database.models import Protocols
from .base_service import BaseService

class ProtocolService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Protocols)
