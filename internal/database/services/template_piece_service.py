from sqlalchemy.orm import Session

from internal.database.models import TemplatePieces

class TemplatePieceService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(TemplatePieces).all()

    def get_by_id(self, id: int):
        return self.db.query(TemplatePieces).filter(TemplatePieces.id == id).first()

    def get_by_name(self, name: str):
        return self.db.query(TemplatePieces).filter(v.name == name).first()

    def create(self, data: dict):
        template_piece = TemplatePieces(**data)
        self.db.add(template_piece)
        self.db.commit()
        self.db.refresh(template_piece)
        return template_piece

    def delete(self, template_piece: TemplatePieces):
        self.db.delete(template_piece)
        self.db.commit()

    def delete_by_id(self, id: int):
        template_piece = self.get_by_id(id)
        self.delete(template_piece)
    
    def delete_by_name(self, name: str):
        template_piece = self.get_by_name(name)
        self.delete(template_piece)

    