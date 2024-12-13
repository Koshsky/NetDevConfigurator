from sqlalchemy.orm import Session

from internal.database.models import Ports

class PortService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Ports).order_by(Ports.name).all()

    def get_by_id(self, id: int):
        return self.db.query(Ports).filter(Ports.id == id).first()

    def get_by_name(self, name: str):
        return self.db.query(Ports).filter(Ports.name == name).first()

    def create(self, data: dict):
        port = Ports(**data)
        self.db.add(port)
        self.db.commit()
        self.db.refresh(port)
        return port

    def delete(self, port: Ports):
        self.db.delete(port)
        self.db.commit()

    def delete_by_id(self, id: int):
        port = self.get_by_id(id)
        self.delete(port)
    
    def delete_by_name(self, name: str):
        port = self.get_by_name(name)
        self.delete(port)

    