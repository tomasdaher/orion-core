from capabilities.registry import CapabilityRegistry
from capabilities.performance_tracker import CapabilityPerformanceTracker


class CapabilitySelector:

    def __init__(self):

        self.registry = CapabilityRegistry()
        self.performance = CapabilityPerformanceTracker()

    def select_best_capability(self, plan_steps):

        data = self.registry.load()
        capabilities = data.get("capabilities", [])

        if not capabilities:
            return None

        best_match = None
        best_score = 0

        for capability in capabilities:

            name = capability.get("name")
            steps = capability.get("steps", [])
            metrics = capability.get("metrics", {})

            usage = metrics.get("usage_count", 0)
            success = metrics.get("success_count", 0)

            if usage == 0:
                continue

            success_rate = success / usage

            # -----------------------------
            # STEP MATCHING (tu lógica)
            # -----------------------------

            overlap = len(set(steps) & set(plan_steps))
            overlap_score = overlap / max(len(plan_steps), 1)

            # -----------------------------
            # PERFORMANCE METRICS
            # -----------------------------

            stats = self.performance.get_stats(name)

            avg_time = stats.get("avg_time", 1)

            if avg_time <= 0:
                avg_time = 1

            speed_score = 1 / avg_time

            usage_score = min(usage / 100, 1)

            # -----------------------------
            # FINAL SCORE
            # -----------------------------

            score = (
                overlap_score * 0.5 +
                success_rate * 0.3 +
                speed_score * 0.1 +
                usage_score * 0.1
            )

            if score > best_score:

                best_score = score
                best_match = capability

        return best_match

    def select_from_registry(self):

        data = self.registry.load()
        capabilities = data.get("capabilities", [])

        if not capabilities:
            return None

        names = [c.get("name") for c in capabilities]

        if not names:
            return None

        return names[0]

    def explore_capability(self):

        import random

        data = self.registry.load()
        capabilities = data.get("capabilities", [])

        if not capabilities:
            return None

        return random.choice(capabilities)