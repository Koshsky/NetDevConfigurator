from sqlalchemy.orm import Session

from internal.database.models import Companies
from .base_service import BaseService
from .device_services.device_service import DeviceService


class CompanyService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Companies)
        self.device_service = DeviceService(db)

    def get_info(self, company: Companies):
        associated_devices = self.device_service.get_devices_by_company_id(company.id)
        return {
            "id": company.id,
            "name": company.name,
            "associated_devices": [device.name for device in associated_devices]
        }
