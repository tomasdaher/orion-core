import json
from typing import Any, Dict, List, Optional


class MemoryService:
    def __init__(self, repository):
        self.repository = repository

    def get_last_execution(self) -> Optional[Dict[str, Any]]:
        row = self.repository.get_last()
        return self._deserialize(row)

    def get_recent_executions(self, limit: int = 5) -> List[Dict[str, Any]]:
        rows = self.repository.get_recent(limit)
        return [self._deserialize(row) for row in rows]

    def get_recent(self, limit: int = 5):
        return self.get_recent_executions(limit)

    def get_by_objective(self, objective_name: str) -> List[Dict[str, Any]]:
        rows = self.repository.get_by_objective(objective_name)
        return [self._deserialize(row) for row in rows]

    def build_context(self, limit: int = 5) -> Dict[str, Any]:
        recent = self.get_recent_executions(limit)

        return {
            "recent_executions": recent,
            "total_recent": len(recent)
        }

    def _deserialize(self, row):

        import json

        try:
            state = json.loads(row[2])
        except Exception:
            # si el estado no puede deserializarse lo ignoramos
            state = {}

        return {
            "id": row[0],
            "objective": row[1],
            "state": state
        }