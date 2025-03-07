import logging
from abc import ABC, abstractmethod
from typing import List

logger = logging.getLogger("COM")


class BaseDriver(ABC):
    @abstractmethod
    def __init__(self, on_open_sequence, comms_prompt_pattern, **driver):
        pass

    @abstractmethod
    def send_command(self, command: str) -> str:
        pass

    def execute(self, commands: str | List[str]) -> str:
        if isinstance(commands, str):
            return self.send_command(commands)
        elif isinstance(commands, list):
            return "".join(self.send_command(command) for command in commands)
        else:
            raise TypeError(
                f"BaseDriver.execute: argument must be str or List[str]. Given: {type(commands).__name__}"
            )

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
