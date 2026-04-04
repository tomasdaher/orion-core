import importlib
import traceback
import os


class ToolValidator:

    def __init__(self):
        self.tools_module = "tools"

    def validate_tool(self, tool_name: str):

        module_name = f"{self.tools_module}.{tool_name}_tool"

        try:
            module = importlib.import_module(module_name)

        except Exception as e:
            print(f"Tool import failed: {tool_name}")
            traceback.print_exc()
            return False

        if not hasattr(module, "run"):
            print(f"Tool missing run() function: {tool_name}")
            return False

        try:
            module.run({"test": True})

        except Exception as e:
            print(f"Tool execution failed: {tool_name}")
            traceback.print_exc()
            return False

        print(f"Tool validated successfully: {tool_name}")

        return True