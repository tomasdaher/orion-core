class GoalOptimizer:

    def recommend_strategy(self, goal):

        progress = goal.progress_percentage()

        if progress < 20:

            return "change_strategy"

        if progress < 50:

            return "increase_execution"

        if progress < 80:

            return "maintain_strategy"

        return "final_push"