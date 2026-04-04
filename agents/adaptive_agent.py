from agents.base_agent import BaseAgent
from core.execution_request import Objective


class AdaptiveAgent(BaseAgent):

    name = "Adaptive_Agent"
    objective = Objective.PROCESS
    priority = 3

    def execute(self, state: dict):

        memory = state.get("memory_context", {})
        recent = memory.get("recent_executions", [])

        # No hay datos históricos
        if not recent:
            state["adaptive_insight"] = {
                "recent_runs": 0,
                "success_rate": 0,
                "failure_rate": 0,
                "trend": "unknown",
                "recommendation": "collect_more_data"
            }
            return state

        success_count = 0
        failure_count = 0

        for execution in recent:

            exec_state = execution.get("state", {})
            status = exec_state.get("execution_status")

            if status == "SUCCESS":
                success_count += 1
            elif status == "FAIL":
                failure_count += 1

        total_runs = len(recent)

        # Protección contra división por cero
        success_rate = success_count / total_runs if total_runs > 0 else 0
        failure_rate = failure_count / total_runs if total_runs > 0 else 0

        # -------------------------
        # Interpretación adaptativa
        # -------------------------

        if success_rate >= 0.75:
            trend = "system_stable"
            recommendation = "increase_execution_confidence"

        elif success_rate >= 0.5:
            trend = "moderate_performance"
            recommendation = "monitor_execution"

        else:
            trend = "unstable"
            recommendation = "trigger_review"

        # Guardamos insight completo
        state["adaptive_insight"] = {
            "recent_runs": total_runs,
            "success_count": success_count,
            "failure_count": failure_count,
            "success_rate": success_rate,
            "failure_rate": failure_rate,
            "trend": trend,
            "recommendation": recommendation
        }

        return state