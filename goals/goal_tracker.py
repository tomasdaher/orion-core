class GoalTracker:

    def __init__(self):

        self.goal_histories = {}

    def record(self, goal):

        if goal.id not in self.goal_histories:
            self.goal_histories[goal.id] = []

        snapshot = {
            "goal_id": goal.id,
            "name": goal.name,
            "progress": goal.progress_percentage(),
            "value": goal.current_value
        }

        self.goal_histories[goal.id].append(snapshot)

    def get_history(self, goal_id):

        return self.goal_histories.get(goal_id, [])