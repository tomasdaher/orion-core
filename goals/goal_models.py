import uuid
import time


class GoalStatus:
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class GoalPriority:
    LOW = 1
    MEDIUM = 5
    HIGH = 10
    CRITICAL = 20


class Goal:

    def __init__(
        self,
        name,
        description,
        metric,
        target_value,
        priority=GoalPriority.MEDIUM
    ):

        self.id = str(uuid.uuid4())

        self.name = name
        self.description = description

        self.metric = metric
        self.target_value = target_value

        self.priority = priority

        self.current_value = 0
        self.status = GoalStatus.ACTIVE

        self.created_at = time.time()
        self.updated_at = time.time()

        self.history = []

    def update_progress(self, value):

        self.current_value = value
        self.updated_at = time.time()

        self.history.append({
            "timestamp": time.time(),
            "value": value
        })

    def progress_percentage(self):

        if self.target_value == 0:
            return 0

        return min(100, (self.current_value / self.target_value) * 100)

    def is_completed(self):

        return self.current_value >= self.target_value

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "metric": self.metric,
            "target": self.target_value,
            "current": self.current_value,
            "progress": self.progress_percentage(),
            "status": self.status,
            "priority": self.priority
        }