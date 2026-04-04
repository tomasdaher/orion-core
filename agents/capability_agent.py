from agents.base_agent import BaseAgent
from core.execution_request import Objective
from capabilities.registry import CapabilityRegistry


class CapabilityAgent(BaseAgent):

    name = "Capability_Agent"
    objective = Objective.PROCESS
    priority = 7

    def execute(self, state: dict):

        registry = CapabilityRegistry()

        execution_plan = state.get("execution_plan", {})
        plan_steps = execution_plan.get("steps", [])

        if not plan_steps:
            return state

        core_pattern = [
            "analyze_input",
            "validate_data",
            "execute_task",
            "store_result"
        ]

        matches = [step for step in core_pattern if step in plan_steps]

        if len(matches) >= 4:

            capability = {
                "name": "standard_processing_pipeline",
                "steps": core_pattern,
                "metrics": {
                    "usage_count": 0,
                    "success_count": 0,
                    "avg_execution_time": 0
                }
            }

            # Verificar si ya existe
            if registry.exists(capability["name"]):
                print("⚠️ Capability already exists:", capability["name"])
                state["capability_registered"] = None
                return state

            # Intentar registrar
            registered = registry.register(capability)

            if registered:
                print("✅ CAPABILITY REGISTERED:", capability["name"])
                state["capability_registered"] = capability["name"]
            else:
                print("⚠️ Capability already exists:", capability["name"])
                state["capability_registered"] = None

        return state