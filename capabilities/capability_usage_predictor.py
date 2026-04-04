import logging
from collections import defaultdict


class CapabilityUsagePredictor:

    """
    Predicts which capabilities are likely to be used
    based on historical execution patterns.
    """

    def __init__(self):

        self.logger = logging.getLogger("Orion")

        # capability transition frequency
        self.transitions = defaultdict(lambda: defaultdict(int))

    def learn_from_history(self, execution_history):

        """
        Learn transitions between capabilities
        from execution history.
        """

        if not execution_history:
            return

        for execution in execution_history:

            for i in range(len(execution) - 1):

                current_step = execution[i]
                next_step = execution[i + 1]

                if current_step.startswith("run_capability:") and next_step.startswith("run_capability:"):

                    current_cap = current_step.split(":")[1]
                    next_cap = next_step.split(":")[1]

                    self.transitions[current_cap][next_cap] += 1

        self.logger.info("🧠 Capability usage predictor updated")

    def predict_next(self, capability_name):

        """
        Predict the most likely next capability.
        """

        next_caps = self.transitions.get(capability_name)

        if not next_caps:
            return None

        predicted = max(next_caps, key=next_caps.get)

        return predicted

    def optimize_plan(self, plan):

        """
        Suggest capability ordering optimizations.
        """

        steps = plan.get("steps", [])

        optimized = []

        for step in steps:

            optimized.append(step)

            if step.startswith("run_capability:"):

                cap = step.split(":")[1]

                prediction = self.predict_next(cap)

                if prediction:

                    predicted_step = f"run_capability:{prediction}"

                    if predicted_step not in optimized:
                        optimized.append(predicted_step)

        return {"steps": optimized}