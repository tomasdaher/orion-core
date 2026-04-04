from capabilities.registry import CapabilityRegistry
from memory.pattern_store import PatternStore


class MetaCapabilityBuilder:

    def __init__(self):

        self.registry = CapabilityRegistry()
        self.pattern_store = PatternStore()

    def build_meta_capabilities(self, threshold=5):

        patterns = self.pattern_store.get_patterns()

        if not patterns:
            return []

        data = self.registry.load()
        capabilities = data.get("capabilities", [])

        existing = {c["name"] for c in capabilities}

        created = []

        for signature, count in patterns.items():

            if count < threshold:
                continue

            steps = signature.split("->")

            # evitar pipelines triviales
            if len(steps) < 3:
                continue

            name = self._generate_meta_name(steps)

            if name in existing:
                continue

            new_capability = {
                "name": name,
                "steps": steps,
                "type": "meta",
                "metrics": {
                    "usage_count": 0,
                    "success_count": 0,
                    "avg_execution_time": 0
                }
            }

            capabilities.append(new_capability)

            created.append(name)

        if created:

            data["capabilities"] = capabilities
            self.registry.save(data)

        return created

    def _generate_meta_name(self, steps):

        base = "_".join(steps)

        if len(base) > 40:
            base = base[:40]

        return f"meta_pipeline_{abs(hash(base)) % 10000}"

