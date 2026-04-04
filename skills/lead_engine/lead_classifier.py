class LeadClassifier:

    name = "classify_lead"

    def execute(self, state):

        lead = state.get("lead")

        if not lead:
            return state

        if lead.company:
            lead.category = "business"
        else:
            lead.category = "individual"

        print(f"🏷 Lead classified: {lead.category}")

        return state