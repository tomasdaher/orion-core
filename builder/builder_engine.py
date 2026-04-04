from builder.tool_designer import ToolDesigner
from builder.tool_generator import ToolGenerator
from builder.tool_validator import ToolValidator
from builder.tool_installer import ToolInstaller


class BuilderEngine:

    def __init__(self):

        self.designer = ToolDesigner()
        self.generator = ToolGenerator()
        self.validator = ToolValidator()
        self.installer = ToolInstaller()

    def build_tools_if_needed(self, state: dict):

        required_tools = self.designer.analyze_need(state)

        if not required_tools:
            return

        for tool_name in required_tools:

            print(f"AI Builder detected tool requirement: {tool_name}")

            # generar tool
            self.generator.generate_tool(tool_name)

            # validar tool
            valid = self.validator.validate_tool(tool_name)

            if not valid:
                print(f"Tool rejected: {tool_name}")
                continue

            # instalar tool
            self.installer.install_tool(tool_name)