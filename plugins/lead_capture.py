import logging
import random


class LeadCapture:

    name = "lead_capture"
    description = "Captures leads from different sources"

    def __init__(self):

        self.logger = logging.getLogger("Orion")

    # ------------------------------------------------
    # Main execution
    # ------------------------------------------------
    def execute(self, state):

        intent = state.get("intent", {})

        # Source detection (robust)
        source = intent.get("source") or state.get("source") or "generic"

        source = source.lower()

        self.logger.info(f"📥 Capturing leads from source: {source}")

        leads = self.capture_from_source(source)

        # Ensure leads container exists
        if "leads" not in state:
            state["leads"] = []

        state["leads"].extend(leads)

        self.logger.info(f"✅ {len(leads)} leads captured")

        return state

    # ------------------------------------------------
    # Source router
    # ------------------------------------------------
    def capture_from_source(self, source):

        if source == "instagram":
            return self.capture_instagram()

        if source == "facebook":
            return self.capture_facebook()

        if source == "web_form":
            return self.capture_web_form()

        return self.capture_generic()

    # ------------------------------------------------
    # Simulated sources (phase 1)
    # ------------------------------------------------
    def capture_instagram(self):

        self.logger.info("📡 Simulating Instagram lead capture")

        return [
            self.generate_fake_lead("instagram"),
            self.generate_fake_lead("instagram")
        ]

    def capture_facebook(self):

        self.logger.info("📡 Simulating Facebook lead capture")

        return [
            self.generate_fake_lead("facebook")
        ]

    def capture_web_form(self):

        self.logger.info("📡 Simulating Web Form lead capture")

        return [
            self.generate_fake_lead("web_form")
        ]

    def capture_generic(self):

        self.logger.info("📡 Simulating Generic lead capture")

        return [
            self.generate_fake_lead("generic")
        ]

    # ------------------------------------------------
    # Fake lead generator (for testing pipeline)
    # ------------------------------------------------
    def generate_fake_lead(self, source):

        names = [
            "Juan Perez",
            "Maria Gomez",
            "Carlos Diaz",
            "Ana Lopez"
        ]

        domains = [
            "gmail.com",
            "hotmail.com",
            "empresa.com"
        ]

        name = random.choice(names)

        email = name.lower().replace(" ", ".") + "@" + random.choice(domains)

        return {
            "name": name,
            "email": email,
            "source": source,
            "score": None
        }