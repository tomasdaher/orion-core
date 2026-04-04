import logging


class LeadCleaner:

    name = "lead_cleaner"
    description = "Cleans and normalizes captured leads"

    def __init__(self):

        self.logger = logging.getLogger("Orion")

    # ------------------------------------------------
    # Main execution
    # ------------------------------------------------
    def execute(self, state):

        leads = state.get("leads", [])

        if not leads:
            self.logger.warning("⚠️ No leads found to clean")
            return state

        self.logger.info(f"🧹 Cleaning {len(leads)} leads")

        cleaned_leads = self.clean_leads(leads)

        state["leads"] = cleaned_leads

        self.logger.info(f"✅ Leads after cleaning: {len(cleaned_leads)}")

        return state

    # ------------------------------------------------
    # Lead cleaning pipeline
    # ------------------------------------------------
    def clean_leads(self, leads):

        normalized = []
        seen_emails = set()

        for lead in leads:

            cleaned = self.normalize_lead(lead)

            email = cleaned.get("email")

            if not email:
                continue

            if email in seen_emails:
                continue

            seen_emails.add(email)

            normalized.append(cleaned)

        return normalized

    # ------------------------------------------------
    # Normalize lead fields
    # ------------------------------------------------
    def normalize_lead(self, lead):

        name = lead.get("name", "").strip()
        email = lead.get("email", "").strip().lower()
        source = lead.get("source", "unknown")

        normalized_lead = {
            "name": name.title(),
            "email": email,
            "source": source,
            "score": lead.get("score")
        }

        return normalized_lead