import os
import importlib
import inspect

from agents.base_agent import BaseAgent


class AgentRegistry:

    def __init__(self, dependencies=None):
        self._agents = {}
        self.dependencies = dependencies or {}

    def discover_and_register(self):

        agents_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "agents")
        )

        for filename in os.listdir(agents_path):

            if filename.endswith(".py") and filename not in ("__init__.py", "base_agent.py"):

                module_name = f"agents.{filename[:-3]}"
                module = importlib.import_module(module_name)

                for _, obj in inspect.getmembers(module, inspect.isclass):

                    if issubclass(obj, BaseAgent) and obj is not BaseAgent:

                        instance = self._instantiate_agent(obj)
                        self._agents[instance.name] = instance

    def _instantiate_agent(self, agent_class):

        signature = inspect.signature(agent_class.__init__)
        params = signature.parameters

        kwargs = {}

        for name in params:
            if name == "self":
                continue

            if name in self.dependencies:
                kwargs[name] = self.dependencies[name]

        return agent_class(**kwargs)

    def get(self, name: str):
        return self._agents.get(name)

    def all(self):
        return self._agents