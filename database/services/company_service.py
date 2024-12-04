from sqlalchemy.orm import Session

from database.models.models import Companies


class CompanyService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Companies).all()

    def get_by_id(self, company_id: int):
        return self.db.query(Companies).filter(Companies.id == company_id).first()

    def create(self, company: Companies):
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def update(self, company_id: int, company_data: Companies):
        db_company = self.get_by_id(company_id)
        if not db_company:
            return None
        db_company.name = company_data.name
        self.db.commit()
        return db_company

    def get_by_name(self, name: str):
        return self.db.query(Companies).filter(Companies.name == name).first()

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
        