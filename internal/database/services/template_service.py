from sqlalchemy.orm import Session

from internal.database.models import Templates

class TemplateService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Templates).all()

    def get_by_id(self, id: int):
        return self.db.query(Templates).filter(Templates.id == id).first()

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
    