from agents.base_agent import BaseAgent
from core.execution_request import Objective

from capabilities.performance_tracker import CapabilityPerformanceTracker
from tools.executor import ToolExecutor
from builder.builder_engine import BuilderEngine

import time


class TaskAgent(BaseAgent):

    name = "Task_Agent"
    objective = Objective.PROCESS
    priority = 1

    def __init__(self):

        super().__init__()

        self.performance_tracker = CapabilityPerformanceTracker()
        self.tool_executor = ToolExecutor()
        self.builder_engine = BuilderEngine()

    def execute(self, state: dict):

        execution_plan = state.get("execution_plan", {})
        steps = execution_plan.get("steps", [])

        if not steps:
            print("No execution steps provided.")
            state["execution_history"] = []
            return state

        # ---------------------------------
        # AI BUILDER CHECK
        # ---------------------------------

        self.builder_engine.build_tools_if_needed(state)

        executed_steps = []

        for step in steps:

            try:

                # -----------------------------
                # TOOL EXECUTION
                # -----------------------------
                if step.startswith("run_tool:"):

                    tool_name = step.split(":")[1]

                    print(f"Ejecutando tool: {tool_name}")

                    result = self.tool_executor.run_tool(
                        tool_name,
                        state.get("data")
                    )

                    state["tool_result"] = result
                    executed_steps.append(step)
                    continue

                # -----------------------------
                # CAPABILITY EXECUTION
                # -----------------------------
                if step.startswith("run_capability:"):

                    capability_name = step.split(":")[1]

                    print(f"Ejecutando capability optimizada: {capability_name}")

                    start_time = time.time()

                    # Simulación ejecución capability
                    time.sleep(0.01)

                    execution_time = time.time() - start_time

                    self.performance_tracker.record_execution(
                        capability_name,
                        execution_time,
                        success=True
                    )

                    executed_steps.append(step)
                    continue

                # -----------------------------
                # NORMAL PLAN STEP
                # -----------------------------
                print(f"Ejecutando step del plan: {step}")

                executed_steps.append(step)

            except Exception as e:

                print(f"Error ejecutando step {step}: {e}")

                self.performance_tracker.record_execution(
                    step,
                    0,
                    success=False
                )

        state["execution_history"] = executed_steps

        return state