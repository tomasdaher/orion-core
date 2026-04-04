import logging

from capabilities.capability_discovery import CapabilityDiscoveryEngine
from capabilities.capability_evolution import CapabilityEvolution
from capabilities.meta_capability_builder import MetaCapabilityBuilder


class CapabilityLearningEngine:

    """
    Central learning engine for Orion.

    Coordinates:
    - Capability discovery
    - Capability evolution
    - Meta capability generation
    """

    def __init__(self):

        self.logger = logging.getLogger("Orion")

        self.discovery = CapabilityDiscoveryEngine()
        self.evolution = CapabilityEvolution()
        self.meta_builder = MetaCapabilityBuilder()

    # ------------------------------------------------
    # Run complete learning cycle
    # ------------------------------------------------
    def run_learning_cycle(self, execution_history=None):

        """
        execution_history example:

        [
            ["capture_lead", "clean_lead", "classify_lead", "store_lead"],
            ["capture_lead", "clean_lead", "classify_lead", "store_lead"],
            ["capture_lead", "clean_lead", "classify_lead", "store_lead"]
        ]
        """

        self.logger.info("🧠 Starting capability learning cycle")

        results = {
            "patterns_discovered": [],
            "capability_insights": {},
            "evolved_capabilities": [],
            "meta_capabilities": []
        }

        try:

            # --------------------------------------------
            # Pattern discovery
            # --------------------------------------------
            if execution_history:

                discovered = self.discovery.discover(execution_history)

                if discovered:
                    self.logger.info(
                        f"🔍 New capability patterns discovered: {discovered}"
                    )

                results["patterns_discovered"] = discovered

            # --------------------------------------------
            # Capability insights
            # --------------------------------------------
            insights = self.evolution.analyze()

            self.logger.info(
                f"📊 Capability insights generated"
            )

            results["capability_insights"] = insights

            # --------------------------------------------
            # Capability evolution
            # --------------------------------------------
            evolved = self.evolution.evolve()

            if evolved:

                self.logger.info(
                    f"🧬 Capabilities evolved: {evolved}"
                )

            results["evolved_capabilities"] = evolved

            # --------------------------------------------
            # Meta capability generation
            # --------------------------------------------
            meta = self.meta_builder.build_meta_capabilities()

            if meta:

                self.logger.info(
                    f"🧬 Meta capabilities created: {meta}"
                )

            results["meta_capabilities"] = meta

        except Exception as e:

            self.logger.error(
                f"❌ Capability learning cycle failed: {e}"
            )

        self.logger.info("🧠 Capability learning cycle completed")

        return results