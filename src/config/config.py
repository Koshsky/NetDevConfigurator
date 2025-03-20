from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class AppConfig:
    """Конфигурация приложения."""

    # Настройки сетки
    grid_columns: int = 8
    templates_width: int = 6
    templates_allow_none: bool = True
    interfaces_width: int = 12
    interfaces_allow_none: bool = False

    # Стили интерфейса
    background_color: str = "#ffffff"
    foreground_color: str = "#000000"
    main_color: str = "#00e0ce"
    second_color: str = "#F4FAFA"

    font: Tuple[str, int] = ("Helvetica", 10)
    padding: Tuple[int, int] = (5, 5)
    border_width: int = 1


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
    default_cert: str = "MVS"
    serial_port: str = "/dev/ttyUSB0"
    mvs_network: str = "192.168.3.0/24"
    backup_folder: str = "./.backups/"
