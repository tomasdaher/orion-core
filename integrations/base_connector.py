from abc import ABC, abstractmethod


class BaseConnector(ABC):

    name = "BaseConnector"

    def __init__(self, config=None):

        self.config = config or {}

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def read(self, query=None):
        pass

    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def execute(self, action, payload=None):
        pass