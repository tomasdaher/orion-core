from skills.lead_engine.lead_pipeline import LeadPipeline


class LeadEngineCapability:

    name = "lead_engine"

    def __init__(self):

        self.pipeline = LeadPipeline()

    def execute(self, state):

        print("🚀 Executing Lead Engine")

        return self.pipeline.execute(state)