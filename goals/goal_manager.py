from goals.goal_models import Goal, GoalStatus
from goals.goal_tracker import GoalTracker
from goals.goal_evaluator import GoalEvaluator
from goals.goal_generator import GoalGenerator
from goals.goal_scheduler import GoalScheduler
from goals.goal_memory import GoalMemory


class GoalManager:

    def __init__(self, logger=None):

        self.goals = {}
        self.logger = logger

        self.tracker = GoalTracker()
        self.evaluator = GoalEvaluator()
        self.generator = GoalGenerator(logger=self.logger)
        self.scheduler = GoalScheduler(logger=self.logger)
        self.memory = GoalMemory()

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

            self.memory.record_completed(goal)

            if self.logger:
                self.logger.info(f"🏁 Goal completed: {goal.name}")

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

    # ----------------------------
    # REGISTER GOAL OBJECT
    # ----------------------------

    def register_goal(self, goal):

        self.goals[goal.id] = goal

        if self.logger:
            self.logger.info(f"🎯 Goal registered: {goal.name}")

        return goal


    # ----------------------------
    # AUTONOMOUS GOAL GENERATION
    # ----------------------------

    def generate_goals(self, state):

        new_goals = self.generator.generate(state, self)

        for goal in new_goals:

            self.register_goal(goal)

        return new_goals

    # ----------------------------
    # SCHEDULE GOALS
    # ----------------------------

    def scheduled_goals(self):

        goals = self.prioritized_goals()

        return self.scheduler.select_goals(goals)