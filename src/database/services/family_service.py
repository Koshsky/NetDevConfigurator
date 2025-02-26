from sqlalchemy.orm import Session

from database.models import Families
from .base_service import BaseService, JsonType
from .device_service import DeviceService


class FamilyService(BaseService):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Families)

    def get_info(self, family: Families) -> JsonType:
        associated_devices = DeviceService(self.db).get_all(family_id=family.id)
        return {
            "id": family.id,
            "name": family.name,
            "associated_devices": [device.name for device in associated_devices],
        }
