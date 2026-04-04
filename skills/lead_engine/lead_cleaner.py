class LeadCleaner:

    name = "clean_data"

    def execute(self, state):

        lead = state.get("lead")

        if not lead:
            return state

        if lead.email:
            lead.email = lead.email.lower().strip()

        if lead.name:
            lead.name = lead.name.strip()

        print("🧹 Lead data cleaned")

        return state