from capabilities.registry import CapabilityRegistry


class CapabilityRanker:

    def __init__(self):
        self.registry = CapabilityRegistry()

    def rank_capabilities(self):

        data = self.registry.load()

        ranked = []

        for capability in data.get("capabilities", []):

            metrics = capability.get("metrics", {})

            usage = metrics.get("usage_count", 0)
            success = metrics.get("success_count", 0)
            avg_time = metrics.get("avg_execution_time", 0)

            if usage == 0:
                continue

            success_rate = success / usage

            # Score de eficiencia
            score = success_rate

            if avg_time > 0:
                score = score / avg_time

            ranked.append({
                "name": capability["name"],
                "score": score,
                "success_rate": success_rate,
                "avg_time": avg_time
            })

        ranked.sort(key=lambda x: x["score"], reverse=True)

        return ranked

    def best_capability(self):

        ranked = self.rank_capabilities()

        if not ranked:
            return None

        return ranked[0]