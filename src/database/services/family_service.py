from sqlalchemy.orm import Session

from database.models import Families
from .base_service import BaseService
from .device_service import DeviceService


class FamilyService(BaseService):
    def __init__(self, db: Session):
        self.device_service = DeviceService(db)
        super().__init__(db, Families)

    def get_info(self, family: Families):
        associated_devices = self.device_service.get_all(family_id=family.id)
        return {
            "id": family.id,
            "name": family.name,
            "associated_devices": [device.name for device in associated_devices],
        }
