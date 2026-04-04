import logging

from core.orchestrator import Orchestrator
from core.capability_registry import CapabilityRegistry
from core.execution_request import Objective


# ------------------------------------------------
# Dummy repository
# ------------------------------------------------
class DummyRepository:

    def save_execution(self, state):
        print("\n💾 Execution saved")


# ------------------------------------------------
# Logging setup
# ------------------------------------------------
def setup_logging():

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s"
    )


# ------------------------------------------------
# Main test
# ------------------------------------------------
def main():

    print("\n🚀 Orion Automation Test\n")

    setup_logging()

    # ------------------------------------------------
    # Repository
    # ------------------------------------------------
    repository = DummyRepository()

    # ------------------------------------------------
    # Capability registry
    # ------------------------------------------------
    registry = CapabilityRegistry()

    # ------------------------------------------------
    # Orchestrator
    # ------------------------------------------------
    orchestrator = Orchestrator(
        repository=repository,
        capability_registry=registry
    )

    # ------------------------------------------------
    # Intent
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
    # Initial state
    # ------------------------------------------------
    state = {

        "objective": Objective.PROCESS,

        "intent": intent,

        "lead": {
            "name": "Juan Perez",
            "email": "juan@example.com",
            "source": "instagram"
        }
    }

    # ------------------------------------------------
    # Execute
    # ------------------------------------------------
    result = orchestrator.run(state)

    print("\n✅ Execution finished\n")

    print("📊 Final state:\n")
    print(result)


if __name__ == "__main__":
    main()