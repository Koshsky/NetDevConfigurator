from sqlalchemy.orm import Session

from internal.database.models import Protocols

class ProtocolService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Protocols).order_by(Protocols.name).all()

    def get_by_id(self, id: int):
        return self.db.query(Protocols).filter(Protocols.id == id).first()

    def get_by_name(self, name: str):
        return self.db.query(Protocols).filter(Protocols.name == name).first()

    def create(self, data: dict):
        protocol = Protocols(**data)
        self.db.add(protocol)
        self.db.commit()
        self.db.refresh(protocol)
        return protocol

    def delete(self, protocol: Protocols):
        self.db.delete(protocol)
        self.db.commit()

    def delete_by_id(self, id: int):
        protocol = self.get_by_id(id)
        self.delete(protocol)
    
    def delete_by_name(self, name: str):
        protocol = self.get_by_name(name)
        self.delete(protocol)

    