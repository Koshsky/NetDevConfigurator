import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

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

logger = logging.getLogger("database.services")


def init_db_connection(config):
    """Initializes the database connection and services.

    Args:
        config: The configuration dictionary.

    Returns:
        A tuple containing the database session and services.

    Raises:
        SystemExit: If the database connection fails.
    """
    try:
        connection_string = (
            f"postgresql://"
            f"{config['username']}:"
            f"{config['password']}@"
            f"{config['host']}:"
            f"{config['port']}/"
            f"{config['database']}"
        )
        engine = create_engine(connection_string)
        session = sessionmaker(bind=engine)()
        db_services = {
            "company": CompanyService(session),
            "device": DeviceService(session),
            "family": FamilyService(session),
            "port": PortService(session),
            "preset": PresetService(session),
            "protocol": ProtocolService(session),
            "template": TemplateService(session),
        }

        # Проверка подключения
        session.execute(text("SELECT 1")).scalar()
        logger.info("Successful connection to database: %s", connection_string)
        return session, db_services

    except Exception as e:
        print(e)
        logger.error("Connection failed to %s: %s", connection_string, e)


def get_entity_collections(entity_services):
    """Retrieves collections of entity names.

    Args:
        entity_services: A dictionary of entity services.

    Returns:
        A dictionary containing tuples of entity names.
    """
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
