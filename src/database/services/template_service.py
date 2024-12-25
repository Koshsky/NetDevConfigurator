from sqlalchemy.orm import Session

from database.models import Templates
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
            "name": template.name,
            "id": template.id,
            "family": family.name,
            "type": template.type,
            "role": template.role,
            "text": template.text,
        }

    def get_info_by_name(self, template_name):
        templates = self.get_by_name(template_name)
        return [self.get_info(template) for template in templates]

    def get_by_name(self, template_name: str):
        if template:= self.db.query(Templates).filter(Templates.name == template_name).all():
            return template
        else:
            raise EntityNotFoundError(f"{Templates.__name__} with name {template_name} not found")

    def get_by_family_id_and_role(self, family_id: int, role: str): # to create a list of suitable templates
        roles_to_check = ['common', role]

        return (
            self.db.query(Templates)
            .filter(
                Templates.family_id == family_id,
                Templates.role.in_(roles_to_check),
            )
            .all()
        )

    def get_by_name_and_role(self, name: str, role: str):  # for unambiguous selection
        return (
            self.db.query(Templates)
            .filter(
                Templates.name == name,
                Templates.role.in_(['common', role] ),
            )
            .first()
        )
