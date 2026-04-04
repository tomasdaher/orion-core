import logging


class LeadNotifier:

    name = "lead_notifier"
    description = "Notifies about new high-value leads"

    def __init__(self):

        self.logger = logging.getLogger("Orion")

    # ------------------------------------------------
    # Main execution
    # ------------------------------------------------
    def execute(self, state):

        leads = state.get("leads", [])

        if not leads:
            self.logger.warning("⚠️ No leads available for notification")
            return state

        self.logger.info("📢 Checking leads for notifications")

        hot_leads = self.get_hot_leads(leads)

        if not hot_leads:
            self.logger.info("ℹ️ No hot leads to notify")
            return state

        self.notify_hot_leads(hot_leads)

        return state

    # ------------------------------------------------
    # Filter hot leads
    # ------------------------------------------------
    def get_hot_leads(self, leads):

        hot = []

        for lead in leads:

            if lead.get("segment") == "hot":

                hot.append(lead)

        return hot

    # ------------------------------------------------
    # Notification logic
    # ------------------------------------------------
    def notify_hot_leads(self, leads):

        self.logger.info(f"🔥 {len(leads)} HOT leads detected")

        for lead in leads:

            name = lead.get("name")
            email = lead.get("email")
            score = lead.get("score")

            self.logger.info(
                f"🚨 HOT LEAD → {name} | {email} | score={score}"
            )