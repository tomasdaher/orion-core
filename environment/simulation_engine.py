import random


class SimulationEngine:

    def run(self, scenario):

        print("🧪 Running simulation")

        results = []

        for step in scenario.get("steps", []):

            outcome = self.execute_step(step)

            results.append(outcome)

        return results

    def execute_step(self, step):

        success_probability = step.get("success_rate", 0.5)

        success = random.random() < success_probability

        return {
            "step": step.get("name"),
            "success": success
        }