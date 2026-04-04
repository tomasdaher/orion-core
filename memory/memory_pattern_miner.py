from collections import defaultdict
from memory.episodic_memory import EpisodicMemory


class MemoryPatternMiner:

    def __init__(self):

        self.memory = EpisodicMemory()

    # ---------------------------------
    # ANALYZE CAPABILITY PERFORMANCE
    # ---------------------------------

    def capability_statistics(self):

        episodes = self.memory.load_all_episodes()

        stats = defaultdict(lambda: {
            "usage": 0,
            "success": 0,
            "fail": 0,
            "avg_time": 0
        })

        for ep in episodes:

            caps = ep.get("capabilities_used", [])
            result = ep.get("result")
            time = ep.get("execution_time", 0)

            for cap in caps:

                stats[cap]["usage"] += 1
                stats[cap]["avg_time"] += time

                if result == "SUCCESS":
                    stats[cap]["success"] += 1
                else:
                    stats[cap]["fail"] += 1

        for cap in stats:

            usage = stats[cap]["usage"]

            if usage > 0:
                stats[cap]["avg_time"] /= usage

        return dict(stats)

    # ---------------------------------
    # FIND DOMINANT CAPABILITIES
    # ---------------------------------

    def dominant_capabilities(self, min_usage=3):

        stats = self.capability_statistics()

        dominant = []

        for cap, data in stats.items():

            usage = data["usage"]
            success = data["success"]

            if usage >= min_usage:

                success_rate = success / usage

                if success_rate >= 0.8:
                    dominant.append({
                        "capability": cap,
                        "usage": usage,
                        "success_rate": success_rate
                    })

        dominant.sort(
            key=lambda x: x["success_rate"],
            reverse=True
        )

        return dominant

    # ---------------------------------
    # FIND UNSTABLE CAPABILITIES
    # ---------------------------------

    def unstable_capabilities(self):

        stats = self.capability_statistics()

        unstable = []

        for cap, data in stats.items():

            usage = data["usage"]
            fail = data["fail"]

            if usage > 3 and fail > 0:

                fail_rate = fail / usage

                if fail_rate > 0.4:

                    unstable.append({
                        "capability": cap,
                        "usage": usage,
                        "fail_rate": fail_rate
                    })

        return unstable