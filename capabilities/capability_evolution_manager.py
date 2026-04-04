import json
import os


class CapabilityEvolutionManager:

    def __init__(self):

        self.file_path = os.path.join(
            os.path.dirname(__file__),
            "capabilities.json"
        )

        # límite de capacidades nuevas por ciclo evolutivo
        self.max_new_capabilities_per_cycle = 5

    # ---------------------------------
    # LOAD CAPABILITIES
    # ---------------------------------
    def load_capabilities(self):

        if not os.path.exists(self.file_path):
            return {"capabilities": []}

        try:
            with open(self.file_path, "r") as f:
                return json.load(f)

        except Exception as e:
            print(f"⚠️ Failed to load capabilities: {e}")
            return {"capabilities": []}

    # ---------------------------------
    # SAVE CAPABILITIES
    # ---------------------------------
    def save_capabilities(self, data):

        try:
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️ Failed to save capabilities: {e}")

    # ---------------------------------
    # BUILD SIGNATURE
    # ---------------------------------
    def build_signature(self, capability):

        steps = capability.get("steps") or capability.get("pattern")

        if not steps:
            return None

        return tuple(steps)

    # ---------------------------------
    # DEDUPLICATE PIPELINES
    # ---------------------------------
    def deduplicate_capabilities(self, data):

        seen_patterns = {}
        cleaned_capabilities = []

        for capability in data.get("capabilities", []):

            signature = self.build_signature(capability)

            if signature is None:
                cleaned_capabilities.append(capability)
                continue

            if signature in seen_patterns:

                print(
                    f"♻️ Duplicate pipeline detected: {capability.get('name')}"
                )
                continue

            seen_patterns[signature] = capability.get("name")
            cleaned_capabilities.append(capability)

        data["capabilities"] = cleaned_capabilities

        return data

    # ---------------------------------
    # PRUNE UNUSED CAPABILITIES
    # ---------------------------------
    def prune_unused_capabilities(self, data, usage_threshold=0):

        cleaned_capabilities = []

        for capability in data.get("capabilities", []):

            metrics = capability.get("metrics", {})
            usage = metrics.get("usage_count", 0)

            if (
                usage <= usage_threshold
                and capability.get("name") != "standard_processing_pipeline"
            ):

                print(
                    f"🧹 Pruning unused capability: {capability.get('name')}"
                )
                continue

            cleaned_capabilities.append(capability)

        data["capabilities"] = cleaned_capabilities

        return data

    # ---------------------------------
    # LIMIT CAPABILITY GROWTH
    # ---------------------------------
    def limit_capability_growth(self, data):

        capabilities = data.get("capabilities", [])

        if len(capabilities) <= 100:
            return data

        print("⚠️ Capability pool too large, trimming...")

        # ordenar por uso
        capabilities.sort(
            key=lambda c: c.get("metrics", {}).get("usage_count", 0),
            reverse=True
        )

        # mantener solo las 100 más usadas
        data["capabilities"] = capabilities[:100]

        return data

    # ---------------------------------
    # RUN EVOLUTION CYCLE
    # ---------------------------------
    def run_evolution_cycle(self):

        print("🧬 Running Capability Evolution Cycle")

        data = self.load_capabilities()

        # 1 limpiar duplicados
        data = self.deduplicate_capabilities(data)

        # 2 eliminar capacidades no usadas
        data = self.prune_unused_capabilities(data)

        # 3 evitar crecimiento infinito
        data = self.limit_capability_growth(data)

        self.save_capabilities(data)

        print("✅ Capability evolution completed")