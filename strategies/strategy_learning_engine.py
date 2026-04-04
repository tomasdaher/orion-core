import logging
from collections import defaultdict


class StrategyLearningEngine:

    """
    Learns which strategies perform best over time.
    """

    def __init__(self):

        self.logger = logging.getLogger("Orion")

        self.strategy_stats = defaultdict(lambda: {
            "executions": 0,
            "success": 0
        })

    def record_execution(self, strategy_mode, success):

        stats = self.strategy_stats[strategy_mode]

        stats["executions"] += 1

        if success:
            stats["success"] += 1

        self.logger.info(
            f"🧠 Strategy recorded: {strategy_mode} | success={success}"
        )

    def get_success_rate(self, strategy_mode):

        stats = self.strategy_stats.get(strategy_mode)

        if not stats or stats["executions"] == 0:
            return 0

        return stats["success"] / stats["executions"]

    def best_strategy(self):

        best = None
        best_rate = 0

        for strategy, stats in self.strategy_stats.items():

            if stats["executions"] == 0:
                continue

            rate = stats["success"] / stats["executions"]

            if rate > best_rate:
                best_rate = rate
                best = strategy

        return best