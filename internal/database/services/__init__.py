# services/__init__.py

from .company_service import CompanyService
from .firmware_service import FirmwareService, determine_firmware_type
from .protocol_service import ProtocolService
from .port_service import PortService
from .family_service import FamilyService
from .template_service import TemplateService
from .device_services.device_firmware_service import DeviceFirmwareService
from .device_services.device_protocol_service import DeviceProtocolService
from .device_services.device_port_service import DevicePortService
from .device_services.device_service import DeviceService
from .device_services.device_template_service import DeviceTemplateService

from .exceptions import EntityNotFoundError


def setup_database_services(session):
    return {
        'company': CompanyService(session),
        'family': FamilyService(session),
        'device': DeviceService(session),
        'firmware': FirmwareService(session),
        'protocol': ProtocolService(session),
        'port': PortService(session),
        'device_firmware': DeviceFirmwareService(session),
        'device_protocol': DeviceProtocolService(session),
        'device_port': DevicePortService(session),
        'template': TemplateService(session),
        'device_template': DeviceTemplateService(session)
    }

def prepare_entity_collections(entity_services):
    return dict(
        companies=tuple(
            company.name for company in entity_services["company"].get_all()
        ),
        families=tuple(
            family.name for family in entity_services["family"].get_all()
        ),
        devices=tuple(
            device.name for device in entity_services["device"].get_all()
        ),
        protocols=tuple(
            protocol.name for protocol in entity_services["protocol"].get_all()
        ),
        ports=(None,)
        + tuple(port.name for port in entity_services["port"].get_all()),
        templates=tuple(set(
            {
                template.name
                for template in entity_services['template'].get_all()
            }
        )),
        template_types=(
            'header',
            'hostname',
            'VLAN',
            'ssh',
            'type-commutation',
            'STP',
            'credentials',
            'addr-set',
            'interface',
            'GW',
            'telnet',
            'SNMP',
            'ZTP',
            'jumbo',
            'priority',
        ),
        roles=(  # common suits for all
            'data',
            'ipmi',
            'or',
            'tsh',
            'video',
            'raisa_or',
            'raisa_agr',
        ),
    )
