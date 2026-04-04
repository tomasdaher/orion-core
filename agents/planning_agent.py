from agents.base_agent import BaseAgent
from core.execution_request import Objective

from capabilities.registry import CapabilityRegistry
from capabilities.capability_graph import CapabilityGraph
from capabilities.capability_selector import CapabilitySelector
from capabilities.capability_ranker import CapabilityRanker
from capabilities.capability_graph_planner import CapabilityGraphPlanner

from memory.episodic_memory import EpisodicMemory

from goals.goal_manager import GoalManager
from goals.goal_optimizer import GoalOptimizer

from planning.goal_plan_translator import GoalPlanTranslator

class PlanningAgent(BaseAgent):

    name = "Planning_Agent"
    objective = Objective.PROCESS
    priority = 5

    def __init__(self):

        super().__init__()

        self.capability_registry = CapabilityRegistry()
        self.capability_graph = CapabilityGraph()

        self.selector = CapabilitySelector()
        self.capability_ranker = CapabilityRanker()
        self.graph_planner = CapabilityGraphPlanner()

        # 🧠 Episodic Memory
        self.episodic_memory = EpisodicMemory()

        # 🎯 Goal Engine
        self.goal_manager = GoalManager(logger=self.logger)
        self.goal_optimizer = GoalOptimizer()

        self.goal_translator = GoalPlanTranslator()

    # ------------------------------------------------
    def execute(self, state: dict):

        # 🔥 1. RESPETAR LOCK GLOBAL REAL
        if state.get("lock_execution_plan"):
            print("🛑 PlanningAgent → plan locked, skipping")
            return state

        # 🔥 2. SI YA HAY PLAN → NO TOCARLO
        if state.get("execution_plan"):
            print("🛑 PlanningAgent → existing plan detected, skipping")
            return state

        strategy = state.get("system_strategy", {})
        policy = strategy.get("execution_policy", {})
        input_data = state.get("data", {})
        objective = state.get("objective")

        # ------------------------------------------------
        # 🎯 GOAL ENGINE INTEGRATION
        # ------------------------------------------------

        goals = self.goal_manager.prioritized_goals()

        if goals:

            active_goal = goals[0]

            recommendation = self.goal_optimizer.recommend_strategy(active_goal)

            print(
                f"🎯 Active Goal → {active_goal.name} | "
                f"progress={active_goal.progress_percentage():.2f}% | "
                f"strategy={recommendation}"
            )

            state["active_goal"] = active_goal.to_dict()
            state["goal_strategy"] = recommendation

            goal_plan = self.goal_translator.translate(active_goal)

            if goal_plan:

                print(f"🎯 Goal translated into plan: {goal_plan}")

                state["execution_plan"] = {
                    "steps": goal_plan,
                    "strategy_mode": "goal_driven",
                    "risk_level": "medium"
                }

                return state

        # ------------------------------------------------
        # 🧠 MEMORY STRATEGY (solo si no hay workflow)
        # ------------------------------------------------

        memory_plan = self.try_memory_strategy(objective)

        if memory_plan:
            plan = memory_plan
            strategy_mode = "memory"

        else:

            # ------------------------------------------------
            # BUILD BASE PLAN
            # ------------------------------------------------

            goal_strategy = state.get("goal_strategy")

            candidate_plan = self.build_default_plan(
                input_data,
                policy,
                goal_strategy
            )

            # ------------------------------------------------
            # TRY LEARNED CAPABILITY
            # ------------------------------------------------

            learned_plan = self.try_capability_plan(candidate_plan)

            if learned_plan:
                plan = learned_plan
                strategy_mode = "learned"

            else:

                # ------------------------------------------------
                # TRY GRAPH PIPELINE
                # ------------------------------------------------

                graph_plan = self.try_graph_pipeline()

                if graph_plan:
                    plan = graph_plan
                    strategy_mode = "graph"
                else:
                    plan = candidate_plan
                    strategy_mode = "default"

        # ------------------------------------------------
        # ✅ SET PLAN (SIN ROMPER NADA)
        # ------------------------------------------------

        state["execution_plan"] = {
            "steps": plan,
            "strategy_mode": strategy_mode,
            "risk_level": policy.get("risk_level", "medium")
        }

        print(f"📋 PlanningAgent plan created: {state['execution_plan']}")

        return state

    # ------------------------------------------------
    # MEMORY STRATEGY
    # ------------------------------------------------

    def try_memory_strategy(self, objective):

        if not objective:
            return None

        episodes = self.episodic_memory.search_by_request(objective.name)

        if not episodes:
            return None

        capability_usage = {}

        for ep in episodes:

            if ep.get("result") != "SUCCESS":
                continue

            capabilities = ep.get("capabilities_used", [])

            for cap in capabilities:
                capability_usage[cap] = capability_usage.get(cap, 0) + 1

        if not capability_usage:
            return None

        best_capability = max(
            capability_usage,
            key=capability_usage.get
        )

        print(f"🧠 Using memory strategy capability: {best_capability}")

        return [f"run_capability:{best_capability}"]

    # ------------------------------------------------
    def try_capability_plan(self, candidate_plan):

        best_capability = self.selector.select_best_capability(candidate_plan)

        if best_capability:

            steps = best_capability.get("steps", [])

            if steps:

                name = best_capability.get("name", "unknown")

                print(f"Using learned capability: {name}")

                return steps

        # ---------------------------------
        # FALLBACK: BEST RANKED CAPABILITY
        # ---------------------------------

        ranked = self.capability_ranker.best_capability()

        if ranked:

            capability_name = ranked.get("name")

            capabilities = self.capability_registry.list_capabilities()

            for capability in capabilities:

                if capability.get("name") == capability_name:

                    print(f"Using best ranked capability: {capability_name}")

                    return [f"run_capability:{capability_name}"]

        return None

    # ------------------------------------------------
    def try_graph_pipeline(self):

        pipeline = self.graph_planner.build_pipeline()

        if not pipeline:
            return None

        print("Using capability graph pipeline")

        return pipeline

    # ------------------------------------------------
    def build_default_plan(self, input_data, policy, goal_strategy=None):

        plan = []

        if input_data:
            plan.append("analyze_input")

        plan.append("validate_data")
        plan.append("execute_task")

        exploration = policy.get("exploration", False)
        retry = policy.get("retry_on_fail", False)

        if exploration:
            plan.append("explore_optimization")

        if retry:
            plan.append("retry_execution")

        # 🎯 Goal based strategy

        if goal_strategy == "change_strategy":
            plan.append("explore_new_capabilities")

        elif goal_strategy == "increase_execution":
            plan.append("increase_execution_intensity")

        elif goal_strategy == "final_push":
            plan.append("maximize_conversion")

        return plan