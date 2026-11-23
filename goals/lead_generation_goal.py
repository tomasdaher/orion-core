from goals.goal_models import Goal, GoalPriority


class LeadGenerationGoal(Goal):

    def __init__(self):

        super().__init__(
            name="increase_lead_conversion",
            description="Capture and process leads automatically",
            metric="leads_processed",
            target_value=100,
            priority=GoalPriority.HIGH
        )

    def evaluate_success(self, state):

        lead = state.get("lead")

        if not lead:
            return False

        if lead.score > 50:
            return True

        return False