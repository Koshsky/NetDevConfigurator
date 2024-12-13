from sqlalchemy.orm import Session

from internal.database.models import Companies


class CompanyService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Companies).order_by(Companies.name).all()

    def get_by_id(self, company_id: int):
        return self.db.query(Companies).filter(Companies.id == company_id).first()
        
    def get_by_name(self, name: str):
        return self.db.query(Companies).filter(Companies.name == name).first()

    def create(self, company: dict):
        company = Companies(**company)
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def delete(self, company):
        if company:
            self.db.delete(company)
            self.db.commit()

    def delete_by_name(self, name: str):
        db_company = self.get_by_name(name)
        self.delete(db_company)

    def delete_by_id(self, company_id: int):
        db_company = self.get_by_id(company_id)
        self.delete(db_company)
        