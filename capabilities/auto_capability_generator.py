import logging


class AutoCapabilityGenerator:

    """
    Generates placeholder capabilities when Orion
    encounters an unknown capability in a pipeline.
    """

    def __init__(self, capability_engine=None):

        self.logger = logging.getLogger("Orion")

        # capability_engine can be injected later by orchestrator
        self.capability_engine = capability_engine

    # ------------------------------------------------
    # Generate capability
    # ------------------------------------------------
    def generate(self, capability_name):

        if not self.capability_engine:

            self.logger.warning(
                "⚠️ AutoCapabilityGenerator has no capability_engine"
            )

            return False

        self.logger.info(
            f"🧠 Auto generating capability: {capability_name}"
        )

        def generated_capability(state):

            print(f"⚙️ Auto capability executing: {capability_name}")

            # placeholder behavior
            state[f"{capability_name}_result"] = "auto_generated"

            return state

        try:

            self.capability_engine.register_capability(
                capability_name,
                generated_capability
            )

            self.logger.info(
                f"✅ Auto capability registered: {capability_name}"
            )

            return True

        except Exception as e:

            self.logger.error(
                f"❌ Failed generating capability {capability_name}: {e}"
            )

            return False