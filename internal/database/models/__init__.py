from .models import (
    Companies,
    Firmwares,
    Protocols,
    Devices,
    DeviceFirmwares,
    DeviceProtocols,
    Families
)

# sqlacodegen --outfile ./internal/database/models/models.py postgresql://postgres:postgres@localhost:5432/device_registry