"""
Database configuration module.
"""

import os


def get_database_url() -> str:
    """
    Get database URL from environment variable or return default value.

    Returns:
        str: Database URL
    """
    return os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/device_registry"
    )
