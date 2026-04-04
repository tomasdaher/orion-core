import os


class ToolGenerator:

    def __init__(self):

        self.tools_dir = "tools"

    def generate_tool(self, tool_name: str):

        file_name = f"{tool_name}_tool.py"
        file_path = os.path.join(self.tools_dir, file_name)

        if os.path.exists(file_path):
            print(f"Tool already exists: {file_name}")
            return file_path

        code = self._build_tool_code(tool_name)

        with open(file_path, "w") as f:
            f.write(code)

        print(f"New tool generated: {file_name}")

        return file_path

    def _build_tool_code(self, tool_name: str):

        return f'''
def run(input_data=None):

    print("Orion generated tool executing: {tool_name}")

    result = {{
        "status": "success",
        "tool": "{tool_name}",
        "input": input_data
    }}

    return result
'''