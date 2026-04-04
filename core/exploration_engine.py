import random


class ExplorationEngine:

    def __init__(self, exploration_rate=0.2):
        """
        exploration_rate:
        Probabilidad de explorar nuevas estrategias
        """
        self.exploration_rate = exploration_rate

    def should_explore(self):

        return random.random() < self.exploration_rate

    def explore(self, execution_plan):

        if not execution_plan:
            return execution_plan

        steps = execution_plan.get("steps", [])

        # Si el plan está optimizado por capability, expandirlo
        if steps and steps[0].startswith("run_capability:"):

            return {
                "steps": [
                    "analyze_input",
                    "validate_data",
                    "execute_task",
                    "explore_optimization",
                    "store_result"
                ],
                "exploration": True
            }

        return execution_plan