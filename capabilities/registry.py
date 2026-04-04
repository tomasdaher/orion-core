import json
from pathlib import Path


class CapabilityRegistry:

    def __init__(self):

        self.storage_path = Path("capabilities/capabilities.json")

        if not self.storage_path.exists():
            self._initialize_storage()

    def _initialize_storage(self):

        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({"capabilities": []}, f, indent=2)

    def load(self):

        with open(self.storage_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):

        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def register(self, capability):

        data = self.load()

        existing = {c["name"] for c in data["capabilities"]}

        if capability["name"] in existing:
            return False

        data["capabilities"].append(capability)
        self.save(data)

        return True

    def list_capabilities(self):

        data = self.load()

        return data["capabilities"]

    def exists(self, name):

        data = self.load()

        return any(c["name"] == name for c in data["capabilities"])