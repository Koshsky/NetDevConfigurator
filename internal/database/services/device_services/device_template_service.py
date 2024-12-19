from functools import wraps
from sqlalchemy.orm import Session
from sqlalchemy import func  # Add this import at the top of the file

from internal.database.models import DeviceTemplates, Templates
from ..decorators import transactional
from ..base_service import BaseService

class DeviceTemplateService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, DeviceTemplates)

    def get_device_templates(self, device_id: int):
        return (
            self.db.query(DeviceTemplates, Templates)
                .join(Templates, DeviceTemplates.port_id == Templates.id)
                .filter(DeviceTemplates.device_id == device_id)
                .all()
        )

    def _get_max_ordered_number(self, device_id: int, preset: str) -> int:
        return self.db.query(func.max(DeviceTemplates.ordered_number)) \
            .filter(DeviceTemplates.device_id == device_id, DeviceTemplates.preset == preset) \
            .scalar() or 0

    @transactional
    def push_back(self, device_id: int, template_id: int, preset: str):
        max_ordered_number = self._get_max_ordered_number(device_id, preset)

        device_template = DeviceTemplates(
            device_id=device_id, 
            template_id=template_id, 
            ordered_number=max_ordered_number + 1,
            preset=preset
        )

        self.db.add(device_template)
        return device_template

    @transactional
    def insert(self, device_id: int, template_id: int, ordered_number: int, preset: str):
        max_ordered_number = self._get_max_ordered_number(device_id, preset)
        if ordered_number > max_ordered_number + 1:
            raise ValueError(f"The ordered_number={ordered_number} value exceeds the allowed limit for device_id={device_id}.")
        # Shift existing templates
        self.db.query(DeviceTemplates) \
            .filter(DeviceTemplates.device_id == device_id,
                    DeviceTemplates.preset == preset,
                    DeviceTemplates.ordered_number >= ordered_number) \
            .update({DeviceTemplates.ordered_number: DeviceTemplates.ordered_number + 1}, 
                    synchronize_session=False)

        new_device_template = DeviceTemplates(
            device_id=device_id,
            template_id=template_id,
            ordered_number=ordered_number,
            preset=preset
        )

        self.db.add(new_device_template)
        return new_device_template
