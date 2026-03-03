import json
import os
from datetime import datetime
from enum import Enum


class PersistenceManager:
    def __init__(self, base_path="storage/executions"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def _serialize(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, dict):
            return {k: self._serialize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._serialize(v) for v in obj]
        return obj

    def save_execution(self, request, state):
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")

        filename = f"execution_{timestamp}.json"
        filepath = os.path.join(self.base_path, filename)

        execution_record = {
            "execution_id": request.execution_id,
            "timestamp": timestamp,
            "objective": request.objective.value,
            "input_data": request.data,
            "final_state": self._serialize(state.get_all())
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(execution_record, f, indent=4)

        return filepath