from capabilities.registry import CapabilityRegistry


class GoalCapabilityMapper:

    def __init__(self):

        self.registry = CapabilityRegistry()

    def map_goal_to_capabilities(self, goal):

        capabilities = self.registry.list_capabilities()

        goal_name = goal.name.lower()

        matched = []

        for capability in capabilities:

            name = capability.get("name", "").lower()

            if goal_name in name:
                matched.append(name)

        return matched