from .models import (
    Companies,
    Firmwares,
    Protocols,
    Families,
    Ports,
    Templates,
    
    Devices,
    DeviceFirmwares,
    DeviceProtocols,
    DeviceTemplates,
    DevicePorts,
)

# sqlacodegen --outfile ~/NetDevConfigurator/internal/database/models/models.py postgresql://postgres:postgres@localhost:5432/device_registry