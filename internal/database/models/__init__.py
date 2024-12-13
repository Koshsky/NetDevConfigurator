from .models import (
    Companies,
    Firmwares,
    Protocols,
    Devices,
    DeviceFirmwares,
    DeviceProtocols,
    DevicePorts,
    Families,
    Ports,
    TemplatePieces
)

# sqlacodegen --outfile ./internal/database/models/models.py postgresql://postgres:postgres@localhost:5432/device_registry