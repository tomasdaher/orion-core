import logging
from typing import Dict, Any, List
import time

# ================================================================
# ORION CORE ORCHESTRATOR
# Central execution brain of Orion
# ================================================================

# ------------------------------------------------
# CORE SYSTEM IMPORTS
# ------------------------------------------------
from core.execution_request import Objective
from core.capability_engine import CapabilityEngine
from core.execution_history_collector import ExecutionHistoryCollector

# ------------------------------------------------
# INTELLIGENCE SYSTEMS
# ------------------------------------------------
from core.exploration_engine import ExplorationEngine
from capabilities.performance_tracker import CapabilityPerformanceTracker
from capabilities.capability_intelligence import CapabilityIntelligence
from capabilities.pattern_detector import PatternDetector
from capabilities.capability_evolution import CapabilityEvolution
from capabilities.meta_capability_builder import MetaCapabilityBuilder
from capabilities.capability_graph import CapabilityGraph
from capabilities.capability_usage_predictor import CapabilityUsagePredictor
from strategies.strategy_learning_engine import StrategyLearningEngine

# ------------------------------------------------
# MEMORY
# ------------------------------------------------
from memory.episodic_memory import EpisodicMemory

# ------------------------------------------------
# CAPABILITY MANAGEMENT
# ------------------------------------------------
from core.capability_builder import CapabilityBuilder
from core.capability_registry import CapabilityRegistry

# ------------------------------------------------
# AUTOMATION SYSTEM
# ------------------------------------------------
from core.pipeline_registry import PipelineRegistry
from core.pipeline_executor import PipelineExecutor
from core.automation_planner import AutomationPlanner

# ------------------------------------------------
# INTENT INTERPRETER
# ------------------------------------------------
from core.intent_interpreter import IntentInterpreter

# ------------------------------------------------
# AUTO CAPABILITY GENERATOR (NEW LAYER)
# ------------------------------------------------
from capabilities.auto_capability_generator import AutoCapabilityGenerator

# ------------------------------------------------
# GOAL ENGINE
# ------------------------------------------------
from core.goal_engine import Goal, GoalEngine

# ------------------------------------------------
# STRATEGY
# ------------------------------------------------
from core.planning.adaptive_planner import AdaptivePlanner
from core.cognition.self_reflection_engine import SelfReflectionEngine
from core.strategy.capability_strategy_optimizer import CapabilityStrategyOptimizer

