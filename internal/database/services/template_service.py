from sqlalchemy.orm import Session

from internal.database.models import Templates
from .family_service import FamilyService
from .base_service import BaseService
from .exceptions import EntityNotFoundError

class TemplateService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Templates)
        self.family_service = FamilyService(db)

    def get_info(self, template):
        family = self.family_service.get_by_id(template.family_id)
        return {
            "id": template.id,
            "family": {
                "id": family.id,
                "name": family.name,
            },
            "name": template.name,
            "type": template.type,
            "role": template.role,
            "text": template.text,
        }

    def get_all_by_role_family_id(self, family_id: int, role: str): # to create a list of suitable templates
        if entity := self.db.query(Templates).filter(Templates.family_id == family_id, Templates.role == role):
            return entity
        else:
            raise EntityNotFoundError("Template not found")

    def get_by_name_type_role(self, name: str, type: str, role: str):  # for unambiguous selection
        if entity := self.db.query(Templates).filter(Templates.name == name, Templates.type == type,
                                               Templates.role == role).first():
            return entity
        else:
            raise EntityNotFoundError("Template not found")
