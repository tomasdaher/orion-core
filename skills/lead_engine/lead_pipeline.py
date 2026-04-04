from skills.lead_engine.lead_capture import LeadCapture
from skills.lead_engine.lead_cleaner import LeadCleaner
from skills.lead_engine.lead_classifier import LeadClassifier
from skills.lead_engine.lead_scorer import LeadScorer
from skills.lead_engine.lead_storage import LeadStorage
from skills.lead_engine.lead_notifier import LeadNotifier


class LeadPipeline:

    name = "lead_engine_pipeline"

    def __init__(self):

        self.steps = [
            LeadCapture(),
            LeadCleaner(),
            LeadClassifier(),
            LeadScorer(),
            LeadStorage(),
            LeadNotifier()
        ]

    def execute(self, state):

        for step in self.steps:

            state = step.execute(state)

        return state