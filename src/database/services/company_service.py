from sqlalchemy.orm import Session

from database.models import Companies
from .base_service import BaseService, JsonType
from .device_service import DeviceService


class CompanyService(BaseService):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Companies)

    def get_info(self, company: Companies) -> JsonType:
        associated_devices = DeviceService(self.db).get_all(company_id=company.id)
        return {
            "id": company.id,
            "name": company.name,
            "associated_devices": [device.name for device in associated_devices],
        }
