import logging


class CapabilityStrategyOptimizer:

    def __init__(self):

        self.logger = logging.getLogger("Orion")

        self.strategy_stats = {
            "memory": {"runs": 0, "success": 0},
            "exploration": {"runs": 0, "success": 0},
            "hybrid": {"runs": 0, "success": 0},
        }

    def record_strategy(self, strategy_name, success):

        if strategy_name not in self.strategy_stats:
            self.strategy_stats[strategy_name] = {"runs": 0, "success": 0}

        self.strategy_stats[strategy_name]["runs"] += 1

        if success:
            self.strategy_stats[strategy_name]["success"] += 1

        self.logger.info(
            f"🧠 Strategy recorded: {strategy_name} | success={success}"
        )

    def get_strategy_performance(self):

        performance = {}

        for strategy, stats in self.strategy_stats.items():

            runs = stats["runs"]
            success = stats["success"]

            if runs == 0:
                rate = 0
            else:
                rate = success / runs

            performance[strategy] = {
                "runs": runs,
                "success": success,
                "success_rate": rate
            }

        return performance

    def get_best_strategy(self):

        performance = self.get_strategy_performance()

        best = None
        best_rate = -1

        for strategy, stats in performance.items():

            rate = stats["success_rate"]

            if rate > best_rate and stats["runs"] > 3:
                best = strategy
                best_rate = rate

        return best

    def recommend_strategy(self):

        best = self.get_best_strategy()

        if best:
            self.logger.info(f"🧠 Best strategy detected: {best}")
            return best

        return "hybrid"