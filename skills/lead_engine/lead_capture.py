from skills.lead_engine.lead_models import Lead


class LeadCapture:

    name = "capture_lead"

    def execute(self, state):

        data = state.get("data", {})

        lead = Lead(
            name=data.get("name"),
            email=data.get("email"),
            company=data.get("company"),
            source=data.get("source", "unknown")
        )

        print(f"📥 Lead captured: {lead.email}")

        state["lead"] = lead

        return state