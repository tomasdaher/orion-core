class GoalTracker:

    def __init__(self):

        self.history = []

    def record(self, goal):

        snapshot = {
            "goal_id": goal.id,
            "name": goal.name,
            "progress": goal.progress_percentage(),
            "value": goal.current_value
        }

        self.history.append(snapshot)

    def get_history(self):

        return self.history