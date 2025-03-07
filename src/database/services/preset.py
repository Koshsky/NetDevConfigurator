import logging
from typing import TYPE_CHECKING, Any, Dict, Generator, Tuple, List

from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from database.models import DevicePresets, Devices, Presets, Templates

from database.models import DevicePresets, Devices, Presets, Templates
from .base_service import BaseService, JsonType
from .device_preset import DevicePresetService
from .device import DeviceService
from .family import FamilyService
from .template import TemplateService

logger = logging.getLogger(__name__)
allowed_roles: Tuple[str, ...] = (  # `common` suits for all
    "data",
    "ipmi",
    "icu",
    "or",
    "tsh",
    "video",
    "raisa_or",
    "raisa_agr",
)


class PresetService(BaseService, DevicePresetService):
    """Service for managing preset-related database operations.

    This service handles creating, retrieving, and validating presets,
    including their associated device, templates, and configurations.
    """

    def __init__(self, db: Session) -> None:
        """Initializes PresetService with database services and models.

        Args:
            db: The SQLAlchemy database session.
        """
        logger.debug("Initializing PresetService")
        super().__init__(db, Presets)
        self.device_service = DeviceService(db)
        self.template_service = TemplateService(db)
        self.family_service = FamilyService(db)

    def create(self, **kwargs: Any) -> "Presets":
        """Creates a new preset with the given attributes.

        Args:
            **kwargs: Keyword arguments representing preset attributes.

        Returns:
            The newly created Presets instance.

        Raises:
            ValueError: If the provided role is invalid.
        """
        role = kwargs.get("role")
        if role not in allowed_roles:
            logger.error("Invalid role provided when creating a preset: %s", role)
            raise ValueError(
                f"Invalid role: '{role}'. Allowed roles are: {allowed_roles}"
            )
        logger.debug("Creating preset with data: %s", kwargs)
        return super().create(**kwargs)

    def get_info(self, preset: "Presets", check: bool = False) -> JsonType:
        """Retrieves comprehensive information about a preset.

        Args:
            preset: The Presets instance to retrieve information for.
            check: Whether to validate the preset configuration.

        Returns:
            A dictionary containing preset details, including associated device,
            family, role, description, and configuration.

        Raises:
            ValueError: If check is True and the preset configuration is invalid.
        """
        logger.debug("Retrieving information for preset: %s", preset.role)
        device = self.device_service.get_info_one(id=preset.device_id)
        if check and not self.validate(preset):
            logger.error(
                "Invalid preset configuration for device: %s, role: %s",
                device["name"],
                preset.role,
            )
            raise ValueError(
                f"Invalid preset configuration. device={device['name']}, role={preset.role}"
            )
        rows: List[Tuple["Presets", "DevicePresets", "Templates"]] = (
            self.db.query(Presets, DevicePresets, Templates)
            .join(DevicePresets, Presets.id == DevicePresets.preset_id)
            .join(Templates, DevicePresets.template_id == Templates.id)
            .join(Devices, Presets.device_id == Devices.id)
            .filter(Presets.id == preset.id)
            .order_by(DevicePresets.ordered_number)
            .all()
        )
        interfaces: Generator[str, None, None] = (
            port["interface"] for port in device["ports"]
        )
        preset_info: Dict[str, JsonType] = {
            "id": preset.id,
            "device": device["name"],
            "family": device["family"],
            "role": preset.role,
            "description": preset.description,
            "configuration": {
                f"{template.type if template.type != 'interface' else next(interfaces, 'INVALID INTERFACE')}": self.template_service.get_info(
                    template
                )
                for _, _, template in rows
            },
        }
        return preset_info
