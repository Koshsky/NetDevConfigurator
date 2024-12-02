from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models.company import Company
import logging

logging.basicConfig(level=logging.INFO)

class CompanyService:
    def __init__(self, session: Session):
        self.session = session

    def create_company(self, name: str, address: str = None) -> Company:
        try:
            new_company = Company(name=name, address=address)
            self.session.add(new_company)
            self.session.commit()
            logging.info(f"Company created: {new_company}")
            return new_company
        except SQLAlchemyError as e:
            self.session.rollback()
            logging.error(f"Error creating company: {e}")
            raise

    def get_company(self, company_id: int) -> Company:
        return self.session.query(Company).filter_by(id=company_id).first()

    def get_all_companies(self):
        return self.session.query(Company).all()

    def update_company(self, company_id: int, name: str = None, address: str = None) -> Company:
        company = self.get_company(company_id)
        if company:
            if name:
                company.name = name
            if address:
                company.address = address
            self.session.commit()
            logging.info(f"Company updated: {company}")
        return company

    def delete_company(self, company_id: int) -> bool:
        company = self.get_company(company_id)
        if company:
            self.session.delete(company)
            self.session.commit()
            logging.info(f"Company deleted: {company}")
            return True
        return False