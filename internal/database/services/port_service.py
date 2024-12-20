from sqlalchemy.orm import Session

from internal.database.models import Ports
from .base_service import BaseService


class PortService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Ports)
