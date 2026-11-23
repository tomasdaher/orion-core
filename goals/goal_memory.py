class GoalMemory:

    """
    Stores historical data about goals.
    Useful for long-term learning.
    """

    def __init__(self):

        self.completed_goals = []

        self.failed_goals = []

    # ------------------------------------------------
    # RECORD COMPLETION
    # ------------------------------------------------

    def record_completed(self, goal):

        self.completed_goals.append(goal.to_dict())

    # ------------------------------------------------
    # RECORD FAILURE
    # ------------------------------------------------

    def record_failed(self, goal):

        self.failed_goals.append(goal.to_dict())

    # ------------------------------------------------
    # STATS
    # ------------------------------------------------

    def stats(self):

        return {
            "completed": len(self.completed_goals),
            "failed": len(self.failed_goals)
        }