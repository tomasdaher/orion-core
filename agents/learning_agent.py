from agents.base_agent import BaseAgent
from core.execution_request import Objective

from capabilities.capability_discovery import CapabilityDiscoveryEngine
from capabilities.meta_capability_builder import MetaCapabilityBuilder
from capabilities.capability_intelligence import CapabilityIntelligence
from capabilities.capability_evolution_manager import CapabilityEvolutionManager
from capabilities.capability_learning_engine import CapabilityLearningEngine

import logging


class LearningAgent(BaseAgent):

    name = "Learning_Agent"
    objective = Objective.PROCESS
    priority = 6

    def __init__(self, memory_service=None):

        super().__init__()

        self.logger = logging.getLogger("Orion")

        self.memory_service = memory_service

        # ------------------------------------------------
        # Capability systems
        # ------------------------------------------------

        self.discovery = CapabilityDiscoveryEngine()
        self.meta_builder = MetaCapabilityBuilder()
        self.capability_intelligence = CapabilityIntelligence()

        # Capability evolution manager
        self.evolution_manager = CapabilityEvolutionManager()

        # ------------------------------------------------
        # Central capability learning engine
        # ------------------------------------------------

        self.capability_learning_engine = CapabilityLearningEngine()

    # ------------------------------------------------
    # Main execution
    # ------------------------------------------------

    def execute(self, state: dict):

        insight = state.get("adaptive_insight", {})
        strategy = state.get("system_strategy", {})

        success_rate = insight.get("success_rate", 0)
        mode = strategy.get("mode", "unknown")

        learning = {}

        if success_rate >= 0.8:
            learning["recommendation"] = "keep_strategy"

        elif success_rate >= 0.4:
            learning["recommendation"] = "adjust_strategy"

        else:
            learning["recommendation"] = "strategy_change_required"

        learning["observed_success_rate"] = success_rate
        learning["current_mode"] = mode

        state["learning_feedback"] = learning

        state["learning_insight"] = {
            "strategy_mode": mode,
            "success_rate": success_rate,
            "recommendation": learning["recommendation"]
        }

        # ------------------------------------------------
        # Execution history for learning
        # ------------------------------------------------

        execution_history = state.get("execution_history", [])

        # ------------------------------------------------
        # CAPABILITY LEARNING ENGINE (central cycle)
        # ------------------------------------------------

        try:

            learning_results = self.capability_learning_engine.run_learning_cycle(
                execution_history
            )

            state["capability_learning_results"] = learning_results

        except Exception as e:

            self.logger.warning(
                f"⚠️ Capability learning engine failed: {e}"
            )

        # ------------------------------------------------
        # CAPABILITY DISCOVERY (legacy compatibility)
        # ------------------------------------------------

        try:

            new_caps = self.discovery.discover(execution_history)

            if new_caps:
                self.logger.info(
                    f"🧠 New capabilities discovered: {new_caps}"
                )

        except Exception as e:

            self.logger.warning(
                f"⚠️ Capability discovery failed: {e}"
            )

        # ------------------------------------------------
        # META CAPABILITY CREATION
        # ------------------------------------------------

        try:

            meta_caps = self.meta_builder.build_meta_capabilities()

            if meta_caps:
                self.logger.info(
                    f"🧬 Meta capabilities created: {meta_caps}"
                )

        except Exception as e:

            self.logger.warning(
                f"⚠️ Meta capability creation failed: {e}"
            )

        # ------------------------------------------------
        # CAPABILITY INTELLIGENCE
        # ------------------------------------------------

        try:

            insights = self.capability_intelligence.analyze_capabilities()

            if insights:
                self.logger.info(
                    f"🧠 Capability insights: {insights}"
                )

            state["capability_insights"] = insights

        except Exception as e:

            self.logger.warning(
                f"⚠️ Capability intelligence failed: {e}"
            )

        # ------------------------------------------------
        # CAPABILITY EVOLUTION
        # ------------------------------------------------

        try:

            self.logger.info("🧬 Running capability evolution cycle")

            self.evolution_manager.run_evolution_cycle()

        except Exception as e:

            self.logger.warning(
                f"⚠️ Capability evolution failed: {e}"
            )

        return state