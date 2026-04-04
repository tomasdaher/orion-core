import os
import json


class ToolRegistry:

    def __init__(self, path="tools/tools_registry.json"):
        self.path = path
        self._ensure_registry()

    def _ensure_registry(self):

        if not os.path.exists(self.path):

            data = {
                "tools": []
            }

            with open(self.path, "w") as f:
                json.dump(data, f, indent=4)

    def load(self):

        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, data):

        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def register_tool(self, tool_info):

        data = self.load()

        tools = data.get("tools", [])

        for tool in tools:
            if tool["name"] == tool_info["name"]:
                print(f"⚠️ Tool already exists: {tool_info['name']}")
                return

        tools.append(tool_info)

        data["tools"] = tools

        self.save(data)

        print(f"🧰 Tool registered: {tool_info['name']}")

    def list_tools(self):

        data = self.load()

        return data.get("tools", [])