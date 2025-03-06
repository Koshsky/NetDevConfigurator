from .company import CompanyService
from .device import DeviceService
from .exceptions import EntityNotFoundError
from .family import FamilyService
from .port import PortService
from .preset import PresetService, allowed_roles
from .protocol import ProtocolService
from .template import TemplateService, allowed_types

__all__ = [
    "CompanyService",
    "DeviceService",
    "FamilyService",
    "PortService",
    "PresetService",
    "ProtocolService",
    "TemplateService",
    "EntityNotFoundError",
]


def setup_database_services(session):
    return {
        "company": CompanyService(session),
        "device": DeviceService(session),
        "family": FamilyService(session),
        "port": PortService(session),
        "preset": PresetService(session),
        "protocol": ProtocolService(session),
        "template": TemplateService(session),
    }


def prepare_entity_collections(entity_services):
    return {
        "company": tuple(
            company.name for company in entity_services["company"].get_all()
        ),
        "family": tuple(family.name for family in entity_services["family"].get_all()),
        "device": tuple(device.name for device in entity_services["device"].get_all()),
        "protocol": tuple(
            protocol.name for protocol in entity_services["protocol"].get_all()
        ),
        "port": tuple(port.name for port in entity_services["port"].get_all()),
        "template": tuple(
            set({template.name for template in entity_services["template"].get_all()})
        ),
        "template_type": allowed_types,
        "role": allowed_roles,
    }
