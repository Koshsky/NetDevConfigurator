from sqlalchemy.orm import Session

from database.models import Templates

from .base_service import BaseService
from .exceptions import EntityNotFoundError
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

    def get_info_by_name(self, template_name):
        templates = (
            self.db.query(Templates).filter(Templates.name == template_name).all()
        )
        return [self.get_info(template) for template in templates]

    def get_by_family_id_and_role(
        self, family_id: int, role: str
    ):  # to create a list of suitable templates
        roles_to_check = ["common", role]

        return (
            self.db.query(Templates)
            .filter(
                Templates.family_id == family_id,
                Templates.role.in_(roles_to_check),
            )
            .all()
        )

    def get_by_name_and_role(self, name: str, role: str):  # for unambiguous selection
        if entity := (
            self.db.query(Templates)
            .filter(
                Templates.name == name,
                Templates.role.in_(["common", role]),
            )
            .first()
        ):
            return entity
        else:
            raise EntityNotFoundError(
                f"there is no template with name={name}, role={role}"
            )

    def delete_by_name_and_role(self, name: str, role: str):
        self.delete(self.get_by_name_and_role(name, role))

    def update_by_name_and_role(self, name: str, role: str, data: dict):
        entity = self.get_by_name_and_role(name, role)
        self.update(entity, data)
