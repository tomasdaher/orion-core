class LeadNotifier:

    name = "notify_sales"

    def execute(self, state):

        lead = state.get("lead")

        if not lead:
            return state

        if getattr(lead, "score", 0) > 60:

            print(
                f"🚨 Sales notified: high-value lead {lead.email}"
            )

        return state


def notify_sales(state):

    handler = LeadNotifier()

    return handler.execute(state)