import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .base_service import EntityNotFoundError
from .company import CompanyService
from .device import DeviceService
from .family import FamilyService
from .port import PortService
from .preset import PresetService, ALLOWED_ROLES
from .protocol import ProtocolService
from .template import TemplateService, ALLOWED_TYPES

__all__ = [
    "CompanyService",
    "DeviceService",
    "FamilyService",
    "PortService",
    "PresetService",
    "ProtocolService",
    "TemplateService",
    "EntityNotFoundError",
    "ALLOWED_ROLES",
    "ALLOWED_TYPES",
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
            f"{config.username}:"
            f"{config.password}@"
            f"{config.host}:"
            f"{config.port}/"
            f"{config.database}"
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
        logger.error("Connection failed to %s: %s", connection_string, e)
