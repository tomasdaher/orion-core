class BuilderGuard:

    def __init__(self):

        self.max_tools_per_cycle = 2

    def check_generation_allowed(self, state: dict, tool_name: str):

        generated = state.get("generated_tools", [])

        if len(generated) >= self.max_tools_per_cycle:

            print("AI Builder limit reached for this execution")

            return False

        if tool_name in generated:

            print(f"Tool already generated in this cycle: {tool_name}")

            return False

        return True

    def register_generated_tool(self, state: dict, tool_name: str):

        generated = state.get("generated_tools", [])

        generated.append(tool_name)

        state["generated_tools"] = generated