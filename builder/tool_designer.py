class ToolDesigner:

    def analyze_need(self, state: dict):

        execution_plan = state.get("execution_plan", {})
        steps = execution_plan.get("steps", [])

        required_tools = []

        for step in steps:

            if step.startswith("run_tool:"):

                tool_name = step.split(":")[1]

                required_tools.append(tool_name)

        return required_tools