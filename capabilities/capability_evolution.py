from capabilities.registry import CapabilityRegistry


class CapabilityEvolution:

    def __init__(self):

        self.registry = CapabilityRegistry()

    def analyze(self):

        capabilities = self.registry.list_capabilities()

        insights = {
            "top_capabilities": [],
            "weak_capabilities": [],
            "unused_capabilities": []
        }

        for cap in capabilities:

            metrics = cap.get("metrics", {})

            usage = metrics.get("usage_count", 0)
            success = metrics.get("success_count", 0)
            avg_time = metrics.get("avg_execution_time", 0)

            success_rate = 0

            if usage > 0:
                success_rate = success / usage

            capability_info = {
                "name": cap["name"],
                "usage": usage,
                "success_rate": success_rate,
                "avg_time": avg_time
            }

            # mejores capabilities
            if usage >= 3 and success_rate >= 0.8:
                insights["top_capabilities"].append(capability_info)

            # capabilities débiles
            if usage >= 3 and success_rate < 0.4:
                insights["weak_capabilities"].append(capability_info)

            # casi nunca usadas
            if usage <= 1:
                insights["unused_capabilities"].append(capability_info)

        return insights

    def evolve(self):

        data = self.registry.load()

        capabilities = data.get("capabilities", [])

        evolved = []

        for cap in capabilities:

            metrics = cap.get("metrics", {})

            usage = metrics.get("usage_count", 0)
            success = metrics.get("success_count", 0)

            success_rate = 0

            if usage > 0:
                success_rate = success / usage

            # marcar capabilities débiles
            if usage >= 3 and success_rate < 0.4:

                cap["status"] = "weak"
                evolved.append(cap["name"])

            # marcar capabilities fuertes
            if usage >= 5 and success_rate >= 0.9:

                cap["status"] = "stable"
                evolved.append(cap["name"])

        data["capabilities"] = capabilities

        self.registry.save(data)

        return evolved
