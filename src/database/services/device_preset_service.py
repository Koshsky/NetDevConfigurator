from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import DevicePresets, Templates, Presets
from .device_service import DeviceService
from .decorators import transactional


def check_template_role(func):
    def wrapper(self, preset: Presets, template: Templates, *args, **kwargs):
        if template.role not in ["common", preset.role]:
            raise ValueError("Template and preset have different roles")
        return func(self, preset, template, *args, **kwargs)

    return wrapper


class DevicePresetService:
    def __init__(self, db: Session):
        self.db = db
        self.device_service = DeviceService(db)

    @check_template_role
    @transactional
    def push_back(self, preset: Presets, template: Templates):
        if self.validate(preset) and template.type == "interface":
            raise ValueError(
                "Cannot insert interface template into preset. Preset has all interface descriptions"
            )
        max_ordered_number = self._get_max_ordered_number(preset.id)

        device_preset = DevicePresets(
            template_id=template.id,
            ordered_number=max_ordered_number + 1,
            preset_id=preset.id,
        )

        self.db.add(device_preset)
        return device_preset

    @check_template_role
    @transactional
    def insert(self, preset: Presets, template: Templates, ordered_number: int):
        if self.validate(preset) and template.type == "interface":
            raise ValueError(
                "Cannot insert interface template into preset. Preset has all interface descriptions"
            )
        max_ordered_number = self._get_max_ordered_number(preset.id)
        if ordered_number > max_ordered_number + 1:
            raise ValueError(
                f"The ordered_number={ordered_number} value exceeds the allowed limit for preset_id={preset.id}."
            )
        # Shift existing templates
        self.db.query(DevicePresets).filter(
            DevicePresets.preset_id == preset.id,
            DevicePresets.ordered_number >= ordered_number,
        ).update(
            {DevicePresets.ordered_number: DevicePresets.ordered_number + 1},
            synchronize_session=False,
        )

        new_device_preset = DevicePresets(
            template_id=template.id, ordered_number=ordered_number, preset_id=preset.id
        )

        self.db.add(new_device_preset)
        return new_device_preset

    def copy(self, source_preset, destination_preset):
        if source_preset == destination_preset:
            raise ValueError("preset_from is preset_to!")
        if source_preset.role != destination_preset.role:
            raise ValueError("Preset roles are different!")
        dev1 = self.device_service.get_by_id(source_preset.device_id)
        dev2 = self.device_service.get_by_id(destination_preset.device_id)
        if dev1.family_id != dev2.family_id:
            raise ValueError("Devices are from different families!")

        self._clear(destination_preset.id)
        records = (
            self.db.query(DevicePresets).filter_by(preset_id=source_preset.id).all()
        )
        for record in records:
            new_record = record.__class__(
                preset_id=destination_preset.id,
                template_id=record.template_id,
                ordered_number=record.ordered_number,
            )
            self.db.add(new_record)

        self.db.commit()

    @transactional
    def remove(self, preset_id: int, ordered_number: int):
        self.db.query(DevicePresets).filter(
            DevicePresets.preset_id == preset_id,
            DevicePresets.ordered_number == ordered_number,
        ).delete(synchronize_session=False)
        # Shift existing templates
        self.db.query(DevicePresets).filter(
            DevicePresets.preset_id == preset_id,
            DevicePresets.ordered_number > ordered_number,
        ).update(
            {DevicePresets.ordered_number: DevicePresets.ordered_number - 1},
            synchronize_session=False,
        )

    def validate(self, preset):
        described_interfaces = len(
            self.db.query(DevicePresets)
            .join(Templates, DevicePresets.template_id == Templates.id)
            .filter(DevicePresets.preset_id == preset.id)
            .filter(Templates.type == "interface")
            .all()
        )
        device_ports = len(
            self.device_service.get_info_by_id(preset.device_id)["ports"]
        )
        if described_interfaces > device_ports:
            raise ValueError(
                f"More interfaces are described in the preset than in the device: {described_interfaces}"
            )

        return described_interfaces == device_ports

    def _get_max_ordered_number(self, preset_id: int) -> int:
        return (
            self.db.query(func.max(DevicePresets.ordered_number))
            .filter(DevicePresets.preset_id == preset_id)
            .scalar()
            or 0
        )

    def _clear(self, preset_id):
        self.db.query(DevicePresets).filter(
            DevicePresets.preset_id == preset_id
        ).delete()
        self.db.commit()
