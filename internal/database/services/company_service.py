from sqlalchemy.orm import Session

from internal.database.models import Companies
from .base_service import BaseService


class CompanyService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Companies)
