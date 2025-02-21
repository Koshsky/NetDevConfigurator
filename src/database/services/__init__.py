from .company_service import CompanyService
from .device_service import DeviceService
from .family_service import FamilyService
from .port_service import PortService
from .preset_service import PresetService
from .protocol_service import ProtocolService
from .template_service import TemplateService

from .exceptions import EntityNotFoundError

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
        "type": (
            "hostname",
            "VLAN",
            "ssh",
            "type-commutation",
            "STP",
            "credentials",
            "addr-set",
            "interface",
            "GW",
            "telnet",
            "SNMP",
            "ZTP",
            "jumbo",
            "priority",
        ),
        "role": (  # `common` suits for all
            "data",
            "ipmi",
            "icu",
            "or",
            "tsh",
            "video",
            "raisa_or",
            "raisa_agr",
        ),
    }
