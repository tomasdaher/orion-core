from goals.goal_models import GoalPriority
from goals.lead_generation_goal import LeadGenerationGoal


class GoalGenerator:

    """
    Generates new goals for the system based on
    current state, performance and capabilities.
    """

    def __init__(self, logger=None):

        self.logger = logger

    # ------------------------------------------------
    # MAIN GENERATION ENTRY
    # ------------------------------------------------

    def generate(self, state, goal_manager):

        new_goals = []

        # ------------------------------------------------
        # LEAD GENERATION GOAL
        # ------------------------------------------------

        leads_processed = state.get("leads_processed", 0)

        active_goals = goal_manager.active_goals()

        has_lead_goal = any(
            g.name == "increase_lead_conversion"
            for g in active_goals
        )

        if not has_lead_goal and leads_processed < 50:

            goal = LeadGenerationGoal()

            new_goals.append(goal)

            if self.logger:
                self.logger.info("🧠 GoalGenerator created LeadGenerationGoal")

        return new_goals