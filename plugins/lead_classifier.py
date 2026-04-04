import logging


class LeadClassifier:

    name = "lead_classifier"
    description = "Scores and classifies leads based on simple heuristics"

    def __init__(self):

        self.logger = logging.getLogger("Orion")

    # ------------------------------------------------
    # Main execution
    # ------------------------------------------------
    def execute(self, state):

        leads = state.get("leads", [])

        if not leads:
            self.logger.warning("⚠️ No leads found to classify")
            return state

        self.logger.info(f"🧠 Classifying {len(leads)} leads")

        classified_leads = []

        for lead in leads:

            scored_lead = self.classify_lead(lead)

            classified_leads.append(scored_lead)

        state["leads"] = classified_leads

        self.logger.info("✅ Lead classification complete")

        return state

    # ------------------------------------------------
    # Lead classification logic
    # ------------------------------------------------
    def classify_lead(self, lead):

        email = lead.get("email", "")

        score = self.calculate_score(email)

        segment = self.assign_segment(score)

        lead["score"] = score
        lead["segment"] = segment

        return lead

    # ------------------------------------------------
    # Score calculation
    # ------------------------------------------------
    def calculate_score(self, email):

        if not email:
            return 0.0

        domain = email.split("@")[-1]

        # Simple scoring heuristic
        if domain.endswith("empresa.com"):
            return 0.9

        if domain.endswith("gmail.com"):
            return 0.4

        if domain.endswith("hotmail.com"):
            return 0.5

        return 0.6

    # ------------------------------------------------
    # Segment assignment
    # ------------------------------------------------
    def assign_segment(self, score):

        if score >= 0.8:
            return "hot"

        if score >= 0.5:
            return "warm"

        return "cold"