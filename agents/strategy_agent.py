from agents.base_agent import BaseAgent
from core.execution_request import Objective


class StrategyAgent(BaseAgent):

    name = "Strategy_Agent"
    objective = Objective.PROCESS
    priority = 4

    def execute(self, state: dict):

        insight = state.get("adaptive_insight", {})

        success_rate = insight.get("success_rate", 0)

        strategy_mode = "unknown"

        if success_rate >= 0.8:
            strategy_mode = "stable"

        elif success_rate >= 0.4:
            strategy_mode = "adaptive"

        else:
            strategy_mode = "recovery"

        # Configuración estratégica que otros agentes pueden usar
        strategy_config = {
            "mode": strategy_mode,
            "success_rate": success_rate,
            "execution_policy": self._build_execution_policy(strategy_mode)
        }

        state["system_strategy"] = strategy_config

        return state

    def _build_execution_policy(self, strategy_mode: str):

        if strategy_mode == "stable":
            return {
                "risk_level": "high",
                "exploration": True,
                "retry_on_fail": False
            }

        if strategy_mode == "adaptive":
            return {
                "risk_level": "medium",
                "exploration": True,
                "retry_on_fail": True
            }

        if strategy_mode == "recovery":
            return {
                "risk_level": "low",
                "exploration": False,
                "retry_on_fail": True
            }

        return {
            "risk_level": "unknown",
            "exploration": False,
            "retry_on_fail": False
        }