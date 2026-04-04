import logging


class GoalCapabilityMapper:

    """
    Maps subgoals to available capabilities.
    """

    def __init__(self, capability_registry):

        self.logger = logging.getLogger("Orion")
        self.registry = capability_registry

    # ------------------------------------------------
    # Map subgoals to capabilities
    # ------------------------------------------------
    def map_subgoals(self, subgoals):

        pipeline = []

        capabilities = self.registry.list_capabilities()

        for subgoal in subgoals:

            capability = self._find_capability(subgoal, capabilities)

            if capability:

                step = f"run_capability:{capability}"
                pipeline.append(step)

                self.logger.info(
                    f"🔗 Subgoal '{subgoal}' mapped to capability '{capability}'"
                )

            else:

                self.logger.warning(
                    f"⚠️ No capability found for subgoal '{subgoal}'"
                )

        return pipeline

    # ------------------------------------------------
    # Find matching capability
    # ------------------------------------------------
    def _find_capability(self, subgoal, capabilities):

        subgoal = subgoal.lower()

        for capability in capabilities:

            name = capability.lower()

            if subgoal in name or name in subgoal:

                return capability

        return None