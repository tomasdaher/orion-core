from agents.base_agent import BaseAgent
from core.execution_request import Objective


class DecisionAgent(BaseAgent):
    name = "Decision_Agent"
    objective = Objective.PROCESS
    priority = 2

    def execute(self, state: dict) -> dict:
        if "processed_data" in state:
            state["decision"] = "processing approved"
            state["execution_status"] = "SUCCESS"
        else:
            state["decision"] = "processing failed"
            state["execution_status"] = "FAILED"

        return state
