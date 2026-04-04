from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ExecutionResult:
    objective: str
    status: str
    agents_used: List[str]
    result: str
    execution_time: float
    timestamp: datetime