from goals.goal_models import Goal, GoalStatus
from goals.goal_tracker import GoalTracker
from goals.goal_evaluator import GoalEvaluator


class GoalManager:

    def __init__(self, logger=None):

        self.goals = {}
        self.logger = logger

        self.tracker = GoalTracker()
        self.evaluator = GoalEvaluator()

    # ----------------------------
    # CREATE GOAL
    # ----------------------------

    def create_goal(
        self,
        name,
        description,
        metric,
        target_value,
        priority
    ):

        goal = Goal(
            name,
            description,
            metric,
            target_value,
            priority
        )

        self.goals[goal.id] = goal

        if self.logger:
            self.logger.info(f"🎯 Goal created: {name}")

        return goal

    # ----------------------------
    # UPDATE PROGRESS
    # ----------------------------

    def update_goal(self, goal_id, value):

        goal = self.goals.get(goal_id)

        if not goal:
            return None

        goal.update_progress(value)

        self.tracker.record(goal)

        if goal.is_completed():
            goal.status = GoalStatus.COMPLETED

        return goal

    # ----------------------------
    # EVALUATE GOALS
    # ----------------------------

    def evaluate_goals(self):

        insights = []

        for goal in self.goals.values():

            result = self.evaluator.evaluate(goal)

            insights.append(result)

        return insights

    # ----------------------------
    # GET ACTIVE GOALS
    # ----------------------------

    def active_goals(self):

        return [
            g for g in self.goals.values()
            if g.status == GoalStatus.ACTIVE
        ]

    # ----------------------------
    # PRIORITIZE
    # ----------------------------

    def prioritized_goals(self):

        return sorted(
            self.active_goals(),
            key=lambda g: g.priority,
            reverse=True
        )