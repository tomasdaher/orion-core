class LeadNotifier:

    name = "notify_sales"

    def execute(self, state):

        lead = state.get("lead")

        if not lead:
            return state

        if lead.score > 60:

            print(
                f"🚨 Sales notified: high-value lead {lead.email}"
            )

        return state