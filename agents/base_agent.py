from abc import ABC, abstractmethod


class BaseAgent(ABC):
    name: str = "BaseAgent"

    @abstractmethod
    def execute(self, state: dict) -> dict:
        pass