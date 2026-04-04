from agents.base_agent import BaseAgent
from core.execution_request import Objective


class ActionAgent(BaseAgent):

    name = "Action_Agent"
    objective = Objective.PROCESS
    priority = 50

    def __init__(
        self,
        integration_manager=None,
        capability_engine=None
    ):

        super().__init__()

        self.integration_manager = integration_manager
        self.capability_engine = capability_engine

    def execute(self, state: dict):

        plan = state.get("execution_plan", {})
        steps = plan.get("steps", [])

        results = []

        for step in steps:

            try:

                # ------------------------------
                # CAPABILITY EXECUTION
                # ------------------------------

                if step.startswith("run_capability:"):

                    _, capability_name = step.split(":", 1)

                    self.logger.info(
                        f"⚡ Running capability: {capability_name}"
                    )

                    capability = None

                    if self.capability_engine:

                        capability = self.capability_engine.get_capability(
                            capability_name
                        )

                    if not capability:

                        self.logger.warning(
                            f"⚠️ Capability not found: {capability_name}"
                        )

                        results.append({
                            "capability": capability_name,
                            "error": "capability_not_found"
                        })

                        continue

                    result = capability.execute(
                        state.get("data")
                    )

                    results.append({
                        "capability": capability_name,
                        "result": result
                    })

                    continue

                # ------------------------------
                # EXTERNAL ACTION
                # ------------------------------

                if step.startswith("action:"):

                    _, connector_name, operation = step.split(":")

                    result = self.integration_manager.execute(
                        connector_name,
                        operation,
                        state.get("data")
                    )

                    results.append({
                        "connector": connector_name,
                        "operation": operation,
                        "result": result
                    })

                    continue

            except Exception as e:

                results.append({
                    "step": step,
                    "error": str(e)
                })

        if results:
            state["execution_results"] = results

        return state