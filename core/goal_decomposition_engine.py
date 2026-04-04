import logging
from typing import List, Dict, Any

logger = logging.getLogger("Orion")


class GoalDecompositionEngine:
    """
    Goal Decomposition Engine

    Responsible for transforming high-level goals into
    structured sub-goals that Orion can execute.

    This enables Orion to operate as a goal-driven system
    rather than purely reactive.

    Example:

        Goal:
            "capture leads from website"

        Decomposed into:
            - create webhook
            - capture data
            - clean leads
            - classify leads
            - store leads
            - notify sales
    """

    def __init__(self, capability_registry=None):
        self.capability_registry = capability_registry

    # ----------------------------------------------------
    # PUBLIC METHOD
    # ----------------------------------------------------

    def decompose(self, goal: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Decompose a high level goal into executable sub-goals.
        """

        logger.info(f"🧠 Decomposing goal: {goal}")

        if not goal:
            return []

        context = context or {}

        # Try capability-based decomposition first
        subgoals = self._decompose_from_capabilities(goal)

        if subgoals:
            logger.info(f"📋 Subgoals generated from capabilities: {len(subgoals)}")
            return subgoals

        # Fallback strategy
        subgoals = self._heuristic_decomposition(goal)

        logger.info(f"📋 Subgoals generated heuristically: {len(subgoals)}")

        return subgoals

    # ----------------------------------------------------
    # CAPABILITY BASED DECOMPOSITION
    # ----------------------------------------------------

    def _decompose_from_capabilities(self, goal: str) -> List[Dict[str, Any]]:
        """
        Try to infer subgoals from registered capabilities.
        """

        if not self.capability_registry:
            return []

        subgoals = []

        capabilities = self.capability_registry.list_capabilities()

        for capability_name in capabilities:

            if capability_name.lower() in goal.lower():

                subgoals.append(
                    {
                        "type": "capability",
                        "name": capability_name,
                        "priority": 1,
                    }
                )

        return subgoals

    # ----------------------------------------------------
    # HEURISTIC DECOMPOSITION
    # ----------------------------------------------------

    def _heuristic_decomposition(self, goal: str) -> List[Dict[str, Any]]:
        """
        Fallback decomposition using simple heuristics.
        """

        subgoals = []

        goal_lower = goal.lower()

        if "lead" in goal_lower:

            subgoals = [
                {"type": "capability", "name": "lead_capture"},
                {"type": "capability", "name": "lead_cleaner"},
                {"type": "capability", "name": "lead_classifier"},
                {"type": "capability", "name": "lead_storage"},
                {"type": "capability", "name": "lead_notifier"},
            ]

        elif "user" in goal_lower:

            subgoals = [
                {"type": "capability", "name": "user_creator"},
                {"type": "capability", "name": "user_segmenter"},
            ]

        else:

            subgoals = [
                {
                    "type": "generic_task",
                    "description": goal
                }
            ]

        return subgoals

    # ----------------------------------------------------
    # PIPELINE GENERATION
    # ----------------------------------------------------

    def build_pipeline(self, subgoals: List[Dict[str, Any]]) -> List[str]:
        """
        Convert subgoals into executable pipeline steps.
        """

        steps = []

        for subgoal in subgoals:

            if subgoal["type"] == "capability":

                steps.append(f"run_capability:{subgoal['name']}")

            elif subgoal["type"] == "generic_task":

                steps.append(f"execute_task:{subgoal['description']}")

        logger.info(f"📋 Pipeline built with {len(steps)} steps")

        return steps