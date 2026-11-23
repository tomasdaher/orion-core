class GoalEvaluator:

    def evaluate(self, goal):

        progress = goal.progress_percentage()

        if goal.is_completed():
            status = "completed"

        elif progress >= 70:
            status = "on_track"

        elif progress >= 40:
            status = "needs_attention"

        else:
            status = "critical"

        return {
            "goal_id": goal.id,
            "goal": goal.name,
            "progress": progress,
            "status": status
        }