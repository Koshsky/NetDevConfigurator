from sqlalchemy.orm import Session

from internal.database.models import Families


class FamilyService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Families).all()

    def get_by_id(self, family_id: int):
        return self.db.query(Families).filter(Families.id == family_id).first()

    def get_by_name(self, name: str):
        return self.db.query(Families).filter(Families.name == name).first()
    
    def create(self, family: dict):
        new_family = Families(**family)
        self.db.add(new_family)
        self.db.commit()
        self.db.refresh(new_family)
        return new_family

    def delete(self, family):
        if family:
            self.db.delete(family)
            self.db.commit()

    def delete_by_name(self, name: str):
        db_family = self.get_by_name(name)
        self.delete(db_family)

    def delete_by_id(self, family_id: int):
        db_family = self.get_by_id(family_id)
        self.delete(db_family)
