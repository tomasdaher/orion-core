class GoalEvaluator:

    def evaluate(self, goal):

        progress = goal.progress_percentage()

        if progress >= 100:

            status = "completed"

        elif progress >= 70:

            status = "on_track"

        elif progress >= 30:

            status = "needs_attention"

        else:

            status = "critical"

        return {
            "goal": goal.name,
            "progress": progress,
            "status": status
        }