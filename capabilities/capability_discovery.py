from collections import Counter
from capabilities.registry import CapabilityRegistry
from capabilities.capability_graph import CapabilityGraph


class CapabilityDiscoveryEngine:

    def __init__(self):

        self.registry = CapabilityRegistry()
        self.graph = CapabilityGraph()

        # cuántas veces debe repetirse un patrón
        self.discovery_threshold = 3

    def discover(self, execution_history):

        """
        execution_history:
        [
            ["analyze_input", "validate_data", "execute_task"],
            ["analyze_input", "validate_data", "execute_task"],
            ...
        ]
        """

        if not execution_history:
            return []

        # 🔧 FIX 1: limpiar execution_history y evitar duplicados
        cleaned_history = []

        for steps in execution_history:

            if not steps:
                continue

            # normalizar pipeline
            cleaned = tuple(step for step in steps if step)

            if not cleaned:
                continue

            cleaned_history.append(cleaned)

        pattern_counter = Counter(cleaned_history)

        new_capabilities = []
        registered_names = set()

        for pattern, count in pattern_counter.items():

            if count < self.discovery_threshold:
                continue

            capability_name = "_".join(pattern)

            # 🔧 FIX 2: evitar duplicados en el mismo ciclo
            if capability_name in registered_names:
                continue

            # ya existe en registry
            if self.registry.exists(capability_name):
                continue

            capability = {
                "name": capability_name,
                "steps": list(pattern),
                "usage": count,
                "discovered": True
            }

            created = self.registry.register(capability)

            if created:

                registered_names.add(capability_name)

                for step in pattern:
                    self.graph.add_edge(capability_name, step)

                new_capabilities.append(capability_name)

        # 🔧 FIX 3: dedupe final (seguridad extra)
        unique_capabilities = list(dict.fromkeys(new_capabilities))

        return unique_capabilities  