import os
import uuid
from typing import TYPE_CHECKING

from config import config

from .environ import del_env, get_env, set_env
from .router_conversation import env_converter

if TYPE_CHECKING:
    from database.models import Device

__all__ = ["get_env", "set_env", "del_env"]


def initialize_device_environment(db_services, device: "Device") -> None:
    """Updates the environment variables related to the device."""
    del_env("DEV_ROLE")

    set_env("DEV_NAME", device.name)
    set_env("DEV_TYPE", device.dev_type)
    company_name = db_services["company"].get_one(id=device.company_id).name
    set_env("DEV_COMPANY", company_name)

    if os.environ["DEV_TYPE"] == "router":
        for env_param, env_value in config.router.__dict__.items():
            if not env_param.startswith("_"):
                set_env(env_param, env_value)
        set_env("MODEL", env_converter.to_machine("MODEL", device.name))
