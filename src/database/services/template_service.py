from sqlalchemy.orm import Session

from database.models import Templates

from .base_service import BaseService
from .family_service import FamilyService


class TemplateService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Templates)
        self.family_service = FamilyService(db)

    def get_info(self, template):
        family = self.family_service.get_one(id=template.family_id)
        return {
            "name": template.name,
            "id": template.id,
            "family": family.name,
            "type": template.type,
            "role": template.role,
            "text": template.text,
        }

    def get_all_relevant(self, family_id, role):
        return self.get_all(
            family_id=family_id,
            role=role,
        ) + self.get_all(
            family_id=family_id,
            role="common",
        )
