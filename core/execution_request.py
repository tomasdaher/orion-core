from enum import Enum
import uuid


class Objective(Enum):
    PROCESS = "process"
    VALIDATE = "validate"
    EXECUTE = "execute"


class ExecutionRequest:
    def __init__(self, objective: Objective, data: dict):
        self.execution_id = str(uuid.uuid4())
        self.objective = objective
        self.data = data