import logging

from core.automation_planner import AutomationPlanner
from core.capability_engine import CapabilityEngine
from core.capability_registry import CapabilityRegistry
from core.pipeline_executor import PipelineExecutor


def setup_logging():

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s"
    )


def main():

    print("\n🚀 Orion Lead Pipeline Test\n")

    # ------------------------------------------------
    # Setup logging
    # ------------------------------------------------
    setup_logging()

    # ------------------------------------------------
    # Create engine
    # ------------------------------------------------
    engine = CapabilityEngine()

    # ------------------------------------------------
    # Load capabilities
    # ------------------------------------------------
    registry = CapabilityRegistry()

    registry.load(engine)

    print("\n📦 Capabilities loaded:")
    print(registry.list_capabilities())

    # ------------------------------------------------
    # Create planner
    # ------------------------------------------------
    planner = AutomationPlanner()

    # ------------------------------------------------
    # Fake intent
    # ------------------------------------------------
    intent = {
        "goal": "lead_generation",
        "source": "instagram",
        "actions": [
            "clean",
            "classify",
            "store",
            "notify"
        ]
    }

    # ------------------------------------------------
    # Generate plan
    # ------------------------------------------------
    plan = planner.plan(intent)

    print("\n📋 Execution plan:")
    print(plan)

    # ------------------------------------------------
    # Initial state
    # ------------------------------------------------
    state = {
        "intent": intent
    }

    # ------------------------------------------------
    # Execute steps (planner generated)
    # ------------------------------------------------
    print("\n⚙️ Executing pipeline...\n")

    for step in plan["steps"]:

        if step.startswith("run_capability:"):

            capability_name = step.split(":")[1]

            state = engine.execute(capability_name, state)

    print("\n✅ Pipeline finished\n")

    print("📊 Final state:")
    print(state)

    # ------------------------------------------------
    # Test executing saved pipeline
    # ------------------------------------------------
    print("\n🚀 Executing saved pipeline directly\n")

    executor = PipelineExecutor(engine)

    executor_state = {
        "source": "instagram"
    }

    final_state = executor.execute(
        "lead_generation_instagram",
        executor_state
    )

    print("\n📊 Final state from executor:")
    print(final_state)


if __name__ == "__main__":
    main()