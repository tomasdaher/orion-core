import time


class GoalScheduler:

    """
    Responsible for deciding which goals
    should be executed next.
    """

    def __init__(self, logger=None):

        self.logger = logger

        self.last_execution = {}

        # cooldown entre ejecuciones del mismo goal
        self.cooldown_seconds = 5

    # ------------------------------------------------
    # SELECT NEXT GOALS
    # ------------------------------------------------

    def select_goals(self, goals):

        now = time.time()

        selected = []

        for goal in goals:

            last_run = self.last_execution.get(goal.id, 0)

            if now - last_run >= self.cooldown_seconds:

                selected.append(goal)

                self.last_execution[goal.id] = now

                if self.logger:
                    self.logger.info(
                        f"📅 Scheduler selected goal: {goal.name}"
                    )

        return selected