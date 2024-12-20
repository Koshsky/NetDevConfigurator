from sqlalchemy.orm import Session

from internal.database.models import Families
from .base_service import BaseService


class FamilyService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Families)
