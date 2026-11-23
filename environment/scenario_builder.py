class ScenarioBuilder:

    def build(self, context):

        scenario = {
            "context": context,
            "steps": [],
        }

        return scenario

    def add_step(self, scenario, step):

        scenario["steps"].append(step)

        return scenario