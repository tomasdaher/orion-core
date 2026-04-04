class SelfReflectionEngine:

    def __init__(self):
        self.failures = []
        self.insights = []

    def record_failure(self, execution_plan, reason):

        self.failures.append({
            "plan": execution_plan,
            "reason": reason
        })

    def analyze_failures(self):

        patterns = {}

        for f in self.failures:

            plan = tuple(f.get("plan", {}).get("steps", []))

            if plan not in patterns:
                patterns[plan] = 0

            patterns[plan] += 1

        insights = []

        for p, count in patterns.items():

            if count >= 3:
                insights.append({
                    "problematic_pipeline": list(p),
                    "failures": count
                })

        self.insights = insights

        return insights