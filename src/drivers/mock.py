import logging

from .base_driver import BaseDriver

logger = logging.getLogger("mock")


class MockDriver(BaseDriver):
    def __init__(self, on_open_sequence, comms_prompt_pattern, **driver):
        self.on_open_sequence = on_open_sequence
        self.comms_prompt_pattern = comms_prompt_pattern

    def send_command(self, command):
        logger.info("Send: %s", command)
        return f"<resp>{command}<@resp>\n"

    def __enter__(self):
        self.execute(self.on_open_sequence)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
