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

    def get_by_name(self, template_name: str):
        if template:= self.db.query(Templates).filter(Templates.name == template_name).all():
            return template
        else:
            raise EntityNotFoundError(f"{Templates.__name__} with name {template_name} not found")

    def get_by_family_id_and_role(self, family_id: int, role: str): # to create a list of suitable templates
        roles_to_check = ['common', role]

        if (
            entities := self.db.query(Templates)
            .filter(
                Templates.family_id == family_id,
                Templates.role.in_(roles_to_check),
            )
            .all()
        ):
            return [template.name for template in entities]
        else:
            raise EntityNotFoundError("Templates not found")

    def get_by_name_and_role(self, name: str, role: str):  # for unambiguous selection
        if template := self.db.query(Templates).filter(
                Templates.name == name,
                Templates.role == role
            ).first():
            return template
        else:
            raise EntityNotFoundError("Template not found")
