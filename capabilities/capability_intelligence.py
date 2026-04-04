from capabilities.registry import CapabilityRegistry


class CapabilityIntelligence:

    def __init__(self):
        self.registry = CapabilityRegistry()

    def analyze_capabilities(self):

        data = self.registry.load()

        insights = {
            "top_capabilities": [],
            "slow_capabilities": [],
            "unstable_capabilities": []
        }

        capabilities = data.get("capabilities", [])

        for capability in capabilities:

            metrics = capability.get("metrics", {})

            usage = metrics.get("usage_count", 0)
            success = metrics.get("success_count", 0)
            avg_time = metrics.get("avg_execution_time", 0)

            if usage == 0:
                continue

            success_rate = success / usage

            capability_info = {
                "name": capability["name"],
                "usage": usage,
                "success_rate": success_rate,
                "avg_time": avg_time
            }

            # 🔥 Best capabilities
            if success_rate > 0.9:
                insights["top_capabilities"].append(capability_info)

            # 🐢 Slow capabilities
            if avg_time > 2:
                insights["slow_capabilities"].append(capability_info)

            # ⚠️ Unstable capabilities
            if success_rate < 0.5:
                insights["unstable_capabilities"].append(capability_info)

        return insights