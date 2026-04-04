import importlib
from tools.registry import ToolRegistry


class ToolExecutor:

    def __init__(self):
        self.registry = ToolRegistry()

    def run_tool(self, tool_name, input_data=None):

        tools = self.registry.list_tools()

        tool_info = None

        for tool in tools:
            if tool["name"] == tool_name:
                tool_info = tool
                break

        if not tool_info:
            print(f"Tool not found: {tool_name}")
            return None

        module_path = tool_info.get("module")

        # asegurar que el módulo tenga el prefijo correcto
        if not module_path.startswith("tools."):
            module_path = f"tools.{module_path}"

        try:

            module = importlib.import_module(module_path)

            if hasattr(module, "run"):

                print(f"Executing tool: {tool_name}")

                result = module.run(input_data)

                return result

            else:

                print(f"Tool {tool_name} has no run() function")
                return None

        except Exception as e:

            print(f"Tool execution failed: {e}")
            return None