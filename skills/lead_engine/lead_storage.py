class LeadStorage:

    name = "store_lead"

    def __init__(self):

        self.storage = []

    def execute(self, state):

        lead = state.get("lead")

        if not lead:
            return state

        self.storage.append(lead.to_dict())

        print(f"💾 Lead stored: {lead.email}")

        return state