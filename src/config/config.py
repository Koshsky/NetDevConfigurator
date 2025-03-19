from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class AppConfig:
    """Конфигурация приложения."""

    grid_columns: int = 8
    templates_width: int = 6
    templates_allow_none: bool = True
    interfaces_width: int = 12
    interfaces_allow_none: bool = False


@dataclass
class DatabaseConfig:
    """Конфигурация базы данных."""

    host: str = "localhost"
    port: int = 5432
    database: str = "device_registry"
    username: str = "postgres"
    password: str = "postgres"


@dataclass
class TFTPConfig:
    """Конфигурация TFTP сервера."""

    address: str = "192.168.3.105"
    port: int = 69
    folder: str = "/srv/tftp"


@dataclass
class HostConfig:
    """Конфигурация хоста."""

    address: List[str] = field(
        default_factory=lambda: [
            "79.134.218.38",
            "192.168.3.201",
            "192.168.0.1",
            "10.4.0.3",
        ]
    )
    port: List[str] = field(default_factory=lambda: ["22"])
    username: List[str] = field(default_factory=lambda: ["admin", "mvsadmin"])
    password: List[str] = field(
        default_factory=lambda: [
            "MVS_admin",
            "MVS_admin20",
            "admin",
            "password",
            "1234",
        ]
    )


@dataclass
class RouterConversion:
    """Конвертация значений роутера."""

    model_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "ESR20": "1",
            "ESR21": "2",
            "ESR31": "3",
            "esr20": "1",
            "esr21": "2",
            "esr31": "3",
        }
    )
    type_complex_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "Standard": "1",
            "All-in-one": "2",
        }
    )
    vers_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "1.23 and newer": "1",
            "old": "2",
        }
    )
    vpn_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "YES": "1",
            "NO": "2",
        }
    )
    teleport_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "YES": "1",
            "NO": "2",
        }
    )
    raisa_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "YES": "1",
            "NO": "2",
        }
    )
    trueconf_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "YES": "1",
            "NO": "2",
        }
    )
    trueroom_conversion: Dict[str, str] = field(
        default_factory=lambda: {
            "YES": "1",
            "NO": "2",
        }
    )


@dataclass
class RouterConfig:
    """Конфигурация роутера."""

    public_ip: str = "192.168.3.231"
    public_mask: int = 24
    gw: str = "192.168.3.1"
    vers: int = 1
    type_complex: int = 1
    stream_count: int = 13
    vpn: int = 1
    teleport: int = 2
    ph_count: int = 15
    raisa: int = 1
    raisa_ip: str = "192.168.3.232"
    trueconf: int = 1
    trueroom: int = 1
    trueroom_count: int = 20
    trueroom_ip1: str = "192.168.3.230"


@dataclass
class Config:
    """Основной класс конфигурации."""

    app: AppConfig = field(default_factory=AppConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    tftp: TFTPConfig = field(default_factory=TFTPConfig)
    host: HostConfig = field(default_factory=HostConfig)
    router: RouterConfig = field(default_factory=RouterConfig)
    router_conversion: RouterConversion = field(default_factory=RouterConversion)
    default_cert: str = "MVS"
    serial_port: str = "/dev/ttyUSB0"
    mvs_network: str = "192.168.3.0/24"
    backup_folder: str = "./.backups/"
