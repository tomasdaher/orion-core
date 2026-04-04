from planning.pipeline_template_library import PipelineTemplateLibrary
from planning.goal_capability_mapper import GoalCapabilityMapper


class GoalPlanTranslator:

    def __init__(self):

        self.templates = PipelineTemplateLibrary()
        self.mapper = GoalCapabilityMapper()

    # ---------------------------------
    # TRANSLATE GOAL → PLAN
    # ---------------------------------

    def translate(self, goal):

        if not goal:
            return None

        goal_name = goal.name

        # ------------------------------------------------
        # 1️⃣ TRY TEMPLATE
        # ------------------------------------------------

        template = self.templates.get_template(goal_name)

        if template:

            print(f"📚 Template pipeline used for goal: {goal_name}")

            return template

        # ------------------------------------------------
        # 2️⃣ TRY CAPABILITY MATCH
        # ------------------------------------------------

        mapped = self.mapper.map_goal_to_capabilities(goal)

        if mapped:

            print(f"🧠 Capability pipeline discovered for goal: {goal_name}")

            return [f"run_capability:{c}" for c in mapped]

        # ------------------------------------------------
        # 3️⃣ NO PLAN FOUND
        # ------------------------------------------------

        print(f"⚠️ No plan found for goal: {goal_name}")

        return None