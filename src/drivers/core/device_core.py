from abc import ABC, abstractmethod
from typing import List, Union


class DeviceCore(ABC):
    # Common fields
    comment_symbol: str
    comms_prompt_pattern: str
    open_sequence: List[str]
    reload: Union[str, List[str]]
    show_run: str

    @property
    @abstractmethod
    def update_startup_config(self) -> Union[str, List[str]]:
        """Command to update startup config"""
        pass

    @property
    @abstractmethod
    def base_configure_192(self) -> List[str]:
        """Base configuration for IP 192.168.1.x"""
        pass

    @property
    @abstractmethod
    def load_firmware(self) -> str:
        """Command to load firmware"""
        pass
