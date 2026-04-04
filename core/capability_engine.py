import logging
from core.capability_registry import CapabilityRegistry


class CapabilityEngine:

    def __init__(self):

        self.logger = logging.getLogger("Orion")

        # 🧠 Capability registry
        self.registry = CapabilityRegistry()

    # ------------------------------------------------
    # 🔥 FIX CLAVE → GET_CAPABILITY
    # ------------------------------------------------
    def get_capability(self, capability_name):

        return self.registry.get(capability_name)

    # ------------------------------------------------
    def has_capability(self, capability_name):

        return self.registry.has_capability(capability_name)

    # ------------------------------------------------
    def execute(self, capability_name, state):

        if not self.registry.has_capability(capability_name):

            raise Exception(
                f"Capability not registered: {capability_name}"
            )

        self.logger.info(
            f"⚙️ Executing capability via engine: {capability_name}"
        )

        return self.registry.execute(capability_name, state)

    # ------------------------------------------------
    def register_capability(self, name, capability):

        self.registry.register(name, capability)

    # ------------------------------------------------
    def list_capabilities(self):

        return self.registry.list_capabilities()

    # ------------------------------------------------
    def reload_capabilities(self):

        self.registry.reload()

    # ------------------------------------------------
    def clear(self):

        self.registry.capabilities = {}

    # ------------------------------------------------
    # 🔥 PLAN OPTIMIZATION
    # ------------------------------------------------
    def optimize_plan(self, execution_plan, state=None):

        """
        Optimization system with protection layer.
        """

        # 🔥 SI EL PLAN ESTÁ BLOQUEADO → NO TOCAR
        if state and state.get("lock_execution_plan"):
            print("🛑 Plan locked → skipping optimization")
            return execution_plan

        # 🔥 FUTURO: lógica de optimización real
        return execution_plan