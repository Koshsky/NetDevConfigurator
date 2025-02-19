from sqlalchemy.orm import Session

from database.models import Templates

from .base_service import BaseService, JsonType
from .family_service import FamilyService


class TemplateService(BaseService):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Templates)
        self.family_service = FamilyService(db)

    def get_info(self, template) -> JsonType:
        family = self.family_service.get_one(id=template.family_id)
        return {
            "name": template.name,
            "id": template.id,
            "family": family.name,
            "type": template.type,
            "role": template.role,
            "text": template.text,
        }
