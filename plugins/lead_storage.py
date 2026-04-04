import logging
import json
from pathlib import Path


class LeadStorage:

    name = "lead_storage"
    description = "Stores leads into persistent JSON storage"

    def __init__(self):

        self.logger = logging.getLogger("Orion")

        # Storage path
        self.storage_path = Path("storage/leads/leads.json")

    # ------------------------------------------------
    # Main execution
    # ------------------------------------------------
    def execute(self, state):

        leads = state.get("leads", [])

        if not leads:
            self.logger.warning("⚠️ No leads to store")
            return state

        self.logger.info(f"💾 Storing {len(leads)} leads")

        stored_leads = self.load_existing_leads()

        updated_leads = stored_leads + leads

        self.save_leads(updated_leads)

        self.logger.info(f"✅ Total leads stored: {len(updated_leads)}")

        return state

    # ------------------------------------------------
    # Load existing leads
    # ------------------------------------------------
    def load_existing_leads(self):

        try:

            if not self.storage_path.exists():
                return []

            with open(self.storage_path, "r", encoding="utf-8") as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

                return []

        except Exception as e:

            self.logger.error(f"❌ Failed loading leads: {e}")

            return []

    # ------------------------------------------------
    # Save leads
    # ------------------------------------------------
    def save_leads(self, leads):

        try:

            # Ensure directory exists
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.storage_path, "w", encoding="utf-8") as file:

                json.dump(leads, file, indent=4)

        except Exception as e:

            self.logger.error(f"❌ Failed saving leads: {e}")