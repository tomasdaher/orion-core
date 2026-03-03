from abc import ABC, abstractmethod


class ExecutionRepository(ABC):

    @abstractmethod
    def save(self, request, state):
        pass
        