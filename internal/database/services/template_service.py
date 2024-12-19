from sqlalchemy.orm import Session

from internal.database.models import Templates
from .family_service import FamilyService

class TemplateService:
    def __init__(self, db: Session):
        self.db = db
        self.family_service = FamilyService(db)
    
    def get_info(self, template_id: int):
        template = self.get_by_id(template_id)
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

    def get_all(self):
        return self.db.query(Templates).all()

    def get_by_id(self, id: int):
        return self.db.query(Templates).filter(Templates.id == id).first()
    
    def get_all_by_role_family_id(self, family_id: int, role: str):
        return self.db.query(Templates).filter(Templates.family_id == family_id, Templates.role == role)

    def get_by_name_type_role(self, name: str, type: str, role: str):
        return self.db.query(Templates).filter(Templates.name == name, Templates.type == type,
                                               Templates.role == role).first()
    def get_by_name(self, name: str):
        return self.db.query(Templates).filter(Templates.name == name).first()

    def create(self, data: dict):
        template = Templates(**data)
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def delete(self, template: Templates):
        self.db.delete(template)
        self.db.commit()

    def delete_by_id(self, id: int):
        template = self.get_by_id(id)
        self.delete(template)
    
    def delete_by_name(self, name: str):
        template = self.get_by_name(name)
        self.delete(template)
    