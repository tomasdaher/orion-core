from tools.registry import ToolRegistry


class ToolInstaller:

    def __init__(self):

        self.registry = ToolRegistry()

    def install_tool(self, tool_name: str):

        data = self.registry.load()

        tools = data.get("tools", [])

        # verificar si ya existe
        for tool in tools:
            if tool.get("name") == tool_name:
                print(f"Tool already registered: {tool_name}")
                return False

        new_tool = {
            "name": tool_name,
            "module": f"{tool_name}_tool",
            "enabled": True
        }

        tools.append(new_tool)

        data["tools"] = tools

        self.registry.save(data)

        print(f"Tool installed successfully: {tool_name}")

        return True