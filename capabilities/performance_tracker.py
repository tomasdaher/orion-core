import time
from capabilities.registry import CapabilityRegistry


class CapabilityPerformanceTracker:

    def __init__(self):
        self.registry = CapabilityRegistry()

    def record_execution(self, capability_name, execution_time, success=True):

        data = self.registry.load()

        for capability in data["capabilities"]:

            if capability["name"] == capability_name:

                metrics = capability.get("metrics", {})

                usage = metrics.get("usage_count", 0) + 1
                success_count = metrics.get("success_count", 0)

                if success:
                    success_count += 1

                prev_avg = metrics.get("avg_execution_time", 0)

                if usage == 1:
                    new_avg = execution_time
                else:
                    new_avg = ((prev_avg * (usage - 1)) + execution_time) / usage

                capability["metrics"] = {
                    "usage_count": usage,
                    "success_count": success_count,
                    "avg_execution_time": new_avg
                }

                break

        self.registry.save(data)

    def get_stats(self, *args, **kwargs):

        data = self.registry.load()
        capabilities = data.get("capabilities", [])

        stats = {}

        for capability in capabilities:

            metrics = capability.get("metrics", {})

            usage = metrics.get("usage_count", 0)
            success = metrics.get("success_count", 0)
            avg_time = metrics.get("avg_execution_time", 0)

            success_rate = 0

            if usage > 0:
                success_rate = success / usage

            stats[capability["name"]] = {
                "usage": usage,
                "success_rate": success_rate,
                "avg_time": avg_time
            }

        return stats