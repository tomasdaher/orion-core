import logging

from core.goal_decomposition_engine import GoalDecompositionEngine
from core.goal_capability_mapper import GoalCapabilityMapper
from capabilities.capability_graph_planner import CapabilityGraphPlanner


class Goal:

    """
    Represents a high level objective for Orion.
    """

    def __init__(self, name, objective, priority="medium"):

        self.name = name
        self.objective = objective
        self.priority = priority

    def __repr__(self):

        return f"Goal(name={self.name}, priority={self.priority})"


class GoalEngine:

    """
    GoalEngine transforms objectives into executable plans.
    """

    def __init__(self, memory, planner):

        self.logger = logging.getLogger("Orion")

        self.memory = memory
        self.planner = planner

        # ------------------------------------------------
        # Goal decomposition engine
        # ------------------------------------------------
        self.decomposition_engine = GoalDecompositionEngine()

        # ------------------------------------------------
        # Capability mapper
        # ------------------------------------------------
        self.capability_mapper = None

        # ------------------------------------------------
        # Capability graph planner
        # ------------------------------------------------
        self.graph_planner = CapabilityGraphPlanner()

        try:

            registry = getattr(planner, "capability_registry", None)

            if registry:

                self.capability_mapper = GoalCapabilityMapper(registry)

                self.logger.info(
                    "🔗 GoalCapabilityMapper initialized"
                )

        except Exception as e:

            self.logger.warning(
                f"⚠️ Capability mapper initialization failed: {e}"
            )

    # ------------------------------------------------
    # Handle new goal
    # ------------------------------------------------
    def process_goal(self, goal, state):

        self.logger.info(f"🎯 Processing goal: {goal.name}")

        # ------------------------------------------------
        # Try to reuse past strategies
        # ------------------------------------------------
        strategy = self._search_memory(goal)

        if strategy:

            self.logger.info(
                f"🧠 Strategy found in memory for goal: {goal.name}"
            )

            state["execution_plan"] = strategy

            return state

        # ------------------------------------------------
        # Goal decomposition
        # ------------------------------------------------
        self.logger.info(
            "🧠 Decomposing goal into subgoals"
        )

        subgoals = self.decomposition_engine.decompose(
            goal.objective
        )

        if subgoals:

            pipeline = None

            # ------------------------------------------------
            # Try capability mapping
            # ------------------------------------------------
            if self.capability_mapper:

                pipeline = self.capability_mapper.map_subgoals(
                    subgoals
                )

            # ------------------------------------------------
            # Fallback to simple pipeline
            # ------------------------------------------------
            if not pipeline:

                pipeline = self.decomposition_engine.build_pipeline(
                    subgoals
                )

            if pipeline:

                self.logger.info(
                    f"📋 Pipeline generated from goal decomposition: {pipeline}"
                )

                state["execution_plan"] = {
                    "steps": pipeline
                }

                return state

        # ------------------------------------------------
        # Capability Graph Planning
        # ------------------------------------------------
        self.logger.info(
            "🧠 Attempting capability graph planning"
        )

        try:

            graph_pipeline = self.graph_planner.build_pipeline()

            if graph_pipeline:

                self.logger.info(
                    f"🔗 Capability graph pipeline generated: {graph_pipeline}"
                )

                state["execution_plan"] = {
                    "steps": graph_pipeline
                }

                return state

        except Exception as e:

            self.logger.warning(
                f"⚠️ Graph planner failed: {e}"
            )

        # ------------------------------------------------
        # Planner fallback
        # ------------------------------------------------
        self.logger.info(
            "🧠 No decomposition or graph plan available → delegating to planner"
        )

        plan = self.planner.create_plan(goal.objective)

        state["execution_plan"] = plan

        return state

    # ------------------------------------------------
    # Memory lookup
    # ------------------------------------------------
    def _search_memory(self, goal):

        try:

            episodes = self.memory.load_episodes()

            for episode in episodes:

                if goal.name in str(episode):

                    return episode.get("execution_plan")

        except Exception as e:

            self.logger.warning(
                f"⚠️ Memory lookup failed: {e}"
            )

        return None