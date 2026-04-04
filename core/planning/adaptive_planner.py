import random


class AdaptivePlanner:

    def __init__(self):
        self.exploration_rate = 0.2

    def choose_strategy(self, memory_insights=None):
        """
        Decide qué estrategia usar:
        - memory
        - exploration
        - hybrid
        """

        if memory_insights:
            top = memory_insights.get("top_capabilities", [])

            if top and random.random() > self.exploration_rate:
                return "memory"

        if random.random() < self.exploration_rate:
            return "exploration"

        return "hybrid"

    def adjust_exploration(self, success_rate):

        if success_rate > 0.8:
            self.exploration_rate *= 0.9

        elif success_rate < 0.4:
            self.exploration_rate *= 1.2

        self.exploration_rate = max(0.05, min(self.exploration_rate, 0.5))