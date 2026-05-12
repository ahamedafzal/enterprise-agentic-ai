from abc import ABC, abstractmethod
from typing import Any
import structlog

logger = structlog.get_logger()

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logger.bind(agent=name)

    @abstractmethod
    async def run(self, input_data: dict) -> dict:
        pass

    def log(self, message: str, **kwargs):
        self.logger.info(message, **kwargs)