class Orchestrator:

    # ================================================================
    # INITIALIZATION
    # ================================================================
    def __init__(self, repository, memory_service=None, capability_registry=None):

        self.repository = repository
        self.memory_service = memory_service
        self.agents: List[Any] = []

        self.logger = logging.getLogger("Orion")

        # ------------------------------------------------
        # INTERNAL REGISTRY
        # ------------------------------------------------
        self.registry = CapabilityRegistry()

        # ------------------------------------------------
        # EXTERNAL REGISTRY (LOADER)
        # ------------------------------------------------
        self.external_registry = capability_registry

        # ------------------------------------------------
        # CAPABILITY ENGINE
        # ------------------------------------------------
        self.capability_engine = CapabilityEngine()

        try:
            self.registry.load(self.capability_engine)
            self.logger.info("📦 Capabilities loaded from registry")
        except Exception as e:
            self.logger.warning(f"⚠️ Registry load failed: {e}")

        # ------------------------------------------------
        # CAPABILITY BUILDER
        # ------------------------------------------------
        self.capability_builder = CapabilityBuilder(
            self.capability_engine,
            registry=self.registry
        )

        # ------------------------------------------------
        # AUTO CAPABILITY GENERATOR
        # ------------------------------------------------
        # This layer allows Orion to generate new capabilities
        # automatically when builder fails to provide one.
        # ------------------------------------------------
        self.auto_capability_generator = AutoCapabilityGenerator(
            self.capability_engine
        )

        # ------------------------------------------------
        # AUTOMATION SYSTEM (PIPELINES)
        # ------------------------------------------------
        self.pipeline_registry = PipelineRegistry()
        self.pipeline_executor = PipelineExecutor(self.capability_engine)
        self.automation_planner = AutomationPlanner()

        # ------------------------------------------------
        # INTENT INTERPRETER
        # ------------------------------------------------
        self.intent_interpreter = IntentInterpreter()

        # ------------------------------------------------
        # INTELLIGENCE SYSTEMS
        # ------------------------------------------------
        self.exploration_engine = ExplorationEngine()
        self.performance_tracker = CapabilityPerformanceTracker()
        self.pattern_detector = PatternDetector()
        self.capability_intelligence = CapabilityIntelligence()
        self.capability_evolution = CapabilityEvolution()
        self.meta_capability_builder = MetaCapabilityBuilder()
        self.capability_graph = CapabilityGraph()
        self.capability_usage_predictor = CapabilityUsagePredictor()
        self.episodic_memory = EpisodicMemory()
        self.strategy_learning_engine = StrategyLearningEngine()

        # ------------------------------------------------
        # GOAL ENGINE
        # ------------------------------------------------
        # Transforms high-level objectives into executable plans.
        # Uses episodic memory for strategy lookup and automation
        # planner as fallback for new goals.
        # ------------------------------------------------
        self.goal_engine = GoalEngine(
            memory=self.episodic_memory,
            planner=self.automation_planner
        )

        # ------------------------------------------------
        # EXECUTION HISTORY COLLECTOR
        # ------------------------------------------------
        # Tracks executed pipelines so Orion can learn
        # from repeated execution patterns.
        # ------------------------------------------------
        self.execution_history_collector = ExecutionHistoryCollector()

        # ------------------------------------------------
        # STRATEGY
        # ------------------------------------------------
        self.adaptive_planner = AdaptivePlanner()
        self.reflection_engine = SelfReflectionEngine()
        self.strategy_optimizer = CapabilityStrategyOptimizer()

    # ================================================================
    # CAPABILITY RESOLUTION
    # ================================================================
    def get_capability(self, name):

        # 1️⃣ Buscar en registry externo primero
        if self.external_registry:
            capability = self.external_registry.get(name)
            if capability:
                return capability

        # 2️⃣ Fallback al engine interno
        if self.capability_engine.has_capability(name):
            return self.capability_engine.get_capability(name)

        return None

    # ================================================================
    # ENTRYPOINT
    # ================================================================
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:

        objective = state.get("objective") or Objective.PROCESS
        return self.handle_request(objective, state)

    # ================================================================
    # TEXT ENTRYPOINT
    # ================================================================
    def run_text(self, text: str) -> Dict[str, Any]:

        """
        Allows Orion to receive natural language instructions.
        """

        self.logger.info(f"🧠 Interpreting instruction: {text}")

        intent = self.intent_interpreter.interpret(text)

        self.logger.info(f"📄 Generated intent: {intent}")

        state = {
            "objective": Objective.PROCESS,
            "intent": intent
        }

        return self.run(state)

    # ================================================================
    # AGENT REGISTRATION
    # ================================================================
    def register_agent(self, agent):

        if hasattr(agent, "memory_service"):
            agent.memory_service = self.memory_service

        self.agents.append(agent)

        self.logger.info(f"Agente registrado: {agent.name}")

    # ================================================================
    # PIPELINE RESOLUTION
    # ================================================================
    def _resolve_pipeline(self, objective: Objective) -> List[Any]:

        eligible_agents = [
            agent for agent in self.agents
            if getattr(agent, "objective", None) == objective
        ]

        return sorted(
            eligible_agents,
            key=lambda agent: getattr(agent, "priority", 999)
        )

    # ================================================================
    # AUTOMATION SYSTEM
    # ================================================================
    def _handle_automation(self, state: Dict[str, Any]) -> Dict[str, Any]:

        intent = state.get("intent")

        if not intent:
            return state

        goal = intent.get("goal")
        source = intent.get("source", "generic")

        # ------------------------------------------------
        # GOAL VS PIPELINE SEPARATION
        # goal_name  → what Orion wants to achieve (semantic)
        # pipeline_name → technical implementation key (operational)
        # ------------------------------------------------
        goal_name = goal
        pipeline_name = f"{goal}_{source}" if goal else f"generic_{source}"

        self.logger.info(f"🧠 Automation request → {pipeline_name}")

        # ------------------------------------------------
        # GOAL ENGINE LAYER
        # Resolve high-level goal before pipeline lookup.
        # If the intent carries a goal, GoalEngine searches
        # episodic memory for a known strategy first, then
        # delegates to AutomationPlanner as fallback.
        # ------------------------------------------------
        if goal:

            orion_goal = Goal(
                name=goal_name,
                objective=intent.get("objective", goal),
                priority=intent.get("priority", "medium")
            )

            self.logger.info(f"🎯 GoalEngine processing: {orion_goal}")

            state = self.goal_engine.process_goal(orion_goal, state)

            if state.get("execution_plan"):

                self.logger.info(
                    f"✅ GoalEngine resolved plan for: {goal_name}"
                )

                return state

        pipeline = self.pipeline_registry.load_pipeline(pipeline_name)

        if pipeline:

            self.logger.info(f"🚀 Using existing pipeline: {pipeline_name}")

            state = self.pipeline_executor.execute(
                pipeline_name,
                state
            )

            return state

        self.logger.info("🧠 No pipeline found → generating")

        plan = self.automation_planner.plan(intent)

        self.pipeline_registry.save_pipeline(
            pipeline_name,
            plan
        )

        state["execution_plan"] = plan

        return state

    # ================================================================
    # PLAN EXECUTION
    # ================================================================
    def _execute_plan(self, state: Dict[str, Any]):

        plan = state.get("execution_plan")

        if not plan:
            print("⚠️ No execution_plan found in state")
            return state

        steps = plan.get("steps", [])

        if not steps:
            print("⚠️ execution_plan has no steps")
            return state

        executed_steps = []

        for step in steps:

            self.logger.info(f"Ejecutando step: {step}")

            capability_name = None

            try:

                if step.startswith("run_capability:"):

                    capability_name = step.split(":")[1]

                    self.logger.info(f"⚡ Running capability: {capability_name}")

                    capability = self.get_capability(capability_name)

                    # ------------------------------------------------
                    # BUILDER LAYER
                    # ------------------------------------------------
                    if not capability:
                        self.logger.warning(
                            f"⚠️ Capability not found → trying builder: {capability_name}"
                        )

                        self.capability_builder.ensure_capability(capability_name)

                        capability = self.get_capability(capability_name)

                    # ------------------------------------------------
                    # AUTO GENERATION LAYER
                    # ------------------------------------------------
                    if not capability:

                        self.logger.warning(
                            f"⚠️ Builder failed → attempting auto generation: {capability_name}"
                        )

                        try:

                            generated = self.auto_capability_generator.generate(
                                capability_name
                            )

                            if generated:

                                self.logger.info(
                                    f"🧠 Auto capability generated: {capability_name}"
                                )

                                capability = self.get_capability(capability_name)

                        except Exception as gen_error:

                            self.logger.warning(
                                f"⚠️ Auto generation failed: {gen_error}"
                            )

                    if not capability:
                        raise Exception(f"Capability not available: {capability_name}")

                    start_time = time.time()

                    if hasattr(capability, "execute"):
                        result = capability.execute(state)
                    else:
                        result = capability(state)

                    execution_time = time.time() - start_time

                    self.performance_tracker.record_execution(
                        capability_name=capability_name,
                        execution_time=execution_time,
                        success=True
                    )

                    state["capability_result"] = result

                elif step == "analyze_input":
                    state["analysis"] = "input analyzed"

                elif step == "validate_data":
                    state["validation"] = "data valid"

                elif step == "execute_task":
                    state["task_result"] = "task executed"

                elif step == "explore_optimization":
                    state["optimization"] = "optimization explored"

                elif step == "retry_failed_tasks":
                    state["retry"] = "retry attempted"

                elif step == "store_result":
                    state["result_stored"] = True

                executed_steps.append(step)

            except Exception as e:

                self.logger.error(f"❌ Error en step {step}: {str(e)}")

                if capability_name:
                    self.performance_tracker.record_execution(
                        capability_name=capability_name,
                        execution_time=0,
                        success=False
                    )

                state["execution_status"] = "STEP_FAILED"
                state["failed_step"] = step
                break

        state["plan_execution"] = {
            "steps_executed": executed_steps,
            "total_steps": len(steps)
        }

        state["plan"] = executed_steps

        # ------------------------------------------------
        # EXECUTION HISTORY TRACKING
        # ------------------------------------------------
        try:

            self.execution_history_collector.record_execution(executed_steps)

            state["execution_history"] = (
                self.execution_history_collector.get_history()
            )

            history = self.execution_history_collector.get_history()

            self.capability_usage_predictor.learn_from_history(history)

        except Exception as e:

            self.logger.warning(
                f"⚠️ Execution history tracking failed: {e}"
            )

        self.pattern_detector.observe_plan(executed_steps)

        new_caps = self.pattern_detector.register_new_capabilities()

        if new_caps:
            self.logger.info(f"🧠 New capabilities discovered: {new_caps}")

        return state

    # ================================================================
    # MAIN REQUEST HANDLER
    # ================================================================
    def handle_request(self, objective: Objective, state: Dict[str, Any]) -> Dict[str, Any]:

        start_time = time.time()

        self.logger.info(f"🚀 Nuevo request: {objective.name}")

        state["objective"] = objective
        state["execution_status"] = "RUNNING"
        state["agents_used"] = []

        # ------------------------------------------------
        # AUTOMATION LAYER
        # ------------------------------------------------
        state = self._handle_automation(state)

        # ------------------------------------------------
        # ADAPTIVE STRATEGY SELECTION
        # ------------------------------------------------
        try:

            capability_insights = self.capability_intelligence.analyze_capabilities()

            strategy = self.adaptive_planner.choose_strategy(capability_insights)

            state["strategy_mode"] = strategy

            self.logger.info(f"🧠 Adaptive strategy selected: {strategy}")

        except Exception as e:

            self.logger.warning(f"⚠️ Strategy selection failed: {e}")

        # ------------------------------------------------
        # MEMORY CONTEXT
        # ------------------------------------------------
        if self.memory_service:

            context = self.memory_service.build_context(limit=5)
            state["memory_context"] = context

            self.logger.info(
                f"🧠 Memory loaded: {context['total_recent']} episodios"
            )

        try:

            pipeline = self._resolve_pipeline(objective)

            if not pipeline:

                self.logger.warning("⚠️ No agents available")

                state["execution_status"] = "NO_AGENTS"
                state["execution_time"] = time.time() - start_time

                self.repository.save_execution(state)
                return state

            for agent in pipeline:

                self.logger.info(
                    f"🤖 Agent: {agent.name} (priority={agent.priority})"
                )

                state = agent.execute(state)
                state["agents_used"].append(agent.name)

            if "execution_plan" in state:

                print(f"📋 Execution plan detected: {state['execution_plan']}")

                if state.get("lock_execution_plan"):
                    print("🛑 Plan locked → skipping optimization & exploration")
                else:

                    state["execution_plan"] = self.capability_usage_predictor.optimize_plan(
                        state["execution_plan"]
                    )

                    state["execution_plan"] = self.capability_engine.optimize_plan(
                        state["execution_plan"],
                        state
                    )

                    if self.exploration_engine.should_explore():

                        self.logger.info("🧪 Exploration mode")

                        state["execution_plan"] = self.exploration_engine.explore(
                            state["execution_plan"]
                        )

            else:
                print("❌ No execution_plan after agents")

            state = self._execute_plan(state)

            state["execution_status"] = "SUCCESS"

        except Exception as e:

            self.logger.error(f"❌ Ejecución fallida: {str(e)}")

            state["execution_status"] = "FAILED"
            state["error"] = str(e)

        # ------------------------------------------------
        # SELF REFLECTION
        # ------------------------------------------------

        try:

            execution_plan = state.get("execution_plan")

            self.reflection_engine.record_failure(
                execution_plan,
                reason="execution_failure"
            )

        except Exception as reflection_error:

            self.logger.warning(
                f"⚠️ Reflection engine failed: {reflection_error}"
            )

        execution_time = time.time() - start_time
        state["execution_time"] = execution_time

        self.repository.save_execution(state)

        self.logger.info(
            f"✅ Finalizado | status={state.get('execution_status')}"
        )

        strategy_mode = state.get("execution_plan", {}).get("strategy_mode", "unknown")

        success = state.get("execution_status") == "SUCCESS"

        self.strategy_learning_engine.record_execution(
            strategy_mode,
            success
        )
        
        # ------------------------------------------------
        # STRATEGY OPTIMIZER LEARNING
        # ------------------------------------------------

        try:

            strategy = state.get("strategy_mode", "hybrid")

            self.strategy_optimizer.record_strategy(
                strategy,
                success
            )

        except Exception as e:

            self.logger.warning(f"⚠️ Strategy optimizer failed: {e}")
        
        # ------------------------------------------------
        # FAILURE ANALYSIS
        # ------------------------------------------------

        try:

            insights = self.reflection_engine.analyze_failures()

            if insights:
                self.logger.info(f"🧠 Reflection insights: {insights}")

        except Exception as e:

            self.logger.warning(f"⚠️ Reflection analysis failed: {e}")
        
        
        try:

            insights = self.capability_intelligence.analyze_capabilities()
            self.logger.info(f"🧠 Insights: {insights}")

            evolved = self.capability_evolution.evolve()
            if evolved:
                self.logger.info(f"🧠 Evolution: {evolved}")

            meta_caps = self.meta_capability_builder.build_meta_capabilities()
            if meta_caps:
                self.logger.info(f"🧠 Meta: {meta_caps}")

            graph = self.capability_graph.build_graph()
            self.logger.info(f"🧠 Graph nodes: {len(graph)}")

        except Exception as e:
            self.logger.warning(f"⚠️ Post-intelligence error: {e}")

        try:

            steps = state.get("execution_plan", {}).get("steps", [])

            capabilities_used = [
                step.split(":")[1]
                for step in steps
                if step.startswith("run_capability:")
            ]

            self.episodic_memory.save_episode(
                request=str(objective.name),
                strategy="capability_execution",
                plan=steps,
                result=state.get("execution_status"),
                execution_time=state.get("execution_time"),
                capabilities_used=capabilities_used
            )

        except Exception as e:
            self.logger.warning(f"⚠️ Episodic memory failed: {e}")

        return state