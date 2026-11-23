class GoalOptimizer:

    def recommend_strategy(self, goal):

        progress = goal.progress_percentage()

        history = goal.history

        # progreso lento
        if len(history) > 3:

            recent = history[-3:]

            values = [h["value"] for h in recent]

            if max(values) - min(values) < 2:

                return "change_strategy"

        if progress < 25:
            return "increase_execution"

        if progress < 75:
            return "maintain_strategy"

        return "final_push"