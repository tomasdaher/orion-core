from environment.scenario_builder import ScenarioBuilder
from environment.simulation_engine import SimulationEngine


class EnvironmentSimulator:

    def __init__(self):

        self.builder = ScenarioBuilder()
        self.engine = SimulationEngine()

    def simulate(self, context):

        scenario = self.builder.build(context)

        results = self.engine.run(scenario)

        return results