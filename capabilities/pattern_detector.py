from collections import defaultdict
from capabilities.registry import CapabilityRegistry
from memory.pattern_store import PatternStore


class PatternDetector:

    def __init__(self):

        self.registry = CapabilityRegistry()

        # memoria en RAM
        self.pattern_memory = defaultdict(int)

        # memoria persistente
        self.pattern_store = PatternStore()

        # cargar patrones históricos
        stored_patterns = self.pattern_store.get_patterns()

        for signature, count in stored_patterns.items():
            self.pattern_memory[signature] = count

    def observe_plan(self, executed_steps):

        if not executed_steps:
            return

        # Convertimos el plan a una firma única
        signature = "->".join(executed_steps)

        # Contador en RAM
        self.pattern_memory[signature] += 1

        # Guardar en memoria persistente
        self.pattern_store.increment_pattern(signature)

    def detect_patterns(self, threshold=3):

        discovered = []

        for signature, count in self.pattern_memory.items():

            if count >= threshold:

                steps = signature.split("->")

                capability_name = self._generate_capability_name(steps)

                discovered.append({
                    "name": capability_name,
                    "steps": steps,
                    "frequency": count
                })

        return discovered

    def register_new_capabilities(self):

        patterns = self.detect_patterns()

        if not patterns:
            return []

        data = self.registry.load()

        capabilities = data.get("capabilities", [])

        existing = {c["name"] for c in capabilities}

        created = []

        for pattern in patterns:

            if pattern["name"] in existing:
                continue

            new_capability = {
                "name": pattern["name"],
                "steps": pattern["steps"],
                "metrics": {
                    "usage_count": 0,
                    "success_count": 0,
                    "avg_execution_time": 0
                }
            }

            capabilities.append(new_capability)

            created.append(pattern["name"])

        if created:
            data["capabilities"] = capabilities
            self.registry.save(data)

        return created

    def _generate_capability_name(self, steps):

        name = "_".join(steps)

        if len(name) > 50:
            name = name[:50]

        return f"auto_pipeline_{abs(hash(name)) % 10000}"
        